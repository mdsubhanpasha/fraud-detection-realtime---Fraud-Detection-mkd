# server.py - Pure Python http.server, No Flask needed!
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200); self.send_header('Content-type','text/html'); self.end_headers()
            self.wfile.write(open('templates/index.html','rb').read())
        else:
            self.send_response(404); self.end_headers()
    def do_POST(self):
        if self.path == '/predict':
            length = int(self.headers['Content-Length'])
            d = json.loads(self.rfile.read(length))
            amt = float(d.get('amount', 0)); is_night = int(d.get('is_night', 0)); is_foreign = int(d.get('is_foreign', 0)); is_new_device = int(d.get('is_new_device', 0)); txn_count = int(d.get('txn_count_1h', 1))
            prob = 10
            reasons = []
            if amt > 50000: prob += 25; reasons.append('High Amount > Rs.50,000')
            if is_night == 1: prob += 12; reasons.append('Night Transaction (12AM-5AM)')
            if is_foreign == 1: prob += 22; reasons.append('Foreign Location')
            if is_new_device == 1: prob += 18; reasons.append('New Device')
            if txn_count > 5: prob += 20; reasons.append(f'High Velocity: {txn_count} txns in 1 hour')
            if amt > 80000 and txn_count > 7: prob += 10; reasons.append('Very High Amount + High Velocity')
            prob = min(99, max(1, int(prob)))
            level = 'HIGH RISK - BLOCK' if prob >= 80 else 'MEDIUM RISK - REVIEW' if prob >= 50 else 'SAFE - ALLOW'
            color = 'red' if prob >= 80 else 'orange' if prob >= 50 else 'green'
            if not reasons: reasons = ['Normal pattern - No suspicious signals']
            out = {'score': prob, 'level': level, 'color': color, 'reasons': reasons}
            self.send_response(200); self.send_header('Content-type','application/json'); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers()
            self.wfile.write(json.dumps(out).encode())
    def log_message(self, format, *args): print(f"{self.address_string()} - {format%args}")

if __name__ == '__main__':
    print('FRAUD-DETECTION Running on http://127.0.0.1:8001 - Pure Python, No pip needed!')
    HTTPServer(('127.0.0.1', 8001), Handler).serve_forever()
