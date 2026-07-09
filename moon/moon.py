import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
SHOW_PLOTS = True

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
X, y = make_moons(n_samples=300, noise=0.2, random_state=42)
fea = ["特征 1", "特征 2"]
tar = ["类别 0", "类别 1"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

def plot_decision_boundary(model, X, y, title, is_scaled=False):

    h = 0.02
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    if is_scaled:
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        grid_points = scaler.transform(grid_points)
        Z = model.predict(grid_points)
    else:
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.RdBu)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.RdBu)
    plt.title(title)
    plt.xlabel("横坐标")
    plt.ylabel("纵坐标")
    if SHOW_PLOTS:
        plt.show()


def plot_confusion_matrix(y_true, y_pred, title):

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', xticklabels=tar, yticklabels=tar)
    plt.xlabel('预测值')
    plt.ylabel('真实值')
    plt.title(title)
    if SHOW_PLOTS:
        plt.show()

results = {}

dt_model = DecisionTreeClassifier(criterion='gini', max_depth=4, min_samples_split=5, random_state=42)
dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)
results['决策树'] = accuracy_score(y_test, y_pred_dt)
print("\n--- 决策树分类报告 ---")
print(classification_report(y_test, y_pred_dt, target_names=tar))

rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, max_features='sqrt', random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
results['随机森林'] = accuracy_score(y_test, y_pred_rf)
print("\n--- 随机森林分类报告 ---")
print(classification_report(y_test, y_pred_rf, target_names=tar))
train_acc_rf = accuracy_score(y_train, rf_model.predict(X_train))
print(f"随机森林 - 训练集准确率: {train_acc_rf:.4f}, 测试集准确率: {results['随机森林']:.4f}")

svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_model.fit(X_train_scaled, y_train)
y_pred_svm = svm_model.predict(X_test_scaled)
results['SVM (RBF核)'] = accuracy_score(y_test, y_pred_svm)
print("\n--- SVM (RBF核) 分类报告 ---")
print(classification_report(y_test, y_pred_svm, target_names=tar))

plot_confusion_matrix(y_test, y_pred_dt, "决策树 - 混淆矩阵")
plot_confusion_matrix(y_test, y_pred_rf, "随机森林 - 混淆矩阵")
plot_confusion_matrix(y_test, y_pred_svm, "SVM(RBF) - 混淆矩阵")

plot_decision_boundary(dt_model, X_train, y_train, "决策树 - 决策边界", is_scaled=False)
plot_decision_boundary(rf_model, X_train, y_train, "随机森林 - 决策边界", is_scaled=False)
plot_decision_boundary(svm_model, X_train, y_train, "SVM(RBF) - 决策边界", is_scaled=True)

feature_importances = rf_model.feature_importances_
plt.figure(figsize=(8, 5))
plt.barh(fea, feature_importances, color='pink')
plt.title("随机森林 - 特征重要性分析")
plt.xlabel("重要性得分")
if SHOW_PLOTS:
    plt.show()

print("\n" + "=" * 40)
print("模型性能对比总结：")
print("=" * 40)
df_results = pd.DataFrame(list(results.items()), columns=['模型名称', '测试集准确率'])
print(df_results.to_string(index=False))
print("=" * 40)
print("结论：SVM (RBF核) 和 随机森林 在处理月牙形非线性数据上表现优异，准确率均高于浅层决策树。")

plt.figure(figsize=(8, 5))
models = list(results.keys())
accuracies = list(results.values())

colors = ['#3498db' if acc < max(accuracies) else '#e74c3c' for acc in accuracies]
plt.bar(models, accuracies, color=colors)
plt.ylim(0.7, 1.0)
plt.title("三种模型在测试集上的准确率对比")
plt.ylabel("准确率")

for i, v in enumerate(accuracies):
    plt.text(i, v + 0.01, f"{v:.4f}", ha='center')
if SHOW_PLOTS:
    plt.show()