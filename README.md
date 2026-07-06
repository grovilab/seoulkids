# 👶 서울 육아 인프라 대시보드

서울시 공공데이터를 활용한 육아 인프라 시각화 Streamlit 멀티페이지 앱입니다.

## 📑 페이지

| 페이지 | 내용 | 데이터 |
|--------|------|--------|
| 🗺️ 아이휴센터 지도 | 노원구 아이휴센터 29개소 위치를 지도에 표시 | `서울특별시 노원구_아이휴센터_20260414.csv` |
| 🧸 키즈카페 통계 | 서울형 키즈카페를 자치구별 그래프로 시각화 | `서울형 키즈카페 시설현황정보.csv` |

## 🗂️ 파일 구조

```
.
├── streamlit_app.py                    # 배포 엔트리(홈) 파일
├── pages/
│   ├── 1_🗺️_아이휴센터_지도.py
│   └── 2_🧸_키즈카페_통계.py
├── requirements.txt                    # 배포 의존성
├── .streamlit/config.toml              # 테마/설정
├── 서울특별시 노원구_아이휴센터_20260414.csv
├── 아이휴센터_좌표.csv                    # 지오코딩 좌표 캐시
├── 서울형 키즈카페 시설현황정보.csv
└── app_gui.py                          # (참고) tkinter 데스크톱 버전 — 클라우드 배포 대상 아님
```

## 🚀 로컬 실행

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## ☁️ Streamlit Community Cloud 배포

1. 이 폴더를 GitHub 저장소에 push 합니다.
2. [share.streamlit.io](https://share.streamlit.io) 접속 → **New app**.
3. 저장소 / 브랜치 선택 후 **Main file path** 를 `streamlit_app.py` 로 지정.
4. **Deploy** 클릭.

> `requirements.txt` 가 자동으로 설치되며, CSV 데이터 파일이 저장소에 포함되어 있어야 합니다.
> 지도 페이지는 좌표 캐시(`아이휴센터_좌표.csv`)를 사용하므로 별도 API 키가 필요 없습니다.

## 📊 데이터 출처

서울특별시 · 노원구 공공데이터
