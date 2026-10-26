"""
Module: course_registration_simulation.py
Author: Ngo Lam Tien (MSSV: 524H0195)
Subject: Software Engineering (503074) - Lab 05/06 (Exercise 2)
Description:
    Mo phong he thong Dang ky Hoc phan dai hoc (University Course Registration)
    theo dung kịch ban tuong tac cua Bieu do Tuan tu (Sequence Diagram).
    Xu ly day du cac luong khao sat danh muc, kiem tra mon tien quyet,
    kiem tra si so con trong, cap nhat CSDL va cap nhat danh sach cho (Waitlist).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

@dataclass
class Course:
    course_id: str
    course_name: str
    credits: int
    prerequisites: List[str] = field(default_factory=list)

@dataclass
class CourseSection:
    section_id: str
    course: Course
    max_seats: int
    enrolled_students: List[str] = field(default_factory=list)
    waitlist: List[str] = field(default_factory=list)

    @property
    def available_places(self) -> int:
        return max(0, self.max_seats - len(self.enrolled_students))

    def is_full(self) -> bool:
        return len(self.enrolled_students) >= self.max_seats

class ElectronicCourseCatalog:
    """He thong Danh muc Khoa hoc dien tu."""
    def __init__(self):
        self.sections: Dict[str, CourseSection] = {}

    def add_section(self, section: CourseSection):
        self.sections[section.section_id] = section

    def get_available_courses(self) -> List[Dict]:
        results = []
        for sec in self.sections.values():
            results.append({
                "section_id": sec.section_id,
                "course_id": sec.course.course_id,
                "course_name": sec.course.course_name,
                "credits": sec.course.credits,
                "available_places": sec.available_places,
                "max_seats": sec.max_seats
            })
        return results

class RegistrationController:
    """Bo dieu phoi nghiep vu Dang ky hoc phan."""
    def __init__(self, catalog: ElectronicCourseCatalog):
        self.catalog = catalog
        self.student_passed_courses: Dict[str, List[str]] = {
            "524H0195": ["CS101", "MATH101"], # Sinh vien da hoan thanh CS101 va MATH101
            "524H9999": [] # Sinh vien chua hoc mon tien quyet nao
        }
        self.enrollment_records: List[Dict] = []

    def register_course(self, student_id: str, section_id: str) -> tuple[bool, str]:
        print(f"\n[REGISTRATION] Yeu cau dang ky lop {section_id} tu Sinh vien MSSV: {student_id}")
        
        # 1. Kiem tra ton tai cua lop hoc phan
        section = self.catalog.sections.get(section_id)
        if not section:
            return False, "Lop hoc phan khong ton tai trong he thong."

        # 2. Kiem tra mon hoc tien quyet (Prerequisites Check)
        passed = self.student_passed_courses.get(student_id, [])
        for prereq in section.course.prerequisites:
            if prereq not in passed:
                msg = f"Tu choi dang ky: Sinh vien chua tich luy mon tien quyet {prereq}."
                print(f"  [KIEM TRA TIEN QUYET] -> THAT BAI: {msg}")
                return False, msg
        print("  [KIEM TRA TIEN QUYET] -> DAT: Sinh vien da hoan thanh day du mon tien quyet.")

        # 3. Kiem tra si so con cho trong (Capacity Check)
        if section.is_full():
            section.waitlist.append(student_id)
            msg = f"Lop {section_id} da het cho ({section.max_seats}/{section.max_seats}). Da dua vao danh sach cho (Waitlist vi tri #{len(section.waitlist)})."
            print(f"  [KIEM TRA CHO TRONG] -> HET CHO: {msg}")
            return False, msg

        # 4. Cap cho va Luu ho so dang ky vao CSDL (Commit Enrollment)
        section.enrolled_students.append(student_id)
        record_id = f"REG_{student_id}_{section_id}_{int(time.time())}"
        self.enrollment_records.append({
            "record_id": record_id,
            "student_id": student_id,
            "section_id": section_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        msg = f"Dang ky thanh cong lop {section_id} ({section.course.course_name}). Ma phieu dang ky: {record_id}."
        print(f"  [LUU HO SO CSDL] -> HOAN TAT: {msg}")
        return True, msg

def run_registration_demo():
    print("=======================================================================")
    print("DEMO MO PHONG BIEU DO TUAN TU DANG KY HOC PHAN (SE - EXERCISE 2)")
    print("=======================================================================")

    # Khoi tao du lieu mau
    c_se = Course("503074", "Software Engineering", 3, prerequisites=["CS101"])
    c_ai = Course("503080", "Artificial Intelligence", 3, prerequisites=["CS101", "MATH101"])

    sec_se1 = CourseSection("503074_01", c_se, max_seats=2)
    sec_ai1 = CourseSection("503080_01", c_ai, max_seats=1)

    catalog = ElectronicCourseCatalog()
    catalog.add_section(sec_se1)
    catalog.add_section(sec_ai1)

    controller = RegistrationController(catalog)

    # 1. Tra cuu danh muc khoa hoc dien tu
    print("\n--- GIAI DOAN 1: SINH VIEN TRA CUU DANH MUC HOC PHAN DIEN TU ---")
    available_courses = catalog.get_available_courses()
    for c in available_courses:
        print(f"  [CATALOG] Ma lop: {c['section_id']} | Mon: {c['course_name']} | Con trong: {c['available_places']}/{c['max_seats']}")

    # 2. Dang ky thanh cong
    print("\n--- GIAI DOAN 2: DANG KY THANH CONG (NORMAL FLOW) ---")
    controller.register_course("524H0195", "503074_01")

    # 3. Dang ky that bai do thieu mon tien quyet (Alternative Flow 1)
    print("\n--- GIAI DOAN 3: THAT BAI DO CHUA HOAN THANH TIEN QUYET ---")
    controller.register_course("524H9999", "503080_01")

    # 4. Dang ky that bai do lop da kin cho (Alternative Flow 2 -> Waitlist)
    print("\n--- GIAI DOAN 4: THAT BAI DO LOP HET CHO (SECTION FULL) ---")
    controller.register_course("524H0001", "503080_01") # Lay cho duy nhat cua lop AI
    controller.register_course("524H0195", "503080_01") # Sinh vien thu 2 dang ky se bi day vao waitlist

    print("\n=======================================================================")

if __name__ == "__main__":
    run_registration_demo()
