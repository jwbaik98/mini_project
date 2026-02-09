
# 감지 시스템

import cv2
from ultralytics import YOLO
from shapely.geometry import Point, Polygon
import numpy as np
from db_manager import save_violation

# 모델 로드 (최신 YOLOv11 또는 YOLO26 환경)
model = YOLO('yolo26n.pt').to('cpu')

# 구역 설정 (640x360 해상도 기준)
stop_line_coords = [(168, 199), (162, 224), (400, 211), (392, 176)]
stop_zone = Polygon(stop_line_coords)
saved_ids = set()

def check_violation(frame, signal_color='RED'):
    # 좌표 일치를 위한 강제 리사이즈
    frame = cv2.resize(frame, (640, 360))
    results = model.track(frame, persist=True, verbose=False)
    violations = []
    
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy().astype(int) # 정수형 변환
        clss = results[0].boxes.cls.cpu().numpy().astype(int)
        
        for box, obj_id, cls in zip(boxes, ids, clss):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[cls]
            center = Point((x1 + x2) / 2, (y1 + y2) / 2)
            
            color = (0, 255, 0) # 기본 녹색
            display_text = ""   
            is_violating = False
            
            # 차량 그룹(car, bus, truck) 필터링
            if label in ['car', 'bus', 'truck', 'motorcycle']:
                display_text = f"ID: {int(obj_id)}" # 확실한 정수 처리
                if signal_color == 'RED' and stop_zone.contains(center):
                    is_violating = True
                    color = (0, 0, 255) # 위반 시 빨간색
                    violations.append(f"ID {obj_id} 위반")

            # 모든 객체 박스 그리기
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # 차량일 때만 깔끔한 ID 라벨 표시
            if display_text:
                (w, h), _ = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                cv2.rectangle(frame, (x1, y1 - 22), (x1 + w, y1), color, -1) # 라벨 배경
                cv2.putText(frame, display_text, (x1, y1 - 7), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # 위반 시 즉시 크롭 저장
            if is_violating and obj_id not in saved_ids:
                # 박스까지 그려진 현재 frame을 전달
                save_violation("정지선 위반", int(obj_id), frame, bbox=[x1, y1, x2, y2])
                saved_ids.add(obj_id)

    # 정지선 가이드라인 표시
    cv2.polylines(frame, [np.array(stop_line_coords)], True, (255, 0, 0), 2)
    return frame, violations