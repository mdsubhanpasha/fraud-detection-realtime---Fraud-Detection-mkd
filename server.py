from flask import Flask, render_template, request, jsonify
import pickle, os
app = Flask(__name__)
model = pickle.load(open('model.pkl','rb')) if os.path.exists('model.pkl') else None
@app.route('/')
def home(): return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    d = request.json
    amt = float(d.get('amount', 0)); is_night = int(d.get('is_night', 0)); is_foreign = int(d.get('is_foreign', 0)); is_new_device = int(d.get('is_new_device', 0)); txn_count = int(d.get('txn_count_1h', 1))
    prob = model.predict_proba([[amt, is_night, is_foreign, is_new_device, txn_count]])[0][1] * 100 if model else 10
    reasons = []
    if amt > 50000: prob += 15; reasons.append('High Amount > Rs.50,000')
    if is_night == 1: prob += 10; reasons.append('Night Transaction (12AM-5AM)')
    if is_foreign == 1: prob += 20; reasons.append('Foreign Location')
    if is_new_device == 1: prob += 15; reasons.append('New Device')
    if txn_count > 5: prob += 20; reasons.append(f'High Velocity: {txn_count} txns in 1 hour')
    prob = min(99, max(1, int(prob)))
    level = 'HIGH RISK - BLOCK' if prob >= 80 else 'MEDIUM RISK - REVIEW' if prob >= 50 else 'SAFE - ALLOW'
    color = 'red' if prob >= 80 else 'orange' if prob >= 50 else 'green'
    if not reasons: reasons = ['Normal pattern - No suspicious signals']
    return jsonify({'score': prob, 'level': level, 'color': color, 'reasons': reasons})
if __name__ == '__main__':
    print('FRAUD-DETECTION Running on http://127.0.0.1:8001')
    app.run(port=8001, debug=True)
