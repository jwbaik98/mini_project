
# 정지선 좌표 확인

import cv2
import numpy as np
import threading
import queue

# CCTV 주소 설정
cctv_url = "http://210.99.70.120:1935/live/cctv006.stream/playlist.m3u8"
pts = []

# 목표 해상도 설정
TARGET_W, TARGET_H = 640, 360

frame_queue = queue.Queue(maxsize=1)

def video_reader():
    cap = cv2.VideoCapture(cctv_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # [수정 부분 1] 읽어온 즉시 640x360으로 리사이즈
        frame = cv2.resize(frame, (TARGET_W, TARGET_H))
        
        if not frame_queue.empty():
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass
        frame_queue.put(frame)
    cap.release()

# ... (draw_roi 함수는 동일)

def draw_roi(event, x, y, flags, param):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append((x, y))
        print(f"📍 좌표 등록 (640x360 기준): ({x}, {y})")

# ... (스레드 시작 부분 동일)

reader_thread = threading.Thread(target=video_reader, daemon=True)
reader_thread.start()

cv2.namedWindow('Select ROI')
cv2.setMouseCallback('Select ROI', draw_roi)

while True:
    if not frame_queue.empty():
        frame = frame_queue.get()
        
        # [수정 부분 2] 이미 리사이즈된 frame 위에 그리기
        for p in pts:
            cv2.circle(frame, p, 5, (0, 255, 0), -1)
        
        if len(pts) == 4:
            cv2.polylines(frame, [np.array(pts)], True, (0, 255, 255), 2)

        cv2.imshow('Select ROI', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print(f"\n✅ 640x360 기준 최종 좌표: {pts}")
        break
    elif key == ord('r'):
        pts = []
        print("🔄 좌표 초기화")

cv2.destroyAllWindows()