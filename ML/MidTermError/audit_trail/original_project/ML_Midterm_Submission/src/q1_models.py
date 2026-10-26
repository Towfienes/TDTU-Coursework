"""Machine Learning Midterm Q1: Linear and Logistic Regression FROM SCRATCH.

Only NumPy implements both learning algorithms. scikit-learn is used for
synthetic dataset creation, splitting, evaluation, and feature standardization.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (mean_squared_error,mean_absolute_error,r2_score,
 accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,
 confusion_matrix,ConfusionMatrixDisplay)

SEED = 42

class LinearRegressionGD:
    """Minimize J=(1/(2m)) sum_i (X_i @ w + b - y_i)^2."""
    def __init__(self, learning_rate=0.08, epochs=1200):
        self.learning_rate, self.epochs = learning_rate, epochs
    def _loss_grad(self, X, y, w, b):
        err = X @ w + b - y
        return float(np.mean(err**2)/2), X.T @ err/len(y), float(np.mean(err))
    def fit(self, X, y):
        X, y = np.asarray(X,float), np.asarray(y,float).ravel()
        self.weights_ = np.zeros(X.shape[1]); self.bias_ = 0.
        self.loss_history_ = []
        for epoch in range(self.epochs):
            loss, dw, db = self._loss_grad(X,y,self.weights_,self.bias_)
            self.loss_history_.append(loss)
            self.weights_ -= self.learning_rate*dw
            self.bias_ -= self.learning_rate*db
        return self
    def predict(self,X):
        return np.asarray(X) @ self.weights_ + self.bias_

class LogisticRegressionGD:
    """Minimize stable binary cross entropy: mean(logaddexp(0,z)-y*z)."""
    def __init__(self, learning_rate=0.13, epochs=2400):
        self.learning_rate, self.epochs = learning_rate, epochs
    @staticmethod
    def sigmoid(z):
        z=np.asarray(z,float)
        out=np.empty_like(z)
        mask=z>=0
        out[mask]=1/(1+np.exp(-z[mask]))
        ez=np.exp(z[~mask]);out[~mask]=ez/(1+ez)
        return out
    def _loss_grad(self,X,y,w,b):
        z=X @ w+b
        p=self.sigmoid(z)
        residual=p-y
        loss=float(np.mean(np.logaddexp(0,z)-y*z))
        return loss,X.T @ residual/len(y),float(np.mean(residual))
    def fit(self,X,y):
        X,y=np.asarray(X,float),np.asarray(y,float).ravel()
        if not set(np.unique(y)).issubset({0.,1.}):
            raise ValueError('Binary y values must be 0/1')
        self.weights_=np.zeros(X.shape[1]);self.bias_=0.
        self.loss_history_=[]
        for epoch in range(self.epochs):
            loss,dw,db=self._loss_grad(X,y,self.weights_,self.bias_)
            self.loss_history_.append(loss)
            self.weights_-=self.learning_rate*dw
            self.bias_-=self.learning_rate*db
        return self
    def predict_proba(self,X):
        return self.sigmoid(np.asarray(X) @ self.weights_ + self.bias_)
    def predict(self,X,threshold=0.5):
        return (self.predict_proba(X)>=threshold).astype(int)

def gradient_check(model,X,y,eps=1e-6):
    """Verify analytic gradients by two-sided finite differences."""
    w=np.array([0.13,-0.07]+[0.]*(X.shape[1]-2));b=0.11
    _,dw,db=model._loss_grad(X,y,w,b)
    estimates=[]
    for j in range(X.shape[1]):
        v=w.copy();v[j]+=eps
        a=model._loss_grad(X,y,v,b)[0]
        v[j]-=2*eps
        c=model._loss_grad(X,y,v,b)[0]
        estimates.append((a-c)/(2*eps))
    estb=(model._loss_grad(X,y,w,b+eps)[0]-model._loss_grad(X,y,w,b-eps)[0])/(2*eps)
    return float(max(np.max(np.abs(np.asarray(estimates)-dw)),abs(estb-db)))

def main(root=None):
    root=Path(root or Path(__file__).resolve().parents[1]); (root/'figures').mkdir(exist_ok=True)
    (root/'results').mkdir(exist_ok=True)
    results={}
    # Q1A: synthetic continuous target, two explanatory variables
    rng=np.random.default_rng(SEED)
    X=rng.normal(size=(360,2)); y=4+3*X[:,0]-2*X[:,1]+rng.normal(0,.65,len(X))
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.20,random_state=SEED)
    sc=StandardScaler().fit(Xtr);Xtr=sc.transform(Xtr); Xte=sc.transform(Xte)
    lin=LinearRegressionGD().fit(Xtr,ytr);pred=lin.predict(Xte)
    grad=gradient_check(LinearRegressionGD(),Xtr[:20],ytr[:20]);assert grad<1e-6,grad
    assert lin.loss_history_[-1]<lin.loss_history_[0]
    results['linear']={
        'dataset':'Synthetic linear regression, seed=42; y=4+3*x1-2*x2+N(0,0.65^2)',
        'n_train':len(ytr),'n_test':len(yte),'epochs':lin.epochs,'learning_rate':lin.learning_rate,
        'train_loss_first':lin.loss_history_[0],'train_loss_last':lin.loss_history_[-1],
        'mse':float(mean_squared_error(yte,pred)),'rmse':float(np.sqrt(mean_squared_error(yte,pred))),
        'mae':float(mean_absolute_error(yte,pred)),'r2':float(r2_score(yte,pred)),
        'grad_check_max_abs_diff':grad,'weights_standardized':lin.weights_.tolist(),'bias_standardized':lin.bias_}
    plt.figure(figsize=(8,4.6));plt.plot(lin.loss_history_,color='#0E7490',lw=2)
    plt.title('Q1A Linear Regression - Gradient Descent');plt.xlabel('Epoch');plt.ylabel('Training loss (MSE / 2)')
    plt.grid(alpha=.22);plt.tight_layout();plt.savefig(root/'figures/q1_linear_loss.png',dpi=170);plt.close()
    plt.figure(figsize=(6,5));plt.scatter(yte,pred,alpha=.7,c='#0891B2',s=24)
    rg=[min(yte.min(),pred.min()),max(yte.max(),pred.max())]
    plt.plot(rg,rg,'--',color='#DC2626',label='Ideal prediction')
    plt.xlabel('Observed y');plt.ylabel('Predicted y');plt.title('Q1A - Test Predictions');plt.legend()
    plt.tight_layout();plt.savefig(root/'figures/q1_linear_predictions.png',dpi=170);plt.close()
    # Q1B: synthetic binary classification with controlled noise/imbalance
    X,y=make_classification(n_samples=600,n_features=5,n_informative=4,
       n_redundant=0,weights=[.55,.45],class_sep=1.2,flip_y=.04,random_state=27)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.20,stratify=y,random_state=SEED)
    sc=StandardScaler().fit(Xtr);Xtr=sc.transform(Xtr);Xte=sc.transform(Xte)
    log=LogisticRegressionGD().fit(Xtr,ytr); p=log.predict_proba(Xte); pred=log.predict(Xte)
    grad=gradient_check(LogisticRegressionGD(),Xtr[:20],ytr[:20]);assert grad<1e-6,grad
    assert log.loss_history_[-1]<log.loss_history_[0]
    results['logistic']={
        'dataset':'Synthetic binary classification, make_classification, seed=27',
        'n_train':len(ytr),'n_test':len(yte),'epochs':log.epochs,'learning_rate':log.learning_rate,
        'train_loss_first':log.loss_history_[0],'train_loss_last':log.loss_history_[-1],
        'accuracy':float(accuracy_score(yte,pred)),'precision':float(precision_score(yte,pred,zero_division=0)),
        'recall':float(recall_score(yte,pred,zero_division=0)),'f1':float(f1_score(yte,pred,zero_division=0)),
        'roc_auc':float(roc_auc_score(yte,p)),'confusion_matrix':confusion_matrix(yte,pred).tolist(),
        'grad_check_max_abs_diff':grad,'weights_standardized':log.weights_.tolist(),'bias_standardized':log.bias_}
    plt.figure(figsize=(8,4.6));plt.plot(log.loss_history_,color='#7C3AED',lw=2)
    plt.title('Q1B Logistic Regression - Gradient Descent');plt.xlabel('Epoch');plt.ylabel('Training loss (Binary cross-entropy)')
    plt.grid(alpha=.22);plt.tight_layout();plt.savefig(root/'figures/q1_logistic_loss.png',dpi=170);plt.close()
    fig,ax=plt.subplots(figsize=(5.8,4.8));ConfusionMatrixDisplay.from_predictions(yte,pred,ax=ax,cmap='Blues',colorbar=False)
    ax.set_title('Q1B - Test Confusion Matrix');fig.tight_layout();fig.savefig(root/'figures/q1_logistic_confusion.png',dpi=170);plt.close(fig)
    (root/'results/q1_metrics.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('Q1 successful: finite-difference gradient checks passed.')
    print(json.dumps(results,indent=2))
    return results

if __name__=='__main__':main()
