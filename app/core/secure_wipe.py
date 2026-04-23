import os
import secrets
import string

class SecureWiper:
    """
    ฝ่ายบดขยี้ฮาร์ดดิสก์: ใช้มาตรฐาน DoD 5220.22-M (3 Passes) 
    และทำลายร่องรอยชื่อไฟล์ (MFT Scrambling)
    """
    def __init__(self):
        self.standard = "DoD 5220.22-M (3-Pass Wipe)"

    def _scramble_filename(self, filepath):
        """เปลี่ยนชื่อไฟล์เป็นตัวอักษรสุ่ม เพื่อทำลายร่องรอยใน Master File Table (MFT)"""
        directory = os.path.dirname(filepath)
        ext = os.path.splitext(filepath)[1]
        
        # สร้างชื่อไฟล์สุ่มความยาว 16 ตัวอักษร
        random_name = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        new_filepath = os.path.join(directory, random_name + ext)
        
        os.rename(filepath, new_filepath)
        return new_filepath

    def wipe_file_dod_standard(self, filepath):
        """ดำเนินการลบแบบ 3-Pass ตามมาตรฐานกระทรวงกลาโหมสหรัฐฯ"""
        if not os.path.exists(filepath):
            return False

        file_size = os.path.getsize(filepath)

        # เปิดไฟล์ในโหมด r+b (อ่านเขียนแบบ Binary ตรงๆ ลง Sector เดิม ไม่สร้างไฟล์ใหม่)
        with open(filepath, "r+b") as f:
            # Pass 1: Overwrite with Zeros (0x00)
            f.seek(0)
            f.write(b'\x00' * file_size)
            f.flush()
            os.fsync(f.fileno()) # บังคับ OS ให้เขียนลง Hardware จริงๆ ห้ามกั๊กไว้ใน Cache

            # Pass 2: Overwrite with Ones (0xFF)
            f.seek(0)
            f.write(b'\xff' * file_size)
            f.flush()
            os.fsync(f.fileno())

            # Pass 3: Overwrite with Random Data
            f.seek(0)
            f.write(os.urandom(file_size))
            f.flush()
            os.fsync(f.fileno())

        # Final Blow: เปลี่ยนชื่อไฟล์ให้เละเทะก่อนลบทิ้ง
        scrambled_path = self._scramble_filename(filepath)
        os.remove(scrambled_path)
        
        return True