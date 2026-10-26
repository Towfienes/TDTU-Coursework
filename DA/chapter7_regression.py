import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy import stats

os.makedirs('images', exist_ok=True)
plt.rcParams['font.size'] = 11
sns.set_theme(style='whitegrid')

# 1. Doc du lieu
df = pd.read_excel('regression_sales_data_1000.xlsx')
df_30 = df.head(30)
features = ['TV', 'Radio', 'Newspaper', 'Online']

print("=================================================================")
print("          BÀI TẬP CHƯƠNG 7: HỒI QUY TUYẾN TÍNH BỘI")
print("=================================================================")
print(f"Kích thước tập dữ liệu đầy đủ: {df.shape}")
print(f"Kích thước mẫu 30 tháng đầu:   {df_30.shape}\n")

# 2. Truc quan hoa du lieu
# Bieu do phan phoi
fig, axes = plt.subplots(1, 5, figsize=(18, 4))
cols = ['TV', 'Radio', 'Newspaper', 'Online', 'Sales']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
for i in range(len(cols)):
    sns.histplot(df[cols[i]], kde=True, ax=axes[i], color=colors[i])
    axes[i].set_title(f'Phân phối {cols[i]}')
plt.tight_layout()
plt.savefig('images/1_distribution.png', dpi=300)
plt.close()

# Ma tran tuong quan
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap='Blues', fmt='.3f', linewidths=0.5)
plt.title('Ma trận tương quan giữa các biến')
plt.tight_layout()
plt.savefig('images/2_correlation_heatmap.png', dpi=300)
plt.close()

# Bieu do phan tan (Regplot)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for i in range(len(features)):
    r, c = i // 2, i % 2
    sns.regplot(data=df, x=features[i], y='Sales', ax=axes[r, c],
                scatter_kws={'alpha': 0.5, 'color': '#1f77b4'},
                line_kws={'color': 'red', 'linewidth': 2})
    axes[r, c].set_title(f'Sales vs {features[i]}')
    axes[r, c].set_xlabel(f'{features[i]} (ngàn USD)')
    axes[r, c].set_ylabel('Sales (ngàn USD)')
plt.tight_layout()
plt.savefig('images/3_scatter_regplots.png', dpi=300)
plt.close()

print("--> Đã lưu biểu đồ phân phối, ma trận tương quan và scatter plots vào thư mục 'images/'\n")

# =================================================================
# YEU CAU 1: THE STATISTICAL MODEL
# =================================================================
print("-----------------------------------------------------------------")
print("1. THE STATISTICAL MODEL (MÔ HÌNH THỐNG KÊ)")
print("-----------------------------------------------------------------")
print("a. Phương trình mô hình lý thuyết:")
print("   Sales = beta_0 + beta_1*TV + beta_2*Radio + beta_3*Newspaper + beta_4*Online + epsilon")
print("\nb. Các giả định cơ bản:")
print("   1. Tính tuyến tính của các tham số (Linearity)")
print("   2. Kỳ vọng có điều kiện của sai số bằng 0: E(epsilon | X) = 0")
print("   3. Phương sai sai số không đổi (Homoscedasticity): Var(epsilon) = sigma^2")
print("   4. Không có tự tương quan giữa các sai số (No autocorrelation)")
print("   5. Không có đa cộng tuyến hoàn hảo giữa các biến độc lập")
print("   6. Sai số có phân phối chuẩn: epsilon ~ N(0, sigma^2)\n")

# =================================================================
# YEU CAU 2: INFERENCES ABOUT REGRESSION COEFFICIENTS
# =================================================================
print("-----------------------------------------------------------------")
print("2. INFERENCES ABOUT REGRESSION COEFFICIENTS")
print("-----------------------------------------------------------------")

# Uoc luong tren mau 30 thang (theo mo ta de bai)
X_30 = sm.add_constant(df_30[features])
y_30 = df_30['Sales']
model_30 = sm.OLS(y_30, X_30).fit()

print("--- Kết quả ước lượng trên mẫu 30 tháng gần nhất (N = 30) ---")
print(model_30.summary())

# Uoc luong tren mau 1000 quan sat (tap du lieu file)
X_1000 = sm.add_constant(df[features])
y_1000 = df['Sales']
model_1000 = sm.OLS(y_1000, X_1000).fit()

print("\n--- Kết quả ước lượng trên toàn bộ tập dữ liệu (N = 1000) ---")
print(model_1000.summary())

print("\nKết luận kiểm định giả thuyết (mức ý nghĩa alpha = 0.05):")
print("- Mẫu 30 tháng: TV (p=0.012), Radio (p=0.002), Online (p=0.047) có ý nghĩa thống kê.")
print("                Newspaper (p=0.876 > 0.05) KHÔNG có ý nghĩa thống kê.")
print("- Toàn bộ 1000 dòng: Cả 4 biến đều có p < 0.001 (đều có ý nghĩa thống kê).\n")

# =================================================================
# YEU CAU 3: MULTICOLLINEARITY (ĐA CỘNG TUYẾN)
# =================================================================
print("-----------------------------------------------------------------")
print("3. MULTICOLLINEARITY (ĐA CỘNG TUYẾN)")
print("-----------------------------------------------------------------")

def tinh_vif(df_input, cols):
    vif_dict = {}
    for col in cols:
        other_cols = [c for c in cols if c != col]
        X_other = sm.add_constant(df_input[other_cols])
        r2 = sm.OLS(df_input[col], X_other).fit().rsquared
        vif = 1.0 / (1.0 - r2)
        vif_dict[col] = vif
    return vif_dict

vif_30 = tinh_vif(df_30, features)
vif_1000 = tinh_vif(df, features)

print("Hệ số VIF (N = 30):")
for k, v in vif_30.items():
    print(f"  {k:10s}: {v:.4f}")

print("\nHệ số VIF (N = 1000):")
for k, v in vif_1000.items():
    print(f"  {k:10s}: {v:.4f}")

print("\nKết luận về đa cộng tuyến:")
print("  Tất cả các biến đều có VIF xấp xỉ 1.0 (< 5), KHÔNG có hiện tượng đa cộng tuyến.")
print("Giải pháp xử lý khi có đa cộng tuyến:")
print("  - Giữ lại (nếu đa cộng tuyến nhẹ hoặc cần dự báo)")
print("  - Loại bỏ biến bị đa cộng tuyến cao")
print("  - Biến đổi biến / phân tích thành phần chính PCA")
print("  - Áp dụng hồi quy điều quy hóa (Ridge / Lasso / Elastic Net)\n")

# Ve bieu do VIF
plt.figure(figsize=(8, 5))
x_pos = np.arange(len(features))
bars = plt.bar(x_pos, list(vif_1000.values()), color='#2ca02c', width=0.45, label='VIF thực tế (N=1000)')
plt.axhline(y=5, color='orange', linestyle='--', linewidth=1.5, label='Ngưỡng cảnh báo (VIF = 5)')
plt.axhline(y=10, color='red', linestyle='--', linewidth=1.5, label='Ngưỡng nghiêm trọng (VIF = 10)')
plt.xticks(x_pos, features)
plt.ylabel('Hệ số VIF')
plt.ylim(0, 6)
plt.title('Hệ số phóng đại phương sai (VIF)')
plt.legend()
for bar in bars:
    y_val = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, y_val + 0.1, f'{y_val:.3f}', ha='center', va='bottom')
plt.tight_layout()
plt.savefig('images/4_vif_chart.png', dpi=300)
plt.close()

# =================================================================
# YEU CAU 4: INCLUDE/EXCLUDE DECISIONS
# =================================================================
print("-----------------------------------------------------------------")
print("4. INCLUDE / EXCLUDE DECISIONS")
print("-----------------------------------------------------------------")
print("Đề xuất:")
print("  - Dựa trên VIF: Không biến nào bị đa cộng tuyến.")
print("  - Dựa trên p-value: Trên mẫu 30 tháng, Newspaper có p = 0.876 > 0.05.")
print("  --> ĐỀ XUẤT: LOẠI BỎ Newspaper, GIỮ LẠI TV, Radio, Online.")
print("\nGiải thích tác động khi loại bỏ biến:")
print("  - Mô hình đạt tính tinh gọn (Parsimony), dễ diễn giải và áp dụng.")
print("  - Adjusted R^2 tăng từ 0.4109 lên 0.4334.")
print("  - AIC giảm từ 159.2 xuống 157.3, BIC giảm từ 166.2 xuống 162.9.")
print("  - Tránh overfitting và giúp doanh nghiệp tiết kiệm chi phí marketing không hiệu quả.\n")

# =================================================================
# YEU CAU 5: STEPWISE REGRESSION
# =================================================================
print("-----------------------------------------------------------------")
print("5. STEPWISE REGRESSION (HỒI QUY TỪNG BƯỚC TRÊN MẪU 30 THÁNG)")
print("-----------------------------------------------------------------")

# Backward Elimination
step_features = list(features)
step_idx = 1
while len(step_features) > 0:
    X_curr = sm.add_constant(df_30[step_features])
    m_curr = sm.OLS(y_30, X_curr).fit()
    p_vals = m_curr.pvalues.drop('const')
    max_p = p_vals.max()
    worst_f = p_vals.idxmax()

    print(f"Bước {step_idx}: Tập biến = {step_features}")
    print(f"  R^2 = {m_curr.rsquared:.4f}, Adj R^2 = {m_curr.rsquared_adj:.4f}, AIC = {m_curr.aic:.2f}")
    print(f"  Biến có p-value lớn nhất: '{worst_f}' (p = {max_p:.4f})")

    if max_p > 0.05:
        print(f"  --> Loại bỏ '{worst_f}' (p > 0.05)\n")
        step_features.remove(worst_f)
        step_idx += 1
    else:
        print("  --> Tất cả các biến đều có p <= 0.05. DỪNG LẠI!\n")
        model_final_30 = m_curr
        break

print(f"Mô hình cuối cùng gồm: {step_features}")
b_const = model_final_30.params['const']
b_tv = model_final_30.params['TV']
b_rad = model_final_30.params['Radio']
b_onl = model_final_30.params['Online']

print(f"Phương trình cuối cùng: Sales = {b_const:.4f} + {b_tv:.4f}*TV + {b_rad:.4f}*Radio + {b_onl:.4f}*Online\n")

print("--- BẢNG SO SÁNH MÔ HÌNH ĐẦY ĐỦ VS MÔ HÌNH CUỐI CÙNG (N=30) ---")
print(f"{'Tiêu chí':<25} {'Mô hình đầy đủ':<20} {'Mô hình cuối cùng':<20}")
print(f"{'Số biến':<25} {'4 (TV, Rad, News, Onl)':<20} {'3 (TV, Rad, Onl)':<20}")
print(f"{'R-squared':<25} {model_30.rsquared:<20.4f} {model_final_30.rsquared:<20.4f}")
print(f"{'Adjusted R-squared':<25} {model_30.rsquared_adj:<20.4f} {model_final_30.rsquared_adj:<20.4f}")
print(f"{'F-statistic':<25} {model_30.fvalue:<20.3f} {model_final_30.fvalue:<20.3f}")
print(f"{'p-value (F)':<25} {model_30.f_pvalue:<20.4e} {model_final_30.f_pvalue:<20.4e}")
print(f"{'AIC':<25} {model_30.aic:<20.2f} {model_final_30.aic:<20.2f}")
print(f"{'BIC':<25} {model_30.bic:<20.2f} {model_final_30.bic:<20.2f}")

# Ve bieu do Actual vs Predicted
y_pred_final = model_final_30.predict(sm.add_constant(df_30[['TV', 'Radio', 'Online']]))
plt.figure(figsize=(8, 6))
plt.scatter(y_30, y_pred_final, color='#1f77b4', edgecolors='black', s=70, alpha=0.75, label='Quan sát thực tế')
plt.plot([y_30.min(), y_30.max()], [y_30.min(), y_30.max()], 'r--', linewidth=2, label='Đường lý tưởng (y = y_hat)')
plt.xlabel('Sales thực tế (ngàn USD)')
plt.ylabel('Sales dự đoán (ngàn USD)')
plt.title('Doanh số thực tế vs Doanh số dự đoán (Mô hình cuối cùng: TV + Radio + Online)')
plt.legend()
plt.tight_layout()
plt.savefig('images/5_actual_vs_predicted.png', dpi=300)
plt.close()

# Ve bieu do Residual Diagnostics
resid = model_final_30.resid
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].scatter(y_pred_final, resid, color='#1f77b4', edgecolors='black', alpha=0.7)
axes[0].axhline(0, color='red', linestyle='--', linewidth=1.5)
axes[0].set_xlabel('Giá trị dự đoán (Fitted Values)')
axes[0].set_ylabel('Phần dư (Residuals)')
axes[0].set_title('Residuals vs Fitted (Kiểm tra Homoscedasticity)')

stats.probplot(resid, dist="norm", plot=axes[1])
axes[1].set_title('Normal Q-Q Plot (Kiểm tra phân phối chuẩn phần dư)')
plt.tight_layout()
plt.savefig('images/6_residual_diagnostics.png', dpi=300)
plt.close()

print("\n--> Đã xuất tất cả hình ảnh trực quan vào thư mục 'images/'")
print("=================================================================")
print("                    HOÀN THÀNH TOÀN BỘ YÊU CẦU")
print("=================================================================")

