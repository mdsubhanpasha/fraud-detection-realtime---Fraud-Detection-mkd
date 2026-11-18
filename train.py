import pickle, random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
random.seed(42)
rows=[]
for i in range(1000):
    amt = random.randint(100, 100000)
    is_night = random.randint(0,1)
    is_foreign = random.randint(0,1)
    is_new_device = random.randint(0,1)
    txn_count_1h = random.randint(1,10)
    fraud = 1 if (amt>50000 and is_night==1) or (is_foreign==1 and is_new_device==1 and txn_count_1h>5) or (amt>80000 and txn_count_1h>7) else 0
    rows.append([amt, is_night, is_foreign, is_new_device, txn_count_1h, fraud])
df = pd.DataFrame(rows, columns=['amount','is_night','is_foreign','is_new_device','txn_count_1h','fraud'])
X = df.drop('fraud', axis=1); y = df['fraud']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
print(f'Train Accuracy: {model.score(X,y)*100:.1f}% | Fraud: {y.sum()} / {len(y)}')
with open('model.pkl','wb') as f: pickle.dump(model, f)
print('Saved model.pkl')
