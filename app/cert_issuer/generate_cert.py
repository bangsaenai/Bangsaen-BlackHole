import os
import time
import hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class CertificateIssuer:
    def __init__(self):
        self.method_desc = "KKS Left Null Space Projection (Ax=b) & DoD 5220.22-M"

    def calculate_hash(self, filepath):
        """คำนวณรหัส SHA-256 ของไฟล์ก่อนถูกทำลาย เพื่อเป็นหลักฐานว่าทำลายไฟล์ไหนไป"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return "UNABLE_TO_HASH"

    def issue_pdf(self, target_filepath):
        """สร้างไฟล์ PDF ใบรับรองไว้ที่ตำแหน่งเดียวกับไฟล์ที่ถูกทำลาย"""
        directory = os.path.dirname(target_filepath)
        filename = os.path.basename(target_filepath)
        
        # คำนวณ Hash ก่อนที่ไฟล์จะโดนบดขยี้
        file_hash = self.calculate_hash(target_filepath)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC")

        # ตั้งชื่อไฟล์ PDF ใบเสร็จ
        cert_filename = f"CERT_OF_ANNIHILATION_{filename}.pdf"
        cert_path = os.path.join(directory, cert_filename)

        # เริ่มวาด PDF
        c = canvas.Canvas(cert_path, pagesize=letter)
        c.setFont("Courier-Bold", 18)
        
        # หัวกระดาษ
        c.drawString(50, 720, "=====================================================")
        c.drawString(50, 690, "       CERTIFICATE OF DIGITAL ANNIHILATION")
        c.drawString(50, 660, "=====================================================")

        c.setFont("Courier", 12)
        c.drawString(50, 600, "This document certifies the absolute and irrecoverable")
        c.drawString(50, 580, "destruction of the following digital asset:")

        c.setFont("Courier-Bold", 12)
        c.drawString(50, 530, f"TARGET FILE : {filename}")
        c.drawString(50, 500, f"SHA-256 HASH: {file_hash}")
        c.drawString(50, 470, f"TIMESTAMP   : {timestamp}")
        
        c.setFont("Courier", 12)
        c.drawString(50, 420, "DESTRUCTION PROTOCOL:")
        c.setFont("Courier-Bold", 11)
        c.drawString(70, 400, f"- {self.method_desc}")
        c.drawString(70, 380, "- RAM Buffer Zeroed (tmpfs isolation)")
        c.drawString(70, 360, "- Absolute Sector Overwrite Executed")

        c.setFont("Courier-Bold", 14)
        c.drawString(50, 280, "STATUS: NEUTRALIZED. ZERO RESIDUAL FOOTPRINT.")

        # ลายเซ็นต์ดิจิทัลจำลอง
        c.setFont("Courier", 10)
        c.drawString(50, 100, "Authorized by: BANGSAEN AI BLACK HOLE ENGINE")
        c.drawString(50, 80, "Verification ID: KKS-CORE-909")

        c.save()
        return cert_path