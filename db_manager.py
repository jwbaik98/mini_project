
# 데이터 베이스(스크린샷 저장)

import sqlite3
import os
import cv2
from datetime import datetime

SAVE_DIR = os.path.join('static', 'evidence')

def init_db():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR, exist_ok=True)
    conn = sqlite3.connect('violations.db')
    c = conn.cursor()
    # object_id를 INTEGER 타입으로 확실히 지정
    c.execute('''CREATE TABLE IF NOT EXISTS violations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  type TEXT,
                  object_id INTEGER,
                  image_path TEXT)''')
    conn.commit()
    conn.close()

def save_violation(v_type, obj_id, frame, bbox=None):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    file_time = now.strftime('%Y%m%d_%H%M%S')
    
    # 💡 [보완] obj_id를 명확하게 파이썬 정수(int)로 변환
    clean_id = int(obj_id)
    
    img_filename = f"crop_{file_time}_{clean_id}.jpg"
    img_path = os.path.join(SAVE_DIR, img_filename)
    
    if bbox:
        x1, y1, x2, y2 = map(int, bbox)
        save_img = frame[max(0, y1):y2, max(0, x1):x2]
    else:
        save_img = frame
        
    cv2.imwrite(img_path, save_img)
    
    conn = sqlite3.connect('violations.db')
    c = conn.cursor()
    web_path = f"static/evidence/{img_filename}"
    # 데이터를 넣을 때 다시 한번 int() 확인
    c.execute("INSERT INTO violations (timestamp, type, object_id, image_path) VALUES (?, ?, ?, ?)",
              (timestamp, v_type, clean_id, web_path))
    conn.commit()
    conn.close()

def get_violation_list():
    try:
        conn = sqlite3.connect('violations.db')
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()
        c.execute("SELECT * FROM violations ORDER BY timestamp DESC LIMIT 10")
        rows = c.fetchall()
        
        data = []
        for row in rows:
            # 💡 [보완] DB에서 읽어온 값이 바이트일 경우를 대비한 예외 처리
            try:
                raw_id = row['object_id']
                if isinstance(raw_id, bytes):
                    # 바이트 데이터인 경우 강제로 숫자로 해석하거나 0으로 처리
                    display_id = int.from_bytes(raw_id, 'little') if len(raw_id) <= 8 else 0
                else:
                    display_id = int(raw_id)
            except:
                display_id = 0

            data.append({
                'timestamp': row['timestamp'],
                'type': row['type'],
                'object_id': display_id,
                'image_path': row['image_path']
            })
        conn.close()
        return data
    except Exception as e:
        print(f"❌ DB 조회 에러: {e}")
        return []