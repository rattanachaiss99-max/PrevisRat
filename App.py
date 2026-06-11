__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# 🔓 เปิดประตู CORS ต้อนรับหน้าบ้านของคุณทุกโดเมนเพื่อความชัวร์ 100%
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โครงสร้างการรับข้อมูลจากหน้าบ้าน Vue 3
class ScriptRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "3D Previs Backend is running online!"}

@app.post("/api/previs")
async def get_previs(request: ScriptRequest):
    try:
        user_text = request.text.lower()
        matched_assets = []
        
        # 🔍 กลไกค้นหาอัจฉริยะแบบประหยัดพลังงาน (Keyword Matching)
        if "เก้าอี้" in user_text or "chair" in user_text:
            matched_assets.append({"name": "SciFi Chair 01", "path": "D:/Assets/Furniture/scifi_chair_01.fbx"})
        if "โต๊ะ" in user_text or "desk" in user_text:
            matched_assets.append({"name": "Damaged SciFi Desk", "path": "D:/Assets/Structures/damaged_desk.fbx"})
        if "ประตู" in user_text or "door" in user_text:
            matched_assets.append({"name": "Blast Door Large", "path": "D:/Assets/Doors/blast_door_01.fbx"})
        if "โดรน" in user_text or "drone" in user_text:
            matched_assets.append({"name": "Surveillance Drone", "path": "D:/Assets/Props/drone_spy.fbx"})
            
        # เผื่อผู้ใช้พิมพ์อย่างอื่นมา ให้ส่งหุ่นโดรนไปโชว์ตัวยืนพื้นไว้ก่อน
        if not matched_assets:
            matched_assets.append({"name": "Surveillance Drone", "path": "D:/Assets/Props/drone_spy.fbx"})
            
        return {
            "status": "success",
            "assets": matched_assets,
            "ai_analysis": "ระบบหลังบ้านประมวลผลคำสำคัญจากบทหนังของคุณเรียบร้อยแล้ว ได้ทำการจัดส่งชิ้นส่วนโมเดล 3D ที่เกี่ยวข้องกลับไป"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}