# Chuẩn report TDTU của người dùng

Đọc toàn bộ file này trước khi làm report trong TDTU. Đây là bộ nhớ dùng chung cho Codex, Claude, Antigravity và các agent khác; không phụ thuộc lịch sử chat. Ghi nhận và đối chiếu ngày 2026-10-14.

## 1. Quyết định người dùng đã xác nhận

| Vấn đề | Quy tắc đã chốt |
| --- | --- |
| Chuẩn ưu tiên | **PDF hoàn thiện của người dùng** khi khác với `Template_EN.docx` |
| Mức độ giống | Giữ đúng bố cục, font, lề, logo, khoảng cách, phân cấp đề mục và đánh số trang; không chỉ bắt chước phong cách chung |
| Công cụ | Công cụ nào cũng được, miễn PDF đúng mẫu |
| Công thức | LaTeX hoặc Equation thật của Word; **không dùng ảnh công thức**, kể cả chụp màn hình hay render công thức thành PNG/SVG rồi chèn |
| Ngôn ngữ | **Tiếng Anh** mặc định, kể cả khi trao đổi với người dùng bằng tiếng Việt |
| Màu trong report | **Hình, biểu đồ, sơ đồ dùng màu dễ phân biệt; ảnh giữ màu gốc.** Văn bản, tiêu đề, công thức, caption và bảng thông thường giữ đen/trắng/xám. Đây là lựa chọn người dùng xác nhận ngày 20/10/2026; không chuyển hình/biểu đồ về grayscale. |
| Phần đầu | Hai bìa → lời cảm ơn → cam đoan → mục lục → **LIST OF FIGURES nếu có hình trong nội dung** |
| Phần thân | Tên và số chương thay đổi theo đề bài; cuối cùng là tài liệu tham khảo |
| Trang trống | Bài mẫu không có hình nên giảng viên yêu cầu bỏ phần danh mục hình, để lại trang trống. Bài mới bỏ trang không dùng; **có hình thì phải có danh mục hình**, không áp dụng máy móc “xóa trang iii” |
| Thông tin mỗi bài | Nếu chưa được cung cấp đủ, phải hỏi **Thầy hay Cô, họ tên giảng viên, danh sách đầy đủ họ tên/MSSV sinh viên, ngày báo cáo/ngày nộp và giờ hạn nộp khi liên quan** |
| Cách phối hợp | Vừa làm vừa hỏi kỹ điểm chưa rõ; kiểm thông tin đã cung cấp trước, không hỏi lại câu đã có câu trả lời |

Yêu cầu mới, rõ ràng của người dùng được ưu tiên. Nếu đề/rubric của môn bắt buộc một bố cục hoặc ngôn ngữ mâu thuẫn, nêu đúng điểm xung đột để làm rõ; không tự bỏ yêu cầu môn hoặc âm thầm đổi chuẩn này.

## 2. Nguồn chuẩn và cách tìm

Tất cả đường dẫn dưới đây tính từ thư mục chứa file này, **không phải thư mục làm việc hiện tại**.

- [524H0195_524H0191.pdf](524H0195_524H0191.pdf): chuẩn hình thức chính, 24 trang vật lý; xuất từ Microsoft Word. Luôn mở các trang tương ứng khi đối chiếu.
- [Template_EN.docx](Template_EN.docx): template trường, 5 section OOXML; bản render kiểm tra có 10 trang. Cung cấp style, lề, section, header, đánh số và logo. Không mặc định DOCX đã giống hoàn toàn PDF.
- [Logo TDTU gốc](docs/report-reference/tdtu-logo.png): trích nguyên byte từ `word/media/image1.png` trong DOCX. Không vẽ lại, đổi màu, kéo méo hoặc thay bằng logo trên mạng.
- [Số đo và dấu vân tay nguồn](docs/report-reference/measurements.json): SHA-256, section/style OOXML, danh mục các phần trong DOCX, font và mốc tọa độ PDF. Đây là bằng chứng đo, không phải file cấu hình tự động áp mọi chi tiết của bài cũ.
- [Ảnh mẫu LIST OF FIGURES do người dùng bổ sung](docs/report-reference/list-of-figures-example.png): chuẩn bổ sung cho danh mục hình; ảnh cho thấy trang vật lý 6, số La Mã iv, tiêu đề giữa trang, tên hình với dấu chấm dẫn và số trang bên phải. Ảnh được lưu nguyên bản; không dùng kích thước pixel của ảnh chụp màn hình để suy ra số đo pt chính xác.

| Nguồn | SHA-256 |
| --- | --- |
| `Template_EN.docx` | `43233c7ab2aa96157b199d7e02521ba4346ed7f07e26cfdf606e72f87059dead` |
| `524H0195_524H0191.pdf` | `49918267441513033d8bd77fefabbaa58c54c22a253672d10841f88cb9755a76` |

Không sửa đè hai nguồn. Nếu hash thay đổi, đọc và đo lại trước khi dựa vào thông số cũ. Giữ các đường dẫn tương đối để cả bộ hướng dẫn vẫn dùng được khi chuyển thư mục.

## 3. Khổ giấy và hệ tọa độ

| Thuộc tính | Thông số | Bằng chứng |
| --- | --- | --- |
| Giấy | A4 dọc, khoảng 210 × 297 mm | PDF: 595.32 × 841.92 pt; DOCX: 11906 × 16838 twip |
| Lề trái | 3.5 cm | DOCX: 1985 twip; PDF bắt đầu thân bài gần x = 99.26 pt |
| Lề phải | 2 cm | DOCX: 1134 twip |
| Lề trên | 3.5 cm | DOCX: 1985 twip |
| Lề dưới | 3 cm | DOCX: 1701 twip |
| Header/footer từ mép giấy | 1.27 cm | DOCX: 720 twip mỗi phía |
| Gutter, cột | Gutter 0, một cột | Các section trong DOCX |
| Chiều rộng nội dung | Khoảng 155 mm / 439.35 pt | Tính từ khổ và lề |
| Trục giữa nội dung | x ≈ 318.9 pt tính từ trái | **Không phải giữa tờ giấy** (x ≈ 297.66 pt) |

Đơn vị: 1 inch = 72 pt = 1440 twip; 1 cm ≈ 28.3465 pt. Tọa độ PDF trong file số đo có gốc ở góc trên trái. `top_pt` là mép trên vùng chữ do bộ trích xuất đo, **không phải baseline hoặc khoảng cách paragraph**. Không đưa trực tiếp giá trị này vào lệnh vẽ baseline.

PDF không lưu thông số paragraph hay lề Word dưới dạng có thể đọc lại chính xác. Vì vậy: lấy thiết lập lề/paragraph từ DOCX làm điểm bắt đầu, rồi kiểm bằng vị trí thực tế trong PDF. Một số đoạn của bài cũ có direct formatting làm nhô ra khỏi vùng mặc định; không suy lề toàn tài liệu từ một dòng lẻ.

## 4. Font và paragraph

Font văn bản: **Times New Roman**, chữ đen. Dùng đúng bản Regular, Bold, Italic, Bold Italic. Không âm thầm thay bằng Times, Liberation Serif, Calibri hoặc font mặc định của LaTeX. PDF mẫu có một số font không nhúng; môi trường render cần có font tương ứng. Khi xuất bài mới, nhúng font nếu công cụ hỗ trợ.

| Vai trò | Cỡ / kiểu | Căn và khoảng cách |
| --- | --- | --- |
| Thân bài | 13 pt thường | Căn đều; mặc định giãn dòng 1.5 |
| Tiêu đề chương | 16 pt đậm, chữ hoa | Căn trái; `CHAPTER n. TITLE` cùng một dòng khi đủ chỗ |
| Mục cấp 1 | 14 pt đậm | Căn trái; `1.1 Title` |
| Mục cấp 2 | 14 pt đậm nghiêng | `1.1.1 Title`; kế thừa DOCX khi cần, PDF chưa có mẫu rõ để xác nhận |
| Mục cấp 3 | 14 pt thường | `1.1.1.1 Title`; dự phòng từ DOCX, không tự thêm cấp không cần thiết |
| Tiêu đề cảm ơn, cam đoan, mục lục, tham khảo | 16 pt đậm, chữ hoa | Căn giữa vùng nội dung |
| LIST OF FIGURES | Tiêu đề 16 pt đậm, chữ hoa; các mục 13 pt thường | Kế thừa hệ font chung; tiêu đề giữa, tên hình trái, số trang phải, dấu chấm dẫn như ảnh bổ sung |
| Mục lục cấp chương | 13 pt đậm | Chữ hoa; dấu chấm dẫn đến số trang căn phải |
| Mục lục cấp mục | 13 pt thường | Số mục thập phân; dấu chấm dẫn đến số trang |
| Số trang | 12 pt ở i–ii; 13 pt từ mục lục và thân bài | Times New Roman thường, header căn giữa vùng nội dung |
| Ngày / Author / Signature and full name | 13 pt nghiêng | Khối ở nửa phải trang |
| Họ tên dưới vùng ký (đã duyệt 24/10/2026) | 13 pt thường cho 1–4 người; 11 pt riêng họ tên khi có 5 người | Tất cả cùng một hàng, khoảng trắng giữa tên bằng nhau; không tự tạo chữ ký tay hay tên ký giả |

Cỡ đo được trong PDF có sai số lượng tử của Word: 12.96 ≈ 13, 14.04 ≈ 14, 15.96 ≈ 16, 21.96 ≈ 22 pt. Không coi đó là yêu cầu dùng các cỡ lẻ tùy ý.

DOCX: `Nidungvnbn` (Nội dung văn bản) dùng 13 pt, line 360/240 = 1.5, before/after 0, first-line 720 twip = 1.27 cm, justify. `Normal` lại là 12 pt, single, before/after 6 pt. **Không dùng Normal trần làm thân bài.** Heading 1–3 dùng line 1.5 và kế thừa before/after 6 pt. Các paragraph có direct formatting có thể khác style.

PDF trang 3: khoảng cách dòng thân bài khoảng 22.44 pt; dòng đầu x ≈ 135.26 pt, dòng tiếp theo x ≈ 99.26 pt, đúng thụt đầu dòng 36 pt. Thân chương có đoạn không thụt, danh sách và các bước toán có nhịp dày hơn. Dùng pattern phù hợp loại nội dung, không áp first-line 1.27 cm lên đề mục, mọi bullet hoặc mọi công thức.

## 5. Hai bìa

Nền trắng, không khung viền, không họa tiết. Giữ thứ tự các khối và khoảng trắng lớn như trang vật lý 1–2 của PDF:

1. `VIETNAM GENERAL CONFEDERATION OF LABOR`.
2. `TON DUC THANG UNIVERSITY` và `FACULTY OF INFORMATION TECHNOLOGY`, 14 pt đậm.
3. Logo TDTU màu gốc, khoảng **41.29 × 22.86 mm** (117.05 × 64.8 pt).
4. Tác giả: một dòng mỗi người, `HỌ TÊN – MSSV`, chữ hoa, 14 pt đậm.
5. Loại báo cáo: ví dụ `FINAL REPORT`, **24 pt đậm**.
6. Tên môn / đề tài: ví dụ `LINEAR ALGEBRA FOR IT`, **22 pt đậm**, chữ hoa.
7. Bìa trong thêm `Advised by` 14 pt thường và tên giảng viên 14 pt đậm.
8. `HO CHI MINH CITY, YYYY`, 14 pt đậm. Năm theo bài đang làm.

Mốc đo từ PDF (pt, gốc trên trái; vị trí **vùng chữ**, không phải baseline):

| Khối | Bìa ngoài trang 1: top | Bìa trong trang 2: top |
| --- | ---: | ---: |
| Dòng tổng liên đoàn | 101.34 | 101.33 |
| Tên trường | 123.89 | 123.41 |
| Tên khoa | 145.97 | 145.49 |
| Logo | 184.14 | 183.07 |
| Tác giả thứ nhất | 284.96 | 289.28 |
| Tác giả thứ hai | 301.04 | 304.16 |
| FINAL REPORT | 391.03 | 394.15 |
| Tên môn | 463.21 | 466.33 |
| Advised by | — | 632.65 |
| Tên giảng viên | — | 654.73 |
| Thành phố, năm | 639.13 | 700.21 |

Logo bắt đầu tại x = 260.38 pt ở cả hai bìa. Mọi khối tiêu đề trên hai bìa căn giữa vùng nội dung. **Quy chuẩn bìa theo người dùng:** dòng tổng liên đoàn (`VIETNAM GENERAL CONFEDERATION OF LABOR`) ở cả hai bìa dùng 14 pt thường và căn giữa đồng bộ (x ≈ 155.30 pt), thẳng hàng với tên trường và tên khoa; không để lệch trái ở bìa ngoài. DOCX và PDF đồng bộ 14 pt căn giữa cho cả hai bìa.

Tên tác giả, MSSV, giảng viên, năm, loại report và tên môn là dữ liệu thay đổi. Hai người trong PDF không mặc nhiên là tác giả của mọi bài sau. Nếu tên đề tài dài hoặc nhóm nhiều người, giữ font và thứ tự; điều chỉnh ngắt dòng/khoảng trắng có kiểm tra, không giảm cỡ chữ để nhét. Không in số trang ở hai bìa.

## 6. Thứ tự trang và đánh số

| Thành phần | Trang vật lý trong PDF mẫu | Số hiển thị của bài mới |
| --- | --- | --- |
| Bìa ngoài | 1 | Không số |
| Bìa trong | 2 | Không số |
| ACKNOWLEDGEMENT | 3 | i |
| DECLARATION OF AUTHORSHIP | 4 | ii |
| Trang trống | 5, số iii | **Bỏ trang không dùng**; không phải quy tắc cấm danh mục hình |
| TABLE OF CONTENT | 6, số iv | iii nếu hai mục trước mỗi mục một trang |
| LIST OF FIGURES (nếu có hình nội dung) | Không có trong PDF gốc; ảnh bổ sung cho thấy trang 6, số iv | Đặt sau mục lục, tiếp tục số La Mã; iv nếu mục lục kết thúc ở iii |
| Chương đầu | 7, số 1 | Bắt đầu lại 1 |
| Các chương tiếp theo | 8–23 | 2, 3, … liên tục, không reset mỗi chương |
| REFERENCES | 24, số 18 | Tiếp tục số Arabic |

Người dùng đã giải thích: trang trống ở bài cũ liên quan đến việc không có LIST OF FIGURES. Đây không phải yêu cầu bỏ danh mục hình ở mọi bài. Logo bìa không được tính là hình nội dung để tạo danh mục. Nếu phần đầu hoặc danh mục hình dài thêm, tiếp tục số La Mã thực tế; không cố định mục lục ở iii hay danh mục hình ở iv bằng cách bỏ số. Số trang ở **header**, trục giữa nội dung x ≈ 318.9 pt, mép chữ trên y ≈ 43.75–44.08 pt. Không có đường kẻ header, không có tên môn lặp lại ở đầu trang, không chuyển số xuống footer.

Cảm ơn và cam đoan mỗi mục bắt đầu trang mới; mục lục, danh mục hình khi có và tài liệu tham khảo cũng vậy. Thân bài bắt đầu trang mới với số 1. PDF có chương 3 bắt đầu gần cuối trang số 6 (trang vật lý 12), nên không suy ra rằng mọi chương bắt buộc bắt đầu trang mới. Khi dàn bài mới, giữ tiêu đề với đoạn mở đầu, tránh tiêu đề bị treo cuối trang; số trang và điểm ngắt sẽ thay đổi theo nội dung.

## 7. Các thành phần nội dung

**Lời cảm ơn:** tiêu đề giữa trang, thân bài Times New Roman 13 pt căn đều, cuối phần nội dung có khối ngày ở nửa phải và hàng họ tên theo quy tắc chữ ký dưới đây. Viết theo môn, người hướng dẫn và công việc thực tế. PDF và DOCX còn có lời cảm ơn nhắc đề tài MERN không cùng môn: đó là nội dung cũ phải thay, không phải văn mẫu được sao chép nguyên xi.

**Cam đoan:** tiêu đề giữa trang; các đoạn 13 pt căn đều, câu chịu trách nhiệm được nhấn đậm như mẫu; khối ngày ở bên phải, hàng họ tên theo quy tắc chữ ký dưới đây. Điền thông tin thật, không tự tạo cam kết sai về nguồn, kết quả hay tác quyền. Không chép tên và ngày của bài mẫu sang bài mới.

**Bố cục chữ ký — người dùng đã duyệt ngày 24/10/2026:** áp dụng mặc định cho ACKNOWLEDGEMENT và DECLARATION OF AUTHORSHIP, hỗ trợ 1–5 tác giả. Giữ đầy đủ dấu tiếng Việt và thứ tự tác giả thực tế.

- Khối ngày → `Author` (1 người) / `Authors` (2–5 người) → `(Signature and full name)` dùng Times New Roman 13 pt nghiêng, căn giữa trong khối rộng khoảng 84 mm ở phía phải vùng nội dung.
- Chừa khoảng 30 pt từ nội dung đến khối ngày; sau dòng hướng dẫn chừa khoảng 3 mm rồi vùng ký cao 30 mm trước họ tên. Giữ cả khối trên cùng trang, không chia cắt vùng ký.
- **Mọi họ tên nằm trên một hàng duy nhất, không xuống dòng và không xếp người lẻ sang hàng dưới.** Một người nằm giữa khối 84 mm bên phải; 2–5 người trải hết chiều rộng nội dung 155 mm, căn giữa từng họ tên và chia đều khoảng trắng giữa các tên. Có thể dùng flex với độ rộng theo tên và `space-around`; không ép mọi tên dài vào ô cố định gây chồng chữ.
- 1–4 người: họ tên Times New Roman 13 pt thường. 5 người: cho phép 11 pt **riêng hàng họ tên**, theo mẫu đã duyệt để giữ một hàng; thân bài và khối ngày vẫn 13 pt. Đây là ngoại lệ cho chữ ký, không phải cho phép thu nhỏ bìa, thân bài hay bảng khác.
- Không vẽ chữ ký, thêm tên ký in nghiêng giả chữ ký hoặc điền chữ ký thay tác giả. Vùng trắng dành cho người thật ký. Không chép tên minh hoạ thành thành viên của bài mới.
- Render và đo với tên thực: cùng cao độ, khoảng cách dương và đều, không tràn lề/chồng chữ. Với tên dài hơn mẫu khiến 5 người vẫn không vừa 11 pt, phải báo giới hạn và thống nhất cách xử lý; không tự cắt tên, bóp ngang chữ, giảm dưới 11 pt hoặc xuống hàng.

Ảnh bố cục đã duyệt: [so sánh 1–5 người](docs/report-reference/signatures-1-to-5-approved.png). Các tên trong ảnh chỉ minh hoạ bố cục; không phải danh sách tác giả mặc định. Ví dụ triển khai hiện có tại `SE/End term/SaigonBite/render/signatures.mjs`; chuẩn ở file này vẫn là nguồn dùng chung, không tạo skill/report guide cạnh tranh.

**Mục lục:** giữ nhãn `TABLE OF CONTENT` như PDF tiếng Anh. Bắt đầu danh sách tại lề trái nội dung. Chương và REFERENCES đậm, mục con thường, dấu chấm dẫn, số trang thẳng hàng bên phải. PDF mẫu có nhịp dòng khoảng 28.44 pt. Tạo từ heading thật, cập nhật sau lần xuất cuối; không gõ lại các số trang của mẫu. Không mặc định thêm lời cảm ơn/cam đoan vào mục lục vì mẫu không có.

**Chương:** giữ hệ `CHAPTER 1. …`, `1.1 …`, `1.2 …`, v.v. Ba chương INTRODUCTION / THEORETICAL BASIS / DESIGNING AND IMPLEMENTING là cấu trúc của bài mẫu, không phải giới hạn mọi môn. Chọn nội dung/chương theo đề, giữ hệ chữ và cách trình bày. Không giữ chữ `Question 1` nếu bài thực tế không tổ chức theo câu hỏi.

**Danh mục hình — bắt buộc khi có hình nội dung:** dùng tiêu đề `LIST OF FIGURES`, trang riêng sau mục lục và trước chương đầu, tiếp tục số La Mã. Bao gồm hình minh họa, sơ đồ, biểu đồ, ảnh kết quả và ảnh chụp màn hình được đưa vào nội dung; không đưa logo bìa hoặc công thức vào danh mục. Nếu không có hình nội dung thì bỏ danh mục và trang trống tương ứng.

Theo ảnh bổ sung: mỗi mục gồm `Figure 1.2.1: Caption` → dấu chấm dẫn → số trang căn phải; mã ví dụ thể hiện chương.mục.số-thứ-tự-hình-trong-mục. Dùng hệ này mặc định nếu đề không quy định khác, đánh số tự động và khớp caption trong thân bài. Caption dài được xuống dòng, số trang ở cuối mục; không chồng lên caption hoặc tràn lề. Tên và số trang lấy từ caption/tham chiếu thật, cập nhật sau dàn trang; không gõ tay dấu chấm và số trang. LaTeX/Word phải tạo được danh mục tự động từ các caption. Nếu danh mục dài hơn một trang, cho tiếp tục bình thường; không thu nhỏ font để nhét một trang. Ảnh không xác nhận vị trí caption ở dưới/trên hình trong thân bài: không tuyên bố đã đo chi tiết đó từ ảnh.

**Danh sách và các bước:** 13 pt; bullet/numbering thực, thụt cấp rõ. Phần bài toán dùng giải thích ngắn, các bước biến đổi và công thức đi liền nhau. Không bê nguyên các dấu `=>`, lỗi khoảng trắng hoặc lỗi diễn đạt của bài cũ thành yêu cầu trình bày.

**Tài liệu tham khảo:** trang riêng, `REFERENCES` 16 pt đậm căn giữa; các mục 13 pt, tên sách/tài liệu nghiêng, thụt treo khoảng 1.27 cm theo mẫu. Mẫu dùng tác giả/năm và không đánh số từng tài liệu. Dùng chuẩn trích dẫn khác khi môn yêu cầu rõ; chỉ đưa tài liệu đã dùng, không sao chép danh sách của bài mẫu. Giữ link hoạt động nếu có.

**Bảng, hình, code:** PDF chuẩn ban đầu không có ví dụ bảng dữ liệu, ảnh nội dung hoặc code listing để suy ra một chuẩn chi tiết; ảnh bổ sung đã xác nhận quy tắc danh mục hình ở trên. Nếu cần, dùng bảng/hình trong vùng nội dung, font đồng bộ, không tràn trang. DOCX có style `Caption` 13 pt căn giữa và `TableGrid` viền đơn 0.5 pt; đây chỉ là nguồn dự phòng, không phải bằng chứng đã có trong PDF. Thống nhất vị trí caption theo yêu cầu môn; hỏi khi lựa chọn đó ảnh hưởng chuẩn nộp bài. Danh mục bảng (`LIST OF TABLES`) theo đề hoặc làm rõ với người dùng khi có bảng và yêu cầu chưa rõ; chưa có quyết định mặc định riêng cho phần này. Không tự thêm abstract hay trang trang trí nếu không cần.

### Màu sắc của hình và biểu đồ trong report

- Dùng màu trên nền trắng để các nhóm và đường biểu diễn dễ phân biệt; giữ cùng ánh xạ màu cho một nhóm xuyên suốt báo cáo.
- Kết hợp màu với nhãn, chú giải, marker hoặc kiểu đường; không dùng riêng màu để truyền đạt thông tin. Heatmap tương quan dùng thang phân kỳ có tâm 0 và miền −1 đến 1.
- Giữ màu gốc của ảnh và logo; không tự chuyển grayscale. Không tự tô màu lại ảnh bằng chứng.
- Chữ, heading, công thức, caption và bảng thông thường vẫn đen/trắng/xám. Quy tắc này áp dụng report toàn TDTU; presentation theo skill slide: hình/biểu đồ cũng có màu, còn nền/chữ/bảng thông thường đơn sắc (người dùng cập nhật ngày 20/10/2026).

## 8. Công thức toán — bắt buộc

- LaTeX: soạn bằng môi trường toán thực, ví dụ `\(...\)`, `\[...\]`, `aligned`, `pmatrix`, `cases`. Công thức xuất ra PDF phải là chữ/ký hiệu/vector từ bộ typesetting, không phải ảnh chèn vào tài liệu.
- Word: dùng Office Math / OMML (`m:oMath`, `m:oMathPara`). Gõ chuỗi LaTeX vào paragraph bình thường chưa phải Equation; phải chuyển thành công thức Word thật.
- Không tạo ảnh công thức PNG/JPEG/SVG/PDF rồi dùng lệnh chèn hình để thay cho toán. Ảnh logo, đồ thị và minh họa vẫn được dùng khi phù hợp.
- Mẫu có font toán **Cambria Math**, cỡ nền khoảng 13 pt, chỉ số dưới/trên nhỏ hơn; dùng Cambria Math khi bộ typesetting hỗ trợ. Không mặc định Computer Modern rồi tuyên bố giống mẫu. Nếu thiếu font, tìm font đã cài hợp lệ hoặc nêu chênh lệch cần xử lý.
- Giữ phân số có gạch, chỉ số dưới/trên thật, ngoặc ma trận co giãn, ký hiệu tổng/căn/chuẩn vector đúng. Không giả lập ma trận bằng dấu cách hoặc bảng ảnh.
- Công thức ngắn đi cùng câu; công thức dài tách dòng và căn theo luồng giải. PDF không đánh số mọi phương trình, nên chỉ thêm số khi bài cần dẫn chiếu.
- Cho phép xuống dòng ở bước biến đổi hợp lý; không thu nhỏ cả công thức đến khó đọc để vừa lề. Kiểm tra ngoặc, dấu căn, phân số, glyph và khoảng cách ở PDF cuối.
- Kiểm tra cả nguồn và PDF: PDF không có image object ở các trang toán là bằng chứng hữu ích nhưng chưa đủ để chứng minh công thức có nguồn chỉnh sửa được. Giữ lại `.tex` hoặc Equation OMML thật trong nguồn.

## 9. Quy trình cho mỗi bài mới

1. Đọc chuẩn này, đề/rubric và file nguồn liên quan. Mở PDF mẫu ở các trang 1, 2, 3, 4, 6, 7, 13, 24 để lấy các pattern bìa, phần đầu, mục lục, chương, toán và tham khảo.
2. Đối chiếu thông tin từ đề, file người dùng cung cấp và cuộc hội thoại với checklist thông tin bên dưới. Gom các điểm thiếu/mâu thuẫn thành câu hỏi cụ thể; nếu đã đủ thì làm ngay, không hỏi xác nhận lại. Vừa làm phần độc lập vừa chờ trả lời. Dữ liệu thiếu được đánh dấu trong bản nháp, không bịa để giao bản cuối.
3. Chọn công cụ sẵn có phù hợp. Với DOCX, làm trên **bản sao** `Template_EN.docx`, giữ section/style/logo/header và chỉnh những điểm khác PDF theo chuẩn này. Với LaTeX, tái hiện thông số đã đo và toán native; class mặc định chưa đủ. Không chọn tool chỉ vì tiện nếu không dựng được mẫu.
4. Dựng và render sớm hai bìa + một trang nội dung có công thức (nếu bài có toán). Kiểm font và vị trí các khối trước khi dàn toàn bộ.
5. Viết nội dung đúng môn và dữ liệu thật. Có hình nội dung thì tạo caption và LIST OF FIGURES; không có thì bỏ phần không dùng, không để trang trống. Đặt số La Mã/Arabic bằng section hoặc cơ chế đánh số thực; tạo heading, mục lục và danh mục hình tự động.
6. Cập nhật mục lục/danh mục hình/tham chiếu bằng công cụ hỗ trợ, xuất PDF, kiểm tất cả trang. Nếu dùng Word mà chưa cập nhật được field, nêu rõ và xử lý trước khi gọi PDF là bản nộp cuối; bật `updateFields` một mình không xác nhận PDF đã có mục lục hay danh mục hình đúng.
7. Đối chiếu trực quan với trang mẫu cùng vai trò, sửa rồi xuất lại. Nội dung mới có thể dài hơn: không ép về 24 trang hoặc sao chép điểm ngắt của bài cũ.
8. Giao PDF đã kiểm; giữ nguồn có thể chỉnh sửa và lệnh build trong thư mục bài. Chỉ đóng gói thêm DOCX/LaTeX khi yêu cầu nộp hoặc người dùng cần. Không đưa file QA tạm vào gói nộp.

### Checklist thông tin phải nắm trước mỗi bài

| Thông tin | Cách xử lý |
| --- | --- |
| Giảng viên | Hỏi **Thầy hay Cô**, họ tên đầy đủ, cách ghi danh xưng/học vị nếu đề yêu cầu. Không đoán từ tên, không lấy giảng viên trong mẫu. Chỉ dùng `Mr.`, `Ms.`, `Dr.`, `Prof.` theo thông tin đã có; không tự gán học vị hay tình trạng hôn nhân. Dùng nhất quán trên bìa, cảm ơn và cam đoan. |
| Sinh viên | Nắm đủ **từng người**: họ tên chính xác, dấu tiếng Việt, MSSV và thứ tự trình bày; mã nhóm/lớp nếu đề yêu cầu. Không mặc định nhóm chỉ có hai người hoặc tái dùng danh sách bài trước. Nếu người dùng chỉ nói “nhóm mình”, hỏi nhóm gồm những ai. |
| Ngày ghi trên report | Phân biệt ngày hoàn thành/ký báo cáo với ngày nộp. Dùng ngày người dùng/đề cung cấp; nếu chưa có thì hỏi, không tự lấy hôm nay hoặc ngày trong mẫu. Đồng bộ ngày ở cảm ơn/cam đoan và năm trên bìa. |
| Hạn nộp | Khi task có hạn nộp, nắm ngày, giờ và múi giờ nếu còn mơ hồ. Với “hôm nay”, “ngày mai”, kiểm ngày giờ hiện tại theo `Asia/Ho_Chi_Minh` (trừ khi người dùng chỉ định múi giờ khác) rồi ghi ngày tuyệt đối trong thông tin làm việc. Không dùng ngày cũ của phiên chat làm đồng hồ hiện tại. Không đưa giờ lên bìa nếu mẫu/đề không yêu cầu. |
| Bài cần làm | Môn, đề tài, loại báo cáo, rubric, nội dung/kết quả thực tế, file cần giao, hình/bảng cần dùng. Kiểm những gì đã cung cấp trước khi hỏi. |

Ví dụ khi còn thiếu: “Bạn bổ sung giúp mình: giảng viên là Thầy hay Cô và họ tên; danh sách sinh viên kèm MSSV; ngày muốn ghi trên báo cáo và hạn nộp (nếu có).” Chỉ giữ những mục thực sự thiếu trong câu hỏi. Nếu dữ liệu mâu thuẫn, trích hai giá trị và hỏi dùng giá trị nào. Khi điểm chưa rõ ảnh hưởng nội dung, bố cục hoặc tính đúng của bài, hỏi kỹ trước khi quyết định phần đó; tiếp tục các phần không phụ thuộc. Không giao bản cuối với thông tin thiết yếu còn suy đoán. Các yêu cầu riêng của một bài không tự trở thành mặc định lâu dài cho mọi bài.

## 10. Kiểm tra trước khi giao

- [ ] Đúng template, đủ hai bìa và các phần đã chốt; tiếng Anh; đã rõ Thầy/Cô, tên giảng viên, toàn bộ sinh viên/MSSV; ngày báo cáo, năm bìa và hạn nộp không mâu thuẫn.
- [ ] A4 dọc, lề 3.5/2/3.5/3 cm (trái/phải/trên/dưới), không dùng lề đều 2.54 cm.
- [ ] Times New Roman đúng biến thể; thân 13, mục 14, chương 16, loại report 24, tên môn 22 pt.
- [ ] Logo đúng asset, tỷ lệ và vị trí; không tự thêm viền/màu nền; căn giữa theo vùng nội dung.
- [ ] Bìa không số; phần đầu i, ii, iii… liên tục, kể cả danh mục hình; không trang trống không dùng; thân bài bắt đầu 1; số ở header.
- [ ] Mục lục khớp heading và số trang **của PDF cuối**, leader và cột số ngay hàng.
- [ ] Có hình nội dung thì có LIST OF FIGURES; mỗi mục khớp caption, mã hình và số trang PDF cuối, kể cả mục dài nhiều dòng; không đưa logo bìa vào danh mục.
- [ ] Công thức native trong nguồn; không ảnh công thức; đủ glyph, không cắt ngoặc/phân số/ma trận.
- [ ] Hình/biểu đồ dùng màu rõ trên nền trắng, ánh xạ màu nhất quán và có nhãn/chú giải; ảnh giữ màu gốc. Phần chữ và bảng thông thường vẫn đơn sắc.
- [ ] Đã xem hình render **mọi trang PDF cuối**, không chỉ extract text; không tràn lề, chồng chữ, tiêu đề treo hoặc trang trắng ngoài ý muốn.
- [ ] Đã đối chiếu bìa, cảm ơn/cam đoan, mục lục, một trang chương, một trang toán và tham khảo với PDF chuẩn. Ghi rõ phần chưa kiểm hoặc chênh lệch còn lại, không tuyên bố “giống hệt” chỉ từ thông số.
- [ ] Không còn placeholder, đề tài MERN, tên/ngày/môn/tham khảo cũ không liên quan; nguồn tham chiếu nguyên vẹn.

Không dùng pixel diff toàn trang làm điều kiện bằng nhau khi nội dung khác. Với bìa, đối chiếu trục và mốc khối cố định; với thân bài, đối chiếu lề, font, line spacing, đề mục và page number. Không có kết quả kiểm trực quan thì chỉ được gọi là bản nháp chưa xác minh hình thức.

## 11. Cách agent tìm bộ nhớ này

`AGENTS.md` là cửa vào chung/Codex. `CLAUDE.md` import `AGENTS.md` và yêu cầu đọc chuẩn khi làm report. `GEMINI.md` chỉ đến cùng hai file cho Gemini/Antigravity. Chỉ cập nhật quy tắc chi tiết tại file này để các agent không giữ bản khác nhau.

Mở **TDTU làm workspace root** để các công cụ phát hiện đầy đủ chỉ dẫn. Nếu mở riêng một thư mục môn và ứng dụng không nạp chỉ dẫn ở thư mục cha, yêu cầu agent đọc `TDTU/AGENTS.md` và file này bằng đường dẫn thực. Không giả định mọi ứng dụng hoặc mọi cấu hình tự đọc mọi file Markdown.

Cơ chế bộ nhớ/rule được đối chiếu với [tài liệu Claude Code](https://code.claude.com/docs/en/memory) và [tài liệu Antigravity](https://antigravity.google/docs/rules/). Các file hướng dẫn là ngữ cảnh cho agent, không phải cơ chế đảm bảo tuyệt đối kết quả; checklist render và đối chiếu vẫn bắt buộc. Sau khi thêm file, kiểm trong phiên mới rằng agent đọc được chuẩn và nhắc đúng: PDF ưu tiên, tiếng Anh, có hình thì có LIST OF FIGURES, bỏ trang không dùng, công thức native, hỏi thông tin giảng viên/sinh viên/ngày giờ còn thiếu.

## 12. Phạm vi đã xác minh

Đã đọc cấu trúc/style của DOCX, render và xem cả 10 trang template bằng LibreOffice đi kèm runtime, đồng thời trích font/tọa độ và xem cả 24 trang PDF hoàn thiện. Số đo PDF và XML được lưu trong `measurements.json`; logo giữ nguyên byte. Đã xem và lưu ảnh LIST OF FIGURES người dùng bổ sung; chưa đo hoặc kiểm toàn bộ PDF 31 trang xuất hiện trong ảnh. Chưa dựng một report mới bằng các quy tắc này và chưa chạy phiên mới trong Claude/Antigravity để kiểm việc tự nạp chỉ dẫn. Đây là bộ chuẩn đã đối chiếu nguồn, không phải tuyên bố mọi công cụ đã được thử end-to-end.
