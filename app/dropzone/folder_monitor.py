import os
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# นำเข้า Core ทั้ง 3 ตัว (ไฟล์ .pyc จะถูกเรียกใช้อัตโนมัติที่นี่)
from app.core.kks_nullspace import KKSBlackHoleEngine
from app.core.secure_wipe import SecureWiper
from app.cert_issuer.generate_cert import CertificateIssuer

class BlackHoleHandler(FileSystemEventHandler):
    def __init__(self, dropzone_path):
        self.dropzone_path = dropzone_path
        self.engine = KKSBlackHoleEngine(target_dim=1024)
        self.wiper = SecureWiper()
        self.cert_issuer = CertificateIssuer()
        self.free_tier_used = False

    def on_created(self, event):
        if event.is_directory or "CERT" in event.src_path or "UPGRADE" in event.src_path:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)
        time.sleep(0.5) 

        if self.free_tier_used:
            print(f"[🛑] BLOCKED: {filename} (Evaluation limit reached)")
            self.issue_upgrade_notice(filename)
            return

        print(f"\n[⚠️] TARGET ACQUIRED: {filename}")
        self.annihilate_file(filepath, filename)
        self.free_tier_used = True 

    def annihilate_file(self, filepath, filename):
        try:
            # 0. ออกใบรับรอง PDF
            print("     [+] Calculating Cryptographic Hash and generating Certificate...")
            cert_path = self.cert_issuer.issue_pdf(filepath)
            
            # 1. ดูดไฟล์ดิบเข้าสู่ RAM
            with open(filepath, 'rb') as f:
                file_data = bytearray(f.read())
            
            # 2. โยนเข้าเตาเผาคณิตศาสตร์ (RAM Wipe)
            self.engine.annihilate_in_memory(file_data)
            
            # 3. บดขยี้ระดับ Hardware และลบทิ้ง (DoD 3-Pass Wipe)
            print("     [+] Executing DoD 5220.22-M 3-Pass Wipe on physical drive...")
            self.wiper.wipe_file_dod_standard(filepath)
            
            print(f"[✅] TARGET NEUTRALIZED. Certificate issued at: {os.path.basename(cert_path)}")
            
        except Exception as e:
            print(f"[❌] ERROR processing {filename}: {e}")

    def issue_upgrade_notice(self, filename):
        notice_path = os.path.join(self.dropzone_path, "UPGRADE_LICENSE_REQUIRED.txt")
        if not os.path.exists(notice_path):
            with open(notice_path, 'w', encoding='utf-8') as f:
                f.write("EVALUATION MODE LIMIT REACHED.\n")
                f.write("Please upgrade to PRO/ENTERPRISE LICENSE for Batch Annihilation.\n")

def start_blackhole_dropzone():
    dropzone_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../BlackHole_Dropzone'))
    os.makedirs(dropzone_dir, exist_ok=True)
    
    event_handler = BlackHoleHandler(dropzone_dir)
    observer = Observer()
    observer.schedule(event_handler, dropzone_dir, recursive=False)
    
    print("==================================================")
    print(f"🕳️ BANGSAEN BLACK HOLE IS ACTIVE 🕳️")
    print(f"Dropzone: {dropzone_dir}")
    print("Waiting for target... (EVALUATION MODE: 1 File Limit)")
    print("Press Ctrl+C to stop.")
    print("==================================================")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[!] Black Hole powering down.")
    observer.join()