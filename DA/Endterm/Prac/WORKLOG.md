# Quá trình thực hiện bài cuối kỳ DAV

## Thông tin và quyết định
- Nhóm, giảng viên, môn và ngày: xem `project.json`, do người dùng cung cấp/xác nhận.
- Ngày báo cáo cố định 20/10/2026; không thay theo ngày build.
- Kế hoạch đã được Astra high phản biện; người dùng yêu cầu triển khai.
- Slide Anh, lời thuyết trình Việt; phân công dự kiến, không bịa % đóng góp.
- Raw dùng cho kết luận chính; thiếu 5% là thí nghiệm riêng với cùng mask cho mean/dropna.

## Nhật ký
- Bắt đầu triển khai: đọc lại chuẩn TDTU, kiểm thư mục và file tham chiếu; thư mục chưa có sản phẩm ngoài kế hoạch.
- Đã lưu ảnh đề, ảnh thông tin nhóm/giảng viên, ảnh slide mẫu và bản sao template; nguồn gốc tại TDTU được giữ nguyên.
- Đã tìm được bundled runtime cho tài liệu; chuẩn bị môi trường riêng cho notebook.

## Trạng thái
Đã hoàn thành sản phẩm và kiểm tái lập sau giải nén. Bộ nộp có Word/PDF, PowerPoint/PDF, notebook đã chạy, code/dữ liệu và hướng dẫn. Chưa nộp lên Elearning; chưa xác nhận nhóm đã diễn tập hoặc thử ứng dụng Microsoft PowerPoint.

## Kết quả triển khai đã chạy
- Tải riêng student-por.csv, xác minh SHA-256 và schema 649×33; raw không thay đổi.
- Cài môi trường Python 3.12 riêng với 50 gói đã khóa dependency; không sửa bundled runtime.
- Hoàn thành notebook 41 cell, trong đó 20 cell code chạy từ kernel sạch; đủ sáu mục biểu đồ và output top/bottom đủ 37 cột.
- Ba unit test kiểm dải điểm/giá trị sai, nhóm hằng và index, báo cáo rỗng/nhóm không có quan sát đều qua.
- Mẫu Word sớm đã kiểm hai bìa, bốn tên, Roman/Arabic, công thức OMML, TOC/LOF/LOT.
- Template tự đánh số Heading nên lần đầu bị lặp CHAPTER; đã vô hiệu numbering kế thừa khi dùng nhãn heading của báo cáo.
- Báo cáo đầy đủ có 31 trang, 3 phương trình native, 6 hình, 12 bảng. 48 mục heading/caption được đối chiếu số trang thực sau hai lượt pagination ổn định.
- Đã sửa pie chart quá cao, đặt nền nhãn phần trăm, giới hạn hình và giữ bảng ngắn liền khối.
- PowerPoint gồm 25 slide, notes Việt, chữ/bảng/chart chỉnh sửa được; biểu đồ box được dựng bằng hình học editable từ thống kê đã xuất.
- Chart workbook yêu cầu độ chính xác Excel: chỉ làm tròn dữ liệu trình bày về 12 chữ số có nghĩa; CSV/JSON phân tích giữ nguyên.
- Logo dùng path ban đầu hiện placeholder khi import/render; đã nhúng byte PNG gốc, xác nhận checksum và có ảnh ở từng slide.
- Native validators xác nhận package/font/chart/import; đã sửa padding bảng phụ lục. Bản cuối không có lỗi/cảnh báo hình học.
- verify_project.py đã qua trên các artifacts: dữ liệu, mask, 649/617 dòng, top/bottom, manifest, Word fields/OMML, 25 notes/logo và 5 workbook chart.
- Tạo skill TDTU cục bộ và dẫn từ AGENTS.md; quick_validate.py báo Skill is valid.
- JEV status hoạt động. Coverage decision qua LIVE_JEV chỉ xét tên ba unit test nên không có bằng chứng cho yêu cầu tài liệu/đóng gói; dùng thêm native Office validators, verify_project và xem render để kiểm các phần đó. Không dùng verdict đó thay cho chạy thực tế.

## Quyết định dùng lại
- Nội dung chính dùng raw; missing là thí nghiệm MCAR riêng.
- Đóng góp cá nhân chưa có dữ liệu thực tế: chỉ có đề xuất vai trò nói, không % bịa.
- TOC/SEQ/PAGEREF vẫn là field trong DOCX, cache được tạo bằng chương trình từ render thật. Không save round-trip DOCX qua LibreOffice.
- Môi trường notebook và môi trường authoring tài liệu tách riêng; README chỉ rõ cả hai.
- Không sửa Template_EN.docx hay PDF chuẩn tại gốc TDTU.

## Nghiệm thu và lỗi tìm được ở bước cuối
- Đã xem đủ 31 trang báo cáo và 25 slide ở render PPTX/PDF. Trang không đổi được đối chiếu byte PNG với bản đã xem; các trang thay đổi được xem lại riêng.
- PDF bộc lộ marker scatter quá nhạt: chuyển sang xám đặc; sửa ngắt dòng headline pie. Render lại cả deck, chỉ slide 15/16 đổi, hai slide này đã xem ở cả hai renderer.
- Lần tái lập đầu trong môi trường có MPLBACKEND=Agg không nhúng hình vào notebook. Đã bật inline backend rõ ràng ở cell setup; chạy lại trong cùng điều kiện, đủ sáu hình và verifier qua.
- Các PNG phân tích, CSV và summary giữ nguyên sau sửa backend. Byte SVG thay đổi do metadata/ID Matplotlib, không được dùng làm tiêu chí tái lập số.
- Giải nén candidate sang thư mục tạm riêng: 3 tests, 20 code cells và verify_project đều qua. Tất cả 14 CSV và structured summary khớp trong sai số tuyệt đối 1e-10. Dùng dependency environment đã khóa/cài, không tuyên bố kiểm trên máy hoặc OS khác.
- `uv pip check`: cả 50 gói tương thích. SHA-256 hai tài liệu tham chiếu gốc giữ nguyên.
- Đã ghi QA_CHECKS, office_verification, package_verification và INTERNAL_AUDIT. Bảng tự kiểm 9,7/10 dùng rubric nội bộ, không phải điểm giảng viên; phần readiness chưa có bằng chứng trình chiếu/diễn tập thực tế.
- ZIP theo chuỗi bốn MSSV, một thư mục cùng tên; không chứa venv, cache, lock hay ảnh render private. Công cụ đóng gói kiểm CRC và an toàn đường dẫn.

## Cách agent khác tiếp tục
1. Đọc README, project.json và REQUIREMENTS trước khi sửa; nguồn tính toán là notebook/summary, không sửa số bằng tay trong tài liệu.
2. Sửa phân tích: cập nhật builder nếu cần, chạy notebook/test/verifier; rebuild report/slide nếu số liệu đổi.
3. Sửa báo cáo: đọc chuẩn TDTU gốc; chạy build_report và update_fields, rồi render/xem trang cuối. Sửa slide: đọc skill `.agents/skills/tdtu-presentation` tại TDTU, finalizer và xem cả PDF.
4. Sau mọi thay đổi ảnh hưởng bộ nộp, chạy `tools/package_submission.py` bằng Python của `.venv` để giải nén/kiểm lại và thay ZIP. Không bỏ qua lỗi chỉ để có file nén.
5. Việc người dùng còn làm: tập thuyết trình, mở PowerPoint trên máy trình chiếu, xác nhận phân công thực tế và nộp Elearning đúng hạn.
