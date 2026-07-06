# -*- coding: utf-8 -*-
"""
[페이지] 노원구 아이휴센터 위치 지도
- 원본 데이터: 서울특별시 노원구_아이휴센터_20260414.csv (cp949)
- 좌표 캐시:   아이휴센터_좌표.csv (없거나 누락 시 Nominatim 지오코딩)
"""
import os
import re
import time

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

# 이 파일은 views/ 하위에 있으므로 데이터가 있는 리포지토리 루트로 한 단계 올라간다.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_CSV = os.path.join(BASE_DIR, "서울특별시 노원구_아이휴센터_20260414.csv")
COORD_CSV = os.path.join(BASE_DIR, "아이휴센터_좌표.csv")

NOWON_CENTER = (37.6542, 127.0568)


def geocode(query: str):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 1, "countrycodes": "kr"},
            headers={"User-Agent": "nowon-ihue-map/1.0"},
            timeout=20,
        )
        j = r.json()
        if j:
            return float(j[0]["lat"]), float(j[0]["lon"])
    except Exception:
        pass
    return None


def simplify_addr(addr: str) -> str:
    return re.split(r"[,(]", str(addr))[0].strip()


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(SRC_CSV, encoding="cp949")
    df.columns = ["번호", "센터명", "동", "연락처", "주소", "기준일자"]

    if os.path.exists(COORD_CSV):
        coord = pd.read_csv(COORD_CSV, encoding="utf-8-sig")[["주소", "위도", "경도"]]
        df = df.merge(coord, on="주소", how="left")
    else:
        df["위도"] = pd.NA
        df["경도"] = pd.NA

    missing = df["위도"].isna()
    if missing.any():
        for idx in df[missing].index:
            addr = simplify_addr(df.at[idx, "주소"])
            res = geocode(addr) or geocode(addr + " 노원구")
            if res:
                df.at[idx, "위도"], df.at[idx, "경도"] = res
            time.sleep(1.1)
        df.to_csv(COORD_CSV, index=False, encoding="utf-8-sig")

    df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
    df["경도"] = pd.to_numeric(df["경도"], errors="coerce")
    return df


st.title("🗺️ 서울특별시 노원구 아이휴센터 위치")
st.caption("기준일자: 2026-04-14 · 데이터 출처: 서울특별시 노원구")

df = load_data()

with st.sidebar:
    st.header("필터")
    dongs = sorted(df["동"].dropna().unique().tolist())
    selected = st.multiselect("동 선택", dongs, default=dongs)
    keyword = st.text_input("센터명 검색", "")

view = df[df["동"].isin(selected)]
if keyword:
    view = view[view["센터명"].str.contains(keyword, case=False, na=False)]

map_df = view.dropna(subset=["위도", "경도"]).copy()

c1, c2, c3 = st.columns(3)
c1.metric("전체 센터 수", f"{len(df)} 개소")
c2.metric("표시 중", f"{len(view)} 개소")
c3.metric("지도 표시(좌표 확보)", f"{len(map_df)} 개소")

if map_df.empty:
    st.warning("표시할 센터가 없습니다. 필터를 확인해 주세요.")
else:
    tooltip = {
        "html": "<b>{센터명}</b><br/>📍 {주소}<br/>📞 {연락처}",
        "style": {"backgroundColor": "#1f2937", "color": "white", "fontSize": "12px"},
    }
    scatter = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[경도, 위도]",
        get_fill_color="[233, 69, 96, 200]",
        get_radius=120,
        radius_min_pixels=6,
        radius_max_pixels=30,
        pickable=True,
    )
    text = pdk.Layer(
        "TextLayer",
        data=map_df,
        get_position="[경도, 위도]",
        get_text="센터명",
        get_size=12,
        get_color="[30, 30, 30]",
        get_alignment_baseline="'top'",
        get_pixel_offset="[0, 10]",
    )
    view_state = pdk.ViewState(
        latitude=map_df["위도"].mean() if not map_df.empty else NOWON_CENTER[0],
        longitude=map_df["경도"].mean() if not map_df.empty else NOWON_CENTER[1],
        zoom=12,
    )
    st.pydeck_chart(
        pdk.Deck(
            layers=[scatter, text],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="light",
        )
    )

st.subheader("📋 센터 목록")
st.dataframe(
    view[["번호", "센터명", "동", "연락처", "주소"]].reset_index(drop=True),
    width="stretch",
    hide_index=True,
)
