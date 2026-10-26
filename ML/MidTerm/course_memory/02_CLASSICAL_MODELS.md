# Các mô hình học máy cơ bản

Đọc [00_SOURCES.md](00_SOURCES.md) để tra mã nguồn. Những công thức dưới đây là dạng chuẩn hóa ký hiệu của slide hoặc phép biến đổi trực tiếp từ chúng; không bổ sung mô hình ngoài tài liệu. Các chỗ thiếu nhất quán nằm ở [04_SOURCE_CAVEATS.md](04_SOURCE_CAVEATS.md).

## 1. k Nearest Neighbors

Nguồn: KNN trang 4-28.

**Mô hình và inference:** instance-based/lazy learning giữ các ví dụ học. Với đầu vào mới, tính khoảng cách tới dữ liệu train, lấy $k$ mẫu gần nhất. Classification bỏ phiếu đa số; regression lấy trung bình đích của các láng giềng:

$$\hat y=\arg\max_c\sum_{i\in N_k(x)}\mathbf1[y_i=c],\qquad
\hat y_{\mathrm{reg}}=\frac1k\sum_{i\in N_k(x)}y_i.$$

Trang 17 có distance-weighted classification:

$$\hat y=\arg\max_c\sum_{i\in N_k(x)}\frac{\mathbf1[y_i=c]}{d(x,x_i)^2}.$$

**Học và lựa chọn:** không có việc tối ưu một vector trọng số như linear regression; dữ liệu train, phép biểu diễn, metric và $k$ quyết định prediction. Cần chọn $k$ bằng đánh giá theo quy trình của môn. KNN trang 11-16 dùng chiều cao, tuổi để phân lớp H/M/L hoặc dự đoán cân nặng; trang 21-23 dùng age-loan-default.

Khoảng cách trong slide:

$$d_2(x,z)=\sqrt{\sum_j(x_j-z_j)^2},\quad
d_1(x,z)=\sum_j|x_j-z_j|,$$
$$d_q(x,z)=\left(\sum_j|x_j-z_j|^q\right)^{1/q},\quad
d_\infty(x,z)=\max_j|x_j-z_j|.$$

Euclidean là $q=2$, Manhattan là $q=1$; Hamming đếm vị trí khác nhau ở dữ liệu phân loại/nhị phân. Cosine, Jaccard, Haversine và Sørensen-Dice xuất hiện trong hình trang 10 ở mức giới thiệu, không có derivation đầy đủ trong bộ slide này. KDTree trang 26-27 minh họa chia không gian và tìm láng giềng.

**Giới hạn và kiểm tra:** đặc trưng khác thang đo cần chuẩn hóa; biến không có thứ tự cần mã hóa phù hợp. KNN có biên quyết định phức tạp nhưng prediction có thể chậm và không sinh ra mô hình dễ diễn giải. Khi cài đặt phải quyết định hòa phiếu, khoảng cách bằng 0 trong trọng số nghịch đảo và giới hạn $1\le k\le N_{\mathrm{train}}$; slide chưa cho mọi quy tắc biên đó.

## 2. Naive Bayes

Nguồn: L2 trang 26-38; NB trang 13-31, 34-42.

**Giả định:** các đặc trưng độc lập có điều kiện khi biết lớp. Không phải độc lập vô điều kiện.

$$P(x\mid c)=\prod_{j=1}^d P(x_j\mid c),\qquad
\hat c=\arg\max_c P(c)\prod_j P(x_j\mid c).$$

Tham số là prior của lớp và phân phối đặc trưng theo lớp. Prior ước lượng bằng số mẫu lớp trên tổng số mẫu.

**Multinomial NB cho văn bản:** bag of words bỏ qua vị trí, giữ số lần từ xuất hiện. Trích vocabulary từ train, gộp tài liệu theo lớp để đếm từ. Lặp từ trong tài liệu phải đóng góp nhiều lần vào tích likelihood; không biến thành chỉ có/không rồi vẫn gọi là multinomial.

$$\hat P(c)=\frac{N_c}{N},\qquad
\hat P(w\mid c)=\frac{\mathrm{count}(w,c)+\alpha}
{\sum_{v\in V}\mathrm{count}(v,c)+\alpha|V|}.$$

Laplace add-1 là $\alpha=1$. Từ không xuất hiện có thể làm tích xác suất bằng 0 nếu không smoothing. NB trang 30 trình bày thêm một token unknown vào vocabulary với mẫu số tăng thành tổng count + $|V|+1$. Nếu cần xử lý OOV, phải chọn rõ quy ước này hoặc quy ước mà đề yêu cầu.

Log-score là phép biến đổi từ tính đơn điệu của log (L2 trang 23; NB trang 18-23):

$$s_c(x)=\log P(c)+\sum_j\log P(x_j\mid c).$$

Với vector counts $n_w$, tổng tương ứng là $\log P(c)+\sum_w n_w\log P(w\mid c)$. Score để chọn lớp không tự là posterior đã chuẩn hóa.

Ví dụ NB trang 31: ba tài liệu lớp Chinese và một lớp Japanese; vocabulary gồm 6 từ. $P(c)=3/4$, $P(j)=1/4$; $P(Chinese\mid c)=3/7$, $P(Tokyo\mid c)=P(Japan\mid c)=1/14$; ba xác suất tương ứng trong lớp j là $2/9$. Tài liệu test “Chinese Chinese Chinese Tokyo Japan” được chọn lớp c theo tích có smoothing.

**Gaussian NB:** đặc trưng liên tục theo Gaussian trong từng lớp; học mean/variance của mỗi đặc trưng theo lớp, rồi đưa mật độ Gaussian vào tích likelihood. Dữ liệu structured có thể dùng phân phối khác theo loại thuộc tính.

**Bernoulli NB:** đặc trưng nhị phân biểu thị từ có xuất hiện hay không; phân biệt với word frequency. Complement và Categorical NB được liệt kê ở L2 trang 38; không có diễn giải thuật toán chi tiết đủ để tự coi chúng là phần đã học sâu.

Code trong NB minh họa `CountVectorizer`, `MultinomialNB`, `GaussianNB`, `BernoulliNB`, `fit`, `predict` và các metrics; code là ví dụ, không phải bằng chứng rằng kết quả trong bài của người dùng đã được chạy.

## 3. Decision Tree

Nguồn: DT toàn bộ 47 trang và DTN toàn bộ 51 trang. Không đồng nhất số trang giữa hai bản.

**Mô hình:** internal node kiểm tra thuộc tính/ngưỡng, edge biểu thị kết quả kiểm tra, leaf đưa ra lớp hoặc giá trị. Inference đi từ root đến leaf. Cây có thể biểu diễn bằng các luật IF-THEN và chia không gian thành vùng.

**Học classification:** chọn phép chia, tạo các tập con, rồi đệ quy. ID3 chọn information gain cao nhất:

$$H(D)=-\sum_c p_c\log_2p_c,\qquad
H_A(D)=\sum_v\frac{|D_v|}{|D|}H(D_v),$$
$$\mathrm{Gain}(A)=H(D)-H_A(D).$$

Quy ước $0\log0=0$. Entropy một lớp là 0; hai lớp cân bằng là 1 bit. Trong ví dụ Play Tennis: entropy ban đầu≈0.940; gain Outlook≈0.247, Humidity≈0.152, Windy≈0.048, Temperature≈0.029; chọn Outlook rồi tính tiếp trên từng nhánh. Không tái dùng phân bố toàn bộ dữ liệu để tính node con.

Information gain có thiên lệch với thuộc tính có nhiều giá trị, ví dụ ID. C4.5 dùng gain ratio:

$$\mathrm{SplitInfo}(A)=-\sum_v\frac{|D_v|}{|D|}\log_2\frac{|D_v|}{|D|},\quad
\mathrm{GainRatio}(A)=\frac{\mathrm{Gain}(A)}{\mathrm{SplitInfo}(A)}.$$

Không chia cho SplitInfo bằng 0. CART ở slide dùng Gini và binary splits:

$$\mathrm{Gini}(D)=1-\sum_c p_c^2,\quad
\mathrm{Gini}_A(D)=\sum_v\frac{|D_v|}{|D|}\mathrm{Gini}(D_v).$$

Chọn impurity **sau chia** nhỏ nhất; tương đương reduction lớn nhất với cùng node cha. Continuous feature có thể xét ngưỡng giữa các giá trị kề nhau đã sắp xếp. Nếu triển khai theo ID3/entropy, không được gọi default classifier dùng Gini rồi mô tả nó như cài đặt ID3.

**Overfitting:** hạn chế max depth, tiêu chí dừng, bỏ thuộc tính không phù hợp, thêm dữ liệu hoặc grow-then-prune. Post-pruning thay một subtree bằng leaf khi đánh giá cho thấy subtree kém hơn. Dữ liệu validation dùng chọn mức độ phức tạp; accuracy train đơn thuần không đủ.

**Regression tree trong bài giảng:** lá dự đoán trung bình các đích trong node. Slide mô tả thay information gain bằng standard deviation reduction:

$$S(T)=\sqrt{\frac1{|T|}\sum_{i\in T}(y_i-\bar y_T)^2},\quad
S(T,A)=\sum_v\frac{|T_v|}{|T|}S(T_v),$$
$$\mathrm{SDR}(T,A)=S(T)-S(T,A).$$

Chọn SDR lớn nhất. Ví dụ Hours Played có $\bar y\approx39.8$, standard deviation≈9.32; Outlook được chọn đầu. Các tiêu chí CV dưới 10% và node có tối đa 3 mẫu là tiêu chí **của ví dụ**, không phải luật cho mọi dữ liệu. Code `DecisionTreeRegressor` không mặc nhiên dùng đúng phép giảm độ lệch chuẩn của ví dụ thủ công; phải phân biệt mô tả trên slide và lựa chọn triển khai.

DTN có các ví dụ cập nhật/ảnh viết tay, code classifier và bài tập cuối có đầu vào/đầu ra liên tục. Các chỗ lời mô tả không khớp cây hoặc bảng cần đối chiếu tại `04_SOURCE_CAVEATS.md`.

## 4. Clustering

Nguồn: CL toàn bộ 83 trang.

Clustering là unsupervised: tương tự nhau trong cụm, khác nhau giữa cụm. Chất lượng phụ thuộc metric, biểu diễn, thuật toán và ý nghĩa ứng dụng. Có thể dùng để hiểu dữ liệu, nén, tìm láng giềng hoặc phát hiện outlier. Không coi cluster IDs là class labels đã biết.

### Partitioning

**k-means (trang 13-21):** biết trước $k$, chia thành các nhóm không rỗng hoặc chọn centers ban đầu; lặp gán về tâm gần nhất và cập nhật tâm bằng mean, dừng khi assignment không đổi.

$$E=\sum_{r=1}^k\sum_{x_i\in C_r}\|x_i-\mu_r\|^2,\qquad
\mu_r=\frac1{|C_r|}\sum_{x_i\in C_r}x_i.$$

Slide đánh giá hiệu quả $O(tkn)$ khi số chiều được xem cố định; thường đạt local optimum, phải chọn k, nhạy noise/outliers và không hợp mọi hình dạng non-convex. Bài tập trang 21/32 có 10 điểm A-J, 3 cụm và centers ban đầu A, E, H; yêu cầu ghi tính toán từng iteration.

**k-modes (trang 22-26):** dữ liệu categorical dùng số vị trí khác nhau/Hamming; tâm bằng mode từng thuộc tính. k-prototypes cho mixed numerical-categorical chỉ được nêu ở phần biến thể.

**k-medoids/PAM (trang 27-32):** representative là một điểm dữ liệu thật, khác centroid có thể không phải mẫu thật. Gán tới medoid gần nhất; xem xét thay medoid bằng điểm khác nếu giảm tổng khoảng cách. Ít bị outlier chi phối so với mean nhưng PAM tốn hơn cho dữ liệu lớn. CLARA chạy trên samples; CLARANS randomized resampling. Trang 33 có project phân N câu thành k cụm nhưng không có pipeline embedding hoàn chỉnh trong chính trang đó.

### Hierarchical

Trang 35-41: AGNES agglomerative gộp bottom-up; DIANA chia top-down. Dendrogram biểu diễn quá trình, cắt tại mức mong muốn để lấy cụm. Single link=min khoảng cách giữa hai mẫu của hai cụm; complete=max; average=trung bình các cặp; centroid/medoid dùng khoảng cách giữa representatives. Phương pháp agglomerative không hoàn tác bước gộp và khó mở rộng do chi phí ít nhất bậc hai theo slide.

$$\mu_C=\frac1N\sum_i x_i,\quad
R_C=\sqrt{\frac1N\sum_i\|x_i-\mu_C\|^2},\quad
D_C=\sqrt{\frac1{N(N-1)}\sum_{i\ne j}\|x_i-x_j\|^2}.$$

Trang 42-46: **BIRCH** nén incremental bằng CF-tree. $CF=(N,LS,SS)$ lưu số điểm, tổng điểm và tổng bình phương (slide dùng theo từng tọa độ). CF ở parent là tổng CF children; branching factor và threshold giới hạn cấu trúc. Có thể scan nhanh nhưng chỉ numeric, nhạy insertion order và thiên về cụm dạng cầu.

Trang 47-49: **CHAMELEON** tạo sparse kNN graph, chia graph thành subclusters rồi merge theo relative interconnectivity và relative closeness. Trang 50-52: probabilistic hierarchical clustering dùng generative distributions, MLE cho từng cụm và likelihood ratio của việc gộp; đây là phần trình bày khái niệm và thuật toán, chưa có code thực nghiệm trong thư mục.

### Density-based

Trang 54-59: **DBSCAN** dùng Eps và MinPts:

$$N_\varepsilon(p)=\{q\in D:d(p,q)\le\varepsilon\}.$$

Core point có đủ MinPts trong neighborhood; border gần core nhưng không đủ mật độ; noise/outlier không thuộc cụm. Theo định nghĩa tập trong slide, một điểm ở trong neighborhood của chính nó. Direct density-reachable từ q sang p cần q là core và p trong neighborhood của q. Density-reachable là chuỗi nối; density-connected cần một điểm mà cả hai reachable từ đó. Mở rộng cụm qua core, có thể tạo cụm hình dạng bất kỳ; nhạy với Eps/MinPts. Không dùng bước lan truyền từ border như thể border cũng là core.

Trang 60-63: **OPTICS** tạo thứ tự chứa cấu trúc mật độ trên nhiều mức tham số. Core-distance là bán kính nhỏ nhất để thành core; reachability-distance từ o tới p là $\max(\mathrm{core\mbox{-}distance}(o),d(o,p))$. Các vùng thấp trên reachability plot minh họa cụm.

Trang 64-67: **DENCLUE** tính tổng influence functions (ví dụ Gaussian), tìm density attractors là cực đại cục bộ và liên kết attractors qua các đường mật độ cao; có thể xử lý noise nhưng có nhiều tham số.

### Grid-based và đánh giá

Trang 69-72: **STING** chia thành grid cells nhiều cấp, lưu count/mean/standard deviation/min/max/distribution, xử lý từ trên xuống; biên cell chữ nhật hạn chế dạng biên cụm. WaveCluster được giới thiệu bằng tên/phương pháp wavelet.

Trang 73-76: **CLIQUE** tìm dense rectangular units trong subspaces chiều cao, dùng nguyên lý Apriori, liên kết units và tạo mô tả cụm; vừa grid-based vừa density-based/subspace. Slide nêu tính mở rộng và tradeoff độ chính xác với đơn giản.

Trang 78-81: đánh giá clustering tendency bằng Hopkins; slide dùng $H=\sum_i y_i/(\sum_i x_i+\sum_i y_i)$ với mô tả khoảng cách tương ứng, H≈0.5 cho phân bố đều và gần 0 cho dữ liệu clustered theo quy ước slide. Phần mô tả lấy mẫu còn cần đọc kỹ nếu thực sự phải cài đặt. Chọn k có elbow, cross-validation và heuristic trên số mẫu; không xem heuristic là nghiệm chắc chắn.

Extrinsic có ground truth, ví dụ BCubed precision/recall; intrinsic không có ground truth, xét compactness/separation, ví dụ silhouette. Slide chỉ nêu tên silhouette và BCubed, **không đưa derivation đầy đủ công thức**. Bốn tiêu chí extrinsic: homogeneity, completeness, rag bag và small cluster preservation. EM, SOM, COBWEB, p-cluster, constraint/link-based clustering cũng xuất hiện trong bản phân loại nhưng không được dạy đầy đủ từng thuật toán.

## 5. Support Vector Machines

Nguồn: SVM trang 3-34.

Classification nhị phân với $y_i\in\{-1,+1\}$; boundary $w^Tx+b=0$, prediction theo dấu. Support vectors là các điểm quyết định margin. Hai mặt chuẩn hóa $w^Tx+b=\pm1$ có khoảng cách $2/\|w\|$.

**Hard margin:**

$$\min_{w,b}\frac12\|w\|^2\quad\text{s.t.}\quad y_i(w^Tx_i+b)\ge1.$$

**Soft margin:**

$$\min_{w,b,\xi}\frac12\|w\|^2+C\sum_i\xi_i,\quad
y_i(w^Tx_i+b)\ge1-\xi_i,\quad\xi_i\ge0.$$

Soft margin cho phép vi phạm và cân bằng độ rộng margin với penalty. Không giả định dữ liệu thực đều linearly separable.

**Kernel trick:** $K(x,z)=\langle\phi(x),\phi(z)\rangle$; tính inner product trong feature space mà không cần tọa độ map tường minh. Ví dụ $\phi(x_1,x_2)=(x_1^2,x_2^2,\sqrt2x_1x_2)$ cho $K(x,z)=(x^Tz)^2$. Một kernel có thể có nhiều feature maps.

Trang 25 liệt kê linear $x^Tz$, polynomial $(\gamma x^Tz+r)^d$, RBF $\exp(-\gamma\|x-z\|^2)$, sigmoid $\tanh(\gamma x^Tz+r)$. Slide nhắc điều kiện tồn tại map/Mercer; không suy ra mọi lựa chọn tham số đều cho kernel hợp lệ. Trang 26-28 minh họa dạng boundary và ảnh hưởng gamma/polynomial degree.

**Học dual soft margin và inference:**

$$\max_\alpha\left[\sum_i\alpha_i-\frac12\sum_{i,j}\alpha_i\alpha_jy_iy_jK(x_i,x_j)\right],$$
$$0\le\alpha_i\le C,\qquad\sum_i\alpha_iy_i=0,$$
$$\hat y=\operatorname{sign}\left(\sum_i\alpha_iy_iK(x_i,x)+b\right).$$

Với support vector có $0<\alpha_i<C$, $b=y_i-\sum_j\alpha_jy_jK(x_j,x_i)$ theo slide. Hard-margin dual không có upper bound C (trang 32). Trang 34 giới thiệu SMO tối ưu một cặp hệ số trong khi giữ các hệ số khác cố định; công thức minh họa chưa bao trùm box constraints/solver hoàn chỉnh. Trang 35 chỉ có mục summary bỏ trống; không có nội dung bị giấu cần suy đoán.

## 6. Linear Regression và Gradient Descent

Nguồn: LR trang 6-25.

$$\hat y=w_0+w_1x\quad\text{(một biến)},\qquad
\hat y_i=w_0+\sum_{j=1}^d w_jx_{ij}\quad\text{(nhiều biến)}.$$

Đặt $x_{i0}=1$ khi gộp intercept vào vector. Học trọng số bằng loss:

$$J(w)=\frac1{2N}\sum_i(\hat y_i-y_i)^2,\qquad
\frac{\partial J}{\partial w_j}=\frac1N\sum_i(\hat y_i-y_i)x_{ij}.$$

Gradient descent:

$$w_j\leftarrow w_j-\eta\frac{\partial J}{\partial w_j}.$$

Tính các gradient tại cùng bộ trọng số trước khi cập nhật; LR trang 24 làm điều này bằng trả cả hai gradient rồi cập nhật. Learning rate lớn có thể vượt quá điểm tối ưu; nhỏ làm học chậm. Mô hình nhạy với outliers do squared error (trang 20). Slide có bài tập giá nhà nhiều biến: trước tiên lập công thức rồi mới cài Python (trang 22).

Dạng ma trận với hàng là mẫu: $X\in\mathbb R^{N\times(d+1)}$, $w\in\mathbb R^{d+1}$, $\hat y=Xw$.

$$\nabla J=\frac1N X^T(Xw-y),\qquad X^TXw=X^Ty.$$

Trang 25 viết loss không chia N nhưng cho cùng normal equation. Từ phương trình này, **nếu $X^TX$ khả nghịch**, suy ra $w=(X^TX)^{-1}X^Ty$. Không tự suy ra ma trận luôn khả nghịch; nếu đề cần cách khác phải xác định phương pháp trong phạm vi được phép. Phần ký hiệu cuối slide có lỗi/thiếu nhất quán, không chép máy móc.

## 7. Perceptron và Logistic Regression

Nguồn: LOG trang 4-43.

### Perceptron

Biological neuron là trực giác cho inputs, weighted sum, bias và activation. Perceptron nhị phân:

$$z=w^Tx+b,\qquad\hat y=\operatorname{sign}(z).$$

Slide dùng nhãn ±1 và tập $M$ gồm các mẫu phân loại sai. Loss surrogate khả vi theo từng vùng:

$$J(w)=-\sum_{i\in M}y_iw^Tx_i,\qquad
\nabla_w J_i=-y_ix_i,\qquad w\leftarrow w+\eta y_ix_i.$$

Bias có thể gộp bằng input hằng 1. Không dùng công thức này với labels 0/1 mà không đổi quy ước. Các slide không cung cấp đầy đủ mọi quy tắc khi score=0 hoặc tiêu chí dừng cho dữ liệu không tách tuyến tính; cần xác định khi cài đặt.

Trang 8-9 liệt kê step, sign, identity, sigmoid, tanh, arctan, ReLU, PReLU, ELU và softplus ở dạng đồ thị/bảng. Không mặc nhiên chọn thêm activation chỉ vì có tên trong bảng.

### Information theory và logistic

Entropy, KL divergence và cross entropy (trang 22-28):

$$H(p)=-\sum_x p(x)\log p(x),\quad
D_{KL}(p\|q)=\sum_x p(x)\log\frac{p(x)}{q(x)},$$
$$H(p,q)=-\sum_xp(x)\log q(x)=H(p)+D_{KL}(p\|q).$$

Phải nhất quán cơ số log; entropy của cây thường log2, derivation logistic dùng natural log.

Logistic regression là mô hình classification dự đoán xác suất, khác linear regression có output không bị giới hạn. Ví dụ pass/fail theo hours studying ở trang 16-21 giải thích nhu cầu output giữa 0 và 1.

$$p_i=\sigma(w^Tx_i+b),\qquad\sigma(z)=\frac1{1+e^{-z}},\qquad
\sigma'(z)=\sigma(z)(1-\sigma(z)).$$

$$P(y=1\mid x)=p,\qquad P(y=0\mid x)=1-p,\qquad
\log\frac{p}{1-p}=w^Tx+b.$$

Loss binary cross entropy với labels 0/1:

$$J(w)=-\frac1N\sum_i[y_i\log p_i+(1-y_i)\log(1-p_i)],$$
$$\frac{\partial J}{\partial w_j}=\frac1N\sum_i(p_i-y_i)x_{ij},\qquad
w_j\leftarrow w_j-\eta\frac1N\sum_i(p_i-y_i)x_{ij}.$$

Trang 36-38 nối minimization cross entropy với maximization log-likelihood Bernoulli. Công thức gradient có hình thức giống linear regression nhưng prediction và loss khác nhau. Khi trả nhãn phải công bố threshold; khi đánh giá ROC dùng scores/probabilities.

LOG trang 42 có hệ số $1/N$ ở gradient; trang 43 thiếu hệ số này trong update dù loss đã lấy trung bình. Ghi chú này dùng gradient của trang 42 để giữ nhất quán. Khi cài tính toán cần tránh overflow của exponential và log(0); đây là yêu cầu số học của công thức, không phải lý do thêm một mô hình khác.
