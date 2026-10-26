# MASTERPROMPT — SaigonBite Final Project (one-shot)

> Prompt duy nhất điều khiển toàn bộ dự án. Copy nguyên khối dưới đây vào bất kỳ agent nào
> (DSH, Claude Code, Codex, Antigravity) đang mở tại `SaigonBite/` để chạy lại từ đầu hoặc tiếp tục.

---

## ROLE

Ghi nhớ chỉ trong **SE/End term**: đọc `../AGENTS.md`. Người dùng chốt định hướng
xây app đạt đủ **Tier 4**, trần **10.0/10**: nền Tier 3 + sandbox API thật +
dashboard Admin tương tác + kiểm thử tự động có kết quả thực thi. Không chỉ ghi
Tier 4 trong report, không tính mock/dashboard tĩnh/test dự kiến là bằng chứng.
Không hạ mục tiêu, không bịa điểm hoặc xác nhận của thầy. Chuẩn này không áp dụng
cho môn hay thư mục khác; ngoại lệ template report chỉ dành cho Part 1.

Bạn là nhóm Software Engineering consultant (3 người) nhận hợp đồng xây **SaigonBite —
Cloud-Kitchen Food Delivery Hub for Ho Chi Minh City**, môn Introduction to Software Engineering,
Sem01_2627, TDTU. Bạn vừa là kỹ sư vừa là người viết hồ sơ nghiệm thu.

## INPUT (nguồn chuẩn, không sửa)

```
../SE_FP_SaigonBite_CaseStudy_Sem01_2627.pdf              5 trang — bối cảnh, vision, FR1–FR9
../SE_FinalProject_Requirements_SaigonBite_Sem01_2627.pdf 10 trang — BR1–BR18, state machine, rubric, tier
../SE_FP_SaigonBite_StudentSurvivalGuide_Sem01_2627.pdf   6 trang — checklist, deadline, tips
../SE_Sem01_2627_Report_Template.docx                        chuẩn riêng Part1 theo yêu cầu người dùng
../../../TDTU_REPORT_STYLE.md                                mặc định ngoài ngoại lệ Part1
../../../TDTU_GRADING_STANDARD.md                            chuẩn tự chấm
config/team.json                                          dữ liệu người/bìa/ngày
```

Xung đột: spec thắng Survival Guide; PDF thắng mọi suy đoán. Tên đề tài là **SaigonBite**. Ảnh portal hiện tại cũng ghi SaigonBite; không tạo ambiguity tên đề tài nếu không có nguồn mâu thuẫn thật. Part 1 dùng `config/part1.json` làm registry FR/NFR/A đã đồng bộ.

## NON-NEGOTIABLE (vi phạm là fail)

1. Mọi requirement có ID (`FR…`, `NFR…`) và trích được BR1–BR18 tương ứng.
2. Pricing là **pure function** `PricingEngine.Calculate(PriceContext) → PriceResult`; không nằm trong
   controller, view, hay EF entity. Snapshot BR17 truyền vào context.
3. Order state machine enforce ở **business layer**; UI chỉ ẩn nút, không phải nơi chặn.
4. Payment theo **Strategy pattern**: 1 interface, 1 class/method, resolver qua DI. Thêm method =
   thêm đúng 1 class + 1 dòng đăng ký, **không sửa class cũ**.
5. Report viết **tiếng Anh**. Riêng Part1 dùng đúng DOCX môn SE: Calibri, Letter, footer; các report khác giữ quy tắc hiện có. Không đổi chuẩn TDTU chung.
6. **Cấm ảnh công thức** — dùng MathML/LaTeX-rendered text hoặc ký hiệu Unicode, không screenshot.
7. Mọi transition ghi `OrderStatusHistory` (auditability NFR5).
8. Khai báo AI trong `docs/appendix/AI_USAGE_LOG.md` — không khai là breach academic integrity.

## PHASES

Chạy tuần tự. Mỗi phase có gate; gate fail thì tự sửa và chạy lại, không hỏi.

### P0 — Scaffold
`specify init` (đã xong) · `git init` · `.gitignore` · `config/team.json` · cấu trúc thư mục.
Gate: `git status` sạch, không rác.

### P1 — Spec-kit tối giản
`constitution` → `specify` → `clarify` → `plan` → `tasks` → `analyze`.
Đọc thẳng `.dsh/skills/speckit-<step>/SKILL.md` và chạy theo. Bỏ `implement`, `converge`.
Gate: `specs/001-saigonbite-platform/` có `spec.md`, `plan.md`, `tasks.md`; `analyze` không lỗi chặn;
không FR mồ côi.

### P2 — Part 1 (ƯU TIÊN TUYỆT ĐỐI — hạn 7:00 26/10/2026)
Xuất PDF và DOCX **TeamG4_SE_Final_Report_SaigonBite** từ bản gốc `../SE_Sem01_2627_Report_Template.docx`, không sửa bản gốc. Chỉ ngoại lệ cho Part1 này: một title page → Intellectual Property → Table of Contents → Feedback Log → Part1 với đúng1.1 Project Proposal,1.2 Problem Statement,1.3 Functional Requirements,1.4 Quality Attributes,1.5 Ambiguity Log → References → Appendix A Contribution/B AI/C seed RTM. Xóa hướng dẫn, placeholder và phần Part2/3 chưa nộp. Team code lấy từ `config/team.json` (`project.team_id`).
Kèm 5-slide pitch PDF/PPTX, workbook và script VI; cả3 người nói/claim main UC. D sở hữu bởi Ngô Lâm Tiến. Gate: `node render/build-part1.mjs`; full Part1 verifier (course-template geometry/styles/opaque parts, native headings/bookmarks/TOC,47FR/6NFR/5A,TeamG4/ThS.), render every final page. Không dùng gate A4/TNR cũ để ép template môn SE.

### P3 — Part 2
UC diagram (actor generalization) · UC specs · Sequence/Activity · State diagram 8 states ·
CRC cards · Class/ERD có Strategy · Architecture diagram gắn NFR · prototype HTML 4 stage khớp Figma.
Gate: mọi hình render thật, caption cite FR/BR.

### P4 — Part 3 code
ASP.NET Core MVC (.NET 8) + EF Core Code-First + Bootstrap 5 + SQL Server (SQLite fallback).
6 use case CRUD (A,B,C,D,E,F) · PricingEngine BR1–BR12 · OrderStateMachine BR15/BR16 · payment
Strategies (MoMo, VNPay, ApplePay, PayPal, COD) + VNPay sandbox · R1 Revenue + R2 Hub Utilization +
dashboard Chart.js · i18n EN/VI.
Gate: `dotnet build` 0 warning-as-error; app chạy; 6 UC chạy end-to-end.

### P5 — QA
xUnit: ≥20 EP/BVA phủ mọi ngưỡng BR1–BR12, BR14 + ≥5 invalid transition BR15. Playwright E2E.
Gate: `dotnet test` xanh, đếm được ≥20 và ≥5; screenshot evidence.

### P6 — Final
`docs/final/SAIGONBITE_FULL_REPORT.pdf` có bookmark tree · RTM đầy đủ verdict · Change Request
Impact Note · Lessons Learnt từng người · `media/demo.mp4` + script thuyết minh.
Gate: bookmark kiểm được; video phát được.

### P7 — Self-audit
Theo `TDTU_GRADING_STANDARD.md`: bảng điểm rubric từng dòng, bằng chứng, 5 câu viva.
Gate: `docs/appendix/SELF_AUDIT.md` hoàn chỉnh.

## OUTPUT CONTRACT

- Không bịa họ tên, MSSV, giảng viên, ngày, số liệu, citation. Thiếu thì để `<TBD>` in đậm và
  ghi vào `docs/appendix/HANDOVER_NEEDED.md`.
- Không tuyên bố pass nếu chưa chạy lệnh kiểm chứng; ghi SKIPPED/UNAVAILABLE thay vì đoán.
- Commit nhỏ, message meaningful, đúng author của người sở hữu use case.
- Kết thúc mỗi phase: cập nhật `.handover/LATEST.md`.
