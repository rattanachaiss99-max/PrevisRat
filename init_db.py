# ไฟล์: init_db.py (เวอร์ชันอัปเดตล่าสุด)
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

print("--- 🚀 เริ่มต้นกระบวนการสร้างคลังข้อมูล 3D Assets จำลอง ---")

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

# ใช้ HuggingFaceEmbeddings แทนคลาสเก่า
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ใช้ langchain_chroma แทนคลาสเก่า
db = Chroma.from_documents(
    documents=documents, 
    embedding=embedding_function, 
    persist_directory="./3d_previs_db"
)

print("\n--- 🎉 เสร็จสิ้นขั้นตอน! ---")