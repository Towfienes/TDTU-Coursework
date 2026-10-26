import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(9.2, 11.2), dpi=300, facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 120)
ax.axis('off')

FONT = 'DejaVu Sans'
MONO = 'DejaVu Sans Mono'

# Colors
C_ATTACK_BG = '#FEF2F2'
C_ATTACK_EDGE = '#DC2626'
C_ATTACK_TXT = '#991B1B'
C_CLIENT_CONTAINER_BG = '#F8FAFC'
C_CLIENT_CONTAINER_EDGE = '#0284C7'
C_COMP_BG = '#F1F5F9'
C_COMP_EDGE = '#64748B'
C_VULN_BG = '#FFFBEB'
C_VULN_EDGE = '#D97706'
C_VULN_TXT = '#B45309'
C_SERVER_BG = '#F8FAFC'
C_SERVER_EDGE = '#334155'
C_SERVER_TXT = '#1E293B'
C_TEXT_DARK = '#0F172A'
C_TEXT_MUTED = '#475569'
C_ARROW = '#1E293B'

# 1. Attacker
p_att = patches.FancyBboxPatch((18, 104), 64, 13, boxstyle="round,pad=1.0,rounding_size=2.5", linewidth=1.8, edgecolor=C_ATTACK_EDGE, facecolor=C_ATTACK_BG)
ax.add_patch(p_att)
p_att_badge = patches.FancyBboxPatch((36, 113.2), 28, 3.2, boxstyle="round,pad=0.4,rounding_size=1.2", linewidth=0, facecolor=C_ATTACK_EDGE)
ax.add_patch(p_att_badge)
t_att_b = ax.text(50, 114.8, "ATTACKER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='white', fontfamily=FONT)
t_att_1 = ax.text(50, 109.8, "Malicious Android Application", ha='center', va='center', fontsize=11, fontweight='bold', color=C_TEXT_DARK, fontfamily=FONT)
t_att_2 = ax.text(50, 106.2, "Unprivileged Linux UID (Sandboxed from other applications)", ha='center', va='center', fontsize=8.5, fontstyle='italic', color=C_TEXT_MUTED, fontfamily=FONT)

# Arrow from Attacker to Client
ax.annotate('', xy=(50, 93.5), xytext=(50, 104), arrowprops=dict(arrowstyle="-|>", color=C_ATTACK_EDGE, lw=2.2, mutation_scale=16))
p_arrow_callout = patches.FancyBboxPatch((53, 96.0), 43, 6.2, boxstyle="round,pad=0.5,rounding_size=1.5", linewidth=1.0, edgecolor=C_ATTACK_EDGE, facecolor='#FFFFFF')
ax.add_patch(p_arrow_callout)
t_arr_1 = ax.text(74.5, 100.0, "Crafted Intent Payload (Inter-App IPC)", ha='center', va='center', fontsize=8.0, fontweight='bold', color=C_ATTACK_TXT, fontfamily=FONT)
t_arr_2 = ax.text(74.5, 97.5, "Manipulated Extras • Nested Intent • Grant URI Flags", ha='center', va='center', fontsize=7.0, color=C_TEXT_DARK, fontfamily=FONT)

# 2. Client Container
p_client_box = patches.FancyBboxPatch((6, 29), 88, 64.5, boxstyle="round,pad=1.5,rounding_size=3.0", linewidth=2.0, edgecolor=C_CLIENT_CONTAINER_EDGE, facecolor=C_CLIENT_CONTAINER_BG, linestyle='--')
ax.add_patch(p_client_box)

# Centered Client Badge with ample width
p_client_badge = patches.FancyBboxPatch((13, 89.2), 74, 3.8, boxstyle="round,pad=0.5,rounding_size=1.2", linewidth=0, facecolor='#0284C7')
ax.add_patch(p_client_badge)
t_cl_b = ax.text(50, 91.1, "VICTIM: Vulnerable Android Client Application (Private UID Sandbox)", ha='center', va='center', fontsize=8.8, fontweight='bold', color='white', fontfamily=FONT)

# 2.1 Entry Component
p_entry = patches.FancyBboxPatch((12, 78.5), 76, 8.8, boxstyle="round,pad=0.8,rounding_size=2.0", linewidth=1.4, edgecolor=C_COMP_EDGE, facecolor=C_COMP_BG)
ax.add_patch(p_entry)
t_en_1 = ax.text(50, 84.0, "Exported Entry Component (Activity / Service / BroadcastReceiver)", ha='center', va='center', fontsize=9.2, fontweight='bold', color=C_TEXT_DARK, fontfamily=FONT)
t_en_2 = ax.text(50, 80.8, 'android:exported="true"   |   Overly Permissive <intent-filter>', ha='center', va='center', fontsize=8.0, fontfamily=MONO, color='#334155')

# Arrow to Vuln 1
ax.annotate('', xy=(50, 71.5), xytext=(50, 78.5), arrowprops=dict(arrowstyle="-|>", color=C_ARROW, lw=1.8, mutation_scale=13))

# 2.2 Vuln Point 1
p_vuln1 = patches.FancyBboxPatch((10, 56.5), 80, 15.0, boxstyle="round,pad=0.9,rounding_size=2.2", linewidth=1.8, edgecolor=C_VULN_EDGE, facecolor=C_VULN_BG)
ax.add_patch(p_vuln1)
p_v1_badge = patches.FancyBboxPatch((16, 68.2), 68, 2.8, boxstyle="round,pad=0.4,rounding_size=1.0", linewidth=0, facecolor='#D97706')
ax.add_patch(p_v1_badge)
t_v1_b = ax.text(50, 69.6, "VULNERABILITY POINT #1: Untrusted Intent / Insecure IPC Boundary", ha='center', va='center', fontsize=8.2, fontweight='bold', color='white', fontfamily=FONT)
t_v1_1 = ax.text(50, 65.5, "Unsafe Intent Handling & Redirection", ha='center', va='center', fontsize=9.2, fontweight='bold', color='#78350F', fontfamily=FONT)
t_v1_2 = ax.text(50, 62.5, "• Trusts attacker-controlled extras without caller verification (Binder.getCallingUid)", ha='center', va='center', fontsize=7.8, color=C_TEXT_DARK, fontfamily=FONT)
t_v1_3 = ax.text(50, 59.5, "• Blindly invokes startActivity(nestedIntent), bypassing android:exported=\"false\"", ha='center', va='center', fontsize=7.8, color=C_TEXT_DARK, fontfamily=FONT)

# Arrow to Vuln 2
ax.annotate('', xy=(50, 49.5), xytext=(50, 56.5), arrowprops=dict(arrowstyle="-|>", color=C_ARROW, lw=1.8, mutation_scale=13))
t_arr_mid = ax.text(51.5, 53.0, "Unauthorized internal component execution", ha='left', va='center', fontsize=7.2, fontstyle='italic', color='#64748B', fontfamily=FONT)

# 2.3 Vuln Point 2
p_vuln2 = patches.FancyBboxPatch((10, 31.5), 80, 18.0, boxstyle="round,pad=0.9,rounding_size=2.2", linewidth=1.8, edgecolor=C_VULN_EDGE, facecolor=C_VULN_BG)
ax.add_patch(p_vuln2)
t_v2_0 = ax.text(50, 46.5, "Private Internal Components (Admin Screens, Data Exporters)", ha='center', va='center', fontsize=8.8, fontweight='bold', color=C_TEXT_DARK, fontfamily=FONT)
p_v2_badge = patches.FancyBboxPatch((16, 42.0), 68, 2.8, boxstyle="round,pad=0.4,rounding_size=1.0", linewidth=0, facecolor='#D97706')
ax.add_patch(p_v2_badge)
t_v2_b = ax.text(50, 43.4, "VULNERABILITY POINT #2: Sensitive Plaintext Storage at Rest", ha='center', va='center', fontsize=8.2, fontweight='bold', color='white', fontfamily=FONT)
t_v2_1 = ax.text(50, 39.5, "Unencrypted SQLite Database (/data/data/<pkg>/databases/)", ha='center', va='center', fontsize=9.2, fontweight='bold', color='#78350F', fontfamily=FONT)
t_v2_2 = ax.text(50, 36.8, "• Schema: user_sessions (user_id TEXT, username TEXT, auth_token TEXT)", ha='center', va='center', fontsize=7.6, fontfamily=MONO, color='#475569')
t_v2_3 = ax.text(50, 34.0, "• Plaintext tokens exposed via exported ContentProvider, adb backup, or root", ha='center', va='center', fontsize=7.8, color=C_TEXT_DARK, fontfamily=FONT)

# Arrow from Client to Server
ax.annotate('', xy=(50, 16.5), xytext=(50, 29.0), arrowprops=dict(arrowstyle="<|-|>", color=C_ARROW, lw=2.2, mutation_scale=16))
p_net_callout = patches.FancyBboxPatch((53, 19.5), 43, 6.8, boxstyle="round,pad=0.5,rounding_size=1.5", linewidth=1.0, edgecolor='#64748B', facecolor='#FFFFFF')
ax.add_patch(p_net_callout)
t_net_1 = ax.text(74.5, 23.8, "HTTPS / REST API Traffic (Network Channel)", ha='center', va='center', fontsize=7.8, fontweight='bold', color=C_TEXT_DARK, fontfamily=FONT)
t_net_2 = ax.text(74.5, 21.0, "Vulnerable to MITM Proxy Interception (Burp Suite)\nPrior to Certificate Pinning Implementation", ha='center', va='center', fontsize=6.8, color='#B91C1C', fontfamily=FONT)

# 3. Server
p_server = patches.FancyBboxPatch((18, 3.5), 64, 13.0, boxstyle="round,pad=1.0,rounding_size=2.5", linewidth=1.8, edgecolor=C_SERVER_EDGE, facecolor=C_SERVER_BG)
ax.add_patch(p_server)
p_srv_badge = patches.FancyBboxPatch((35, 13.5), 30, 3.0, boxstyle="round,pad=0.4,rounding_size=1.2", linewidth=0, facecolor=C_SERVER_EDGE)
ax.add_patch(p_srv_badge)
t_srv_b = ax.text(50, 15.0, "VICTIM / SERVER", ha='center', va='center', fontsize=9.5, fontweight='bold', color='white', fontfamily=FONT)
t_srv_1 = ax.text(50, 10.0, "Backend API & Authentication Server", ha='center', va='center', fontsize=11, fontweight='bold', color=C_TEXT_DARK, fontfamily=FONT)
t_srv_2 = ax.text(50, 6.5, "Authenticates users, validates session tokens, and serves confidential state", ha='center', va='center', fontsize=8.2, fontstyle='italic', color=C_TEXT_MUTED, fontfamily=FONT)

fig.canvas.draw()
renderer = fig.canvas.get_renderer()

checks = [
    ("Attacker Badge", t_att_b, p_att_badge),
    ("Attacker Title", t_att_1, p_att),
    ("Attacker Subtitle", t_att_2, p_att),
    ("Arrow Callout 1", t_arr_1, p_arrow_callout),
    ("Arrow Callout 2", t_arr_2, p_arrow_callout),
    ("Client Badge", t_cl_b, p_client_badge),
    ("Entry Title", t_en_1, p_entry),
    ("Entry Filter", t_en_2, p_entry),
    ("Vuln 1 Badge", t_v1_b, p_v1_badge),
    ("Vuln 1 Title", t_v1_1, p_vuln1),
    ("Vuln 1 Detail 1", t_v1_2, p_vuln1),
    ("Vuln 1 Detail 2", t_v1_3, p_vuln1),
    ("Vuln 2 Subheader", t_v2_0, p_vuln2),
    ("Vuln 2 Badge", t_v2_b, p_v2_badge),
    ("Vuln 2 Title", t_v2_1, p_vuln2),
    ("Vuln 2 Schema", t_v2_2, p_vuln2),
    ("Vuln 2 Detail", t_v2_3, p_vuln2),
    ("Net Callout 1", t_net_1, p_net_callout),
    ("Net Callout 2", t_net_2, p_net_callout),
    ("Server Badge", t_srv_b, p_srv_badge),
    ("Server Title", t_srv_1, p_server),
    ("Server Subtitle", t_srv_2, p_server),
]

all_passed = True
for name, txt, box in checks:
    t_bb = txt.get_window_extent(renderer)
    b_bb = box.get_window_extent(renderer)
    margin_left = t_bb.x0 - b_bb.x0
    margin_right = b_bb.x1 - t_bb.x1
    margin_top = b_bb.y1 - t_bb.y1
    margin_bottom = t_bb.y0 - b_bb.y0
    overflow = margin_left < 0 or margin_right < 0 or margin_top < 0 or margin_bottom < 0
    status = "OVERFLOW!" if overflow else "OK"
    if overflow:
        all_passed = False
    print(f"{name:<20}: {status} (L={margin_left:.1f}px, R={margin_right:.1f}px, T={margin_top:.1f}px, B={margin_bottom:.1f}px)")

print(f"\nOverall boundary check: {'ALL PASSED!' if all_passed else 'FAILED!'}")

if all_passed:
    plt.tight_layout()
    plt.savefig('architecture_diagram.png', dpi=300, facecolor='white', bbox_inches='tight')
    print("architecture_diagram.png successfully updated!")
