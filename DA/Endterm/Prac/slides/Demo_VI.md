# Demo notebook — ba phút

Mở notebook đã chạy sẵn trước khi trình bày. Đóng các cửa sổ riêng tư; tăng cỡ chữ để người cuối lớp đọc được. Không tải dữ liệu hoặc cài thư viện trong giờ báo cáo.

## Trước buổi báo cáo

Chạy toàn bộ notebook bằng lệnh trong README. Xem lại outputs I.3, II.2, II.4, IV.1 và IV.2. Nếu dùng editor có kernel, chọn đúng môi trường dự án; các cell sau phụ thuộc các cell đầu. Người demo cần biết `df` là bản gốc đã thêm thuộc tính, còn `corrupted`, `imputed`, `dropped` là ba bản dùng riêng cho thí nghiệm.

## 0:00–0:55 — Missing và hai nhánh

Mở **I.3**. Chỉ vào `default_rng(42)` và lựa chọn 32 dòng không hoàn lại.

Lời dẫn: “Năm phần trăm của 649 là 32,45 nên chúng em chọn 32 ô absences, tương đương 4,93%. Hai phương pháp cùng xuất phát từ đúng một bản bị che. Mean imputation giữ 649 dòng; dropna còn 617. Đây là thiếu dữ liệu giả lập, không phải tình trạng thiếu ở UCI.”

Chỉ bảng missing comparison và mask. Nếu được hỏi mean, nêu **3,623987** là mean tính sau khi che, không dùng giá trị gốc đã bị che để điền.

## 0:55–1:45 — Insert và transform

Mở **II.2**, chỉ `.insert()` và vị trí cột `prior_grade_mean` trước G3. Chỉ ba cột mới, công thức và ngưỡng band.

Lời dẫn: “Mean của G1/G2 không chứa G3. Cột performance_band có chứa kết quả G3 nên chúng em loại nó khỏi xếp hạng yếu tố giải thích.”

Mở **II.4**, chỉ `groupby('school')` và hai lần `transform`. Giải thích phép biến đổi giữ đúng index của từng dòng; nhóm hằng được gán 0 để tránh chia cho 0. Dữ liệu được chuẩn hóa tương đối trong từng trường.

## 1:45–2:45 — Tổng hợp và top/bottom

Mở **IV.1**, chỉ lệnh `summary = comprehensive_report(df)` và output. Hàm có input rõ ràng, vừa hiển thị vừa trả dictionary cho bước xuất artifacts.

Mở **IV.2a**, cuộn ngang bảng top ten để thấy đủ cột; giải thích CSV cũng có đủ 37 cột. Chỉ stable sort và source index.

Lời dẫn: “Chúng em giữ đúng mười dòng. Các trường hợp đồng điểm giữ thứ tự nguồn để kết quả tái lập; người có cùng điểm bị bỏ khỏi danh sách không có nghĩa là kém hơn.”

## 2:45–3:00 — Chốt

“Báo cáo và slide dùng lại số liệu từ cùng lần chạy notebook. Kết quả mạnh về liên hệ với điểm kỳ trước; failures có liên hệ mạnh nhất trong nhóm biến hoàn cảnh dạng số/thứ bậc đã xét. Đây vẫn là phân tích quan sát, chưa kết luận nhân quả.”

## Khi demo gặp lỗi

Dùng ngay output đã lưu trong notebook. Nếu notebook không mở được, dùng PDF slide và CSV tương ứng trong `results/tables/`. Không sửa số bằng tay để tiếp tục demo, không chạy một cell phụ thuộc khi chưa có state đầu vào, và không chờ tải mạng trước lớp.

Phần này là kịch bản chuẩn bị, không xác nhận nhóm đã diễn tập thực tế.
