import os
import re
import subprocess
from PIL import Image

SE_DIR = '/home/towfienes/TDTU/SE'
IMG_DIR = os.path.join(SE_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

with open('/tmp/mermaid.min.js', 'r', encoding='utf-8') as f:
    mjs = f.read()

# Define the Mermaid diagrams
DIAGRAMS = {
    'exercise1_1_mailbox_email_class': """classDiagram
    direction TB

    class EmailAccount {
        - accountId: String
        - ownerName: String
        - emailAddress: String
        - totalStorageUsed: long
        + createMailbox(name: String): Mailbox
        + deleteMailbox(mailboxId: String): boolean
        + syncMailboxes(): void
    }

    class Mailbox {
        - mailboxId: String
        - name: String
        - type: MailboxType
        - totalMessages: int
        - unreadCount: int
        - storageSize: long
        - maxQuota: long
        + addMessage(msg: EmailMessage): boolean
        + removeMessage(msgId: String): boolean
        + getMessageById(msgId: String): EmailMessage
        + listMessages(page: int, size: int): List~EmailMessage~
        + filterBySender(sender: String): List~EmailMessage~
        + search(keyword: String): List~EmailMessage~
        + emptyFolder(): void
        + calculateUnreadCount(): int
    }

    class EmailMessage {
        - messageId: String
        - subject: String
        - bodyText: String
        - bodyHtml: String
        - sentDate: DateTime
        - receivedDate: DateTime
        - isRead: boolean
        - isStarred: boolean
        - isDraft: boolean
        - priority: PriorityLevel
        - totalSize: long
        + markAsRead(): void
        + markAsUnread(): void
        + toggleStarred(): void
        + moveToMailbox(target: Mailbox): boolean
        + reply(content: String, replyAll: boolean): EmailMessage
        + forward(recipients: List~EmailAddress~): EmailMessage
        + addAttachment(file: Attachment): boolean
        + removeAttachment(attId: String): boolean
    }

    class Attachment {
        - attachmentId: String
        - fileName: String
        - contentType: String
        - fileSize: long
        - fileData: byte[]
        + download(): byte[]
        + getFileInfo(): String
    }

    class EmailAddress {
        - displayName: String
        - emailAddress: String
        + validate(): boolean
        + getFormatted(): String
    }

    class Recipient {
        - recipientType: RecipientType
        + getType(): RecipientType
    }

    class PriorityLevel {
        <<enumeration>>
        LOW
        NORMAL
        HIGH
    }

    class MailboxType {
        <<enumeration>>
        INBOX
        SENT
        DRAFTS
        TRASH
        SPAM
        CUSTOM
    }

    class RecipientType {
        <<enumeration>>
        TO
        CC
        BCC
    }

    EmailAccount "1" *-- "1..*" Mailbox : contains
    Mailbox "1" o-- "0..*" EmailMessage : stores
    EmailMessage "1" *-- "0..*" Attachment : attaches
    EmailMessage "1" --> "1" EmailAddress : sender
    EmailMessage "1" *-- "1..*" Recipient : recipients
    Recipient "1" --> "1" EmailAddress : refers_to
    EmailMessage ..> PriorityLevel
    Mailbox ..> MailboxType
    Recipient ..> RecipientType""",

    'exercise1_2_courseware_cms_class': """classDiagram
    direction TB

    class Person {
        <<abstract>>
        # personId: String
        # fullName: String
        # email: String
        # phone: String
        + getContactInfo(): String
    }

    class Tutor {
        - tutorId: String
        - specializations: List~CourseArea~
        - maxWeeklyHours: int
        + isAvailable(slot: TimeSlot): boolean
        + addSpecialization(area: CourseArea): void
        + getAssignedSchedules(year: int): List~CourseSchedule~
        + updateAvailability(slot: TimeSlot, free: boolean): void
    }

    class CourseAdministrator {
        - adminId: String
        - department: String
        + createCourse(c: Course): boolean
        + assignCourseToTutor(courseId: String, tutorId: String): boolean
        + createCourseSchedule(cs: CourseSchedule): boolean
        + publishAnnualCalendar(year: int): CourseCalendar
    }

    class Course {
        - courseId: String
        - courseName: String
        - description: String
        - area: CourseArea
        - totalHours: int
        - maxEnrolment: int
        + addTopic(t: Topic): void
        + removeTopic(topicId: String): void
        + getSyllabus(): List~Topic~
        + updateDetails(desc: String): void
    }

    class Topic {
        - topicId: String
        - title: String
        - objectives: String
        - durationHours: int
        - orderIndex: int
        + getTopicDetails(): String
        + setOrder(order: int): void
        + updateObjectives(obj: String): void
    }

    class CourseSchedule {
        - scheduleId: String
        - startDate: Date
        - endDate: Date
        - roomLocation: String
        - status: ScheduleStatus
        - currentEnrolment: int
        + assignTutor(t: Tutor): boolean
        + setTimeSlot(slot: TimeSlot): void
        + checkCapacity(): boolean
        + cancelSchedule(): void
    }

    class CourseCalendar {
        - calendarId: String
        - academicYear: int
        - publishedDate: Date
        - isPublished: boolean
        + addSchedule(cs: CourseSchedule): void
        + publish(): void
        + searchByArea(area: CourseArea): List~CourseSchedule~
        + exportCalendar(): File
    }

    class TimeSlot {
        - dayOfWeek: String
        - startTime: Time
        - endTime: Time
        + conflictsWith(other: TimeSlot): boolean
    }

    class CourseArea {
        <<enumeration>>
        LEARNING_MANAGEMENT
        SOFTWARE_LANGUAGES
        SOFTWARE_TECHNOLOGIES
        DATA_SCIENCE
        CYBER_SECURITY
    }

    class ScheduleStatus {
        <<enumeration>>
        DRAFT
        ASSIGNED
        CONFIRMED
        IN_PROGRESS
        COMPLETED
        CANCELLED
    }

    Person <|-- Tutor : inheritance
    Person <|-- CourseAdministrator : inheritance
    Course "1" *-- "1..*" Topic : consists of
    Course "1" o-- "0..*" CourseSchedule : instantiated as
    CourseSchedule "0..*" --> "0..1" Tutor : taught by
    CourseSchedule "1" *-- "1..*" TimeSlot : scheduled at
    CourseCalendar "1" o-- "0..*" CourseSchedule : publishes
    CourseAdministrator ..> Course : manages
    CourseAdministrator ..> CourseSchedule : schedules
    CourseAdministrator ..> CourseCalendar : publishes
    Tutor "1" o-- "0..*" TimeSlot : availability
    Course ..> CourseArea
    CourseSchedule ..> ScheduleStatus""",

    'exercise2_course_registration_sequence': """sequenceDiagram
    autonumber
    actor Student as s: Student
    participant UI as : PortalUI
    participant Catalog as : CourseCatalog
    participant RegCtrl as : RegistrationController
    participant Section as : CourseSection
    participant DB as : EnrollmentDB

    rect rgb(240, 248, 255)
        Note over Student, Catalog: Giai đoạn 1: Tra cứu danh mục học phần điện tử
        Student ->> UI: accessCourseCatalog()
        UI ->> Catalog: getAvailableCourses(semester)
        Catalog -->> UI: return courseList (id, name, credits, availablePlaces)
        UI -->> Student: displayCourseCatalog(courseList)
    end

    rect rgb(255, 250, 240)
        Note over Student, Section: Giai đoạn 2: Gửi yêu cầu đăng ký & Kiểm tra sĩ số
        Student ->> UI: selectCourse(courseId)
        Student ->> UI: clickRegisterButton()
        UI ->> RegCtrl: registerCourse(studentId, courseId)
        
        RegCtrl ->> Section: checkPrerequisites(studentId)
        Section -->> RegCtrl: prerequisitesSatisfied (true)

        RegCtrl ->> Section: checkSeatAvailability()
        Section ->> Section: compare(enrolledCount, maxSeats)
    end

    alt Chỗ còn trống (places available > 0)
        Section -->> RegCtrl: availabilityStatus(true, remainingSeats)
        RegCtrl ->> Section: incrementEnrollment()
        Section -->> RegCtrl: seatReservedSuccessfully

        RegCtrl ->> DB: createEnrollmentRecord(studentId, courseId, timestamp)
        DB -->> RegCtrl: enrollmentRecordConfirmed(recordId)

        RegCtrl -->> UI: registrationSuccess(recordId, courseName)
        UI -->> Student: showRegistrationConfirmation("Đăng ký thành công!")

    else Hết chỗ (places == 0)
        Section -->> RegCtrl: availabilityStatus(false, 0)
        RegCtrl -->> UI: registrationFailed("Lớp học đã đủ sĩ số")
        UI -->> Student: showErrorMessage("Đăng ký thất bại: Lớp đã kín chỗ! Đã đưa vào Waitlist")

    else Không thỏa điều kiện tiên quyết (Prerequisites not met)
        Section -->> RegCtrl: prerequisitesSatisfied (false)
        RegCtrl -->> UI: registrationFailed("Chưa hoàn thành học phần tiên quyết")
        UI -->> Student: showErrorMessage("Lỗi: Bạn chưa đủ điều kiện tiên quyết của môn này!")
    end""",

    'exercise3_atm_cash_withdrawal_activity': """flowchart TD
    startNode([● Bắt đầu]) --> insertCard[Khách hàng đưa thẻ ATM vào khe]
    insertCard --> readCard[Đầu đọc đọc thông tin thẻ trên Chip/Từ]
    
    readCard --> checkCardValid{Thẻ hợp lệ & Còn hạn?}
    checkCardValid -- Không --> ejectInvalidCard[Nhả thẻ & Báo lỗi thẻ không hợp lệ]
    ejectInvalidCard --> endNode1([● Kết thúc])

    checkCardValid -- Có --> promptPin[Yêu cầu khách hàng nhập mã PIN]
    promptPin --> enterPin[Khách hàng nhập mã PIN trên bàn phím số]
    enterPin --> verifyPin{Xác thực mã PIN tại Bank Host?}

    verifyPin -- Sai PIN --> incPinCount[Tăng số lần thử: attempts = attempts + 1]
    incPinCount --> checkMaxAttempts{attempts >= 3?}
    checkMaxAttempts -- Đúng --> swallowCard[Nuốt thẻ ATM & Khóa tài khoản tạm thời]
    swallowCard --> showLockMsg[Hiển thị cảnh báo: Thẻ bị giữ lại vì nhập sai PIN quá 3 lần]
    showLockMsg --> endNode2([● Kết thúc])
    checkMaxAttempts -- Sai --> showRetryPin[Hiển thị: Mã PIN không đúng. Vui lòng nhập lại]
    showRetryPin --> promptPin

    verifyPin -- Đúng PIN --> resetAttempts[Đặt lại số lần thử attempts = 0]
    resetAttempts --> selectAccount[Chọn loại tài khoản: Thanh toán / Tiết kiệm]
    selectAccount --> inputAmount[Khách hàng nhập số tiền cần rút]

    inputAmount --> checkMultiple{Số tiền là bội số hợp lệ & trong hạn mức lần rút?}
    checkMultiple -- Không --> showInvalidAmount[Báo lỗi: Số tiền không hợp lệ hoặc vượt hạn mức lần rút]
    showInvalidAmount --> askNewAmount{Thử lại số tiền khác?}
    askNewAmount -- Có --> inputAmount
    askNewAmount -- Không --> returnCardEarly[Nhả thẻ ATM] --> endNode3([● Kết thúc])

    checkMultiple -- Có --> checkAtmMoney{ATM còn đủ tiền mặt để chi trả?}
    checkAtmMoney -- Không --> showAtmEmpty[Báo lỗi: ATM hiện không đủ tiền mặt theo yêu cầu]
    showAtmEmpty --> returnCardEarly

    checkAtmMoney -- Có --> queryBalance[Gửi yêu cầu kiểm tra số dư tới Hệ thống Core Banking]
    queryBalance --> checkBalance{Số dư khả dụng >= Số tiền + Phí giao dịch?}
    checkBalance -- Không --> showInsufficientFund[Báo lỗi: Số dư tài khoản không đủ]
    showInsufficientFund --> askNewAmount

    checkBalance -- Có --> fork1[══ Khởi tạo tiến trình xử lý song song ══]

    fork1 --> debitAccount[Core Banking: Trừ số dư tài khoản & Ghi sổ nhật ký giao dịch]
    fork1 --> countCash[Bộ đếm tiền ATM: Phân bổ và đếm các mệnh giá tiền mặt]

    debitAccount --> join1[══ Đồng bộ hóa tiến trình ══]
    countCash --> join1

    join1 --> ejectCardFirst[Cây ATM đẩy thẻ ra & Phát âm thanh cảnh báo]
    ejectCardFirst --> customerTakesCard[Khách hàng rút thẻ khỏi khe nhận thẻ]
    
    customerTakesCard --> dispenseCash[Mở cửa khe tiền & Đẩy tiền mặt ra]
    dispenseCash --> customerTakesCash[Khách hàng nhận tiền mặt]

    customerTakesCash --> askReceipt{Khách hàng muốn in biên lai giao dịch?}
    askReceipt -- Có --> printReceipt[In hóa đơn giấy tại khe biên lai]
    askReceipt -- Không --> sendSMS[Gửi thông báo biến động số dư qua SMS / Mobile App]

    printReceipt --> completeTransaction[Hoàn tất phiên giao dịch & Cảm ơn quý khách]
    sendSMS --> completeTransaction
    completeTransaction --> endNode4([● Kết thúc])""",

    'exercise3_atm_cash_withdrawal_swimlane': """flowchart TD
    subgraph LANE_CUSTOMER["🏊 KHÁCH HÀNG (CUSTOMER)"]
        c1([● Bắt đầu]) --> c_insert["Đưa thẻ ATM vào khe"]
        c_enter_pin["Nhập mã PIN bí mật"]
        c_choose["Chọn giao dịch Rút tiền & Nhập số tiền"]
        c_take_card["Rút thẻ ATM khỏi khe"]
        c_take_cash["Nhận tiền mặt tại cửa nhả"]
        c_receive_rcpt["Nhận biên lai / SMS biến động"] --> c_end([● Kết thúc])
    end

    subgraph LANE_ATM_UI["🖥️ GIAO DIỆN & PHẦN CỨNG ATM (TERMINAL UI & DEVICES)"]
        dev_reader["Đầu đọc đọc chip EMV / Thẻ từ"]
        dev_show_pin["Màn hình hiển thị nhắc nhập PIN"]
        dev_epp["Bàn phím EPP mã hóa PIN"]
        dev_menu["Hiển thị menu chọn tài khoản & số tiền"]
        dev_eject_card["Cơ cấu nhả thẻ & Loa phát chuông cảnh báo"]
        dev_shutter["Mở cửa chớp nhả tiền mặt"]
        dev_printer["Máy in in biên lai giấy"]
    end

    subgraph LANE_ATM_CTRL["⚙️ BỘ ĐIỀU KHIỂN ATM (ATM TERMINAL CONTROLLER)"]
        ctrl_card_valid{Thẻ hợp lệ?}
        ctrl_chk_format{Bội số 50k & Trong hạn mức?}
        ctrl_chk_reserve{ATM đủ tiền mặt?}
        ctrl_bill_picker["Kích hoạt bộ đếm và phân bổ tờ tiền"]
        ctrl_chk_card_taken{Khách đã rút thẻ?}
        ctrl_chk_cash_taken{Khách đã lấy tiền?}
        ctrl_retain_card["Timeout 30s: Nuốt thẻ vào Retain Box"]
        ctrl_retract_cash["Timeout 30s: Thu hồi tiền vào Retract Bin"]
    end

    subgraph LANE_BANK_HOST["🏦 HỆ THỐNG NGÂN HÀNG (CORE BANKING HOST)"]
        bank_auth{Xác thực PIN & Thẻ?}
        bank_pin_fail["Tăng attempts (>=3 khóa thẻ)"]
        bank_chk_bal{Số dư khả dụng >= Tiền + Phí?}
        bank_debit["Ghi nợ tài khoản & Ghi Audit Log"]
        bank_rollback["Thực hiện Auto-Reversal / Hoàn trả tiền"]
        bank_sms["Gửi tin nhắn SMS / OTT biến động"]
    end

    %% Luong tuong tac lien phan vung
    c_insert --> dev_reader --> ctrl_card_valid
    ctrl_card_valid -- Không --> dev_eject_card
    ctrl_card_valid -- Có --> dev_show_pin --> c_enter_pin --> dev_epp --> bank_auth
    
    bank_auth -- Sai PIN --> bank_pin_fail
    bank_pin_fail --> dev_show_pin
    
    bank_auth -- Thành công --> dev_menu --> c_choose --> ctrl_chk_format
    ctrl_chk_format -- Không --> dev_menu
    ctrl_chk_format -- Có --> ctrl_chk_reserve
    
    ctrl_chk_reserve -- Không --> dev_eject_card
    ctrl_chk_reserve -- Có --> bank_chk_bal

    bank_chk_bal -- Không đủ --> dev_menu
    bank_chk_bal -- Đủ số dư --> fork_bar[══ FORK: XỬ LÝ SONG SONG ══]

    fork_bar --> bank_debit
    fork_bar --> ctrl_bill_picker

    bank_debit --> join_bar[══ JOIN: ĐỒNG BỘ ══]
    ctrl_bill_picker --> join_bar

    join_bar --> dev_eject_card --> ctrl_chk_card_taken
    ctrl_chk_card_taken -- Quá 30s không lấy --> ctrl_retain_card --> bank_rollback
    ctrl_chk_card_taken -- Đã rút thẻ --> c_take_card --> dev_shutter --> ctrl_chk_cash_taken

    ctrl_chk_cash_taken -- Quá 30s không lấy --> ctrl_retract_cash --> bank_rollback
    ctrl_chk_cash_taken -- Đã nhận tiền --> c_take_cash --> dev_printer --> c_receive_rcpt
    bank_rollback --> c_end"""
}

for name, code in DIAGRAMS.items():
    escaped_block = code.replace('\\\\', '\\\\\\\\').replace('`', '\\\\`').replace('$', '\\\\$')
    
    html_page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    margin: 0;
    padding: 30px;
    background: #ffffff;
    display: inline-block;
}}
#container {{
    display: inline-block;
    background: #ffffff;
}}
</style>
<script>{mjs}</script>
</head>
<body>
<div id="container"></div>
<script>
async function render() {{
    mermaid.initialize({{
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose'
    }});
    const res = await mermaid.render('d_{name}', `{escaped_block}`);
    const cont = document.getElementById('container');
    cont.innerHTML = res.svg;
    const svg = cont.querySelector('svg');
    svg.removeAttribute('style');
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    
    const vb = svg.viewBox.baseVal;
    const w = Math.ceil(vb.width);
    const h = Math.ceil(vb.height);
    document.title = w + 'x' + h;
}}
render();
</script>
</body>
</html>"""

    tmp_html = f'/tmp/render_{name}.html'
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_page)

    res = subprocess.run([
        'chromium', '--no-sandbox', '--headless', '--disable-gpu', '--virtual-time-budget=4000',
        '--dump-dom', tmp_html
    ], capture_output=True, text=True)

    # Save SVG directly from container
    svg_match = re.search(r'<div id="container">(<svg.*?</svg>)</div>', res.stdout, re.DOTALL)
    if svg_match:
        svg_file = os.path.join(IMG_DIR, f"{name}.svg")
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(svg_match.group(1))
        print(f"Saved real SVG: {svg_file} ({os.path.getsize(svg_file)} bytes)")

    m = re.search(r'<title>(\d+)x(\d+)</title>', res.stdout)
    if m:
        w_orig, h_orig = int(m.group(1)), int(m.group(2))
        win_w = w_orig + 80
        win_h = h_orig + 80
    else:
        win_w, win_h = 1400, 1800

    raw_png = f'/tmp/raw_{name}.png'
    subprocess.run([
        'chromium', '--no-sandbox', '--headless', '--disable-gpu',
        '--force-device-scale-factor=2',
        f'--window-size={win_w},{win_h}',
        f'--screenshot={raw_png}',
        tmp_html
    ], check=True)

    img = Image.open(raw_png)
    bbox = img.getbbox()
    if bbox:
        pad = 25
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(img.width, bbox[2] + pad)
        bottom = min(img.height, bbox[3] + pad)
        cropped = img.crop((left, top, right, bottom))
    else:
        cropped = img

    out_file = os.path.join(IMG_DIR, f"{name}.png")
    cropped.save(out_file, 'PNG')
    print(f"Saved PNG: {out_file} (size: {cropped.size})")

print("All diagrams rendered successfully in SVG & Retina PNG formats!")
