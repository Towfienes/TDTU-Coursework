"""
Module: email_mailbox_model.py
Author: Ngo Lam Tien (MSSV: 524H0195)
Subject: Software Engineering (503074) - Lab 04/06 (Exercise 1.1)
Description:
    Mo hinh huong doi tuong bieu dien Hop thu (Mailbox) va Thu dien tu (EmailMessage)
    theo tieu chuan RFC 5322 va kien truc OOP co ban.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

class MailboxType(Enum):
    INBOX = "Inbox (Hop thu den)"
    SENT = "Sent (Thu da gui)"
    DRAFTS = "Drafts (Thu nhap)"
    TRASH = "Trash (Thung rac)"
    SPAM = "Spam (Thu rac)"
    CUSTOM = "Custom (Thu muc nguoi dung)"

class PriorityLevel(Enum):
    LOW = "Thap"
    NORMAL = "Binh thuong"
    HIGH = "Cao"

class RecipientType(Enum):
    TO = "To (Nguoi nhan chinh)"
    CC = "Cc (Dong kinh gui)"
    BCC = "Bcc (Gui an danh)"

@dataclass
class Attachment:
    attachment_id: str
    file_name: str
    content_type: str
    file_size_bytes: int
    data_payload: bytes = b""

    def get_info(self) -> str:
        return f"{self.file_name} ({self.content_type}, {self.file_size_bytes / 1024:.1f} KB)"

@dataclass
class EmailAddress:
    display_name: str
    email_address: str

    def is_valid(self) -> bool:
        return "@" in self.email_address and "." in self.email_address.split("@")[-1]

    def __str__(self):
        return f'"{self.display_name}" <{self.email_address}>' if self.display_name else self.email_address

@dataclass
class Recipient:
    recipient_type: RecipientType
    address: EmailAddress

@dataclass
class EmailMessage:
    message_id: str
    subject: str
    body_text: str
    sender: EmailAddress
    recipients: List[Recipient] = field(default_factory=list)
    sent_date: datetime = field(default_factory=datetime.now)
    is_read: bool = False
    is_starred: bool = False
    is_draft: bool = False
    priority: PriorityLevel = PriorityLevel.NORMAL
    attachments: List[Attachment] = field(default_factory=list)

    @property
    def total_size_bytes(self) -> int:
        body_size = len(self.body_text.encode('utf-8')) + len(self.subject.encode('utf-8'))
        att_size = sum(att.file_size_bytes for att in self.attachments)
        return body_size + att_size

    def mark_as_read(self):
        self.is_read = True

    def mark_as_unread(self):
        self.is_read = False

    def toggle_starred(self):
        self.is_starred = not self.is_starred

    def add_attachment(self, attachment: Attachment):
        self.attachments.append(attachment)

class Mailbox:
    def __init__(self, mailbox_id: str, name: str, mailbox_type: MailboxType, max_quota_bytes: int = 100 * 1024 * 1024):
        self.mailbox_id = mailbox_id
        self.name = name
        self.mailbox_type = mailbox_type
        self.max_quota_bytes = max_quota_bytes
        self.messages: List[EmailMessage] = []

    @property
    def total_messages(self) -> int:
        return len(self.messages)

    @property
    def unread_count(self) -> int:
        return sum(1 for m in self.messages if not m.is_read)

    @property
    def storage_size_bytes(self) -> int:
        return sum(m.total_size_bytes for m in self.messages)

    def add_message(self, msg: EmailMessage) -> bool:
        if self.storage_size_bytes + msg.total_size_bytes > self.max_quota_bytes:
            print(f"[MAILBOX FULL] Khong the luu thu: Dung luong hop thu '{self.name}' da vuot han muc.")
            return False
        self.messages.append(msg)
        return True

    def remove_message(self, message_id: str) -> bool:
        for idx, m in enumerate(self.messages):
            if m.message_id == message_id:
                del self.messages[idx]
                return True
        return False

    def search(self, keyword: str) -> List[EmailMessage]:
        kw = keyword.lower()
        return [m for m in self.messages if kw in m.subject.lower() or kw in m.body_text.lower()]


if __name__ == "__main__":
    print("DEMO MO HINH LOP MAILBOX & EMAIL MESSAGE (EXERCISE 1.1)")
    inbox = Mailbox("mbx_01", "Inbox", MailboxType.INBOX)
    sender = EmailAddress("Giang vien Mai Van Manh", "manhmv@tdtu.edu.vn")
    receiver = EmailAddress("Ngo Lam Tien", "524H0195@student.tdtu.edu.vn")

    msg = EmailMessage(
        message_id="msg_001",
        subject="Thong bao nop bai thuc hanh Lab 06 SE",
        body_text="Cac em hoan thanh day du Exercise 1, 2, 3 va nop file zip 524H0195_lab06.zip len Elearning.",
        sender=sender,
        recipients=[Recipient(RecipientType.TO, receiver)],
        priority=PriorityLevel.HIGH
    )
    msg.add_attachment(Attachment("att_1", "Lab04_6Class_Sequence.pdf", "application/pdf", 117725))

    inbox.add_message(msg)
    print(f"Hop thu: {inbox.name} | Tong thu: {inbox.total_messages} | Chua doc: {inbox.unread_count}")
    print(f"Thu gan nhat: '{msg.subject}' tu {msg.sender}")
    print(f"Dung luong thu: {msg.total_size_bytes / 1024:.2f} KB | Dinh kem: {len(msg.attachments)} tep.")
