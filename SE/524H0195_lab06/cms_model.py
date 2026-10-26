"""
Module: cms_model.py
Author: Ngo Lam Tien (MSSV: 524H0195)
Subject: Software Engineering (503074) - Lab 04/06 (Exercise 1.2)
Description:
    Mo hinh huong doi tuong He thong Quan ly Khoa hoc (Courseware Management System - CMS).
    Mieu ta Course, Topic, Tutor, CourseAdministrator, CourseSchedule, CourseCalendar.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import date, time
from typing import List, Optional

class CourseArea(Enum):
    LEARNING_MANAGEMENT = "Learning Management Techniques"
    SOFTWARE_LANGUAGES = "Software Languages"
    SOFTWARE_TECHNOLOGIES = "Software Technologies"
    DATA_SCIENCE = "Data Science & AI"
    CYBER_SECURITY = "Cyber Security"

class ScheduleStatus(Enum):
    DRAFT = "Draft (Du thao)"
    ASSIGNED = "Assigned (Da phan cong)"
    CONFIRMED = "Confirmed (Da xac nhan)"
    IN_PROGRESS = "In Progress (Dang giang day)"
    COMPLETED = "Completed (Hoan thanh)"
    CANCELLED = "Cancelled (Da huy)"

@dataclass
class TimeSlot:
    day_of_week: str
    start_time: time
    end_time: time

    def conflicts_with(self, other: "TimeSlot") -> bool:
        if self.day_of_week != other.day_of_week:
            return False
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)

@dataclass
class Topic:
    topic_id: str
    title: str
    objectives: str
    duration_hours: int
    order_index: int

class Person:
    def __init__(self, person_id: str, full_name: str, email: str, phone: str):
        self.person_id = person_id
        self.full_name = full_name
        self.email = email
        self.phone = phone

class Tutor(Person):
    def __init__(self, tutor_id: str, full_name: str, email: str, phone: str, specializations: List[CourseArea], max_weekly_hours: int = 20):
        super().__init__(tutor_id, full_name, email, phone)
        self.specializations = specializations
        self.max_weekly_hours = max_weekly_hours
        self.availabilities: List[TimeSlot] = []

    def is_available(self, requested_slot: TimeSlot) -> bool:
        # Kiem tra xem khung gio co nam trong danh sach ranh hay khong
        for slot in self.availabilities:
            if not slot.conflicts_with(requested_slot):
                return True
        return True # Mac dinh co san neu chua set chi tiet

    def can_teach(self, area: CourseArea) -> bool:
        return area in self.specializations

class Course:
    def __init__(self, course_id: str, course_name: str, description: str, area: CourseArea, total_hours: int, max_enrolment: int = 40):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.area = area
        self.total_hours = total_hours
        self.max_enrolment = max_enrolment
        self.topics: List[Topic] = []

    def add_topic(self, topic: Topic):
        self.topics.append(topic)
        self.topics.sort(key=lambda t: t.order_index)

class CourseSchedule:
    def __init__(self, schedule_id: str, course: Course, start_date: date, end_date: date, time_slot: TimeSlot, room_location: str):
        self.schedule_id = schedule_id
        self.course = course
        self.start_date = start_date
        self.end_date = end_date
        self.time_slot = time_slot
        self.room_location = room_location
        self.assigned_tutor: Optional[Tutor] = None
        self.status: ScheduleStatus = ScheduleStatus.DRAFT

    def assign_tutor(self, tutor: Tutor) -> bool:
        if not tutor.can_teach(self.course.area):
            print(f"[ERROR] Tutor {tutor.full_name} khong co chuyen mon ve {self.course.area.value}.")
            return False
        if not tutor.is_available(self.time_slot):
            print(f"[ERROR] Tutor {tutor.full_name} bi trung gio day.")
            return False
        self.assigned_tutor = tutor
        self.status = ScheduleStatus.ASSIGNED
        print(f"[SUCCESS] Da phan cong Tutor {tutor.full_name} cho lop {self.schedule_id} ({self.course.course_name}).")
        return True

class CourseCalendar:
    def __init__(self, calendar_id: str, academic_year: int):
        self.calendar_id = calendar_id
        self.academic_year = academic_year
        self.schedules: List[CourseSchedule] = []
        self.is_published = False

    def add_schedule(self, schedule: CourseSchedule):
        self.schedules.append(schedule)

    def publish(self):
        self.is_published = True
        print(f"[CALENDAR] Da xuat ban LICH DAO TAO THUONG NIEN NAM HOC {self.academic_year}! Tong so lop mo: {len(self.schedules)}.")

class CourseAdministrator(Person):
    def __init__(self, admin_id: str, full_name: str, email: str, phone: str, department: str):
        super().__init__(admin_id, full_name, email, phone)
        self.department = department

    def create_course(self, course_id: str, name: str, desc: str, area: CourseArea, hours: int) -> Course:
        c = Course(course_id, name, desc, area, hours)
        print(f"[ADMIN] Tao moi khoa hoc: {c.course_id} - {c.course_name}")
        return c

    def publish_annual_calendar(self, calendar: CourseCalendar):
        calendar.publish()


if __name__ == "__main__":
    print("DEMO MO HINH LOP HE THONG CMS (EXERCISE 1.2)")
    admin = CourseAdministrator("ADM_01", "Phong Dao Tao TDTU", "pdt@tdtu.edu.vn", "02837755035", "Dao tao")
    
    c_arch = admin.create_course("SE_503074", "Software Architecture & UML", "Chuyen de thiet ke kien truc phan mem", CourseArea.SOFTWARE_TECHNOLOGIES, 45)
    c_arch.add_topic(Topic("TP_01", "Class Modeling", "Thiet ke bieu do lop huong doi tuong", 15, 1))
    c_arch.add_topic(Topic("TP_02", "Sequence Modeling", "Tuong tac giua cac doi tuong", 15, 2))
    c_arch.add_topic(Topic("TP_03", "Activity Modeling", "Quy trinh xu ly du lieu hoat dong", 15, 3))

    tutor = Tutor("TUT_01", "ThS. Mai Van Manh", "manhmv@tdtu.edu.vn", "0901234567", specializations=[CourseArea.SOFTWARE_TECHNOLOGIES, CourseArea.SOFTWARE_LANGUAGES])

    slot = TimeSlot("Thursday", time(7, 30), time(11, 0))
    schedule = CourseSchedule("SCH_2026_01", c_arch, date(2026, 9, 1), date(2026, 12, 31), slot, "Phong C.102")

    schedule.assign_tutor(tutor)

    annual_cal = CourseCalendar("CAL_2026", 2026)
    annual_cal.add_schedule(schedule)
    admin.publish_annual_calendar(annual_cal)
