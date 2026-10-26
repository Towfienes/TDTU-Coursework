# Những chỗ cần đối chiếu trước khi làm bài

Đây là ghi chú đọc nguồn, không sửa các PDF/Word gốc và không thay đổi yêu cầu môn học. Mã file ở [00_SOURCES.md](00_SOURCES.md). Mọi nhận xét dưới đây dựa trên đối chiếu trong tài liệu hoặc tính lại công thức của tài liệu, không dùng nguồn bên ngoài.

## Các điểm đã xác nhận từ trang gốc

1. **Logistic gradient bị thiếu hệ số ở trang tổng kết.** LOG trang 39 định nghĩa mean loss, trang 42 derivation cho gradient $(1/N)\sum_i(p_i-y_i)x_{ij}$; trang 43 update viết $\eta\sum_i$ thiếu $1/N$. Giữ gradient trang 42 khi loss là mean; nếu dùng sum loss thì phải nói rõ việc đổi quy ước và learning rate. Không chép cả hai rồi gọi là nhất quán.
2. **Sunny regression branch có lời mô tả sai tên thuộc tính.** DT trang 43/DTN trang 46 nói chọn Temp vì SDR lớn nhất nhưng bảng cho Windy≈7.62, Temp≈0.678, Humidity≈0.370; cây trang sau dùng Windy. Tính theo bảng chọn Windy. DT trang 45/DTN trang 48 trên Rainy branch chọn Temp theo bảng là tình huống khác, không sửa nhầm cả hai.
3. **Normal equation có chuỗi ký hiệu cuối không nhất quán.** LR trang 25 có dòng đúng $X^TXw=X^Ty$, sau đó định nghĩa b và biến đổi A,w không khớp. Dùng trực tiếp normal equation; chỉ suy ra inverse khi $X^TX$ khả nghịch. Không lấy các dòng cuối làm phép biến đổi đáng tin cậy.
4. **SVM trang 29 chuyển giữa hard/soft margin.** Primal được in không có slack, nhưng dual phía dưới có bound $\alpha_i\le C$. Đọc cùng trang 12-13 và 32-33: hard margin không upper bound C; soft margin có slack/penalty C và bound C. Không khẳng định hai biểu thức in trên trang 29 là cùng một bài toán nếu bỏ qua sự khác nhau này.

## Các quy ước hoặc mô tả cần thận trọng

- **t-test:** EVAL trang 21 viết variance của chênh lệch với mẫu số k; trang 20 lại nhắc Student t với k-1 degrees of freedom. Trang 23 dùng chữ z vừa chỉ tail probability sig/2 vừa như critical value. Nếu đề yêu cầu tính kiểm định chính xác, cần xác định quy ước giảng viên muốn; không so t-statistic trực tiếp với 0.025 chỉ vì sig/2=0.025. Hình trang 21 cũng bị overlap chữ trong PDF gốc; không phải lỗi trích xuất.
- **ROC/AUC:** EVAL trang 14 gọi AUC như “sorting-based algorithm”, trong khi trang 24 giải thích area under ROC. Khi viết bài dùng khái niệm diện tích để tránh lẫn thuật toán dựng ROC với metric AUC.
- **F-beta:** EVAL trang 9 diễn giải trọng số bằng beta, nhưng biểu thức dùng beta bình phương. Giữ đúng biểu thức đã in, không tự bỏ số mũ.
- **Ví dụ R²:** EVAL trang 36 có actual [200000,300000,400000], predicted [210000,295000,390000]. Dòng “If R²=0.95” là giả định giải thích, không phải kết quả tính từ bảng. Tính theo bảng cho $SS_{res}=225000000$, $SS_{tot}=20000000000$, $R^2=0.98875$. Không báo 0.95 như kết quả bảng này.
- **Hamming:** KNN trang 20 có hình công thức absolute difference và ví dụ category bằng nhau/khác nhau; với categorical nói chung dùng đếm mismatch như định nghĩa k-modes ở CL trang 23. Không tự gán các màu số 1/2/3 rồi tính độ chênh số như thể có thứ tự.
- **Hopkins:** CL trang 78 mô tả hai lần sampling “from D” chưa phân biệt rõ điểm ngẫu nhiên trong không gian và điểm lấy từ tập. Chiều ý nghĩa H gắn với cách định nghĩa x,y và numerator của trang đó. Nếu cần implementation, đọc lại đề và làm rõ thay vì đem một công thức theo quy ước khác vào mà không nói.
- **LSTM:** DL trang 86 dùng xấp xỉ derivative của đường cell state bằng forget gate, không phải đạo hàm đầy đủ gồm mọi đường qua gates. Ký hiệu ở ảnh là **không tiến về 0** (mũi tên có gạch), không phải tiến về 0. Phải phóng to để tránh đọc sai nét nhỏ.
- **Classification và regression tree:** bài thủ công trình bày ID3/SDR; code thư viện không tự xác nhận đã thực hiện đúng thuật toán thủ công. Khi bài yêu cầu tự cài, phải bám tiêu chí của đề; khi cho dùng thư viện, mô tả đúng estimator/criterion thực tế.
- **Softmax trong đề cương:** SYL ghi “Softmax layer for multi-label classification”; cách dùng trong sơ đồ NN/DL thể hiện distribution giữa classes. Khi có đề phải phân biệt multiclass với multi-label; không tự chọn loss/output trước khi rõ target.
- **Đánh giá môn:** SYL là bản đề cương cũ với midterm 20% presentation, final 50% report; L1 trang 39 ghi project/presentation ở cả midterm và final. Chỉ coi đây là bối cảnh; đề/rubric người dùng gửi quyết định sản phẩm hiện tại.

## Ranh giới kiến thức

**Có trình bày đủ cốt lõi để giải thích:** kNN, Naive Bayes, entropy/gain/gain ratio/Gini, tree pruning, SDR regression tree, k-means/k-modes/k-medoids, hierarchical/linkage, DBSCAN, SVM margin/kernel/dual, linear regression/GD, perceptron, logistic/cross entropy, FFNN/backprop, CNN, RNN/BPTT, LSTM gates, attention/Transformer, random forest/AdaBoost/gradient boosting.

**Có giới thiệu nhưng không đủ tài liệu triển khai sâu mọi chi tiết:** Complement/Categorical NB, SMO đầy đủ, silhouette/BCubed derivation, EM/SOM/COBWEB, GRU, RBM/deep belief networks, training Word2Vec/GloVe/FastText/ELMo/BERT từ đầu, mọi CNN named architecture, Adam, reinforcement learning và GAN. Genetic algorithms được nhắc trong SYL nhưng không có slide riêng.

PCA/dimensionality reduction được nhắc như chủ đề/ứng dụng; không có bài PCA riêng và derivation eigenvalue trong nguồn. Không tự thêm PCA vào bài chỉ vì biết từ kiến thức nền. Các tên thư viện và hyperlinks trong slide cũng không có nghĩa nội dung ngoài hyperlink đã được đọc hoặc được phép sử dụng.

## Giới hạn việc đọc và lưu

- Đã xem toàn bộ trang PDF dưới dạng các ảnh ghép để đọc tổng thể; các trang công thức và bảng cần đối chiếu được mở lớn hơn. Không tuyên bố đã kiểm chứng từng con số trong mọi hình hoặc giải toàn bộ bài tập.
- Bản trích xuất Markdown giữ văn bản PDF/Word, có thể thiếu công thức, code dưới dạng ảnh và handwritten annotations. Ghi chú tổng hợp giữ nội dung chính của hình/công thức; PDF gốc vẫn là nguồn để đọc lại chi tiết.
- Word được đọc qua XML gồm toàn bộ paragraphs/ô bảng và các phần phụ có trong file; không render kiểm tra bố cục Word vì nhiệm vụ là học nội dung, không sửa hay giao một Word/PDF mới.
- Các bảng research benchmark ở DL phản ánh dữ liệu được đưa vào bài giảng, không được kiểm chứng bằng chạy lại và không phải kết quả của nhóm.
- Không đọc nội dung sách/website chỉ được liệt kê trong tài liệu, không lấy nội dung từ `ML/MidTermError` hoặc các bài nộp khác.
