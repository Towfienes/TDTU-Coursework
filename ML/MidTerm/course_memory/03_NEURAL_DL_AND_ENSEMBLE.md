# Neural networks, deep learning và ensemble learning

Nguồn trong [00_SOURCES.md](00_SOURCES.md). Ghi chú chỉ diễn giải slide và chuẩn hóa ký hiệu; các bảng benchmark là số liệu **của tài liệu**, không phải thực nghiệm của bài giữa kỳ.

## 1. Feed Forward Neural Network và MLP

Nguồn: NN trang 3-16; LOG trang 4-10.

ANN gồm các neurons nối bằng weights. FFNN truyền từ input qua hidden layers tới output; MLP là dạng feedforward nhiều lớp với activation phi tuyến. RNN có kết nối hồi quy và cần xét thời gian. Không coi mọi neural network là cùng một cấu trúc.

Đánh số layer như NN, input activation là $a^1=x$:

$$z^\ell=W^\ell a^{\ell-1}+b^\ell,\qquad a^\ell=\sigma(z^\ell).$$

$w^\ell_{jk}$ nối neuron k ở lớp trước đến neuron j ở lớp hiện tại. Mỗi lớp phải khớp chiều ma trận; bias có chiều bằng số neurons của lớp. $\sigma$ là activation của lớp, không bắt buộc luôn là sigmoid.

Các activation chính: sigmoid, tanh và $\mathrm{ReLU}(z)=\max(0,z)$. Neural network có thể trả giá trị regression hoặc vector cho classification tùy output layer và loss. Đề cương nói softmax; DL có softmax trong RNN, CNN và Transformer. Chuẩn hóa thành xác suất lớp:

$$\mathrm{softmax}(z)_j=\frac{e^{z_j}}{\sum_k e^{z_k}}.$$

Đây là cách viết tường minh phép softmax được dùng trong các sơ đồ; không suy ra softmax cho bài multi-label độc lập. Đề cương có một chỗ dùng chữ multi-label không đủ chính xác, xem caveats.

Ví dụ NN trang 13-16: hai inputs đều bằng 1; hidden preactivations 1.0, 1.3, 0.8; sigmoid cho khoảng 0.73, 0.79, 0.69. Weights từ hidden đến output 0.3, 0.5, 0.9; output sigmoid khoảng 0.77, target 0. Đây là forward example, không phải mô hình đã được train.

## 2. Backpropagation

Nguồn: NN trang 18-32.

Loss quadratic của một mẫu:

$$C_x=\frac12\|y-a^L\|^2,\qquad C=\frac1N\sum_x C_x.$$

Backpropagation tính gradient bằng chain rule; gradient descent dùng gradient đó để cập nhật tham số. Hai bước có vai trò khác nhau.

Đặt $\delta^\ell=\partial C_x/\partial z^\ell$. Với squared loss:

$$\delta^L=(a^L-y)\odot\sigma'(z^L),$$
$$\delta^\ell=((W^{\ell+1})^T\delta^{\ell+1})\odot\sigma'(z^\ell),$$
$$\frac{\partial C_x}{\partial W^\ell}=\delta^\ell(a^{\ell-1})^T,\qquad
\frac{\partial C_x}{\partial b^\ell}=\delta^\ell.$$

Tương đương theo phần tử $\partial C_x/\partial w^\ell_{jk}=a^{\ell-1}_k\delta^\ell_j$. $\odot$ là nhân từng phần tử; không thay bằng matrix product.

Quy trình: khởi tạo weights; forward lưu $z,a$; tính output error; truyền ngược qua hidden layers; lấy gradient theo weights/bias; lấy trung bình nếu loss định nghĩa là mean qua nhiều mẫu; cập nhật $W,b$; lặp theo tiêu chí dừng. Không cập nhật weights ở giữa lúc vẫn đang dùng chúng để tính gradient các lớp khác.

Công thức output delta trên **gắn với squared loss trong NN**, không được dùng nguyên xi cho mọi loss/output. Bài logistic đã cung cấp derivation cross entropy riêng. Nếu tự cài mạng cho đề giữa kỳ, cần kiểm tra gradient và shape bằng một ví dụ nhỏ trước khi tin kết quả train.

## 3. Deep Learning là representation learning

Nguồn: DL trang 3-15.

Traditional pipeline tách feature extractor khỏi learner; DL học các mức biểu diễn trong mạng và có thể end-to-end từ input đến output. Hình mặt người minh họa lớp đầu nhận cạnh, lớp sâu kết hợp cấu trúc phức tạp hơn. Slide nhấn mạnh nhiều mức biểu diễn, dữ liệu đủ lớn và tính toán mạnh.

Deep belief network/RBM, autoencoder, GAN và residual network có sơ đồ/tên trong phần lịch sử. Autoencoder gồm encoder-code-decoder, học representation để giảm chiều; RBM là generative stochastic network. Không có derivation đầy đủ cách train GAN/RBM hoặc residual blocks trong bộ tài liệu này. Không chọn phương pháp chỉ vì tên xuất hiện ở timeline.

## 4. Convolutional Neural Network

Nguồn: DL trang 16-46.

CNN khai thác cấu trúc cục bộ và nhiều cấp của dữ liệu. Filter/kernel trượt trên input; nhân các giá trị tương ứng và cộng để tạo feature map. Dữ liệu nhiều channels được tổng hợp qua channels của cùng filter; nhiều filters tạo nhiều output channels.

Sơ đồ chính: input → convolution → ReLU → pooling, có thể lặp nhiều lần → flatten → fully connected → output. Kernel học trong training; không mặc định mọi filter chỉ là ma trận chọn tay như ví dụ minh họa cạnh.

- Stride là độ dịch filter (trang 29).
- Padding VALID/SAME là hai tình huống được vẽ (trang 30); khi tính shape phải biết chính xác stride và padding.
- ReLU loại giá trị âm bằng $\max(0,z)$ (trang 31-32).
- Pooling giảm kích thước không gian và giữ đặc trưng nổi bật (trang 33-37); slide có max pooling, average pooling trong LeNet.
- Flatten chuyển feature maps thành vector để đưa vào FC; không phải một phép học như convolution.

Ví dụ trang 24/32: input $6\times6\times3$, hai filters $3\times3\times3$, stride 1 và không padding → output $4\times4\times2$. Từ cách đếm vị trí filter suy ra chiều một trục $\lfloor(n+2p-f)/s\rfloor+1$ khi padding đối xứng p; công thức này là suy luận từ cơ chế trượt, không phải câu chép nguyên văn slide.

LeNet-5 trang 44: input grayscale $32\times32\times1$ → convolution với 6 filters $5\times5$, stride 1, no padding → $28\times28\times6$ → average pooling $2\times2$, stride 2 → $14\times14\times6$. Các tầng sau là convolution, pooling và FC/softmax theo sơ đồ. Các tên AlexNet, VGGNet, GoogLeNet, ResNet, ZFNet xuất hiện ở trang 42 nhưng không có bài triển khai đầy đủ từng kiến trúc.

Trang 45 có CNN trên ma trận word representations cho NLP. Trang 46 minh họa Keras Sequential với Conv2D, MaxPooling2D, Flatten, Dense, sigmoid output, binary_crossentropy và optimizer adam. Adam chỉ được dùng như tên optimizer trong code; chưa có derivation thuật toán Adam trong tài liệu.

## 5. RNN và Backpropagation Through Time

Nguồn: DL trang 47-72; NN trang 7-8.

RNN dùng sequential information và hidden state ghi thông tin trước đó. Unfold theo thời gian cho thấy cùng bộ weights được dùng lại tại các bước; không tạo weights độc lập cho mỗi vị trí.

$$s_t=f(Ux_t+Ws_{t-1}),\qquad \hat y_t=\mathrm{softmax}(Vs_t).$$

DL trang 60 có dạng tanh với bias; có thể viết $s_t=\tanh(Ux_t+Ws_{t-1}+b)$ và logits $Vs_t+b_o$. Trang 59-64 gồm one-hot inputs, phép nhân ma trận và tính hidden/output cụ thể.

Các kiểu sequence mapping: one-to-many, many-to-one, many-to-many với chiều dài bằng hoặc khác nhau (trang 49,56). Ứng dụng: translation, email reply, POS tagging, sentiment và image captioning. Lựa chọn lấy output cuối hay mỗi bước phụ thuộc target thực tế.

Loss cross entropy trên sequence được cộng theo thời gian (trang 65):

$$E=-\sum_t\sum_c y_{tc}\log\hat y_{tc}.$$

Ở slide viết gọn $-\sum_t y_t\log\hat y_t$; phải hiểu phép cộng theo classes khi y là vector. BPTT unroll mạng, cộng đóng góp gradient từ từng bước và dùng chain rule xuyên các hidden states. Nhân nhiều Jacobians có thể làm gradient rất nhỏ; slide minh họa vanishing gradient và khó học phụ thuộc xa như France…French. Không tự thêm một giải pháp ngoài những cách được tài liệu trình bày.

## 6. LSTM và GRU

Nguồn: DL trang 73-91.

LSTM là một dạng RNN cho long-term dependencies. Cell state lưu thông tin; gates học điều gì giữ, ghi mới và đưa ra. Viết thống nhất từ trang 77-80:

$$f_t=\sigma(W_fx_t+U_fh_{t-1}+b_f),\quad
i_t=\sigma(W_ix_t+U_ih_{t-1}+b_i),$$
$$o_t=\sigma(W_ox_t+U_oh_{t-1}+b_o),\quad
\tilde c_t=\tanh(W_cx_t+U_ch_{t-1}+b_c),$$
$$c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t,\qquad
h_t=o_t\odot\tanh(c_t).$$

Trang 77 đặt trạng thái đầu bằng 0 và định nghĩa Hadamard product. Forget gate điều tiết cell state cũ; input gate điều tiết candidate; output gate điều tiết hidden output. Trang 82-86 phân tích đường truyền trực tiếp của cell state, với xấp xỉ derivative theo forget gate; gate gần 1 giúp gradient được giữ. Không coi xấp xỉ này là toàn bộ đạo hàm đầy đủ hoặc bảo đảm không bao giờ vanishing.

GRU có reset/update gates trong sơ đồ trang 73, không có derivation chi tiết riêng. Trang 87-89 có embedding→LSTM, stacked LSTM và BiLSTM hai hướng. Trang 90-91 có encoder-decoder NMT và attention lấy weighted context từ các encoder states.

## 7. Word representations và pretrained models

Nguồn: DL trang 93-102.

Word embeddings biểu diễn từ bằng vector dense trong số chiều nhỏ hơn vocabulary; hình minh họa các quan hệ ngữ nghĩa trong không gian vector. Word2Vec có CBOW và Skip-gram (trang 96); GloVe và FastText được giới thiệu. Static embedding khác contextual representations: vector sau có thể thay đổi theo câu.

ELMo ở trang 100-101 dùng LSTM-based language model trên corpus rồi lấy hidden states cho token để tạo contextual representation, gồm forward/backward LM. Bảng trang 98 và 102 minh họa benchmark từ tài liệu, không chứng minh một mô hình luôn tốt hơn trên dữ liệu giữa kỳ.

Phải phân biệt **nội dung về pretrained models được dạy** với **quyền tải và dùng pretrained weights cho bài**. Chưa có quyền/đề bài yêu cầu tải corpus hoặc weights; việc đọc slide không tự cho phép mở rộng dữ liệu.

## 8. Transformer và BERT

Nguồn: DL trang 103-134.

Động cơ: RNN tính tuần tự hạn chế parallelization; CNN cần nhiều lớp để nối phụ thuộc xa; attention cho phép biểu diễn quan hệ trực tiếp. Self-attention dùng các phần tử cùng sequence làm nguồn context. Multi-head attention học nhiều kiểu liên hệ; ví dụ “I kicked the ball” minh họa who/did what/to whom.

Từ embeddings X:

$$Q=XW^Q,\quad K=XW^K,\quad V=XW^V,$$
$$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V,$$
$$\mathrm{MultiHead}(Q,K,V)=\mathrm{Concat}(head_1,\ldots,head_h)W^O,$$
$$head_i=\mathrm{Attention}(QW_i^Q,KW_i^K,VW_i^V).$$

Trang 115-117 cho các công thức. Queries/keys quyết định weights attention; values được tổng hợp. Positional encoding cộng tín hiệu vị trí vào embeddings (trang 118), vì sơ đồ attention cần thông tin thứ tự.

Encoder chứa self-attention, feedforward và add/normalize; decoder chứa masked self-attention, encoder-decoder attention và feedforward (trang 119-123). Mask trong sơ đồ decoder ngăn dùng token tương lai khi dự đoán. Stacked encoder/decoder cho translation là ví dụ chính; không tự đổi thành một kiến trúc khác không có trong tài liệu.

Trang 124 so sánh bậc độ phức tạp: self-attention $O(n^2d)$, RNN $O(nd^2)$, convolution $O(knd^2)$, với n=length, d=dimension, k=kernel width. Tiêu đề “Attention is Cheap” phải hiểu trong điều kiện ví dụ; không kết luận luôn rẻ khi sequence dài.

Bảng translation trang 125/132: Transformer big có BLEU 28.4 EN-DE và 41.8 EN-FR trên benchmark minh họa; đó không phải số liệu từ mô hình của người dùng. Không dùng các mốc “state of the art” trong slide làm tuyên bố về hiện tại.

BERT (trang 126-134) dùng bidirectional Transformer encoder, pretrained bằng masked language model và next sentence prediction theo bài giảng. Input kết hợp token, segment và position embeddings. Fine-tuning có classification với [CLS], QA dự đoán start/end và NER theo token. Sơ đồ/bảng cũng nhắc GPT/GPT-2 và số liệu benchmark của thời điểm tài liệu. Không có nội dung để tự thêm LoRA/RAG hoặc các biến thể LLM khác.

## 9. Ensemble Learning

Nguồn: ENS toàn bộ 24 trang; trang 4-9 ôn cây quyết định.

Ensemble kết hợp nhiều individual models. Bagging train các models trên những random subsets theo kiểu có thể song song; boosting học tuần tự và tập trung sai sót trước đó. Số models/trees minh họa 1000 không phải mặc định bắt buộc.

**Random Forest (trang 11-12):** dùng decision trees với bagging; mỗi cây học trên random subset, mỗi split xét random subset features; từng cây dự đoán và kết hợp majority vote theo ví dụ classification. Không coi RF đơn thuần là nhiều cây giống hệt nhau trên cùng dữ liệu và cùng features.

**AdaBoost (trang 13-18):** tài liệu dùng biểu diễn trọng số sau, giữ đúng một quy ước xuyên suốt:

$$D_1(i)=1/N,\qquad
\varepsilon_t=\sum_iD_t(i)\mathbf1[y_i\ne h_t(x_i)],$$
$$\alpha_t=\log\frac{1-\varepsilon_t}{\varepsilon_t},\qquad
D_{t+1}(i)\propto D_t(i)\exp\left(\alpha_t\mathbf1[y_i\ne h_t(x_i)]\right),$$
$$\hat y=\operatorname{sign}\left(\sum_t\alpha_t h_t(x)\right).$$

Chuẩn hóa trọng số mẫu để tổng bằng 1 sau mỗi vòng. Trọng số mẫu và trọng số model là hai thứ khác nhau; model có weighted error thấp có tiếng nói lớn hơn. Trang 17 diễn giải có learning rate nhân vào log ratio. Không ghép update của một quy ước với hệ số của quy ước khác. Khi thực hiện phải xử lý error 0/1 và weak learner không tốt hơn random; slide chưa trình bày tất cả tình huống số học.

**Gradient Boosting (trang 19-23):** model mới fit lỗi residual/negative gradient của model tổng hiện tại, rồi cộng đóng góp. Bài giảng có thuật toán tổng quát:

$$F_0=\arg\min_\rho\sum_iL(y_i,\rho),\qquad
r_{im}=-\left[\frac{\partial L(y_i,F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}},$$
$$h_m\ \text{fit }r_{im},\qquad
\rho_m=\arg\min_\rho\sum_iL(y_i,F_{m-1}(x_i)+\rho h_m(x_i)),$$
$$F_m=F_{m-1}+\rho_mh_m.$$

Với squared loss, negative gradient là residual theo quy ước hệ số của loss. Inference cộng các đóng góp cây với đúng coefficients; không bỏ initialization và weights chỉ vì trang 23 nói ngắn “adding predictions”. Không thay gradient boosting trong bài bằng XGBoost/LightGBM/CatBoost nếu đề không cho phép: các phương pháp đó không được trình bày trong thư mục này.
