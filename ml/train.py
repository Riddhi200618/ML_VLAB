"""Reproducible training: run python ml/train.py from the project root."""
from pathlib import Path
import csv, json, hashlib
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor, LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'dist/data/advertising.csv'
rows = list(csv.DictReader(path.open()))
features = ['TV', 'Radio', 'Newspaper']
X = np.array([[float(r[f]) for f in features] for r in rows])
y = np.array([float(r['Sales']) for r in rows])
train, test = train_test_split(np.arange(len(y)), test_size=.2, random_state=42)
scaler = StandardScaler().fit(X[train])
xt, xv = scaler.transform(X[train]), scaler.transform(X[test])
model = SGDRegressor(loss='squared_error', penalty=None, learning_rate='constant', eta0=.01,
                     max_iter=5000, tol=1e-8, n_iter_no_change=30, random_state=42).fit(xt, y[train])
ols = LinearRegression().fit(xt, y[train])
baseline = DummyRegressor(strategy='mean').fit(xt, y[train])
def metrics(actual, pred):
    return dict(rmse=float(np.sqrt(mean_squared_error(actual,pred))),
                mae=float(mean_absolute_error(actual,pred)), r2=float(r2_score(actual,pred)))
pred = model.predict(xv)
artifact = dict(schema_version=1, algorithm='SGDRegressor', library=f'scikit-learn {sklearn.__version__}',
    features=features, target='Sales', train_rows=len(train), test_rows=len(test), seed=42,
    source='https://www.kaggle.com/datasets/ashydv/advertising-dataset',
    dataset_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    mean=scaler.mean_.tolist(), scale=scaler.scale_.tolist(), coefficients=model.coef_.tolist(),
    intercept=float(model.intercept_[0]), epochs=int(model.n_iter_),
    settings=dict(learning_rate=.01, penalty=None, max_epochs=5000),
    ranges=[dict(min=float(X[train,i].min()),max=float(X[train,i].max())) for i in range(3)],
    metrics=dict(train=metrics(y[train],model.predict(xt)),test=metrics(y[test],pred),
                 least_squares=metrics(y[test],ols.predict(xv)),baseline=metrics(y[test],baseline.predict(xv))),
    test_examples=[dict(row=int(i)+1,inputs=X[i].tolist(),actual=float(y[i]),prediction=float(p)) for i,p in zip(test,pred)])
# Verify the browser's exported prediction formula against scikit-learn.
exported=((X[test]-np.array(artifact['mean']))/np.array(artifact['scale']))@np.array(artifact['coefficients'])+artifact['intercept']
np.testing.assert_allclose(exported,pred,rtol=1e-12,atol=1e-12)
assert not set(train)&set(test)
assert artifact['metrics']['test']['rmse'] < artifact['metrics']['baseline']['rmse']
out=ROOT/'dist/models';out.mkdir(exist_ok=True)
(out/'sales-sgd.json').write_text(json.dumps(artifact,indent=2)+'\n')
print(json.dumps(dict(epochs=artifact['epochs'],metrics=artifact['metrics']),indent=2))
