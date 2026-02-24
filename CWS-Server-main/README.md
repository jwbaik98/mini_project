# CWS-Server (CCTV Web System Server)

## 프로젝트 개요
Yellow YOLO CCTV 관제 대시보드 웹 애플리케이션

Flask 기반의 CCTV 모니터링 시스템으로, 실시간 영상 스트림, ROI 설정, 위반 차량 조회 등의 기능을 제공합니다.

## 주요 기능
- 📺 실시간 CCTV 모니터링
- 🎯 ROI (Region of Interest) 설정
- 🚨 위반 차량 조회 및 기록
- ⚙️ 시스템 설정
- 📊 통계 대시보드

## 프로젝트 구조
```
CWS-Server-main/
├── src/
│   ├── app.py                    # Flask 메인 애플리케이션
│   ├── database.py              # 데이터베이스 관리
│   ├── static/                  # 정적 파일
│   │   ├── css/
│   │   │   └── styles.css      # 메인 스타일시트
│   │   ├── js/
│   │   │   └── logic.js        # 클라이언트 사이드 로직
│   │   └── images/
│   │       └── logo.png        # 로고 이미지
│   └── templates/              # Flask 템플릿
│       ├── layout.html         # 기본 레이아웃 템플릿
│       ├── common/            # 공통 템플릿 컴포넌트
│       │   ├── header.html    # 헤더
│       │   ├── nav.html       # 네비게이션
│       │   └── footer.html    # 푸터
│       └── content/           # 페이지 콘텐츠
│           ├── index.html     # 메인 페이지
│           └── monitoring.html # 모니터링 페이지
└── README.md
```

## 설치 및 실행

### 1. 필수 패키지 설치
```bash
pip install flask
```

### 2. 서버 실행
```bash
cd src
python app.py
```

### 3. 브라우저 접속
```
http://localhost:5000
```

## 파일 설명

### Backend
- **app.py**: Flask 라우팅 및 API 엔드포인트 정의
  - `/` - 기본 대시보드
  - `/api/v1/update` - 위반 데이터 수신 API
  - `/get_status` - 위반 기록 조회 API
  
- **database.py**: SQLite 데이터베이스 관리 함수

### Frontend
- **styles.css**: 전체 UI 스타일 정의 (다크 테마)
- **logic.js**: 
  - 페이지 전환 로직
  - ROI 좌표 설정 기능
  - 비디오/이미지 업로드 처리
  - 위반 카드 동적 추가

### Templates
- **layout.html**: Jinja2 기본 템플릿 (header, nav, footer 포함)
- **common/**: 재사용 가능한 공통 컴포넌트
- **content/**: 실제 페이지 콘텐츠

## Flask 사용 가이드

현재 HTML 파일들은 Flask url_for() 방식을 사용하고 있습니다. 정적 파일로만 사용하려면 주석 처리된 직접 참조 경로를 활성화하세요.

### 코드 내 `#` 주석 표시
파일 내에 `# TODO:` 또는 `#` 주석으로 표시된 부분은 추가 구현이나 정적 참조 방식입니다.

#### 예시:
```html
<!-- Flask 방식 (현재 사용 중) -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}" />

<!-- 직접 참조 (주석 처리됨) -->
<!-- # 직접 참조: <link rel="stylesheet" href="../../static/css/styles.css" /> -->
```

### Flask 사용법
1. **정적 파일 경로**: `url_for('static', filename='...')` 사용 (현재 적용됨)
2. **라우팅**: app.py에 페이지 라우트 추가 필요
3. **템플릿 상속**: `{% extends 'layout.html' %}` 활용 (현재 적용됨)
4. **동적 데이터**: Jinja2 템플릿 문법으로 서버 데이터 렌더링

### 정적 파일로만 사용하려면:
주석 처리된 직접 참조 경로를 활성화하고, Flask url_for() 코드를 주석 처리하세요.

## 기능 설명

### 1. Overview 페이지
- 카메라 수, 알람 수, 연결 상태 등 통계 정보 표시

### 2. Live Feeds 페이지
- 실시간 영상 스트림 표시
- ROI 영역 설정 기능
- 비디오/이미지 파일 업로드
- 신호등 전광판 상태 표시
- 위반 내역 실시간 표시

### 3. Playback 페이지
- 위반 차량 조회
- 차량번호, 시간, 위치 정보 표시

### 4. Settings 페이지
- 서버 주소 설정
- 해상도 설정

## 변경 사항

### mini_project-main에서 마이그레이션
- ✅ 로그인 기능 제거 (모든 기능 제한 없이 사용 가능)
- ✅ `그림1.png` → `logo.png`로 이름 변경
- ✅ `script.js` → `logic.js`로 이동 및 로그인 로직 제거
- ✅ Flask 템플릿 상속 구조 구현
- ✅ 공통 컴포넌트 분리 (header, nav, footer)
- ✅ Flask url_for() 방식으로 정적 파일 경로 설정

## 개발 계획
- [ ] app.py에 index, monitoring 라우트 추가
- [ ] 데이터베이스 연동 강화
- [ ] 실시간 비디오 스트리밍 구현
- [ ] ROI 데이터 서버 전송 및 저장 (/api/roi)
- [ ] 위반 차량 이미지 업로드 및 저장
- [ ] 위반 데이터 조회 API 개선

## 라이선스
MIT License

## 문의
프로젝트 관련 문의사항은 이슈를 등록해주세요.
