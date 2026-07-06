# -*- coding: utf-8 -*-
"""
서울 육아 인프라 대시보드 - 멀티페이지 엔트리
Streamlit Community Cloud 배포용 메인 파일.

st.navigation 으로 페이지를 명시적으로 등록하므로,
파일명(이모지/한글) 인식 문제 없이 항상 사이드바 내비게이션이 표시됩니다.
실행:  streamlit run streamlit_app.py
"""
import streamlit as st

st.set_page_config(
    page_title="서울 육아 인프라 대시보드",
    page_icon="👶",
    layout="wide",
)

home = st.Page("views/home.py", title="홈", icon="👶", default=True)
map_page = st.Page("views/map_ihue.py", title="아이휴센터 지도", icon="🗺️")
cafe_page = st.Page("views/kids_cafe.py", title="키즈카페 통계", icon="🧸")

nav = st.navigation([home, map_page, cafe_page])
nav.run()
