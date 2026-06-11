# ไฟล์: init_db.py (เวอร์ชัน OpenAI เคลียร์ปัญหาแรมเต็ม)
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings  # 🌟 สลับมาใช้ค่าย OpenAI ตัวบางเบา
from langchain_core.documents import Document
import os

print("--- 🚀 เริ่มต้นกระบวนการสร้างคลังข้อมูล 3D Assets ด้วย OpenAI ---")

# ⚠️ สำคัญมาก: ใส่รหัส OpenAI API Key ตัวจริงของคุณไว้ที่นี่ เพื่อให้เครื่องคอมคุณรันเทสได้
os.environ["OPENAI_API_KEY"] = ""

documents = [
    Document(
        page_content="เก้าอี้เหล็กสไตล์ไซไฟล้ำยุค สีเงิน มีไฟเรืองแสงสีฟ้า เหมาะกับห้องทดลองหรือยานอวกาศ คอนเซปต์อนาคตดูล้ำสมัย เทคโนโลยี", 
        metadata={"name": "SciFi Chair 01", "path": "D:/Assets/Furniture/scifi_chair_01.fbx"}
    ),
    Document(
        page_content="โต๊ะทำงานเหล็ก พังทลาย มีรอยไหม้ หน้าจอคอมพิวเตอร์แตกและมีประกายไฟช็อต เหมาะกับฉากสงคราม ห้องร้าง หรือฐานทัพที่โดนโจมตี", 
        metadata={"name": "Damaged SciFi Desk", "path": "D:/Assets/Structures/damaged_desk.fbx"}
    ),
    Document(
        page_content="ประตูเหล็กกล้าบานเลื่อนไฮดรอลิกขนาดใหญ่ ยานอวกาศ ประตูเซฟตี้หนาแน่น มีป้ายเตือนอันตรายสีเหลืองดำ ล็อกแน่นหนา ฉากทางเข้า", 
        metadata={"name": "Blast Door Large", "path": "D:/Assets/Doors/blast_door_01.fbx"}
    ),
    Document(
        page_content="หุ่นยนต์โดรนตรวจการขนาดเล็ก ทรงกลม ลอยตัวได้ มีเลนส์กล้องไฟสีแดงตรงกลาง สไตล์ Cyberpunk สายลับ ลาดตระเวน คอยจับตาดู", 
        metadata={"name": "Surveillance Drone", "path": "D:/Assets/Props/drone_spy.fbx"}
    )
]

print(f"-> โหลดข้อมูลดิบของโมเดล 3D เข้าสู่ระบบเรียบร้อย (จำนวน {len(documents)} ชิ้น)")

# 🌟 สลับมาใช้ตัวแปลงมิติข้อมูลของ OpenAI (ขนาด 1536 มิติ ตรงกันกับไฟล์ App.py)
embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")

# สั่งบันทึกข้อมูลลงแฟลชไดรฟ์จำลองในชื่อเดิม
db = Chroma.from_documents(
    documents=documents, 
    embedding=embedding_function, 
    persist_directory="./3d_previs_db"
)

print("\n--- 🎉 เสร็จสิ้นขั้นตอน! คลังข้อมูลเวกเตอร์ OpenAI พร้อมใช้งานแล้ว ---")