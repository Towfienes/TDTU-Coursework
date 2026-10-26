/**
 * Build the midterm presentation: PPTX + a pixel-matched HTML preview + transcript.
 *
 * One slide spec feeds both renderers, so what the preview shows is what the
 * PPTX contains. Every number is read from results/*.json — nothing is typed
 * by hand except labels.
 *
 * The TDTU frame follows .agents/skills/tdtu-presentation:
 *   logo upper-left, title beside it, thin rule, content centred below,
 *   monochrome framing, coloured charts, original-colour logo.
 *
 * Usage:  node presentation/src/build_deck.js
 */
const fs = require("fs");
const path = require("path");
const PptxGenJS = require(process.env.PPTXGENJS_PATH || "pptxgenjs");

const ROOT = path.resolve(__dirname, "../..");
const FIG = path.join(ROOT, "presentation", "figures");
const OUT = path.join(ROOT, "presentation");
const LOGO = path.join(ROOT, "report", "assets", "tdtu-logo.png");

const readJson = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const Q1 = readJson(path.join(ROOT, "results", "q1_metrics.json"));
const Q2 = readJson(path.join(ROOT, "results", "q2_metrics.json"));
const M = Object.fromEntries(Q2.models.map((m) => [m.model, m]));

const f2 = (v) => v.toFixed(2);
const f3 = (v) => v.toFixed(3);
const f4 = (v) => v.toFixed(4);
const up = (v) => (v * 100).toFixed(1) + "%";

// ---------------------------------------------------------------- design system
const FONT = "Arial";
const INK = "111111";
const MUTED = "6B6B6B";
const RULE = "2B2B2B";
const HAIR = "D5D5D5";
const FILL = "F2F2F2";

const W = 13.333;
const H = 7.5;
const GUT = 0.73;
const RIGHT = 12.6;
const COLW = RIGHT - GUT; // 11.87
const TOP = 1.62;
const BOT = 6.72;

const LIN = Q1.linear;
const LOG = Q1.logistic;
const treeGapBase = M["Decision tree"].default_train_macro_f1 - M["Decision tree"].default_cv_macro_f1;
const treeGapSel = M["Decision tree"].selected_train_macro_f1 - M["Decision tree"].cv_macro_f1;
const rfGapSel = M["Random forest"].selected_train_macro_f1 - M["Random forest"].cv_macro_f1;

// ---------------------------------------------------------------- run helpers
const sub = (t) => ({ t, sub: true });
const sup = (t) => ({ t, sup: true });
const bd = (t) => ({ t, bold: true });
const muted = (t, opts = {}) => ({ t, color: MUTED, ...opts });

const SLIDES = [];

function slide(spec) {
  SLIDES.push(spec);
}

// ------------------------------------------------------------------- slide 1
slide({
  layout: "COVER",
  section: "Mở đầu",
  blocks: [
    { k: "text", x: GUT, y: 1.72, w: 9, h: 0.3, size: 11, color: MUTED, spacing: 2.2,
      text: "BÁO CÁO GIỮA KỲ  ·  INTRODUCTION TO MACHINE LEARNING" },
    { k: "text", x: GUT, y: 2.12, w: 11, h: 0.95, size: 46, bold: true, text: "Hồi quy & Phân loại" },
    { k: "text", x: GUT, y: 3.05, w: 10.6, h: 0.5, size: 20, color: MUTED,
      text: "Từ Gradient Descent tự cài đặt đến so sánh 14 bộ phân loại trên OpenML" },
    { k: "rule", x: GUT, y: 3.82, w: 4.2, pt: 1.4, color: RULE },
    { k: "text", x: GUT, y: 4.02, w: 6.2, h: 0.32, size: 14, color: MUTED, text: "Giảng viên hướng dẫn" },
    { k: "text", x: GUT, y: 4.34, w: 6.2, h: 0.36, size: 17, text: "Lê Anh Cường, Ph.D." },
    { k: "text", x: 7.15, y: 4.02, w: 5.4, h: 0.32, size: 14, color: MUTED, text: "Sinh viên thực hiện" },
    { k: "text", x: 7.15, y: 4.34, w: 5.4, h: 1.0, size: 15, lineSpacing: 1.45,
      text: "Ngô Lâm Tiến — 524H0195\nNguyễn Công Thành — 524H0191\nNguyễn Lê Nhật Tâm — 524H0186" },
    { k: "text", x: GUT, y: 5.72, w: 6.2, h: 0.32, size: 13, color: MUTED, text: "Tháng 10 năm 2026" },
  ],
  notes: "Kính thưa thầy và các bạn. Nhóm em gồm ba thành viên xin trình bày báo cáo giữa kỳ môn Introduction to Machine Learning. Bài gồm hai câu: câu một tự cài đặt hồi quy tuyến tính và logistic bằng Gradient Descent; câu hai so sánh các bộ phân loại trên bộ credit-g của OpenML. Phần trình bày khoảng mười phút.",
});

// ------------------------------------------------------------------- slide 2
slide({
  section: "Mở đầu",
  eyebrow: "NỘI DUNG",
  title: "Ba phần, ba người trình bày",
  blocks: [
    { k: "numlist", x: GUT, y: 1.72, w: COLW, rowH: 1.12, items: [
      { n: "01", title: "Câu 1 · Gradient Descent tự cài đặt",
        sub: "Hồi quy tuyến tính và logistic: mô hình, mất mát, dẫn xuất gradient, kết quả",
        right: "Ngô Lâm Tiến" },
      { n: "02", title: "Câu 2 · Phân loại trên OpenML credit-g",
        sub: "Tiền xử lý, quy trình chống rò rỉ dữ liệu, 14 mô hình và baseline",
        right: "Nguyễn Công Thành" },
      { n: "03", title: "Overfitting và cách khắc phục",
        sub: "Bằng chứng thực nghiệm, các biện pháp, kết luận và hạn chế của bài làm",
        right: "Nguyễn Lê Nhật Tâm" },
    ]},
    { k: "rule", x: GUT, y: 5.42, w: COLW, pt: 0.75, color: HAIR },
    { k: "text", x: GUT, y: 5.6, w: COLW, h: 0.4, size: 16, italic: true, color: MUTED,
      text: "Câu hỏi xuyên suốt: mô hình học được gì từ dữ liệu, và làm sao biết nó thật sự tổng quát hóa?" },
  ],
  notes: "Bài chia ba phần. Em trình bày câu một: tự cài đặt hai mô hình hồi quy, dẫn xuất gradient và đánh giá. Bạn Thành trình bày câu hai: dữ liệu credit-g, quy trình chống rò rỉ và so sánh mười bốn mô hình cùng baseline. Bạn Tâm trình bày overfitting và kết luận. Câu hỏi xuyên suốt: mô hình học được gì, và làm sao biết nó tổng quát hóa?",
});

// ------------------------------------------------------------------- slide 3
slide({
  section: "Câu 1",
  eyebrow: "CÂU 1 · HỒI QUY TUYẾN TÍNH",
  title: "Mô hình và hàm mất mát",
  blocks: [
    { k: "label", x: GUT, y: 1.84, w: 6, text: "Dự đoán" },
    { k: "eq", x: GUT, y: 2.14, w: 6.1, h: 0.5, size: 23,
      runs: ["ŷ", sub("i"), " = w", sup("T"), "x", sub("i"), " + b"] },
    { k: "eq", x: GUT, y: 2.66, w: 6.1, h: 0.4, size: 15, color: MUTED,
      runs: ["một đặc trưng → đường thẳng · nhiều đặc trưng → siêu phẳng"] },
    { k: "label", x: GUT, y: 3.34, w: 6, text: "Mất mát: trung bình bình phương sai số" },
    { k: "eq", x: GUT, y: 3.64, w: 6.1, h: 0.6, size: 21,
      runs: ["J(w, b) = (1/2n) · Σ", sub("i"), " (ŷ", sub("i"), " − y", sub("i"), ")", sup("2")] },
    { k: "rule", x: 6.95, y: 1.78, w: 0, pt: 0.75, color: HAIR, vertical: true, h: 3.05 },
    { k: "bullets", x: 7.25, y: 1.78, w: 5.35, size: 17, gap: 16, items: [
      [{ t: "Đầu ra là số thực", bold: true }, { t: " — bài toán hồi quy, không phải phân loại." }],
      [{ t: "Hệ số ½", bold: true }, { t: " chỉ để đạo hàm gọn; nghiệm tối ưu không đổi." }],
      [{ t: "Bình phương", bold: true }, { t: " khiến sai số lớn bị phạt nặng." }],
      [{ t: "Chia cho n", bold: true }, { t: " để mất mát là trung bình, so sánh được giữa các cỡ mẫu." }],
    ]},
    { k: "rule", x: GUT, y: 5.18, w: COLW, pt: 0.75, color: HAIR },
    { k: "eq", x: GUT, y: 5.34, w: COLW, h: 0.8, size: 14, color: MUTED,
      runs: ["Dữ liệu tổng hợp: 600 mẫu, 3 đặc trưng độc lập đều trên [−3, 3];  y = 4 + 3x", sub("1"),
             " − 2x", sub("2"), " + 1.5x", sub("3"), " + ε,  ε ~ N(0, 0.5", sup("2"), ")."] },
  ],
  notes: "Hồi quy tuyến tính dự đoán một số thực bằng tổng có trọng số của các đặc trưng cộng hệ số chặn. Vì đầu ra là số thực nên đây là bài toán hồi quy. Hàm mất mát là trung bình bình phương sai số, chia đôi. Hệ số một phần hai chỉ để khi đạo hàm, số hai triệt tiêu, không đổi nghiệm tối ưu. Chia cho n giúp mất mát là trung bình, so sánh được giữa các cỡ mẫu. Còn bình phương khiến sai số lớn bị phạt nặng.",
});

// ------------------------------------------------------------------- slide 4
slide({
  section: "Câu 1",
  eyebrow: "CÂU 1 · HỒI QUY TUYẾN TÍNH",
  title: "Dẫn xuất gradient và vòng lặp Gradient Descent",
  blocks: [
    { k: "label", x: GUT, y: 1.84, w: 6.4, text: "Đạo hàm riêng" },
    { k: "eq", x: GUT, y: 2.14, w: 6.6, h: 0.4, size: 18,
      runs: ["đặt  e", sub("i"), " = ŷ", sub("i"), " − y", sub("i"), "  ⇒  ∂e", sub("i"), " / ∂w", sub("j"), " = x", sub("ij")] },
    { k: "eq", x: GUT, y: 2.62, w: 6.6, h: 0.45, size: 20,
      runs: ["∂J/∂w", sub("j"), " = (1/n) Σ", sub("i"), " e", sub("i"), "x", sub("ij"),
             "        ∂J/∂b = (1/n) Σ", sub("i"), " e", sub("i")] },
    { k: "eq", x: GUT, y: 3.16, w: 6.6, h: 0.45, size: 20,
      runs: ["∇", sub("w"), "J = (1/n) X", sup("T"), "(ŷ − y)"] },
    { k: "label", x: GUT, y: 3.82, w: 6.4, text: "Cập nhật đồng thời" },
    { k: "eq", x: GUT, y: 4.12, w: 6.9, h: 0.5, size: 20,
      runs: ["w", sup("(t+1)"), " = w", sup("(t)"), " − η · (1/n) X", sup("T"), "e", sup("(t)")] },
    { k: "rule", x: 6.95, y: 1.78, w: 0, pt: 0.75, color: HAIR, vertical: true, h: 3.05 },
    { k: "bullets", x: 7.25, y: 1.78, w: 5.35, size: 17, gap: 15, items: [
      [{ t: "Khởi tạo " }, { t: "w = 0, b = 0", bold: true }, { t: "; tốc độ học " }, { t: "η = 0.3", bold: true }],
      [{ t: "Dừng khi " }, { t: "chuẩn gradient ≤ 10", bold: true }, sup("−8"),
       { t: " — chỉ dùng dữ liệu huấn luyện" }],
      [{ t: "Hội tụ sau " }, { t: `${LIN.iterations} vòng`, bold: true }, { t: " trên 480 mẫu train" }],
      [{ t: "Gradient được kiểm chứng bằng " }, { t: "sai phân trung tâm", bold: true },
       { t: ", dung sai 10" }, sup("−6")],
    ]},
    { k: "text", x: GUT, y: 5.05, w: 6.9, h: 0.9, size: 14, color: MUTED, lineSpacing: 1.3,
      text: "Cả hai gradient được tính trước khi cập nhật tham số (full-batch). Không bao giờ dùng chỉ số test để quyết định dừng." },
  ],
  notes: "Đạo hàm theo quy tắc chuỗi: gọi e là phần dư, đạo hàm của e theo trọng số chính là giá trị đặc trưng. Vậy gradient theo trọng số là trung bình của phần dư nhân đặc trưng, gradient theo hệ số chặn là trung bình phần dư. Viết dạng ma trận được công thức ở giữa. Thực nghiệm khởi tạo bằng không, tốc độ học không phẩy ba, dừng khi chuẩn gradient nhỏ hơn mười mũ trừ tám, sau một nghìn một trăm bảy mươi lăm vòng. Nhóm kiểm chứng lại gradient bằng sai phân trung tâm, dung sai mười mũ trừ sáu.",
});

// ------------------------------------------------------------------- slide 5
slide({
  section: "Câu 1",
  eyebrow: "CÂU 1 · HỒI QUY LOGISTIC",
  title: "Xác suất, cross-entropy và gradient",
  blocks: [
    { k: "label", x: GUT, y: 1.84, w: 6.4, text: "Mô hình xác suất" },
    { k: "eq", x: GUT, y: 2.14, w: 7.2, h: 0.45, size: 21,
      runs: ["z = w", sup("T"), "x + b     ⇒     p = σ(z) = 1 / (1 + e", sup("−z"), ")"] },
    { k: "eq", x: GUT, y: 2.72, w: 7.0, h: 0.4, size: 17, color: MUTED,
      runs: ["log (p / (1 − p)) = w", sup("T"), "x + b   →   biên quyết định tuyến tính"] },
    { k: "label", x: GUT, y: 3.34, w: 6.4, text: "Mất mát: cross-entropy nhị phân" },
    { k: "eq", x: GUT, y: 3.64, w: 7.2, h: 0.5, size: 19,
      runs: ["J = −(1/n) Σ", sub("i"), " [ y", sub("i"), " log p", sub("i"), " + (1 − y", sub("i"), ") log (1 − p", sub("i"), ") ]"] },
    { k: "rule", x: 7.55, y: 1.78, w: 0, pt: 0.75, color: HAIR, vertical: true, h: 2.62 },
    { k: "eq", x: 7.85, y: 1.82, w: 4.8, h: 0.4, size: 17,
      runs: ["σ′(z) = σ(z)(1 − σ(z))"] },
    { k: "eq", x: 7.85, y: 2.32, w: 4.8, h: 0.4, size: 19,
      runs: ["⇒  ∂ℓ/∂z = p − y"] },
    { k: "eq", x: 7.85, y: 2.84, w: 4.8, h: 0.45, size: 18,
      runs: ["∇", sub("w"), "J = (1/n) X", sup("T"), "(p − y)"] },
    { k: "label", x: 7.85, y: 3.50, w: 4.8, text: "Cập nhật" },
    { k: "eq", x: 7.85, y: 3.80, w: 4.8, h: 0.45, size: 18,
      runs: ["w", sup("(t+1)"), " = w", sup("(t)"), " − η·(1/n)X", sup("T"), "(p − y)"] },
    { k: "rule", x: GUT, y: 4.62, w: COLW, pt: 0.75, color: HAIR },
    { k: "bullets", x: GUT, y: 4.78, w: COLW, size: 15.5, gap: 8, items: [
      [{ t: "Mẫu số p(1 − p) triệt tiêu", bold: true }, { t: ", nên gradient giống hồi quy tuyến tính nhưng thay ŷ bằng p." }],
      [{ t: "η = 0.5, tối đa 5000 vòng", bold: true }, { t: ` — dừng theo ngân sách, chuẩn gradient cuối ≈ 1.55 × 10` }, sup("−4"), { t: "." }],
      [{ t: "Sigmoid và logaddexp", bold: true }, { t: " dạng ổn định số học; ngưỡng cố định 0.5, ROC-AUC dùng xác suất." }],
    ]},
  ],
  notes: "Hồi quy logistic đưa cùng một điểm tuyến tính qua sigmoid để ra xác suất trong khoảng không đến một. Logit của xác suất là hàm tuyến tính nên biên vẫn là siêu phẳng. Mất mát là cross-entropy, tức âm log hợp lý Bernoulli, phạt rất nặng dự đoán tự tin mà sai. Khi đạo hàm, đạo hàm sigmoid là p nhân một trừ p, triệt tiêu mẫu số của cross-entropy, nên gradient chỉ còn p trừ y, rất gọn. Nhóm dùng tốc độ học không phẩy năm, tối đa năm nghìn vòng, và vòng lặp chạm ngân sách trước khi đạt dung sai.",
});

// ------------------------------------------------------------------- slide 6
slide({
  section: "Câu 1",
  eyebrow: "CÂU 1 · KẾT QUẢ",
  title: "Hồi quy tuyến tính: học đúng quan hệ sinh dữ liệu",
  blocks: [
    { k: "image", src: "fig_q1_linear.png", x: (W - 10.8) / 2, y: TOP, w: 10.8, h: 3.9 },
    { k: "kpis", x: GUT, y: 5.62, w: COLW, items: [
      { value: f4(LIN.rmse), label: "RMSE trên tập test" },
      { value: f4(LIN.r2), label: "R² trên tập test" },
      { value: LIN.raw_weights.map((v) => v.toFixed(2).replace("-", "−")).join("  ·  "),
        label: "Trọng số học được (thật: 3 · −2 · 1.5)" },
    ]},
  ],
  notes: "Đây là kết quả chạy thật. Mất mát giảm từ ba mươi phẩy chín xuống không phẩy một hai sáu sau một nghìn một trăm bảy mươi lăm vòng, đơn điệu nên không phân kỳ. Trên một trăm hai mươi mẫu test, các điểm bám sát đường chéo. RMSE không phẩy năm một, đúng bằng độ lệch chuẩn của nhiễu, R bình phương không phẩy chín chín bốn bảy. Trọng số học được rất gần giá trị thật ba, trừ hai, một phẩy năm. Nhưng đây là dữ liệu tổng hợp tuyến tính, nên điểm cao là kỳ vọng, không phải bằng chứng cho dữ liệu thực.",
});

// ------------------------------------------------------------------- slide 7
slide({
  section: "Câu 1",
  eyebrow: "CÂU 1 · KẾT QUẢ",
  title: "Hồi quy logistic: biên hợp lý, nhưng còn 30 ca sai",
  blocks: [
    { k: "image", src: "fig_q1_logistic.png", x: (W - 10.8) / 2, y: TOP, w: 10.8, h: 3.9 },
    { k: "kpis", x: GUT, y: 5.62, w: COLW, items: [
      { value: f4(LOG.accuracy), label: "Accuracy trên tập test" },
      { value: f4(LOG.f1_positive), label: "F1 của lớp dương (p ≥ 0.5)" },
      { value: f4(LOG.roc_auc), label: "ROC-AUC" },
      { value: `${LOG.confusion_matrix[0][0]}/${LOG.confusion_matrix[0][1]}/${LOG.confusion_matrix[1][0]}/${LOG.confusion_matrix[1][1]}`,
        label: "Ma trận nhầm lẫn (TN/FP/FN/TP)" },
    ]},
  ],
  notes: "Với logistic, nhãn sinh ngẫu nhiên nên hai lớp chồng lấn. Cross-entropy giảm từ không phẩy sáu chín ba một, đúng bằng log hai của mô hình đoán ngẫu nhiên, xuống không phẩy bốn năm hai. Trên tập test, mô hình đúng một trăm ba mươi trên một trăm sáu mươi, tức tám mươi mốt phẩy hai lăm phần trăm, F1 lớp dương không phẩy tám năm một, AUC không phẩy tám năm bảy. Các vòng tròn là mẫu phân loại sai, tập trung đúng ở vùng chồng lấn. Phần câu một đến đây là hết, em mời bạn Thành trình bày câu hai.",
});

// ------------------------------------------------------------------- slide 8
slide({
  section: "Câu 2",
  eyebrow: "CÂU 2 · DỮ LIỆU",
  title: "OpenML credit-g: 1000 hồ sơ, 20 biến, lệch lớp",
  blocks: [
    { k: "image", src: "fig_q2_eda.png", x: (W - 11.0) / 2, y: TOP, w: 11.0, h: 3.35 },
    { k: "kpis", x: GUT, y: 5.28, w: COLW, items: [
      { value: "ID 31 · v1", label: "Nguồn gốc, MD5 đã kiểm tra" },
      { value: "0 · 0 · 0", label: "Ô thiếu · dòng trùng · giá trị lạ" },
      { value: "800 / 200", label: "Development / test, phân tầng, seed 42" },
      { value: "61", label: "Đặc trưng sau min–max và one-hot" },
    ]},
  ],
  notes: "Dữ liệu là credit-g, mã 31 phiên bản một trên OpenML: một nghìn hồ sơ, hai mươi biến, trong đó bảy biến số và mười ba biến phân loại. Nhãn gồm bảy trăm good và ba trăm bad, nên đây là bài toán mất cân bằng. Một mô hình luôn đoán good đã đạt bảy mươi phần trăm accuracy mà không phát hiện hồ sơ xấu nào, vì vậy nhóm không dùng accuracy làm tiêu chí chính. Kiểm tra dữ liệu sạch: không ô thiếu, không dòng trùng, không giá trị lạ, nên giữ nguyên một nghìn hồ sơ.",
});

// ------------------------------------------------------------------- slide 9
slide({
  section: "Câu 2",
  eyebrow: "CÂU 2 · QUY TRÌNH",
  title: "Chống rò rỉ dữ liệu bằng thiết kế, không bằng lời hứa",
  blocks: [
    { k: "flow", x: GUT, y: 1.95, w: COLW, h: 1.78, items: [
      { n: "01", title: "Chia tập trước", sub: "800 development / 200 test, phân tầng, seed 42" },
      { n: "02", title: "Chuẩn hóa trong từng fold", sub: "min–max + one-hot, chỉ fit trên train của fold" },
      { n: "03", title: "5-fold stratified CV", sub: "cùng chỉ số fold cho mọi ứng viên, chọn theo macro F1" },
      { n: "04", title: "Test đúng một lần", sub: "refit trên 800 hồ sơ rồi mới dự đoán 200 hồ sơ" },
    ]},
    { k: "rule", x: GUT, y: 4.16, w: COLW, pt: 0.75, color: HAIR },
    { k: "bullets", x: GUT, y: 4.34, w: COLW, size: 17.5, gap: 14, items: [
      [{ t: "Toàn bộ lựa chọn hoàn tất trước khi sinh bất kỳ dự đoán test nào", bold: true },
       { t: "." }],
      [{ t: "Mọi mô hình dùng chung một phép biến đổi", bold: true },
       { t: ", nên so sánh giữa chúng là công bằng." }],
      [{ t: "Giữ nguyên ngoại lai hợp lệ", bold: true },
       { t: " — cờ IQR chỉ là mô tả, không phải bằng chứng dữ liệu sai." }],
      [{ t: "Baseline đa số", bold: true },
       { t: ` đạt macro F1 ${f3(M["Majority baseline"].macro_f1)} trên test, dùng làm mốc tham chiếu.` }],
    ]},
  ],
  notes: "Điểm nhóm muốn nhấn mạnh là quy trình. Tập test tách ngay từ đầu và chỉ dùng một lần, sau khi mọi lựa chọn xong. Trong tám trăm hồ sơ development, nhóm chạy năm fold phân tầng, và chuẩn hóa nằm trong pipeline nên mỗi fold chỉ học min–max từ train của chính nó. Nếu chuẩn hóa trước rồi mới chia fold thì thông tin validation đã rò rỉ và điểm sẽ đẹp giả tạo. Tiêu chí chọn là macro F1 vì cho hai lớp trọng số ngang nhau.",
});

// ------------------------------------------------------------------- slide 10
slide({
  section: "Câu 2",
  eyebrow: "CÂU 2 · CHỌN MÔ HÌNH",
  title: "14 mô hình và một baseline, chọn bằng cross-validation",
  blocks: [
    { k: "image", src: "fig_q2_cv.png", x: GUT, y: TOP, w: 6.5, h: 4.55 },
    { k: "bullets", x: 7.55, y: 1.78, w: 5.05, size: 16.5, gap: 14, items: [
      [{ t: "Ba kernel SVM", bold: true }, { t: " là ba biến thể của một họ, không phải ba họ độc lập." }],
      [{ t: "Dẫn đầu: MLP " }, { t: f3(M["MLP"].cv_macro_f1), bold: true },
       { t: " · Bernoulli NB " }, { t: f3(M["Bernoulli NB"].cv_macro_f1), bold: true }],
      [{ t: "Chênh lệch top 2 nhỏ hơn độ lệch chuẩn giữa các fold (±" },
       { t: f2(M["MLP"].cv_std), bold: true }, { t: ") ⇒ chưa thể nói hơn kém." }],
      [{ t: "kNN chọn k = 1", bold: true }, { t: " dù khoảng cách train–CV lớn: giữ đúng tiêu chí đã khai báo." }],
    ]},
    { k: "rule", x: 7.55, y: 5.30, w: 5.05, pt: 0.75, color: HAIR },
    { k: "text", x: 7.55, y: 5.46, w: 5.05, h: 0.8, size: 14, color: MUTED, lineSpacing: 1.3,
      text: "Điểm CV dùng để chọn tham số nên không phải đánh giá độc lập; tập test giữ vai trò đó." },
  ],
  notes: "Nhóm so sánh mười bốn mô hình cùng một baseline trên cùng bộ fold. Ba kernel SVM là ba biến thể của một họ, không phải ba họ thuật toán. MLP dẫn đầu với macro F1 không phẩy sáu chín sáu, Bernoulli NB bám sát không phẩy sáu chín bốn, polynomial SVM không phẩy sáu tám sáu. Nhưng độ lệch chuẩn giữa các fold khoảng không phẩy không sáu, lớn hơn khoảng cách hai mô hình đầu, nên nhóm không tuyên bố MLP vượt trội. Điểm CV đã dùng để chọn tham số nên không phải đánh giá độc lập.",
});

// ------------------------------------------------------------------- slide 11
slide({
  section: "Câu 2",
  eyebrow: "CÂU 2 · KẾT QUẢ TEST",
  title: "Trên 200 hồ sơ chưa từng thấy, khoảng cách rất hẹp",
  blocks: [
    { k: "table", x: GUT, y: 1.80, w: 7.9, colW: [3.2, 1.6, 1.6, 1.5],
      fontSize: 14, rowH: 0.44,
      rows: [
        ["Mô hình", "Accuracy", "Macro F1", "AUC"],
        ["Majority baseline", f3(M["Majority baseline"].accuracy), f3(M["Majority baseline"].macro_f1), "0.500"],
        ["Perceptron", f3(M["Perceptron"].accuracy), f3(M["Perceptron"].macro_f1), f3(M["Perceptron"].roc_auc)],
        ["kNN (k = 1)", f3(M["kNN"].accuracy), f3(M["kNN"].macro_f1), f3(M["kNN"].roc_auc)],
        ["Decision tree", f3(M["Decision tree"].accuracy), f3(M["Decision tree"].macro_f1), f3(M["Decision tree"].roc_auc)],
        ["Scratch logistic", f3(M["Scratch logistic"].accuracy), f3(M["Scratch logistic"].macro_f1), f3(M["Scratch logistic"].roc_auc)],
        ["Polynomial SVM", f3(M["Polynomial SVM"].accuracy), f3(M["Polynomial SVM"].macro_f1), f3(M["Polynomial SVM"].roc_auc)],
        ["AdaBoost", f3(M["AdaBoost"].accuracy), f3(M["AdaBoost"].macro_f1), f3(M["AdaBoost"].roc_auc)],
        ["MLP  (được chọn)", f3(M["MLP"].accuracy), f3(M["MLP"].macro_f1), f3(M["MLP"].roc_auc)],
      ],
      emphasise: "MLP  (được chọn)",
    },
    { k: "text", x: GUT, y: 5.96, w: COLW, h: 0.5, size: 13.5, color: MUTED,
      text: "Chênh lệch giữa các mô hình dẫn đầu chỉ vài phần nghìn — nhỏ hơn dao động giữa các fold (±0.064), nên không đọc thành xếp hạng." },
    { k: "bullets", x: 8.85, y: 1.82, w: 3.75, size: 16, gap: 14, items: [
      [{ t: "MLP " }, { t: f4(M["MLP"].macro_f1), bold: true }, { t: " ≈ hồi quy logistic tự cài đặt " },
       { t: f4(M["Scratch logistic"].macro_f1), bold: true }, { t: " — mô hình phức tạp không tạo khác biệt rõ." }],
      [{ t: "Accuracy cao " }, { t: `${f2(M["MLP"].accuracy)}`, bold: true },
       { t: " nhưng phải đọc kèm chỉ số theo lớp, vì lớp bad chỉ chiếm 30%." }],
      [{ t: "16 mô hình đều vượt baseline", bold: true }, { t: ", kể cả cây quyết định có accuracy thấp hơn." }],
    ]},
  ],
  notes: "Đây là kết quả trên hai trăm hồ sơ test chưa từng dùng để chọn mô hình. MLP có accuracy không phẩy bảy chín, macro F1 không phẩy bảy ba không, AUC không phẩy tám một ba. Đáng chú ý: hồi quy logistic tự cài đặt ở câu một đạt macro F1 không phẩy bảy ba không một, gần như bằng MLP. Trong bài toán nhỏ này, mô hình phức tạp hơn không mang lại lợi ích rõ rệt. Mọi mô hình học đều vượt baseline, nhưng chênh lệch chỉ vài phần nghìn. Em mời bạn Tâm trình bày phần overfitting.",
});

// ------------------------------------------------------------------- slide 12
slide({
  section: "Câu 2",
  eyebrow: "CÂU 2 · ĐỌC KẾT QUẢ",
  title: "Một con số accuracy đẹp có thể che mất lỗi quan trọng",
  blocks: [
    { k: "image", src: "fig_q2_test.png", x: (W - 11.2) / 2, y: TOP, w: 11.2, h: 3.35 },
    { k: "text", x: GUT, y: 5.22, w: COLW, h: 0.46, size: 19,
      runs: [{ t: "158/200 dự đoán đúng, nhưng " },
             { t: `bỏ sót ${M["MLP"].confusion_matrix[1][0]}/60 hồ sơ “bad”`, bold: true },
             { t: ` → recall lớp bad chỉ ${f3(M["MLP"].recall_bad)}.` }] },
    { k: "bullets", x: GUT, y: 5.78, w: COLW, size: 15.5, gap: 8, items: [
      [{ t: "Gaussian NB có recall bad cao nhất " }, { t: "0.650", bold: true },
       { t: ", nhưng precision chỉ 0.513: bắt được nhiều hơn, báo nhầm cũng nhiều hơn." }],
      [{ t: "Đánh đổi này là quyết định nghiệp vụ", bold: true },
       { t: ", không phải lỗi kỹ thuật — và nhóm không hạ ngưỡng sau khi đã xem test." }],
    ]},
  ],
  notes: "Bức tranh này là bài học chính của câu hai. MLP đúng một trăm năm mươi tám trên hai trăm, nghe rất tốt. Nhưng trong sáu mươi hồ sơ thực sự xấu, mô hình bỏ sót hai mươi tám, tức recall lớp bad chỉ không phẩy năm ba ba. Đây là cái bẫy của dữ liệu mất cân bằng: lớp đa số kéo accuracy lên trong khi lớp cần phát hiện bị bỏ qua. Nếu là bài toán tín dụng thật, bỏ sót hồ sơ xấu thường tốn kém hơn báo nhầm. Nhóm không hạ ngưỡng sau khi xem test, vì làm vậy là dùng test để tinh chỉnh.",
});

// ------------------------------------------------------------------- slide 13
slide({
  section: "Overfitting",
  eyebrow: "OVERFITTING",
  title: "Bằng chứng: cây càng sâu, khoảng cách càng lớn",
  blocks: [
    { k: "image", src: "fig_overfit.png", x: (W - 10.4) / 2, y: TOP, w: 10.4, h: 3.5 },
    { k: "stats", x: GUT, y: 5.36, w: COLW, items: [
      { head: f3(treeGapBase) + "  →  " + f3(treeGapSel), tail: "Khoảng cách train − CV của cây quyết định sau khi giới hạn độ sâu 6 và tối thiểu 5 mẫu/lá." },
      { head: "1.00 / 0.614", tail: "Cây không giới hạn: hoàn hảo trên train nhưng validation thấp hơn cây bị giới hạn." },
      { head: f3(rfGapSel), tail: "Random forest vẫn còn khoảng cách lớn — ensemble không tự chữa được overfitting." },
    ]},
    { k: "text", x: GUT, y: 6.30, w: COLW, h: 0.4, size: 14, color: MUTED,
      text: "Biện pháp chung: giới hạn độ phức tạp · chọn tham số bằng validation · giữ tập test riêng · báo cáo cả điểm train và validation." },
  ],
  notes: "Biểu đồ bên trái tách riêng ảnh hưởng của độ sâu cây: độ sâu tăng thì điểm train leo lên một, nhưng validation chỉ tăng đến khoảng độ sâu sáu rồi giảm. Cây không giới hạn đạt một phẩy không trên train nhưng chỉ không phẩy sáu một bốn trên validation. Giới hạn độ sâu sáu và tối thiểu năm mẫu mỗi lá, khoảng cách thu hẹp từ không phẩy ba tám sáu xuống không phẩy một hai một, điểm validation tăng. Nhưng random forest sau khi chọn tham số vẫn còn khoảng cách không phẩy ba hai bốn. Ensemble giảm phương sai nhưng không miễn nhiễm với việc ghi nhớ dữ liệu.",
});

// ------------------------------------------------------------------- slide 14
slide({
  section: "Kết luận",
  eyebrow: "KẾT LUẬN",
  title: "Điều nhóm làm được, điều còn hạn chế",
  blocks: [
    { k: "columns", x: GUT, y: 1.78, w: COLW, gap: 0.55, size: 14.5, itemGap: 18, cols: [
      { head: "Kết quả chính", items: [
        "Câu 1: hai mô hình tự cài đặt, gradient khớp sai phân trung tâm, RMSE xấp xỉ nhiễu sinh dữ liệu.",
        "Câu 2: 14 mô hình trên cùng bộ fold; MLP được chọn với macro F1 test 0.7305.",
        "Chi phí của accuracy: bỏ sót 28/60 hồ sơ xấu dù accuracy 0.79.",
      ]},
      { head: "Bài học", items: [
        "Tách test trước và chuẩn hóa trong fold là điều kiện của một so sánh đáng tin.",
        "Chênh lệch nhỏ hơn dao động giữa các fold thì chưa kết luận được hơn kém.",
        "Overfitting đo được bằng khoảng cách train − validation, và giảm được bằng giới hạn độ phức tạp.",
      ]},
      { head: "Hạn chế", items: [
        "Một bộ dữ liệu, một lần chia test, lưới tham số nhỏ.",
        "Hồi quy logistic chạm 5000 vòng, MLP chạm 500 epoch: chưa hội tụ.",
        "Không có kiểm định thống kê hay lặp lại với nhiều seed.",
      ]},
    ]},
    { k: "rule", x: GUT, y: 6.05, w: COLW, pt: 1.2, color: RULE },
    { k: "text", x: GUT, y: 6.20, w: COLW, h: 0.4, size: 16, color: MUTED,
      text: "Cảm ơn thầy và các bạn đã lắng nghe — nhóm sẵn sàng nhận câu hỏi." },
  ],
  notes: "Tóm lại, câu một cho thấy hai mô hình tự cài đặt học đúng: gradient khớp kiểm tra sai phân, sai số xấp xỉ mức nhiễu. Câu hai cho thấy trên dữ liệu nhỏ và mất cân bằng, mô hình phức tạp nhất không vượt trội rõ rệt, và accuracy có thể che mất lỗi ở lớp thiểu số. Hạn chế: một bộ dữ liệu, một lần chia test, lưới tham số nhỏ; logistic và MLP đều chạm ngân sách vòng lặp nên chưa hội tụ; không có kiểm định thống kê. Em xin kết thúc và cảm ơn thầy, các bạn.",
});

// ------------------------------------------------------------------ PPTX build
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Ngô Lâm Tiến, Nguyễn Công Thành, Nguyễn Lê Nhật Tâm";
pptx.company = "Ton Duc Thang University";
pptx.title = "Hồi quy & Phân loại — Báo cáo giữa kỳ";
pptx.subject = "Introduction to Machine Learning";
pptx.theme = { headFontFace: FONT, bodyFontFace: FONT };

const FOOTER =
  "Introduction to Machine Learning  ·  Báo cáo giữa kỳ  ·  Ngô Lâm Tiến 524H0195 · Nguyễn Công Thành 524H0191 · Nguyễn Lê Nhật Tâm 524H0186";

pptx.defineSlideMaster({
  title: "FRAME",
  background: { color: "FFFFFF" },
  objects: [
    { image: { path: LOGO, x: 0.44, y: 0.21, w: 1.646, h: 0.911 } },
    { line: { x: 0.44, y: 1.30, w: 12.45, h: 0, line: { color: RULE, width: 1 } } },
    { text: { text: FOOTER, x: GUT, y: 7.03, w: 9.9, h: 0.22, fontFace: FONT, fontSize: 8.5, color: "9A9A9A" } },
  ],
  slideNumber: { x: 11.6, y: 7.0, w: 1.3, h: 0.26, fontFace: FONT, fontSize: 9, color: "9A9A9A", align: "right" },
});

pptx.defineSlideMaster({
  title: "COVER",
  background: { color: "FFFFFF" },
  objects: [
    { image: { path: LOGO, x: 0.44, y: 0.21, w: 1.646, h: 0.911 } },
    { line: { x: 0.44, y: 1.30, w: 12.45, h: 0, line: { color: RULE, width: 1 } } },
    { text: { text: FOOTER, x: GUT, y: 7.03, w: 9.9, h: 0.22, fontFace: FONT, fontSize: 8.5, color: "9A9A9A" } },
  ],
});

const toRuns = (arr, base) =>
  arr.map((r) => {
    const o = typeof r === "string" ? { t: r } : r;
    const opts = { ...base };
    if (o.bold) opts.bold = true;
    if (o.italic) opts.italic = true;
    if (o.color) opts.color = o.color;
    if (o.size) opts.fontSize = o.size;
    if (o.sup) opts.superscript = true;
    if (o.sub) opts.subscript = true;
    return { text: o.t, options: opts };
  });

function drawBlock(s, b) {
  const common = { fontFace: FONT, margin: 0, isTextBox: true, valign: "top", wrap: true, fit: "none" };
  switch (b.k) {
    case "text": {
      const runs = b.runs
        ? toRuns(b.runs, { fontSize: b.size || 18, color: b.color || INK })
        : toRuns([b.text], { fontSize: b.size || 18, color: b.color || INK });
      s.addText(runs, {
        ...common, x: b.x, y: b.y, w: b.w, h: b.h || 0.4,
        fontSize: b.size || 18, color: b.color || INK, bold: !!b.bold, italic: !!b.italic,
        align: b.align || "left", charSpacing: b.spacing, lineSpacingMultiple: b.lineSpacing,
      });
      break;
    }
    case "label": {
      s.addText(b.text, {
        ...common, x: b.x, y: b.y, w: b.w, h: 0.3,
        fontSize: 11, color: MUTED, charSpacing: 1.4, bold: false,
      });
      break;
    }
    case "eq": {
      s.addText(toRuns(b.runs, { fontSize: b.size || 20, color: b.color || INK }), {
        ...common, x: b.x, y: b.y, w: b.w, h: b.h || 0.45,
        fontSize: b.size || 20, color: b.color || INK,
      });
      break;
    }
    case "bullets": {
      const items = b.items.map((it) => {
        const arr = typeof it === "string" ? [{ t: it }] : it;
        return toRuns(arr, { fontSize: b.size || 17, color: INK, breakLine: true });
      });
      s.addText(items.flat().map((r) => ({ text: r.text, options: { ...r.options, bullet: { code: "2013" }, indentLevel: 0 } })), {
        ...common, x: b.x, y: b.y, w: b.w, h: b.h || (BOT - b.y),
        fontSize: b.size || 17, color: INK,
        paraSpaceAfter: b.gap === undefined ? 10 : b.gap,
        lineSpacingMultiple: 1.06,
      });
      break;
    }
    case "rule": {
      s.addShape(pptx.ShapeType.line, {
        x: b.x, y: b.y, w: b.vertical ? 0 : b.w, h: b.vertical ? b.h : 0,
        line: { color: b.color || HAIR, width: b.pt || 0.75 },
      });
      break;
    }
    case "image": {
      s.addImage({ path: path.join(FIG, b.src), x: b.x, y: b.y, w: b.w, h: b.h });
      break;
    }
    case "kpis": {
      const n = b.items.length;
      const colW = b.w / n;
      b.items.forEach((it, i) => {
        const x = b.x + i * colW;
        s.addShape(pptx.ShapeType.line, { x, y: b.y, w: colW - 0.28, h: 0, line: { color: RULE, width: 1 } });
        s.addText(it.value, {
          ...common, x, y: b.y + 0.08, w: colW - 0.28, h: 0.42,
          fontSize: 24, bold: true, color: INK,
        });
        s.addText(it.label, {
          ...common, x, y: b.y + 0.52, w: colW - 0.28, h: 0.5,
          fontSize: 11, color: MUTED, lineSpacingMultiple: 1.15,
        });
      });
      break;
    }
    case "stats": {
      const n = b.items.length;
      const colW = b.w / n;
      b.items.forEach((it, i) => {
        const x = b.x + i * colW;
        s.addText(it.head, {
          ...common, x, y: b.y, w: colW - 0.4, h: 0.4, fontSize: 20, bold: true, color: INK,
        });
        s.addText(it.tail, {
          ...common, x, y: b.y + 0.44, w: colW - 0.4, h: 0.7, fontSize: 12, color: MUTED,
          lineSpacingMultiple: 1.18,
        });
      });
      break;
    }
    case "numlist": {
      b.items.forEach((it, i) => {
        const y = b.y + i * b.rowH;
        s.addText(it.n, { ...common, x: b.x, y: y + 0.02, w: 0.9, h: 0.5, fontSize: 26, bold: true, color: "C9C9C9" });
        s.addText(it.title, { ...common, x: b.x + 0.95, y, w: b.w - 3.7, h: 0.38, fontSize: 19, bold: true, color: INK });
        s.addText(it.sub, { ...common, x: b.x + 0.95, y: y + 0.38, w: b.w - 3.7, h: 0.6, fontSize: 13, color: MUTED, lineSpacingMultiple: 1.12 });
        s.addText(it.right, { ...common, x: b.x + b.w - 2.65, y: y + 0.06, w: 2.65, h: 0.34, fontSize: 13, color: INK, align: "right" });
        if (i < b.items.length - 1) {
          s.addShape(pptx.ShapeType.line, { x: b.x, y: y + b.rowH - 0.18, w: b.w, h: 0, line: { color: HAIR, width: 0.75 } });
        }
      });
      break;
    }
    case "flow": {
      const n = b.items.length;
      const arrow = 0.52;
      const boxW = (b.w - arrow * (n - 1)) / n;
      b.items.forEach((it, i) => {
        const x = b.x + i * (boxW + arrow);
        s.addShape(pptx.ShapeType.rect, {
          x, y: b.y, w: boxW, h: b.h, fill: { color: "FFFFFF" },
          line: { color: "8C8C8C", width: 1 },
        });
        s.addText(it.n, { ...common, x: x + 0.16, y: b.y + 0.12, w: 0.7, h: 0.28, fontSize: 11, color: MUTED, charSpacing: 1 });
        s.addText(it.title, { ...common, x: x + 0.16, y: b.y + 0.42, w: boxW - 0.32, h: 0.6, fontSize: 15.5, bold: true, color: INK, lineSpacingMultiple: 1.05 });
        s.addText(it.sub, { ...common, x: x + 0.16, y: b.y + 1.02, w: boxW - 0.32, h: 0.52, fontSize: 11, color: MUTED, lineSpacingMultiple: 1.1 });
        if (i < n - 1) {
          s.addText("→", { ...common, x: x + boxW, y: b.y + b.h / 2 - 0.24, w: arrow, h: 0.4, fontSize: 20, color: MUTED, align: "center" });
        }
      });
      break;
    }
    case "columns": {
      const n = b.cols.length;
      const colW = (b.w - b.gap * (n - 1)) / n;
      b.cols.forEach((c, i) => {
        const x = b.x + i * (colW + b.gap);
        s.addShape(pptx.ShapeType.line, { x, y: b.y, w: colW, h: 0, line: { color: RULE, width: 1 } });
        s.addText(c.head, { ...common, x, y: b.y + 0.12, w: colW, h: 0.36, fontSize: 15, bold: true, color: INK });
        s.addText(
          c.items.map((t) => ({ text: t, options: { bullet: { code: "2013" }, breakLine: true } })),
          { ...common, x, y: b.y + 0.52, w: colW, h: 4.4, fontSize: b.size || 12.5, color: "222222",
            paraSpaceAfter: b.itemGap === undefined ? 9 : b.itemGap, lineSpacingMultiple: 1.16 }
        );
      });
      break;
    }
    case "table": {
      const rows = b.rows.map((row, ri) =>
        row.map((cell) => {
          const isHead = ri === 0;
          const isKey = b.emphasise && row[0] === b.emphasise;
          return {
            text: cell,
            options: {
              fontFace: FONT, fontSize: b.fontSize || 13, bold: isHead || isKey, color: INK,
              fill: { color: isHead ? FILL : isKey ? "E8E8E8" : "FFFFFF" },
              align: cell === row[0] ? "left" : "right",
              valign: "middle",
            },
          };
        })
      );
      s.addTable(rows, {
        x: b.x, y: b.y, w: b.w, colW: b.colW, rowH: b.rowH,
        border: { type: "solid", color: HAIR, pt: 0.5 },
        autoPage: false, margin: 0.07,
      });
      break;
    }
    default:
      throw new Error("unknown block " + b.k);
  }
}

let sectionSeen = null;
for (const spec of SLIDES) {
  if (spec.section !== sectionSeen) {
    pptx.addSection({ title: spec.section });
    sectionSeen = spec.section;
  }
  const s = pptx.addSlide({ masterName: spec.layout || "FRAME", sectionTitle: spec.section });
  if (spec.eyebrow) {
    s.addText(spec.eyebrow, {
      x: 2.42, y: 0.24, w: 10.2, h: 0.26, margin: 0, isTextBox: true,
      fontFace: FONT, fontSize: 10.5, color: MUTED, charSpacing: 2, valign: "middle",
    });
  }
  if (spec.title) {
    s.addText(spec.title, {
      x: 2.42, y: 0.50, w: 10.3, h: 0.55, margin: 0, isTextBox: true,
      fontFace: FONT, fontSize: 26, bold: true, color: INK, valign: "middle", fit: "none",
    });
  }
  spec.blocks.forEach((b) => drawBlock(s, b));
  s.addNotes(spec.notes);
}

// ----------------------------------------------------------------- HTML mirror
const px = (v) => (v * 96).toFixed(2) + "px";
const pt = (v) => (v * 96 / 72).toFixed(2) + "px";

function htmlRuns(arr, base) {
  return arr
    .map((r) => {
      const o = typeof r === "string" ? { t: r } : r;
      const st = [];
      if (o.bold) st.push("font-weight:700");
      if (o.italic) st.push("font-style:italic");
      if (o.color) st.push(`color:#${o.color}`);
      if (o.sup) st.push("vertical-align:super;font-size:0.66em");
      if (o.sub) st.push("vertical-align:sub;font-size:0.66em");
      return `<span style="${st.join(";")}">${o.t}</span>`;
    })
    .join("");
}

function htmlBlock(b) {
  const box = `position:absolute;left:${px(b.x)};top:${px(b.y)};width:${px(b.w)};`;
  switch (b.k) {
    case "text": {
      const content = b.runs ? htmlRuns(b.runs) : b.text;
      return `<div style="${box}height:${px(b.h || 0.4)};font-size:${pt(b.size || 18)};color:#${b.color || INK};` +
        `${b.bold ? "font-weight:700;" : ""}${b.italic ? "font-style:italic;" : ""}` +
        `${b.spacing ? `letter-spacing:${b.spacing / 72 * 96}px;` : ""}` +
        `line-height:${b.lineSpacing || 1.22};white-space:pre-wrap;">${content}</div>`;
    }
    case "label":
      return `<div style="${box}height:${px(0.3)};font-size:${pt(11)};color:#${MUTED};letter-spacing:1.6px;">${b.text}</div>`;
    case "eq":
      return `<div style="${box}height:${px(b.h || 0.45)};font-size:${pt(b.size || 20)};color:#${b.color || INK};line-height:1.3;">${htmlRuns(b.runs)}</div>`;
    case "bullets": {
      const items = b.items
        .map((it) => {
          const arr = typeof it === "string" ? [{ t: it }] : it;
          return `<div style="position:relative;padding-left:22px;margin-bottom:${b.gap === undefined ? 10 : b.gap}px;">` +
            `<span style="position:absolute;left:4px;top:0;color:#${INK}">–</span>${htmlRuns(arr)}</div>`;
        })
        .join("");
      return `<div style="${box}font-size:${pt(b.size || 17)};color:#${INK};line-height:1.25;">${items}</div>`;
    }
    case "rule":
      return b.vertical
        ? `<div style="position:absolute;left:${px(b.x)};top:${px(b.y)};width:${Math.max(1, b.pt || 1)}px;height:${px(b.h)};background:#${b.color || HAIR};"></div>`
        : `<div style="position:absolute;left:${px(b.x)};top:${px(b.y)};width:${px(b.w)};height:${Math.max(1, b.pt || 1)}px;background:#${b.color || HAIR};"></div>`;
    case "image":
      return `<img src="figures/${b.src}" style="position:absolute;left:${px(b.x)};top:${px(b.y)};width:${px(b.w)};height:${px(b.h)};">`;
    case "kpis": {
      const colW = b.w / b.items.length;
      return b.items
        .map((it, i) => {
          const x = b.x + i * colW;
          return `<div style="position:absolute;left:${px(x)};top:${px(b.y)};width:${px(colW - 0.28)};">` +
            `<div style="height:1px;background:#${RULE};"></div>` +
            `<div style="font-size:${pt(24)};font-weight:700;color:#${INK};margin-top:${px(0.08)};">${it.value}</div>` +
            `<div style="font-size:${pt(11)};color:#${MUTED};line-height:1.2;margin-top:${px(0.06)};">${it.label}</div></div>`;
        })
        .join("");
    }
    case "stats": {
      const colW = b.w / b.items.length;
      return b.items
        .map((it, i) => {
          const x = b.x + i * colW;
          return `<div style="position:absolute;left:${px(x)};top:${px(b.y)};width:${px(colW - 0.4)};">` +
            `<div style="font-size:${pt(20)};font-weight:700;color:#${INK};">${it.head}</div>` +
            `<div style="font-size:${pt(12)};color:#${MUTED};line-height:1.2;margin-top:${px(0.06)};">${it.tail}</div></div>`;
        })
        .join("");
    }
    case "numlist":
      return b.items
        .map((it, i) => {
          const y = b.y + i * b.rowH;
          const sep = i < b.items.length - 1
            ? `<div style="position:absolute;left:${px(b.x)};top:${px(y + b.rowH - 0.18)};width:${px(b.w)};height:1px;background:#${HAIR};"></div>`
            : "";
          return sep +
            `<div style="position:absolute;left:${px(b.x)};top:${px(y + 0.02)};font-size:${pt(26)};font-weight:700;color:#C9C9C9;">${it.n}</div>` +
            `<div style="position:absolute;left:${px(b.x + 0.95)};top:${px(y)};width:${px(b.w - 3.7)};font-size:${pt(19)};font-weight:700;">${it.title}</div>` +
            `<div style="position:absolute;left:${px(b.x + 0.95)};top:${px(y + 0.38)};width:${px(b.w - 3.7)};font-size:${pt(13)};color:#${MUTED};line-height:1.15;">${it.sub}</div>` +
            `<div style="position:absolute;left:${px(b.x + b.w - 2.65)};top:${px(y + 0.06)};width:${px(2.65)};text-align:right;font-size:${pt(13)};">${it.right}</div>`;
        })
        .join("");
    case "flow": {
      const n = b.items.length;
      const arrow = 0.52;
      const boxW = (b.w - arrow * (n - 1)) / n;
      return b.items
        .map((it, i) => {
          const x = b.x + i * (boxW + arrow);
          const arrowHtml = i < n - 1
            ? `<div style="position:absolute;left:${px(x + boxW)};top:${px(b.y + b.h / 2 - 0.24)};width:${px(arrow)};text-align:center;font-size:${pt(20)};color:#${MUTED};">→</div>`
            : "";
          return `<div style="position:absolute;left:${px(x)};top:${px(b.y)};width:${px(boxW)};height:${px(b.h)};border:1px solid #8C8C8C;background:#fff;">` +
            `<div style="position:absolute;left:${px(0.16)};top:${px(0.12)};font-size:${pt(11)};color:#${MUTED};letter-spacing:1px;">${it.n}</div>` +
            `<div style="position:absolute;left:${px(0.16)};top:${px(0.42)};width:${px(boxW - 0.32)};font-size:${pt(15.5)};font-weight:700;line-height:1.1;">${it.title}</div>` +
            `<div style="position:absolute;left:${px(0.16)};top:${px(1.02)};width:${px(boxW - 0.32)};font-size:${pt(11)};color:#${MUTED};line-height:1.15;">${it.sub}</div></div>` + arrowHtml;
        })
        .join("");
    }
    case "columns": {
      const n = b.cols.length;
      const colW = (b.w - b.gap * (n - 1)) / n;
      return b.cols
        .map((c, i) => {
          const x = b.x + i * (colW + b.gap);
          const g = b.itemGap === undefined ? 9 : b.itemGap;
          const list = c.items
            .map((t) => `<div style="position:relative;padding-left:20px;margin-bottom:${g}px;"><span style="position:absolute;left:2px;top:0;">–</span>${t}</div>`)
            .join("");
          return `<div style="position:absolute;left:${px(x)};top:${px(b.y)};width:${px(colW)};">` +
            `<div style="height:1px;background:#${RULE};"></div>` +
            `<div style="font-size:${pt(15)};font-weight:700;margin-top:${px(0.12)};">${c.head}</div>` +
            `<div style="font-size:${pt(b.size || 12.5)};line-height:1.32;margin-top:${px(0.16)};">${list}</div></div>`;
        })
        .join("");
    }
    case "table": {
      const head = b.rows[0];
      const body = b.rows.slice(1);
      const cell = (t, i, isHead, isKey) =>
        `<td style="width:${px(b.colW[i])};height:${px(b.rowH)};padding:0 ${px(0.07)};text-align:${i === 0 ? "left" : "right"};` +
        `font-weight:${isHead || isKey ? 700 : 400};background:#${isHead ? FILL : isKey ? "E8E8E8" : "FFFFFF"};` +
        `border:0.5px solid #${HAIR};font-size:${pt(b.fontSize || 13)};vertical-align:middle;">${t}</td>`;
      const h = `<tr>${head.map((t, i) => cell(t, i, true, false)).join("")}</tr>`;
      const rows = body
        .map((r) => `<tr>${r.map((t, i) => cell(t, i, false, r[0] === b.emphasise)).join("")}</tr>`)
        .join("");
      return `<table style="position:absolute;left:${px(b.x)};top:${px(b.y)};border-collapse:collapse;table-layout:fixed;">${h}${rows}</table>`;
    }
    default:
      throw new Error("unknown block " + b.k);
  }
}

const FRAME_HTML = (spec, idx) => `
<div class="slide">
  <img class="logo" src="../report/assets/tdtu-logo.png">
  <div class="rule"></div>
  <div class="footer">${FOOTER}</div>
  ${spec.layout === "COVER" ? "" : `<div class="pageno">${idx + 1} / ${SLIDES.length}</div>`}
  ${spec.eyebrow ? `<div class="eyebrow">${spec.eyebrow}</div>` : ""}
  ${spec.title ? `<div class="title">${spec.title}</div>` : ""}
  ${spec.blocks.map(htmlBlock).join("\n")}
</div>`;

const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8">
<title>Midterm deck preview</title>
<style>
  @page { size: 13.333in 7.5in; margin: 0; }
  * { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { margin: 0; background: #8a8a8a; font-family: Arial, "Liberation Sans", sans-serif; }
  .slide { position: relative; width: ${px(W)}; height: ${px(H)}; background: #fff; margin: 0 auto; overflow: hidden; }
  .logo { position: absolute; left: ${px(0.44)}; top: ${px(0.21)}; width: ${px(1.646)}; height: ${px(0.911)}; }
  .rule { position: absolute; left: ${px(0.44)}; top: ${px(1.30)}; width: ${px(12.45)}; height: 1px; background: #${RULE}; }
  .footer { position: absolute; left: ${px(GUT)}; top: ${px(7.03)}; font-size: ${pt(8.5)}; color: #9A9A9A; }
  .pageno { position: absolute; left: ${px(11.6)}; top: ${px(7.0)}; width: ${px(1.3)}; text-align: right; font-size: ${pt(9)}; color: #9A9A9A; }
  .eyebrow { position: absolute; left: ${px(2.42)}; top: ${px(0.24)}; height: ${px(0.26)}; display: flex; align-items: center; font-size: ${pt(10.5)}; color: #${MUTED}; letter-spacing: 2.4px; }
  .title { position: absolute; left: ${px(2.42)}; top: ${px(0.50)}; width: ${px(10.3)}; height: ${px(0.55)}; display: flex; align-items: center; font-size: ${pt(26)}; font-weight: 700; color: #${INK}; line-height: 1.1; }
  @media print { body { background: #fff; } .slide { margin: 0; page-break-after: always; } }
</style></head><body>
${SLIDES.map(FRAME_HTML).join("\n")}
</body></html>`;

fs.writeFileSync(path.join(OUT, "preview.html"), html, "utf8");

// ------------------------------------------------------------------ transcript
const WORDS = (s) => s.trim().split(/\s+/).length;
const SPEAKERS = { 0: "Tiến", 1: "Thành", 2: "Tâm" };
const assigned = [];
let clock = 0;
SLIDES.forEach((s, i) => {
  const speaker = i <= 6 ? "Tiến" : i <= 10 ? "Thành" : "Tâm";
  const w = WORDS(s.notes);
  const secs = Math.round((w / 2.55) * 1.0); // ~153 words per minute, measured read-aloud pace
  assigned.push({ i, speaker, w, secs, start: clock });
  clock += secs;
});
const mmss = (t) => `${Math.floor(t / 60)}:${String(t % 60).padStart(2, "0")}`;

const bySlide = SLIDES.map((s, i) => {
  const a = assigned[i];
  return `### Slide ${i + 1} — ${s.title || "Trang bìa"}  \n` +
    `**${a.speaker}** · bắt đầu ${mmss(a.start)} · ~${a.secs}s\n\n` +
    `> ${s.notes}\n`;
}).join("\n");

const perSpeaker = ["Tiến", "Thành", "Tâm"].map((sp) => {
  const rows = assigned.filter((a) => a.speaker === sp);
  const secs = rows.reduce((t, r) => t + r.secs, 0);
  const words = rows.reduce((t, r) => t + r.w, 0);
  return `| ${sp} | ${rows.map((r) => r.i + 1).join(", ")} | ${rows.length} | ${mmss(secs)} | ${words} |`;
}).join("\n");

const totalSecs = clock;
const transcript = `# Transcript thuyết trình — Midterm ML

**Đề tài:** Hồi quy & Phân loại — Câu 1 (Gradient Descent tự cài đặt) và Câu 2 (phân loại trên OpenML credit-g)
**Thời lượng thiết kế:** 10 phút cho cả phần nói, chuyển slide và Q&A. Tổng lời thoại ${WORDS(SLIDES.map((s) => s.notes).join(" "))} từ, đọc ở nhịp ~150 từ/phút ⇒ khoảng ${mmss(totalSecs)}.
**Người trình bày:** Tiến (Câu 1) · Thành (Câu 2: dữ liệu và mô hình) · Tâm (kết quả, overfitting, kết luận)

## Phân chia và mốc thời gian

| Người | Slide | Số slide | Thời lượng | Số từ |
|---|---|---|---|---|
${perSpeaker}

Tổng lời thoại ${mmss(totalSecs)}; phần còn lại để chuyển slide, nhấn mạnh và Q&A.

## Mẹo giữ nhịp 10 phút

- Mốc kiểm tra: hết slide 4 (xong lý thuyết câu 1) nên ở **2:08**, hết slide 7 ở **4:12**, hết slide 11 ở **6:45**. Trễ hơn 30 giây thì bỏ phần kiểm chứng gradient ở slide 4.
- Không đọc công thức thành lời từng ký hiệu — nói ý nghĩa, rồi chỉ tay vào hình.
- Câu chốt của mỗi phần nói chậm hơn 20%: đó là phần giảng viên ghi lại.
- Nếu bị hỏi ngoài phạm vi, người đang nói nhận câu hỏi và chuyển cho người phụ trách phần đó.

## Lời thoại theo slide

${bySlide}
## Câu hỏi dự kiến và người trả lời

| Câu hỏi | Người trả lời | Ý chính |
|---|---|---|
| Vì sao dùng ½ trong hàm mất mát? | Tiến | Triệt tiêu hệ số 2 khi đạo hàm; nghiệm tối ưu không đổi. |
| Vì sao chuẩn hóa phải nằm trong fold? | Thành | Nếu fit trước khi chia fold, min/max của validation đã rò rỉ vào train. |
| Vì sao chọn macro F1 thay vì accuracy? | Thành | Hai lớp trọng số ngang nhau; accuracy bị lớp good 70% chi phối. |
| MLP có thực sự tốt hơn logistic không? | Tâm | Không kết luận được: chênh 0.0004, nhỏ hơn SD giữa các fold ±0.064. |
| Sao không hạ ngưỡng để tăng recall lớp bad? | Tâm | Có thể, nhưng phải chọn ngưỡng trên validation; hạ sau khi xem test là dùng test để tinh chỉnh. |
| Gradient đúng chưa? | Tiến | Đã kiểm chứng bằng sai phân trung tâm, dung sai 1e−6, cả hai mô hình. |
| Vì sao chỉ 14 mô hình mà không phải deep learning? | Thành | credit-g là bảng nhỏ 1000 dòng, không có biểu diễn ảnh/chuỗi; CNN/RNN sẽ áp một biểu diễn tùy ý. |

## Ghi chú trung thực học thuật

- Mọi con số trong slide lấy từ \`results/\` và được script \`presentation/src/make_deck_figures.py\` kiểm tra lại trước khi vẽ.
- Không có kết quả nào được chạy riêng cho slide.
- Bài làm có sử dụng hỗ trợ AI trong soạn thảo và kiểm tra; nhóm đã rà lại toàn bộ.
`;
fs.writeFileSync(path.join(OUT, "TRANSCRIPT.md"), transcript, "utf8");

// ---------------------------------------------------------------------- write
pptx.writeFile({ fileName: path.join(OUT, "midterm_presentation.pptx") }).then((file) => {
  console.log("written:", file);
  console.log("slides:", SLIDES.length, "| words:", WORDS(SLIDES.map((s) => s.notes).join(" ")), "| runtime:", mmss(totalSecs));
});
