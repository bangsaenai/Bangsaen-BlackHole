import sys
import os

# ชี้ Path ให้มองเห็นโฟลเดอร์ทั้งหมดในโปรเจกต์
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dropzone.folder_monitor import start_blackhole_dropzone

if __name__ == "__main__":
    try:
        # สตาร์ทระบบเฝ้าระวังโฟลเดอร์หลุมดำ
        start_blackhole_dropzone()
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Failed to initialize the Black Hole: {e}")