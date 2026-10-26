import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

TEMPLATE_PATH = 'BMTT_Midterm Theory Report Template.docx'
OUTPUT_PATH = 'BMTT_Midterm_Theory_Report_Topic13_Completed.docx'
DIAGRAM_PATH = 'architecture_diagram.png'

doc = docx.Document(TEMPLATE_PATH)

def format_run(run, text, font_name="Times New Roman", font_size=12, bold=False, italic=False, color_rgb=None):
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = color_rgb
    return run

def insert_p_after(prev_element, doc, style='Normal', space_after=6, space_before=0, line_spacing=1.145833, align=None, keep_with_next=False):
    new_p = doc.add_paragraph(style=style)
    pf = new_p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = line_spacing
    if align is not None:
        new_p.alignment = align
    if keep_with_next:
        pf.keep_with_next = True
    prev_element.addnext(new_p._p)
    return new_p

def insert_item_after(prev_element, doc, bold_prefix="", body_text="", space_after=4, space_before=0, left_indent_pt=18, **kwargs):
    p = insert_p_after(prev_element, doc, space_after=space_after, space_before=space_before)
    p.paragraph_format.left_indent = Pt(left_indent_pt)
    
    # Clean hyphen bullet prefix without circular dots
    r_dash = p.add_run("- ")
    format_run(r_dash, "- ", bold=True)
    
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        format_run(r1, bold_prefix, bold=True)
    if body_text:
        r2 = p.add_run(body_text)
        format_run(r2, body_text, bold=False)
    return p

def insert_code_box_after(prev_element, doc, code_text, caption_text=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.autofit = False
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.columns[0].width = Inches(6.0)
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.0)
    
    # Soft background and left accent border
    shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shd)
    
    borders = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(borders)
    
    # Internal cell margins
    tcMar = parse_xml(r'''
        <w:tcMar {} >
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="160" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="160" w:type="dxa"/>
        </w:tcMar>
    '''.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(tcMar)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(code_text)
    format_run(r, code_text, font_name="Consolas", font_size=9.2, color_rgb=RGBColor(0x0F, 0x17, 0x2A))
    
    prev_element.addnext(tbl._tbl)
    
    curr = tbl._tbl
    if caption_text:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(3)
        p_cap.paragraph_format.space_after = Pt(7)
        r_cap = p_cap.add_run(caption_text)
        format_run(r_cap, caption_text, font_name="Times New Roman", font_size=10, italic=True, color_rgb=RGBColor(0x47, 0x55, 0x69))
        tbl._tbl.addnext(p_cap._p)
        curr = p_cap._p
        
    return curr

def remove_p(p):
    p._p.getparent().remove(p._p)

print("Starting report rebuild with perfected layout and updated diagram...")

# -------------------------------------------------------------
# Section 1: Project Metadata
# -------------------------------------------------------------
for i in range(5, 10):
    p = doc.paragraphs[i]
    pPr = p._p.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
    if pPr is not None:
        numPr = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr')
        if numPr is not None:
            pPr.remove(numPr)
    p.paragraph_format.left_indent = Pt(18)

# P5: ClassID & Group ID with clean tab stop at 3.0 inches
p05 = doc.paragraphs[5]
p05.text = ""
p05.paragraph_format.tab_stops.add_tab_stop(Inches(3.0), WD_TAB_ALIGNMENT.LEFT)
r5_dash = p05.add_run("- ")
format_run(r5_dash, "- ", bold=True)
r5_lbl1 = p05.add_run("ClassID: ")
format_run(r5_lbl1, "ClassID: ", bold=True)
r5_tab = p05.add_run("\tGroup ID:")
format_run(r5_tab, "\tGroup ID:", bold=True)

# P6: Project Title
p06 = doc.paragraphs[6]
p06.text = ""
r6_dash = p06.add_run("- ")
format_run(r6_dash, "- ", bold=True)
r_t_lbl = p06.add_run("Project Title: ")
format_run(r_t_lbl, "Project Title: ", bold=True)
r_t_val = p06.add_run("Security in Client-Server Android Applications: Permissions, Intent Security, and Local Data Protection")
format_run(r_t_val, "Security in Client-Server Android Applications: Permissions, Intent Security, and Local Data Protection", bold=False)

# P7: Student Name (two columns with tab stop at 3.0 inches, perfectly fitting one line)
p07 = doc.paragraphs[7]
p07.text = ""
p07.paragraph_format.tab_stops.add_tab_stop(Inches(3.0), WD_TAB_ALIGNMENT.LEFT)
r7_dash = p07.add_run("- ")
format_run(r7_dash, "- ", bold=True)
r7_lbl1 = p07.add_run("Student Name: ")
format_run(r7_lbl1, "Student Name: ", bold=True)
r7_txt = p07.add_run("_______________\tStudent Name: _______________")
format_run(r7_txt, "_______________\tStudent Name: _______________", bold=False)

# P8: Student ID (two columns with tab stop at 3.0 inches, perfectly fitting one line)
p08 = doc.paragraphs[8]
p08.text = ""
p08.paragraph_format.tab_stops.add_tab_stop(Inches(3.0), WD_TAB_ALIGNMENT.LEFT)
r8_dash = p08.add_run("- ")
format_run(r8_dash, "- ", bold=True)
r8_lbl1 = p08.add_run("Student ID: ")
format_run(r8_lbl1, "Student ID: ", bold=True)
r8_txt = p08.add_run("_______________\tStudent ID: _______________")
format_run(r8_txt, "_______________\tStudent ID: _______________", bold=False)

# P9: Topic Domain
p09 = doc.paragraphs[9]
p09.text = ""
r9_dash = p09.add_run("- ")
format_run(r9_dash, "- ", bold=True)
r_d_lbl = p09.add_run("Topic Domain: ")
format_run(r_d_lbl, "Topic Domain: ", bold=True)
r_d_val = p09.add_run("Mobile Application Security / Application Security")
format_run(r_d_val, "Mobile Application Security / Application Security", bold=False)

# Keep with next for all Heading 3 paragraphs
headings_idx = [4, 10, 14, 20, 23, 29, 34, 38, 43]
for idx in headings_idx:
    doc.paragraphs[idx].paragraph_format.keep_with_next = True

# -------------------------------------------------------------
# Section 2: Executive Summary (Abstract)
# -------------------------------------------------------------
p11 = doc.paragraphs[11]
p12 = doc.paragraphs[12]
p13 = doc.paragraphs[13]

abstract_text = (
    "Android applications operate within a multi-layered security architecture comprising Linux-based "
    "process sandboxing, a granular permission framework, discrete application components, inter-process communication "
    "via Intents, and private local storage. However, severe vulnerabilities emerge when developers misconfigure "
    "component exposure, place unwarranted trust in incoming IPC messages, or persist sensitive assets insecurely. "
    "This report investigates two critical client-side vulnerability classes: Intent Injection/Redirection, wherein "
    "an unvalidated Intent allows an untrusted caller to execute privileged internal functionality, and insecure "
    "local data storage, focusing on the risks of plaintext credentials and session tokens within SQLite databases. "
    "We analyze the technical root causes, step-by-step exploitation mechanics, impacts across the Confidentiality, "
    "Integrity, and Availability (CIA) triad, and rigorous architectural mitigations. Additionally, we contextualize "
    "these client-side weaknesses within the broader client-server threat model, establishing the theoretical foundation "
    "for our final project demonstration. In that phase, we will construct a client-server Android chat application in an "
    "authorized laboratory environment, execute a controlled Man-in-the-Middle (MITM) traffic interception using Burp "
    "Suite against an intentionally vulnerable configuration, and systematically remediate the exposure by implementing "
    "SSL/Certificate Pinning."
)

p_abs = insert_p_after(p11._p, doc, space_after=12)
r_abs = p_abs.add_run(abstract_text)
format_run(r_abs, abstract_text)

remove_p(p12)
remove_p(p13)

# -------------------------------------------------------------
# Section 3: Technical Background Concepts
# -------------------------------------------------------------
p15 = [p for p in doc.paragraphs if p.text.strip() == '(Min 300 words)'][0]
p16 = [p for p in doc.paragraphs if p.text.startswith('Instruction: Before explaining')][0]
p17 = [p for p in doc.paragraphs if p.text.startswith('If your topic is Buffer Overflow')][0]
p18 = [p for p in doc.paragraphs if p.text.startswith('If your topic is Phishing')][0]
p19 = [p for p in doc.paragraphs if p.text.startswith('If your topic is Encryption')][0]

curr = p15._p

sec3_intro = (
    "To understand vulnerabilities within modern Android client-server applications, one must first analyze the "
    "fundamental architectural paradigms that define Android’s system security model. The operating system departs "
    "substantially from traditional desktop computing environments by isolating applications at the kernel level and "
    "enforcing an explicit component-based communication model. This architecture relies on six foundational pillars: "
    "process sandboxing, the permission model, the application manifest, modular components, the Intent inter-process "
    "communication (IPC) framework, and local storage mechanisms."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec3_intro)
format_run(r, sec3_intro)
curr = p._p

# A. Sandbox
p_a_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_a_head.add_run("A. Android Application Sandbox")
format_run(r, "A. Android Application Sandbox", bold=True)
curr = p_a_head._p

sec3_a_body = (
    "At the foundation of Android security is the Linux kernel application sandbox. Unlike traditional desktop operating "
    "systems where all user-level processes execute under a shared user identifier (UID) and possess identical access "
    "rights to user files, Android assigns a unique, immutable Linux UID to each application upon installation "
    "(e.g., u0_a142). The Android runtime environment enforces strict process isolation: each application executes within "
    "its own dedicated process running an independent instance of the Android Runtime (ART) virtual machine. At the kernel "
    "level, standard Linux Discretionary Access Control (DAC) file permissions (typically rwx------ or 0700) restrict read "
    "and write access for the application's private data directory (/data/data/<package_name>/) exclusively to that application's "
    "designated UID. In conjunction with Security-Enhanced Linux (SELinux) mandatory access control (MAC) policies, this sandbox "
    "constitutes the primary perimeter preventing direct process memory tampering and unauthorized file access between disparate applications."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec3_a_body)
format_run(r, sec3_a_body)
curr = p._p

# B. Permission Model
p_b_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_b_head.add_run("B. Android Permission Model")
format_run(r, "B. Android Permission Model", bold=True)
curr = p_b_head._p

sec3_b_body = (
    "While sandboxing isolates applications by default, applications frequently require access to sensitive hardware "
    "interfaces, system subsystems, and private user data. The Android Permission Model acts as a gatekeeper governing "
    "access to these restricted resources, operating under the principle of least privilege. Permissions are categorized "
    "into distinct protection levels:"
)
p = insert_p_after(curr, doc, space_after=4)
r = p.add_run(sec3_b_body)
format_run(r, sec3_b_body)
curr = p._p

curr = insert_item_after(curr, doc, "Normal (Install-Time) Permissions: ",
    "Applied to low-risk operations that pose minimal privacy or security concerns, such as accessing network state "
    "(android.permission.ACCESS_NETWORK_STATE) or establishing outbound socket connections (android.permission.INTERNET). "
    "These permissions are automatically granted by the operating system upon application installation without interactive prompts.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Dangerous (Runtime) Permissions: ",
    "Applied to high-risk operations granting direct access to sensitive user data or privacy-critical hardware, including "
    "CAMERA, RECORD_AUDIO, READ_CONTACTS, and ACCESS_FINE_LOCATION. Since Android 6.0 (API level 23), dangerous permissions "
    "must be explicitly requested at runtime, requiring deliberate user authorization through an interactive system dialog.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Signature Permissions: ",
    "The highest standard protection level for inter-application trust. A signature permission is granted automatically by "
    "the OS only if the requesting application is signed with the identical cryptographic signing certificate as the application "
    "declaring the permission. This mechanism allows a single developer or organization to share privileged components and "
    "sensitive data securely between a suite of proprietary apps without exposing them to third parties.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Special Permissions: ",
    "Regulate access to advanced system capabilities, such as SYSTEM_ALERT_WINDOW (drawing overlays over other applications) "
    "or WRITE_SETTINGS, requiring explicit user navigation into dedicated system settings management menus.",
    space_after=6)._p

# C. AndroidManifest.xml
p_c_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_c_head.add_run("C. AndroidManifest.xml")
format_run(r, "C. AndroidManifest.xml", bold=True)
curr = p_c_head._p

sec3_c_body = (
    "The AndroidManifest.xml file serves as the definitive structural blueprint and central root of trust for an Android package. "
    "Located at the root of the project source, it declares the package identity, required hardware features, requested permissions "
    "(<uses-permission>), custom-defined permissions (<permission>), and all application components. Crucially, the manifest defines "
    "the external attack surface through the android:exported attribute. If a component is declared with android:exported=\"true\", "
    "it can be instantiated, invoked, or queried by any external application installed on the operating system. Conversely, "
    "android:exported=\"false\" restricts invocation strictly to components residing within the same package or sharing the same Linux UID. "
    "Starting in Android 12 (API level 31), developers are mandated to declare android:exported explicitly for every component declaring "
    "intent filters, eliminating prior implicit defaulting ambiguities that historically generated unintended attack vectors."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec3_c_body)
format_run(r, sec3_c_body)
curr = p._p

# D. Android Components
p_d_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_d_head.add_run("D. Android Application Components")
format_run(r, "D. Android Application Components", bold=True)
curr = p_d_head._p

sec3_d_body = (
    "Android applications are not monolithic executables initiated from a static main() function; rather, they are composed of four "
    "loosely coupled, modular components, each serving a distinct lifecycle and communication role:"
)
p = insert_p_after(curr, doc, space_after=4)
r = p.add_run(sec3_d_body)
format_run(r, sec3_d_body)
curr = p._p

curr = insert_item_after(curr, doc, "Activity: ",
    "A visual component representing a single interactive screen with a graphical user interface (UI), facilitating direct human-computer interaction.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Service: ",
    "An invisible background component designed to perform long-running operations without providing a direct UI, such as audio playback or network synchronization.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "BroadcastReceiver: ",
    "An asynchronous listener component designed to receive and process broadcast messages issued by the system (e.g., ACTION_BOOT_COMPLETED, battery status changes) or by other applications.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "ContentProvider: ",
    "A structured data abstraction component that encapsulates an underlying data store—most commonly an embedded SQLite database—and provides standardized CRUD (Create, Read, Update, Delete) interfaces across process boundaries via uniform resource identifiers (URIs).",
    space_after=6)._p

# E. Intents and Intent Filters
p_e_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_e_head.add_run("E. Intents and Intent Filters")
format_run(r, "E. Intents and Intent Filters", bold=True)
curr = p_e_head._p

sec3_e_body = (
    "Inter-process communication (IPC) and inter-component signaling in Android are primarily conducted through message-passing "
    "objects termed Intents. An Intent represents an asynchronous request encapsulating: an Action string (e.g., Intent.ACTION_VIEW), "
    "a Data URI and MIME type, Category identifiers, Extras (a key-value Bundle carrying arbitrary serializable or parcelable payloads), "
    "and Flags (bitmask instructions dictating activity backstack management and URI permissions, such as FLAG_GRANT_READ_URI_PERMISSION). "
    "Intents are bifurcated into two foundational categories: Explicit Intents specifically designate the destination component by "
    "explicitly declaring its target package name and class name, ensuring direct routing for secure internal navigation. Conversely, "
    "Implicit Intents declare a desired action and data type without specifying a recipient; the Android OS resolves implicit intents "
    "dynamically by matching them against <intent-filter> declarations across all installed applications."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec3_e_body)
format_run(r, sec3_e_body)
curr = p._p

# F. Local Storage and SQLite
p_f_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_f_head.add_run("F. Local Storage and SQLite")
format_run(r, "F. Local Storage and SQLite", bold=True)
curr = p_f_head._p

sec3_f_body = (
    "Android provides multiple local storage mechanisms, among which the embedded SQLite relational database is the industry standard "
    "for structured data persistence. Conceptually, an application’s SQLite database is created within the app-private internal storage "
    "sandbox located at /data/data/<package_name>/databases/<database_name>.db. At this location, the database file inherits the Linux "
    "filesystem DAC permissions assigned to the app's unique UID, ensuring that other standard applications on an uncompromised device "
    "cannot directly read or write the database file through standard filesystem system calls.\n"
    "However, developers frequently conflate access control with data confidentiality. Operating system sandboxing is strictly an access "
    "control boundary—it establishes authorization checks governing process access. It does not provide encryption at rest. If the "
    "database stores sensitive records (such as authentication tokens, passwords, or personal chat messages) in plaintext, the "
    "confidentiality of that data remains entirely dependent on the perfection of the surrounding access control perimeters. Any "
    "failure in component access restrictions, backup configurations, or OS-level integrity instantly reveals the plaintext data."
)
p = insert_p_after(curr, doc, space_after=12)
r = p.add_run(sec3_f_body)
format_run(r, sec3_f_body)
curr = p._p

remove_p(p16)
remove_p(p17)
remove_p(p18)
remove_p(p19)

# -------------------------------------------------------------
# Section 4: System Architecture & Logic Diagram
# -------------------------------------------------------------
p20 = [p for p in doc.paragraphs if p.text.startswith('4. System Architecture')][0]
p21 = [p for p in doc.paragraphs if p.text.startswith('Instruction: Insert a diagram')][0]
p22 = [p for p in doc.paragraphs if p.text.startswith('Required: Label the "Attacker')][0]

curr = p20._p

# Insert image (centered, optimal width of 5.4 inches so it fits beautifully on page)
p_img = insert_p_after(curr, doc, space_before=6, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
r_img = p_img.add_run()
r_img.add_picture(DIAGRAM_PATH, width=Inches(5.4))
curr = p_img._p

# Insert caption
p_cap = insert_p_after(curr, doc, space_before=2, space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER, keep_with_next=True)
r_cap = p_cap.add_run("Figure 1. Simplified security architecture of a vulnerable client-server Android application.")
format_run(r_cap, "Figure 1. Simplified security architecture of a vulnerable client-server Android application.", italic=True, font_size=11)
curr = p_cap._p

sec4_overview = (
    "Figure 1 illustrates the simplified architectural model and threat landscape of a vulnerable client-server Android application, "
    "delineating the interaction between an untrusted third-party application, the vulnerable client, and the remote backend infrastructure. "
    "The diagram models three primary entities, their communication boundaries, and two distinct vulnerability points:"
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec4_overview)
format_run(r, sec4_overview)
curr = p._p

# Architectural Entity 1: Attacker
p_ent1 = insert_p_after(curr, doc, space_before=4, space_after=2, keep_with_next=True)
r = p_ent1.add_run("Architectural Entity 1 — Attacker (Malicious Android Application):")
format_run(r, "Architectural Entity 1 — Attacker (Malicious Android Application):", bold=True)
curr = p_ent1._p

ent1_body = (
    "The attacker represents a separate, unprivileged third-party Android application installed on the same physical device. In accordance "
    "with the Android security model, the attacker operates within its own isolated Linux UID and possesses no special system privileges. "
    "It cannot directly read the victim’s internal memory or inspect its private filesystem directory. Consequently, the attacker's primary "
    "vector of attack consists of exploiting exposed Inter-Process Communication (IPC) interfaces by crafting and dispatching weaponized "
    "Intent payloads to the victim."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(ent1_body)
format_run(r, ent1_body)
curr = p._p

# Architectural Entity 2: Victim
p_ent2 = insert_p_after(curr, doc, space_before=4, space_after=2, keep_with_next=True)
r = p_ent2.add_run("Architectural Entity 2 — Victim (Vulnerable Android Client Application):")
format_run(r, "Architectural Entity 2 — Victim (Vulnerable Android Client Application):", bold=True)
curr = p_ent2._p

ent2_body = (
    "The victim application executes within its own isolated runtime sandbox (/data/data/com.victim.app/). Its architecture incorporates two "
    "fatal security vulnerability points:"
)
p = insert_p_after(curr, doc, space_after=3)
r = p.add_run(ent2_body)
format_run(r, ent2_body)
curr = p._p

curr = insert_item_after(curr, doc, "Vulnerability Point #1 (Untrusted Intent / Exported Component Boundary): ",
    "The application exposes an entry-point component (such as an Activity, Service, or BroadcastReceiver) to external applications by configuring "
    "android:exported=\"true\" in AndroidManifest.xml without enforcing custom signature-level permissions. Furthermore, the component logic implements "
    "unsafe Intent handling: it accepts untrusted Intent extras supplied by the attacker and processes or forwards them without validating the sender, "
    "sanitizing payload flags, or allowlisting destination component targets.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Vulnerability Point #2 (Sensitive Plaintext Storage / Insecure Exposure Path): ",
    "Within its private internal directory, the application persists sensitive authentication secrets, such as session Bearer tokens and account identifiers, "
    "inside an unencrypted SQLite database (sessions.db). While the Linux sandbox isolates this file from direct read access by the attacker app, the absence "
    "of encryption at rest creates a critical failure point whenever secondary exposure paths arise—such as through an insecure exported ContentProvider, "
    "an automated application backup (adb backup), debuggable test builds, or a compromised/rooted runtime environment.",
    space_after=6)._p

# Architectural Entity 3: Server
p_ent3 = insert_p_after(curr, doc, space_before=4, space_after=2, keep_with_next=True)
r = p_ent3.add_run("Architectural Entity 3 — Victim / Server (Backend API & Authentication Server):")
format_run(r, "Architectural Entity 3 — Victim / Server (Backend API & Authentication Server):", bold=True)
curr = p_ent3._p

ent3_body = (
    "The remote backend server serves as the authoritative issuer of session tokens and state management. The Android client exchanges "
    "authentication credentials and operational data with the server across the network via HTTPS/REST APIs. In an insecure laboratory setup, "
    "this communication channel is also susceptible to Man-in-the-Middle (MITM) proxy inspection if the client's network security configuration "
    "erroneously trusts user-installed Certificate Authority (CA) certificates—a vulnerability that forms the core remediation scope of the "
    "final project demonstration using Certificate Pinning."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(ent3_body)
format_run(r, ent3_body)
curr = p._p

sec4_synthesis = (
    "Data and Control Flow Synthesis:\n"
    "As depicted by the directional control and data flows in Figure 1, the attacker application initiates the exploit by dispatching a crafted "
    "Intent across the IPC boundary to the victim's exported component. The vulnerable component executes the input blindly (Vulnerability Point #1), "
    "triggering unauthorized internal state transitions, escalating privileges to launch unexported activities, or exfiltrating private tokens "
    "persisted in the unencrypted SQLite database (Vulnerability Point #2)."
)
p = insert_p_after(curr, doc, space_after=12)
r = p.add_run(sec4_synthesis)
format_run(r, sec4_synthesis)
curr = p._p

remove_p(p21)
remove_p(p22)

# -------------------------------------------------------------
# Section 5: The Mechanics of the Vulnerability (The "Why")
# -------------------------------------------------------------
p23 = [p for p in doc.paragraphs if p.text.startswith('5. The Mechanics')][0]
p24 = [p for p in doc.paragraphs if p.text.strip() == '(Min 400 words)'][0]
p25 = [p for p in doc.paragraphs if p.text.startswith('Instruction: This is the core')][0]
p26 = [p for p in doc.paragraphs if p.text.startswith('Step-by-Step Analysis')][0]
p27 = [p for p in doc.paragraphs if p.text.startswith('Code/Logic Snippet')][0]
p28 = [p for p in doc.paragraphs if p.text.startswith('The "root cause"')][0]

curr = p24._p

sec5_intro = (
    "The security failures inherent in mobile application architectures typically stem from misplaced trust across architectural boundaries "
    "and a lack of defense-in-depth. In client-server Android applications, these weaknesses manifest prominently in two interconnected "
    "vulnerability scenarios: Intent Injection/Redirection and Unencrypted Local Storage. Below, we provide an exhaustive technical "
    "examination of their exploitation mechanics, root causes, theoretical implementations, and realistic exposure pathways."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec5_intro)
format_run(r, sec5_intro)
curr = p._p

# 5.1 Subsection
p_51_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_51_head.add_run("5.1 Intent Injection / Unsafe Intent Handling")
format_run(r, "5.1 Intent Injection / Unsafe Intent Handling", bold=True)
curr = p_51_head._p

sec5_step_intro = "Step-by-Step Exploitation Analysis:"
p = insert_p_after(curr, doc, space_after=3, keep_with_next=True)
r = p.add_run(sec5_step_intro)
format_run(r, sec5_step_intro, bold=True)
curr = p._p

curr = insert_item_after(curr, doc, "Step 1 (Component Exposure): ",
    "The developer configures an Activity, Service, or BroadcastReceiver in AndroidManifest.xml with android:exported=\"true\", "
    "or includes an <intent-filter> without explicitly declaring android:exported=\"false\". Crucially, no restrictive android:permission "
    "(such as a signature-level permission) is attached to the component declaration. This exposes the component as a publicly callable "
    "IPC endpoint accessible to any application on the device.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Step 2 (Intent Weaponization): ",
    "A malicious third-party application installed on the same device constructs an explicit or implicit Intent targeting the exported component. "
    "The attacker embeds manipulated parameters within the Intent's Bundle extras, such as altered action strings, malicious URIs, or—most "
    "critically—a nested Parcelable Intent object (an 'Intent within an Intent') designed to invoke a privileged, non-exported internal component.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Step 3 (Omission of Trust Validation): ",
    "The victim application's exported component receives the incoming Intent via onCreate(), onStartCommand(), or onReceive(). The application "
    "developer assumes that inputs received across the IPC boundary are benign and fails to implement caller validation (e.g., verifying "
    "Binder.getCallingUid() or calling package signatures), fails to sanitize URI permissions flags, and fails to validate the target destination "
    "of the encapsulated nested Intent against an allowlist.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Step 4 (Privileged Execution and Redirection): ",
    "The victim application extracts the nested Intent from the extra bundle and passes it directly to a system dispatch method, such as "
    "startActivity(nestedIntent) or startService(nestedIntent). Because this invocation is initiated from the victim's own process context, "
    "the Android OS treats the invocation with the full ambient authority and permissions of the victim application. Consequently, the "
    "operating system bypasses android:exported=\"false\" restrictions, granting the attacker indirect execution of private, sensitive "
    "activities (such as internal administration screens or data export routines) or granting read access to private ContentProviders via "
    "URI permission escalation (FLAG_GRANT_READ_URI_PERMISSION).",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Step 5 (Unauthorized Impact and Exfiltration): ",
    "The attacker accomplishes privilege escalation, triggers unintended application state changes, or exfiltrates confidential application data. "
    "For example, if the redirected private activity returns sensitive data through setResult(RESULT_OK, returnIntent), the victim's proxy component "
    "may unwittingly relay this result back to the attacker's calling activity.",
    space_after=6)._p

p = insert_p_after(curr, doc, space_after=4, keep_with_next=True)
r = p.add_run("Theoretical Vulnerable Implementation (Kotlin):")
format_run(r, "Theoretical Vulnerable Implementation (Kotlin):", bold=True)
curr = p._p

# Listing 1: Clean code lines under 60 chars so it never wraps awkwardly
vuln_code_kotlin = (
    "// INSECURE: Exported Activity forwarding untrusted nested Intents\n"
    "class GatewayActivity : AppCompatActivity() {\n"
    "    override fun onCreate(savedInstanceState: Bundle?) {\n"
    "        super.onCreate(savedInstanceState)\n"
    "        // Extract nested Intent from untrusted external caller\n"
    "        val targetIntent =\n"
    "            intent.getParcelableExtra<Intent>(\"key_forward_intent\")\n"
    "        if (targetIntent != null) {\n"
    "            // FLAW: Executes with victim's internal authority!\n"
    "            // Bypasses android:exported=\"false\" on private components\n"
    "            startActivity(targetIntent)\n"
    "        }\n"
    "        finish()\n"
    "    }\n"
    "}"
)
curr = insert_code_box_after(curr, doc, vuln_code_kotlin, "Listing 1. Vulnerable Kotlin code exhibiting Intent Redirection.")

sec5_1_explain = (
    "Technical Root Causes:\n"
    "In Listing 1, GatewayActivity acts as an open confused deputy. An external application cannot directly launch private components like "
    "InternalTokenExportActivity because they are marked with android:exported=\"false\". However, by supplying an explicit Intent targeting "
    "InternalTokenExportActivity inside the 'key_forward_intent' extra, the attacker tricks GatewayActivity into launching it on the attacker's "
    "behalf. The root causes include: (1) Unnecessarily exporting components without access permissions, (2) Blindly trusting IPC payloads, "
    "(3) Forwarding unvalidated nested Intents, and (4) Propagating dangerous URI permission flags without sanitization."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec5_1_explain)
format_run(r, sec5_1_explain)
curr = p._p

p = insert_p_after(curr, doc, space_after=4, keep_with_next=True)
r = p.add_run("Secure Alternative Implementation (Kotlin with AndroidX IntentSanitizer):")
format_run(r, "Secure Alternative Implementation (Kotlin with AndroidX IntentSanitizer):", bold=True)
curr = p._p

# Listing 2: Clean code lines under 65 chars so it never wraps awkwardly
secure_code_kotlin = (
    "// SECURE: Destination allowlisting and Intent sanitization\n"
    "class GatewayActivity : AppCompatActivity() {\n"
    "    override fun onCreate(savedInstanceState: Bundle?) {\n"
    "        super.onCreate(savedInstanceState)\n"
    "        val targetIntent =\n"
    "            intent.getParcelableExtra<Intent>(\"key_forward_intent\")\n"
    "        if (targetIntent != null) {\n"
    "            // 1. Resolve destination component via PackageManager\n"
    "            val resolved = targetIntent.resolveActivity(packageManager)\n"
    "            if (resolved != null && resolved.packageName == packageName) {\n"
    "                // 2. Enforce strict allowlist of permissible classes\n"
    "                val allowed = setOf(\n"
    "                    \"com.victim.app.SafePublicActivity\",\n"
    "                    \"com.victim.app.HelpActivity\"\n"
    "                )\n"
    "                if (allowed.contains(resolved.className)) {\n"
    "                    // 3. Strip dangerous flags via IntentSanitizer\n"
    "                    val safeIntent = IntentSanitizer.Builder()\n"
    "                        .allowAction(Intent.ACTION_VIEW)\n"
    "                        .allowPackage(packageName)\n"
    "                        .allowComponent(resolved)\n"
    "                        .build()\n"
    "                        .sanitize(targetIntent)\n"
    "                    startActivity(safeIntent)\n"
    "                } else {\n"
    "                    Log.w(\"Security\", \"Blocked unauthorized component\")\n"
    "                }\n"
    "            }\n"
    "        }\n"
    "        finish()\n"
    "    }\n"
    "}"
)
curr = insert_code_box_after(curr, doc, secure_code_kotlin, "Listing 2. Hardened Kotlin implementation enforcing destination allowlisting and IntentSanitizer.")

# 5.2 Subsection
p_52_head = insert_p_after(curr, doc, space_before=8, space_after=3, keep_with_next=True)
r = p_52_head.add_run("5.2 Unencrypted Local Storage / SQLite")
format_run(r, "5.2 Unencrypted Local Storage / SQLite", bold=True)
curr = p_52_head._p

sec5_2_schema_text = (
    "Theoretical SQLite Database Scenario:\n"
    "Consider an Android client application communicating with a backend API that maintains local persistent session state "
    "inside an internal SQLite database (/data/data/com.victim.app/databases/app_session.db). The relational database schema is structured as follows:"
)
p = insert_p_after(curr, doc, space_after=4)
r = p.add_run(sec5_2_schema_text)
format_run(r, sec5_2_schema_text)
curr = p._p

# Listing 3: Clean SQL lines under 60 chars
sql_schema = (
    "CREATE TABLE user_sessions (\n"
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "    user_id TEXT NOT NULL,\n"
    "    username TEXT NOT NULL,\n"
    "    auth_token TEXT NOT NULL,  -- Plaintext Bearer / JWT token\n"
    "    session_expiry INTEGER NOT NULL\n"
    ");"
)
curr = insert_code_box_after(curr, doc, sql_schema, "Listing 3. Theoretical SQLite schema persisting plaintext session tokens.")

sec5_2_nuance = (
    "Technical Analysis of Plaintext Storage Weakness:\n"
    "The fundamental security flaw in Listing 3 is the persistence of high-value authentication credentials (auth_token) directly in "
    "plaintext without cryptographic protection at rest. The auth_token (typically a JWT or Bearer token issued by the backend server) "
    "acts as an authoritative bearer credential. Anyone who obtains this token can impersonate the victim against the backend server's REST APIs, "
    "bypassing passwords and multi-factor authentication entirely.\n\n"
    "Crucial Academic Nuance Regarding the Android Sandbox:\n"
    "It is technically incorrect to claim that any arbitrary, unprivileged malicious Android application can simply read another application's "
    "private SQLite database directly. Under normal operating conditions on an intact device, the Android Linux kernel sandbox rigorously "
    "enforces Discretionary Access Control (DAC): the database file at /data/data/com.victim.app/databases/app_session.db is owned by "
    "the victim's unique UID (e.g., u0_a142:u0_a142) with strict POSIX permissions 0600. An unprivileged malicious application running under "
    "a distinct UID (e.g., u0_a189) attempting to open this file directly via Linux file I/O will immediately encounter an EACCES "
    "(Permission denied) kernel error.\n\n"
    "Realistic Exposure Pathways:\n"
    "While direct filesystem reads are restricted by the sandbox, storing sensitive data in plaintext remains a severe architectural vulnerability "
    "because the sandbox is an access control boundary, not a cryptographic guarantee. If access control is undermined through configuration errors, "
    "auxiliary vulnerabilities, or environment compromise, the plaintext data is immediately exposed. Realistic exposure pathways include:\n"
    "1. Insecure Exported ContentProviders: Developers frequently wrap SQLite databases in a ContentProvider to facilitate inter-component "
    "data sharing. If the provider specifies android:exported=\"true\" without defining explicit android:readPermission attributes or fails to "
    "sanitize incoming URI selection queries, any installed malicious application can issue queries (content://com.victim.app.provider/user_sessions) "
    "or execute SQL injection attacks to dump the entire plaintext database.\n"
    "2. Unprotected IPC Leaks: An internal service or receiver might query the SQLite database and unwittingly broadcast the retrieved tokens in "
    "an unencrypted implicit Intent extra, exposing them to any background listener registered for that action.\n"
    "3. Application Backups (adb backup): By default, Android applications have android:allowBackup=\"true\" unless explicitly disabled in "
    "AndroidManifest.xml. An attacker with temporary physical access or USB debugging access can execute 'adb backup -f backup.ab -noapk com.victim.app', "
    "unpack the archive with standard tools, and extract the unencrypted SQLite database in seconds.\n"
    "4. Storage Misplacement: Developers frequently store database exports, cache dumps, or database backup files in shared external storage "
    "(/sdcard/ or getExternalFilesDir()), where any application holding legacy READ_EXTERNAL_STORAGE permissions can inspect them.\n"
    "5. Debuggable Build Flags: Releasing an application with android:debuggable=\"true\" enables the Android debug bridge tool 'run-as com.victim.app', "
    "allowing any local shell user to assume the application’s UID and copy the SQLite file directly from internal storage.\n"
    "6. Rooted and Compromised Devices: Millions of users deliberately root their devices, or devices become compromised through local privilege "
    "escalation exploits. On a rooted device, the root user (UID 0) bypasses all POSIX DAC permissions and SELinux policies, allowing any root-privileged "
    "application to read all private databases across the entire filesystem.\n"
    "7. Secondary Application Vulnerabilities: If the application contains a path traversal vulnerability or an arbitrary file-read flaw in an exported "
    "component, an attacker can coerce the app into reading and exfiltrating its own private SQLite database file.\n"
    "8. Physical Device Theft / Forensic Seizure: If an unencrypted device is lost or stolen, forensic imaging tools can extract raw flash memory, "
    "recovering plaintext SQLite database records directly.\n\n"
    "Access Control vs. Encryption at Rest:\n"
    "This analysis demonstrates the foundational difference between Access Control and Encryption at Rest:\n"
    "- Access Control (Android Sandbox) governs WHO is permitted to access a resource based on process identity and permissions. It relies on the absolute integrity of the underlying operating system kernel, configuration flags, and inter-process boundaries.\n"
    "- Encryption at Rest governs WHAT can be deciphered if the underlying storage media or access boundary is bypassed. By utilizing strong cryptography (e.g., AES-256 via SQLCipher), the data remains completely confidential even if an attacker extracts the raw database file."
)

for para in sec5_2_nuance.split('\n\n'):
    p = insert_p_after(curr, doc, space_after=6)
    r = p.add_run(para)
    format_run(r, para)
    curr = p._p

# Root Cause Classification
p_rc_head = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_rc_head.add_run("Root Cause Classification:")
format_run(r, "Root Cause Classification:", bold=True)
curr = p_rc_head._p

sec5_rc_body = (
    "To provide academic rigor, we explicitly classify the root causes of both vulnerability classes:\n"
    "- Intent Injection / Redirection: Classified as a combination of Architectural Design/Configuration Flaws (overly permissive component exposure, "
    "omitting signature permissions) and Implementation Flaws (lack of IPC input validation, blind forwarding of nested intents).\n"
    "- Insecure Local Storage: Classified as an Insecure Security Design Flaw (persisting high-value authentication secrets without cryptographic "
    "defense-in-depth) and Implementation Failures (omitting encryption at rest, failing to disable backup flags, and exposing database queries through insecure ContentProviders).\n"
    "- Developer Error Context: While developer cognitive errors (misunderstanding manifest defaults, neglecting input validation, using convenience shortcuts) "
    "contribute directly to these vulnerabilities, reducing them solely to 'human error' is insufficient. The fundamental failure lies in architectural "
    "design: treating the operating system sandbox as the sole security boundary and violating the core principles of least privilege and defense-in-depth."
)
p = insert_p_after(curr, doc, space_after=12)
r = p.add_run(sec5_rc_body)
format_run(r, sec5_rc_body)
curr = p._p

remove_p(p25)
remove_p(p26)
remove_p(p27)
remove_p(p28)

# -------------------------------------------------------------
# Section 6: Impact Analysis (The CIA Triad)
# -------------------------------------------------------------
p29 = [p for p in doc.paragraphs if p.text.startswith('6. Impact Analysis')][0]
p30 = [p for p in doc.paragraphs if p.text.startswith('Instruction: Analyze how this')][0]
p31 = [p for p in doc.paragraphs if p.text.startswith('Confidentiality:')][0]
p32 = [p for p in doc.paragraphs if p.text.startswith('Integrity:')][0]
p33 = [p for p in doc.paragraphs if p.text.startswith('Availability:')][0]

curr = p29._p

sec6_intro = (
    "Security vulnerabilities must be evaluated through the lens of the classic Confidentiality, Integrity, and Availability (CIA) triad. "
    "In client-server Android applications, the vulnerabilities discussed above present profound, multifaceted impacts across all three dimensions:"
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec6_intro)
format_run(r, sec6_intro)
curr = p._p

curr = insert_item_after(curr, doc, "Confidentiality: ",
    "Confidentiality suffers the most immediate and severe impact in mobile application security breaches. When an unencrypted SQLite database "
    "is exposed via an insecure ContentProvider, an unauthorized application backup (adb backup), or an IPC leak, sensitive assets are directly compromised. "
    "The theft of persistent authentication tokens (e.g., OAuth tokens, JWTs, or session cookies) allows the attacker to achieve complete account takeover "
    "on the backend server. The attacker can impersonate the legitimate user across network APIs without ever learning their plaintext password or "
    "triggering multi-factor authentication challenges. Furthermore, unencrypted storage routinely exposes Personally Identifiable Information (PII), "
    "confidential chat histories, financial records, and cryptographic keys. Similarly, Intent Redirection allows an attacker to coerce an internal "
    "component into exporting private files or returning sensitive internal state to an untrusted caller.",
    space_after=4)._p

curr = insert_item_after(curr, doc, "Integrity: ",
    "Integrity is compromised when unauthorized external entities alter application state, tamper with stored records, or trigger unapproved system actions. "
    "In Intent-related vulnerabilities, an attacker leverages Intent Injection to invoke internal, privileged components that modify user account parameters, "
    "alter privacy settings, or initiate unauthorized transactions (such as transferring funds or sending unauthorized chat messages from the victim’s account). "
    "When SQLite databases or ContentProviders lack appropriate write access restrictions (android:writePermission), an attacker can execute arbitrary "
    "SQL UPDATE or INSERT statements, poisoning cached server responses, injecting fraudulent transaction records, or tampering with user roles stored locally. "
    "These manipulations corrupt the trustworthiness of the client’s state and can subsequently corrupt server-side records during synchronization.",
    space_after=4)._p

curr = insert_item_after(curr, doc, "Availability: ",
    "While mobile vulnerabilities frequently focus on data theft, Availability impacts present a substantial operational risk. An attacker can craft "
    "malformed, oversized, or unparcelable Intent payloads (e.g., containing non-serializable objects or invalid extra types) that trigger unhandled "
    "runtime exceptions (BadParcelableException, ClassCastException, or NullPointerException) within exported Activities, Services, or BroadcastReceivers. "
    "When dispatched repeatedly, these malicious Intents force the victim application into a continuous crash loop (Denial of Service - DoS), exhausting "
    "device memory and CPU resources, draining the battery, and rendering the application entirely unusable. Furthermore, malformed SQL queries or concurrent "
    "lock contention against unencrypted SQLite databases can corrupt the underlying database file (SQLITE_CORRUPT), permanently disabling local data "
    "access until the user manually wipes all application data. Although Availability impacts may carry lower long-term financial consequences than "
    "credential exfiltration, they severely degrade service reliability and user trust.",
    space_after=12)._p

remove_p(p30)
remove_p(p31)
remove_p(p32)
remove_p(p33)

# -------------------------------------------------------------
# Section 7: Proposed Methods /or Prevention & Mitigation
# -------------------------------------------------------------
p34 = [p for p in doc.paragraphs if p.text.startswith('7. Proposed')][0]
p35 = [p for p in doc.paragraphs if p.text.strip() == '(Min 200 words)'][0]
p36 = [p for p in doc.paragraphs if p.text.startswith('Instruction: How do industry')][0]
p37 = [p for p in doc.paragraphs if p.text.startswith('Example: "To prevent SQL')][0]

curr = p35._p

sec7_intro = (
    "Remediating Intent-related weaknesses and local storage vulnerabilities requires a defense-in-depth engineering strategy combining manifest hardening, "
    "robust IPC validation, cryptographic data protection, and automated testing across the software development lifecycle."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec7_intro)
format_run(r, sec7_intro)
curr = p._p

# A. Manifest
p_7a = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_7a.add_run("A. Android Permissions and Manifest Hardening")
format_run(r, "A. Android Permissions and Manifest Hardening", bold=True)
curr = p_7a._p

curr = insert_item_after(curr, doc, "Enforce Explicit Component Isolation: ",
    "Set android:exported=\"false\" explicitly on all Activities, Services, and Receivers that are intended solely for internal intra-app use. "
    "In modern Android (API 31+), never rely on implicit export defaults.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Leverage Signature-Level Permissions: ",
    "When components must be accessed across multiple applications developed by the same organization, define custom permissions with "
    "android:protectionLevel=\"signature\". The Android OS will automatically restrict IPC access to applications signed with the identical "
    "cryptographic signing key, shutting out all third-party malicious apps.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Restrict Intent Filters: ",
    "Avoid declaring unnecessary <intent-filter> tags on internal components, as the presence of an intent filter can unintentionally increase exposure.",
    space_after=6)._p

# B. Intent Security
p_7b = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_7b.add_run("B. Secure Intent Handling and IPC Architecture")
format_run(r, "B. Secure Intent Handling and IPC Architecture", bold=True)
curr = p_7b._p

curr = insert_item_after(curr, doc, "Prefer Explicit Intents: ",
    "Always use explicit Intents (specifying target package and class name) for all internal communication to guarantee that messages are never intercepted or handled by malicious external applications.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Input Validation and Allowlisting: ",
    "Treat all incoming Intent extras as untrusted network inputs. Never pass raw nested Intent extras directly to startActivity() or startService(). "
    "Always resolve the target component using PackageManager and strictly validate the destination against a hardcoded allowlist of permitted classes within the application’s own package.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Utilize Modern Intent Sanitizers: ",
    "Implement the official AndroidX IntentSanitizer library to strip sensitive flags (such as FLAG_GRANT_READ_URI_PERMISSION and FLAG_GRANT_WRITE_URI_PERMISSION) and enforce strict URI and component constraints before processing.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Enforce PendingIntent Immutability: ",
    "Always construct PendingIntent instances with FLAG_IMMUTABLE (mandatory in API 31+) unless mutability is strictly required, preventing malicious applications from hijacking or altering the pending operation.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Verify Caller Identity: ",
    "For exported Services or ContentProviders that must accept external calls, verify the caller's identity at runtime using Binder.getCallingUid() and validate the caller's package certificate via PackageManager.",
    space_after=6)._p

# C. Local Storage Hardening
p_7c = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_7c.add_run("C. Local Storage Hardening and Cryptography")
format_run(r, "C. Local Storage Hardening and Cryptography", bold=True)
curr = p_7c._p

curr = insert_item_after(curr, doc, "Principle of Data Minimization: ",
    "Avoid storing high-value secrets locally whenever feasible. Never persist plaintext passwords, and avoid caching long-lived authentication tokens in local storage if short-lived tokens in volatile memory suffice.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Disable Insecure Application Backups: ",
    "Explicitly declare android:allowBackup=\"false\" in AndroidManifest.xml to prevent attackers from extracting private SQLite databases and shared preferences via adb backup.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Enforce Secure ContentProvider Configuration: ",
    "Protect ContentProviders by setting android:exported=\"false\" or enforcing granular android:readPermission and android:writePermission controls.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Implement Encryption at Rest with SQLCipher: ",
    "For applications that must persist sensitive data, replace standard SQLite with an encrypted database engine such as SQLCipher (or Room with SQLCipher). "
    "SQLCipher provides transparent, full-database 256-bit AES encryption, ensuring that database files, journals, and temporary tables remain completely unreadable without the cryptographic key.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Hardware-Backed Key Management via Android Keystore: ",
    "Never hardcode encryption keys in source code, strings resources, or compiled bytecode. Cryptographic keys must be generated and stored within the "
    "hardware-backed Android Keystore system (leveraging Trusted Execution Environments - TEE, or StrongBox Keymaster), ensuring that key material can never be extracted from device memory.",
    space_after=6)._p

# D. SDLC Verification
p_7d = insert_p_after(curr, doc, space_before=6, space_after=3, keep_with_next=True)
r = p_7d.add_run("D. Secure Development Lifecycle (SDLC) Verification")
format_run(r, "D. Secure Development Lifecycle (SDLC) Verification", bold=True)
curr = p_7d._p

curr = insert_item_after(curr, doc, "Automated Static and Dynamic Analysis: ",
    "Integrate mobile application security testing tools into CI/CD pipelines, such as Mobile Security Framework (MobSF), Android Lint, and Semgrep, to automatically detect exported components and unencrypted storage flaws.",
    space_after=3)._p

curr = insert_item_after(curr, doc, "Standard Compliance: ",
    "Benchmark mobile client design and implementation against industry standards, specifically the OWASP Mobile Application Security Verification Standard (MASVS) categories MASVS-STORAGE and MASVS-PLATFORM, as well as the OWASP Mobile Application Security Testing Guide (MASTG).",
    space_after=12)._p

remove_p(p36)
remove_p(p37)

# -------------------------------------------------------------
# Section 8: Plan for Final Demonstration
# -------------------------------------------------------------
p38 = [p for p in doc.paragraphs if p.text.startswith('8. Plan for Final')][0]
p39 = [p for p in doc.paragraphs if p.text.startswith('Instruction: Briefly outline')][0]
p40 = [p for p in doc.paragraphs if p.text.startswith('Tools required:')][0]
p41 = [p for p in doc.paragraphs if p.text.startswith('Scenario:')][0]
p42 = [p for p in doc.paragraphs if p.text.startswith('Success Criteria:')][0]

curr = p38._p

sec8_intro = (
    "This section bridges the theoretical security foundations established in this midterm report with the practical, hands-on demonstration "
    "planned for the end-of-semester final project. The final project transitions from client-side component analysis to end-to-end client-server "
    "network communication security, focusing on traffic interception and transport-layer defense. All demonstration activities will be strictly "
    "conducted in an authorized, controlled educational laboratory environment."
)
p = insert_p_after(curr, doc, space_after=6)
r = p.add_run(sec8_intro)
format_run(r, sec8_intro)
curr = p._p

sec8_tools_text = (
    "Android Studio (Ladybug / Hedgehog or compatible) with modern Android SDK and Kotlin toolchain for mobile client development; "
    "Android Virtual Device (AVD) / Test Device: An Android Emulator running API 30+ (Google APIs system image) or physical test device configured with proxy routing; "
    "Backend API Server: A lightweight RESTful/WebSocket server implemented in Python (Flask/FastAPI) or Node.js (Express), providing user authentication and secure messaging endpoints over HTTPS; "
    "Burp Suite Community / Professional: Industry-standard security proxy used to intercept, inspect, and manipulate HTTP/HTTPS traffic between the client and backend server; "
    "PortSwigger Burp CA Certificate: Custom proxy Certificate Authority (CA) certificate installed into the test environment for TLS interception; "
    "Diagnostic Utilities: Android Debug Bridge (adb) and Logcat for inspecting real-time runtime events, TLS connection states, and cryptographic handshake exceptions."
)
curr = insert_item_after(curr, doc, "Tools Required: ", sec8_tools_text, space_after=6)._p

sec8_scenario_text = (
    "The demonstration will be executed in an authorized laboratory environment across four phases: "
    "(1) Baseline Application Deployment: The team will construct a functional Android client-server chat application. The Android client authenticates against the backend server, obtains an authentication token, and sends encrypted chat messages over HTTPS; "
    "(2) Controlled Interception / Man-in-the-Middle Demonstration: To demonstrate transport-layer vulnerability, the team will configure the Android client with an intentionally vulnerable Network Security Configuration (res/xml/network_security_config.xml) that trusts user-installed certificates (<trust-anchors><certificates src=\"user\" /></trust-anchors>). The PortSwigger Burp CA certificate will be installed in the Android user certificate store, and the emulator’s network settings will route all traffic through the Burp Suite proxy. The team will demonstrate complete plaintext interception of sensitive chat messages and authentication tokens in Burp's Proxy HTTP history, proving how a rogue or user-trusted CA undermines TLS confidentiality; "
    "(3) Remediation via SSL / Certificate Pinning: The team will harden the Android client by implementing Certificate Pinning (Public Key Pinning). This will be achieved either by embedding the server's Subject Public Key Information (SPKI) SHA-256 pin directly into the native Android network_security_config.xml (<pin-set>) or programmatically via OkHttp's CertificatePinner; "
    "(4) Post-Remediation Verification: With the Burp Suite proxy still active, the team will re-attempt client communication with the backend. The team will show that the Android client detects that the proxy's certificate chain does not match the pinned public key hash, immediately aborting the TLS handshake. Logcat output will confirm an explicit SSLPeerUnverifiedException / Certificate pinning failure, and Burp Suite will show zero decrypted plaintext traffic; "
    "(5) Theory Integration / Optional Component Security: If presentation time permits, the team will briefly demonstrate a basic Android client-side Intent validation check, reinforcing the connection between the midterm theory and practical client implementation."
)
curr = insert_item_after(curr, doc, "Demonstration Scenario: ", sec8_scenario_text, space_after=6)._p

sec8_criteria_text = (
    "The final demonstration will be considered successful upon achieving three measurable milestones: "
    "(1) Proof of Interception: Clear visual verification in Burp Suite capturing plaintext HTTP requests/responses containing user credentials and messages in the vulnerable baseline configuration; "
    "(2) Proof of Defense: Conclusive verification that the hardened application refuses connection establishment when proxied, generating an explicit certificate pinning handshake error in Logcat and preventing traffic decryption; "
    "(3) Technical Rigor: Clear verbal and architectural articulation of why standard X.509 CA trust hierarchies are vulnerable to MITM attacks and how certificate pinning successfully enforces cryptographic identity assurance."
)
curr = insert_item_after(curr, doc, "Success Criteria: ", sec8_criteria_text, space_after=12)._p

remove_p(p39)
remove_p(p40)
remove_p(p41)
remove_p(p42)

# -------------------------------------------------------------
# Section 9: References (IEEE with hanging indent)
# -------------------------------------------------------------
p43 = [p for p in doc.paragraphs if p.text.startswith('9. References')][0]
p44 = [p for p in doc.paragraphs if p.text.startswith('Instruction: List at least')][0]
p45 = [p for p in doc.paragraphs if p.text.startswith('[Format: IEEE')][0]
p46 = [p for p in doc.paragraphs if p.text.startswith('[e.g., NIST')][0]

curr = p43._p

references = [
    "[1] Google Android Developers, \"Permissions on Android,\" Android Developers Documentation, 2024. [Online]. Available: https://developer.android.com/guide/topics/permissions/overview",
    "[2] Google Android Developers, \"Intents and Intent Filters,\" Android Developers Documentation, 2024. [Online]. Available: https://developer.android.com/guide/components/intents-filters",
    "[3] Google Android Developers, \"Remediating Intent Redirection Vulnerability,\" Android Privacy and Security Documentation, 2023. [Online]. Available: https://developer.android.com/privacy-and-security/risks/intent-redirection",
    "[4] Google Android Developers, \"Data and File Storage Overview,\" Android Developers Documentation, 2024. [Online]. Available: https://developer.android.com/training/data-storage",
    "[5] OWASP Foundation, \"OWASP Mobile Application Security Verification Standard (MASVS) v2.0.0,\" OWASP Foundation, 2023. [Online]. Available: https://mas.owasp.org/",
    "[6] OWASP Foundation, \"Testing Local Data Storage (MASTG-STORAGE-0037),\" Mobile Application Security Testing Guide (MASTG), 2024. [Online]. Available: https://mas.owasp.org/MASTG/knowledge/android/MASVS-STORAGE/MASTG-KNOW-0037/",
    "[7] National Institute of Standards and Technology (NIST), \"Vetting the Security of Mobile Applications,\" NIST Special Publication 800-163 Rev. 1, Apr. 2019. [Online]. Available: https://doi.org/10.6028/NIST.SP.800-163r1"
]

for ref in references:
    p = insert_p_after(curr, doc, space_after=4)
    p.paragraph_format.left_indent = Pt(20)
    p.paragraph_format.first_line_indent = Pt(-20)
    r = p.add_run(ref)
    format_run(r, ref)
    curr = p._p

remove_p(p44)
remove_p(p45)
remove_p(p46)

# Remove any empty trailing paragraph if exists
for p in list(doc.paragraphs):
    if p.text.strip() == "" and len(p.runs) == 0 and p != doc.paragraphs[0]:
        try:
            remove_p(p)
        except Exception:
            pass

# Save document
doc.save(OUTPUT_PATH)
print(f"Successfully rebuilt final completed report at {OUTPUT_PATH}")
