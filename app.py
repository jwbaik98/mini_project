
# 전체 작동 구동시스템

import cv2
import threading
import webbrowser
import time
from flask import Flask, render_template, Response
from detection import check_violation
from db_manager import init_db, get_violation_list
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)
cctv_url = "http://210.99.70.120:1935/live/cctv006.stream/playlist.m3u8"
camera = cv2.VideoCapture(cctv_url)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            time.sleep(1)
            camera.open(cctv_url)
            continue
        
        # 분석 실행 및 결과 프레임 획득
        processed_frame, _ = check_violation(frame)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
@app.route('/api/violations')
def api_violations():
    # DB의 최신 리스트를 JSON 형식으로 반환 (실시간 갱신용)
    violations = get_violation_list()
    return jsonify(violations)        

@app.route('/')
def index():
    violations = get_violation_list()
    return render_template('index.html', violations=violations)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    init_db() # DB 초기화
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
@app.route('/api/violations')
def api_violations():
    violations = get_violation_list()
    return jsonify(violations) # 이 부분이 JSON 데이터를 전송함