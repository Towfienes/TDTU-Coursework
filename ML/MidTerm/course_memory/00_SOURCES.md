# Danh mục nguồn Introduction to Machine Learning

Phạm vi: toàn bộ tài liệu trong `ML/Introduction to machine learning`. Đã đọc 15 bộ PDF với **680 trang** và một đề cương Word. `.DS_Store` là metadata macOS, không phải tài liệu môn học. Nguồn không bị sửa.

## Cách hiểu tình trạng đọc

PDF được trích xuất chữ theo từng trang và toàn bộ trang được render để đọc nội dung hình/công thức, kể cả những trang ít hoặc không có text. Đã xem tất cả các ảnh ghép trang; phóng to thêm các công thức/bảng cần đối chiếu. Đây là đọc nội dung môn học, không phải kiểm chứng lại toàn bộ nghiên cứu và mọi phép tính trên slide.

Bản Word được đọc toàn bộ đoạn văn và ô bảng theo XML. Không dùng layout Word để suy ra số trang vì chưa render. Ghi chú nguồn có 613 đoạn, kể cả đoạn trống và các phần phụ được trích.

Các trang trích xuất dưới 100 ký tự không có nghĩa trang trống: nhiều nội dung ở dạng ảnh. Số trang trong danh mục là số trang PDF, đếm từ 1.

## Tài liệu và mã tra cứu

| Mã | Tài liệu gốc | Trang | Nội dung |
|---|---|---:|---|
| L1 | [Lecture 1 -  Introduction to ML.pdf](../../Introduction%20to%20machine%20learning/Lecture%201%20-%20%20Introduction%20to%20ML.pdf) | 39 | Khái niệm AI/ML; data-model-learning; mô hình và inference; loại học; lịch sử; assessment |
| PREP | [Data Preparation for ML.pdf](../../Introduction%20to%20machine%20learning/Data%20Preparation%20for%20ML.pdf) | 17 | Chuẩn bị dữ liệu, structured/unstructured, NumPy và Pandas |
| L2 | [Lecture 2 - Principle of Machine Learning.pdf](../../Introduction%20to%20machine%20learning/Lecture%202%20-%20Principle%20of%20Machine%20Learning.pdf) | 39 | ERM, generalization, xác suất, generative/discriminative, Bayes và MLE |
| KNN | [Lecture 3 - kNN algorithm.pdf](../../Introduction%20to%20machine%20learning/Lecture%203%20-%20kNN%20algorithm.pdf) | 28 | kNN classification/regression, distance, scaling, encoding, KDTree |
| EVAL | [Lecture 3b - Evaluation .pdf](../../Introduction%20to%20machine%20learning/Lecture%203b%20-%20Evaluation%20.pdf) | 37 | Confusion matrix, classification/regression metrics, ROC, CV, bootstrap, t-test |
| NB | [Lecture 4 - Naive_bayes_classification.pdf](../../Introduction%20to%20machine%20learning/Lecture%204%20-%20Naive_bayes_classification.pdf) | 42 | NB structured/text, bag of words, smoothing, Gaussian/Bernoulli, micro/macro |
| DT | [Lecture 5 - Decision tree.pdf](../../Introduction%20to%20machine%20learning/Lecture%205%20-%20Decision%20tree.pdf) | 47 | Decision tree, ID3, pruning, gain ratio, Gini và regression tree |
| DTN | [Lecture - Decision tree - new.pdf](../../Introduction%20to%20machine%20learning/Lecture%20-%20Decision%20tree%20-%20new.pdf) | 51 | Bản cây quyết định bổ sung, hình/ghi chú, code và bài tập continuous features |
| CL | [Lecture 6 - Unsupervised Learning and Clustering.pdf](../../Introduction%20to%20machine%20learning/Lecture%206%20-%20Unsupervised%20Learning%20and%20Clustering.pdf) | 83 | Partitioning, hierarchical, density/grid, đánh giá cụm |
| SVM | [Lecture 7 - SVM 2024.pdf](../../Introduction%20to%20machine%20learning/Lecture%207%20-%20SVM%202024.pdf) | 35 | SVM margin, soft margin, kernel trick, dual, inference, SMO |
| LR | [Lecture 8 - Linear Regression and Gradient Descent.pdf](../../Introduction%20to%20machine%20learning/Lecture%208%20-%20Linear%20Regression%20and%20Gradient%20Descent.pdf) | 25 | Regression một/nhiều biến, loss, gradient descent, code, normal equation |
| LOG | [Lecture 9 - Perceptron and Logistic Regression.pdf](../../Introduction%20to%20machine%20learning/Lecture%209%20-%20Perceptron%20and%20Logistic%20Regression.pdf) | 43 | Perceptron, activation, entropy/KL/cross entropy, logistic và gradient |
| NN | [Lecture 10 - Neural Networks and Backpropagation Algorithm.pdf](../../Introduction%20to%20machine%20learning/Lecture%2010%20-%20Neural%20Networks%20and%20Backpropagation%20Algorithm.pdf) | 34 | ANN/MLP/FFNN/RNN, forward, quadratic loss, backprop |
| DL | [Lecture 11-12 - DL introduction.pdf](../../Introduction%20to%20machine%20learning/Lecture%2011-12%20-%20DL%20introduction.pdf) | 136 | Representation learning, CNN, RNN/BPTT/LSTM, embeddings, Transformer và BERT |
| ENS | [Lecture 13 - Ensemble Learning.pdf](../../Introduction%20to%20machine%20learning/Lecture%2013%20-%20Ensemble%20Learning.pdf) | 24 | Bagging, random forest, AdaBoost, gradient boosting |

## Vị trí các nội dung trong từng bộ slide

### L1

4-11: khái niệm; 17-32: sơ đồ và ví dụ; 34: loại học; 36-38: lịch sử/chủ đề; 39: đánh giá môn.

Bản trích xuất: [Lecture 1 -  Introduction to ML.md](sources/Lecture%201%20-%20%20Introduction%20to%20ML.md). Trang có ít hơn 100 ký tự text: 10, 13, 23, 24, 27, 29, 30, 34, 36.

### PREP

2-6: pipeline/data preparation; 7-13: thư viện; 14-17: thực hành và links bài tập.

Bản trích xuất: [Data Preparation for ML.md](sources/Data%20Preparation%20for%20ML.md). Trang có ít hơn 100 ký tự text: 5, 7, 9, 11, 13, 14.

### L2

3-11: học/loss/risk; 12-21: probability và Bayes; 22-25: MLE Gaussian; 26-38: NB; 39: link practice.

Bản trích xuất: [Lecture 2 - Principle of Machine Learning.md](sources/Lecture%202%20-%20Principle%20of%20Machine%20Learning.md). Trang có ít hơn 100 ký tự text: 9, 11, 13, 18, 19, 25, 26, 27, 29, 35, 36.

### KNN

4-17: thuật toán/ví dụ; 18-25: loại thuộc tính/chuyển đổi/bài tập; 26-27: KDTree; 28: giới hạn.

Bản trích xuất: [Lecture 3 - kNN algorithm.md](sources/Lecture%203%20-%20kNN%20algorithm.md). Trang có ít hơn 100 ký tự text: 8, 9, 10, 11, 12, 14, 16, 19, 20, 21, 22, 23, 25, 27.

### EVAL

4-12: confusion/metrics; 13-16: ROC/code; 17-23: evaluation/significance; 24-27: lựa chọn/code; 29-37: regression metrics/examples.

Bản trích xuất: [Lecture 3b - Evaluation .md](sources/Lecture%203b%20-%20Evaluation%20.md). Trang có ít hơn 100 ký tự text: 1, 2, 3, 12, 15, 16, 26, 27, 28, 32, 34, 35, 36, 37.

### NB

3-12: vấn đề/probabilistic models; 13-31: text NB/smoothing/ví dụ; 32-36: Reuters/evaluation; 37-42: code/Gaussian/Bernoulli.

Bản trích xuất: [Lecture 4 - Naive_bayes_classification.md](sources/Lecture%204%20-%20Naive_bayes_classification.md). Trang có ít hơn 100 ký tự text: 12, 40.

### DT

3-17: mô hình/xây cây; 18-26: entropy/IG; 27-30: overfitting/pruning; 31-34: gain ratio/Gini; 35-47: code/regression/SDR.

Bản trích xuất: [Lecture 5 - Decision tree.md](sources/Lecture%205%20-%20Decision%20tree.md). Trang có ít hơn 100 ký tự text: 1, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 30, 32, 34, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47.

### DTN

3-18: mô hình/xây cây; 19-27: entropy/IG; 28: code; 29-32: pruning; 33-36: gain ratio/Gini; 37-51: code/SDR/regression/exercise.

Bản trích xuất: [Lecture - Decision tree - new.md](sources/Lecture%20-%20Decision%20tree%20-%20new.md). Trang có ít hơn 100 ký tự text: 1, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 32, 34, 36, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51.

### CL

3-11: khái niệm/phân loại; 13-33: k-means/modes/medoids/bài tập/project; 35-52: hierarchy/BIRCH/CHAMELEON/probability; 54-67: DBSCAN/OPTICS/DENCLUE; 69-76: STING/CLIQUE; 78-81: evaluation; 83: summary.

Bản trích xuất: [Lecture 6 - Unsupervised Learning and Clustering.md](sources/Lecture%206%20-%20Unsupervised%20Learning%20and%20Clustering.md). Trang có ít hơn 100 ký tự text: 18, 19, 20, 21, 23, 25, 26, 30, 31, 32, 59, 66, 67.

### SVM

3-13: hyperplanes/margins; 14-28: kernel/maps/examples; 29-34: optimization/dual/inference/SMO; 35: summary trống.

Bản trích xuất: [Lecture 7 - SVM 2024.md](sources/Lecture%207%20-%20SVM%202024.md). Trang có ít hơn 100 ký tự text: 1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35.

### LR

6-14: mô hình/loss/đạo hàm; 15-18: GD/learning rate; 19-20: nhiều biến/outliers; 21-23: summary/bài tập; 24: code; 25: normal equation.

Bản trích xuất: [Lecture 8 - Linear Regression and Gradient Descent.md](sources/Lecture%208%20-%20Linear%20Regression%20and%20Gradient%20Descent.md). Trang có ít hơn 100 ký tự text: 15, 17, 18, 24, 25.

### LOG

4-14: neuron/perceptron/activation/update; 16-21: pass/fail/logistic; 22-28: information theory; 29-38: sigmoid/log-likelihood; 39-43: gradient/update.

Bản trích xuất: [Lecture 9 - Perceptron and Logistic Regression.md](sources/Lecture%209%20-%20Perceptron%20and%20Logistic%20Regression.md). Trang có ít hơn 100 ký tự text: 1, 5, 6, 8, 9, 11, 12, 15, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43.

### NN

3-9: kiến trúc; 11-16: forward/ví dụ; 18-21: học/loss/GD; 22-32: chain rule/backprop equations/algorithm; 34: reference.

Bản trích xuất: [Lecture 10 - Neural Networks and Backpropagation Algorithm.md](sources/Lecture%2010%20-%20Neural%20Networks%20and%20Backpropagation%20Algorithm.md). Trang có ít hơn 100 ký tự text: 1, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34.

### DL

3-15: DL/lịch sử/autoencoder/RBM; 16-46: CNN/LeNet/code; 47-72: RNN/BPTT; 73-91: LSTM/GRU/BiLSTM/attention NMT; 93-102: embeddings/ELMo; 103-125: Transformer; 126-134: BERT/benchmarks; 135-136: references/end.

Bản trích xuất: [Lecture 11-12 - DL introduction.md](sources/Lecture%2011-12%20-%20DL%20introduction.md). Trang có ít hơn 100 ký tự text: 3, 6, 7, 8, 9, 11, 12, 16, 25, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 40, 41, 45, 46, 47, 48, 49, 52, 53, 54, 55, 56, 58, 59, 60, 62, 63, 64, 66, 67, 68, 69, 70, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 90, 94, 96, 98, 101, 102, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 127, 128, 129, 130, 131, 132, 133, 134, 136.

### ENS

2-3: ensemble; 4-9: ôn cây; 10-12: bagging/RF; 13-18: AdaBoost; 19-23: gradient boosting; 24: references.

Bản trích xuất: [Lecture 13 - Ensemble Learning.md](sources/Lecture%2013%20-%20Ensemble%20Learning.md). Trang có ít hơn 100 ký tự text: 4, 5, 7, 8, 10, 14, 15, 21.

## SYL Đề cương môn học

Nguồn: [Đề cương 503044 - en - K - Introduction to Machine Learning - 3.0.docx](../../Introduction%20to%20machine%20learning/%C4%90e%CC%82%CC%80%20cu%CC%9Bo%CC%9Bng%20503044%20-%20en%20-%20K%20-%20Introduction%20to%20Machine%20Learning%20-%203.0.docx).

Bản trích xuất: [Đề cương 503044 - en - K - Introduction to Machine Learning - 3.0.md](sources/%C4%90e%CC%82%CC%80%20cu%CC%9Bo%CC%9Bng%20503044%20-%20en%20-%20K%20-%20Introduction%20to%20Machine%20Learning%20-%203.0.md).

Đã đọc thông tin học phần 503044, mục tiêu/chuẩn đầu ra, nhiệm vụ sinh viên, danh mục sách, bảng đánh giá, toàn bộ lịch học, phần phê duyệt và lịch sử phiên bản. Tên/chữ Signed trên đề cương không được dùng làm chữ ký hoặc thông tin advisor của nhóm.

Lịch: chương 1 introduction; chương 2 NumPy/Matplotlib/Pandas; chương 3 kNN/NB/evaluation; chương 4 SVM; chương 5 linear regression/GD; chương 6 perceptron/logistic; chương 7 clustering; chương 8 MLP/backprop; chương 9 RNN/BPTT; chương 10 CNN/LSTM/DL; chương 11 advanced methods gồm RL/GAN/Transformer/ensemble. Lịch theo đề cương không đồng nhất thứ tự đánh số các file PDF.

Assessment trong đề cương: process 1=10%, process 2=20%, midterm=20% presentation, final=50% report. Tại lần đọc ban đầu chưa có đề. Đề hiện hành và quyết định thực nghiệm nằm ở `../ASSIGNMENT.md`; kết quả và báo cáo nằm ở `../README.md`.

## Đối chiếu và bảo toàn nguồn

`inventory.json` lưu SHA-256 của tất cả 17 files, gồm cả metadata, để nhận biết nguồn thay đổi. `sources/` có 16 Markdown tương ứng 16 tài liệu học thuật. Nội dung formula/image không có text layer cần quay về PDF gốc; không khẳng định bản text là bản chép đầy đủ của mọi trang.

Không truy cập nội dung website/sách được dẫn bằng link trong slide. Các hyperlinks chỉ được lưu như một phần tài liệu người dùng cung cấp.
