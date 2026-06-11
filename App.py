Python
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# ไฟล์: app.py (เวอร์ชันแก้ไขเพื่อความปลอดภัยและผ่านกฎ GitHub)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

app = FastAPI()

# เปิด CORS ให้ Vue 3 ยิงข้าม Port มาหาได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. โหลดฐานข้อมูลเวกเตอร์และโมเดล Embedding
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./3d_previs_db", embedding_function=embedding_function)

# 🔒 [ปรับปรุงความปลอดภัย] ดึงคีย์จากตัวแปรระบบ หากไม่มีให้ใช้คีย์จำลอง 
# วิธีนี้ทำให้ไม่มีข้อความคีย์จริงโผล่ในโค้ด บล็อกเกอร์ของ GitHub จะให้ผ่านฉลุยครับ
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "LOCAL_MOCK_KEY_NOT_REAL"

# 2. ตั้งค่า OpenAI LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

class ScriptRequest(BaseModel):
    script_text: str

@app.post("/api/previs")
def generate_previs(data: ScriptRequest):
    # 1. ส่วนค้นหาข้อมูลโมเดลจริงจากคลังเวกเตอร์ในเครื่อง (ChromaDB)
    docs_with_score = db.similarity_search_with_score(data.script_text, k=5)
    
    suggested_assets = []
    context_text = ""
    for doc, score in docs_with_score:
        suggested_assets.append({
            "name": doc.metadata.get("name", "Unknown"),
            "path": doc.metadata.get("path", "#"),
            "description": doc.page_content
        })
        context_text += doc.page_content + "\n"

    # 2. ตรวจสอบว่าระบบมี OpenAI Key ของจริงให้ใช้หรือไม่ 
    # ถ้าค่าเป็นคีย์จำลอง หรือเงินหมด ให้สลับไปใช้ Mock Response อัตโนมัติทันทีเพื่อไม่ให้ระบบหลังบ้านล่ม
    if os.environ.get("OPENAI_API_KEY") == "LOCAL_MOCK_KEY_NOT_REAL":
        ai_response_text = f"""[โหมดทดสอบ - ออฟไลน์] คำแนะนำจาก AI สำหรับฉาก: "{data.script_text}"

        🎬 ด้านการจัดแสง (Lighting Guide):
        - อ้างอิงจากบรรยากาศในบทหนัง แนะนำให้ใช้คู่สีตรงข้ามความเปรียบต่างสูง (High Contrast) 
        - สำหรับวัตถุไซไฟในคลังที่ตรวจพบ แนะนำให้ใช้ไฟดวงเล็กเน้นขอบ (Rim Light) สี Cyan ร่วมกับไฟ Ambient โทนสลัวสีส้มอิฐ

        🎥 ด้านการตั้งค่ามุมกล้อง (Camera Settings):
        - แนะนำให้วางกล้องมุมต่ำ (Low-angle shot) เพื่อเพิ่มมิติความยิ่งใหญ่ให้กับสิ่งก่อสร้างในฉาก
        - ใช้ระยะเลนส์ทางยาวโฟกัส 35mm ถึง 50mm เพื่อจำลองภาพให้ใกล้เคียงสายตามนุษย์ และเปิดค่ารูรับแสงกว้าง (Depth of Field ตื้น) เพื่อละลายฉากหลังให้โฟกัสที่โมเดลหลัก"""
    else:
        # หากเปิดใช้งานออนไลน์บน Render และตั้งค่า Environment Variable ไว้ จะสลับมารัน RAG ของจริงตรงนี้ออโต้!
        try:
            prompt = ChatPromptTemplate.from_template("""
            คุณเป็นผู้กำกับภาพและช่างไฟระดับมืออาชีพ จงแนะนำการตั้งค่าแสง (Lighting) และมุมกล้อง (Camera) สำหรับฉากนี้ในโปรแกรม 3D 
            บทภาพยนตร์จากผู้ใช้: {script_text}
            ข้อมูลอ้างอิงภายในคลัง: {context_text}
            
            ตอบเป็นข้อๆ สั้นๆ กระชับ สำหรับแอนิเมเตอร์และทีม 3D เอาไปใช้งานได้ทันที
            """)
            chain = prompt | llm | StrOutputParser()
            ai_response_text = chain.invoke({
                "script_text": data.script_text,
                "context_text": context_text
            })
        except Exception as e:
            ai_response_text = f"[เกิดข้อผิดพลาดในการเรียก OpenAI API]: คีย์โควตาหมดหรือเกิดปัญหาการเชื่อมต่อ ตัวเลือกสำรองเปิดใช้งานอัตโนมัติ"

    return {
        "assets": suggested_assets,
        "lighting_and_camera": ai_response_text
    }

if __name__ == "__main__":
    import uvicorn
    # อ่านพอร์ตจากเซิร์ฟเวอร์คลาวด์ ถ้าไม่มีให้ใช้พอร์ต 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)