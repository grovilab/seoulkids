# -*- coding: utf-8 -*-
"""
[페이지] 서울형 키즈카페 자치구별 그래프 시각화
- 데이터: 서울형 키즈카페 시설현황정보.csv (cp949)
- pandas + streamlit + altair
"""
import os

import altair as alt
import pandas as pd
import streamlit as st

# views/ 하위 → 데이터가 있는 리포지토리 루트로 한 단계 위로.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE_DIR, "서울형 키즈카페 시설현황정보.csv")


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV, encoding="cp949")
    df["자치구명"] = df["자치구명"].astype(str).str.strip()
    df["무료여부"] = df["사용료무료여부"].map({"Y": "무료", "N": "유료"}).fillna("미상")
    return df


df = load_data()

st.title("🧸 서울형 키즈카페 자치구별 현황")
st.caption(f"데이터 출처: 서울특별시 · 총 {len(df)}개 시설")

with st.sidebar:
    st.header("필터")
    gu_all = sorted(df["자치구명"].unique().tolist())
    sel_gu = st.multiselect("자치구 선택", gu_all, default=gu_all)
    sel_fee = st.multiselect(
        "사용료", ["무료", "유료", "미상"], default=["무료", "유료", "미상"]
    )

view = df[df["자치구명"].isin(sel_gu) & df["무료여부"].isin(sel_fee)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("전체 시설 수", f"{len(view)} 개")
c2.metric("자치구 수", f"{view['자치구명'].nunique()} 개구")
if not view.empty:
    top_gu = view["자치구명"].value_counts().idxmax()
    top_n = int(view["자치구명"].value_counts().max())
    c3.metric("최다 자치구", f"{top_gu}", f"{top_n}개")
else:
    c3.metric("최다 자치구", "-")
c4.metric("무료 시설", f"{int((view['무료여부'] == '무료').sum())} 개")

if view.empty:
    st.warning("선택한 조건에 해당하는 시설이 없습니다.")
    st.stop()

st.divider()

st.subheader("① 자치구별 키즈카페 수")
gu_count = (
    view.groupby("자치구명").size().reset_index(name="시설수").sort_values("시설수", ascending=False)
)
bar = (
    alt.Chart(gu_count)
    .mark_bar(cornerRadiusEnd=4, color="#4C78A8")
    .encode(
        x=alt.X("시설수:Q", title="시설 수"),
        y=alt.Y("자치구명:N", sort="-x", title=None),
        tooltip=["자치구명", "시설수"],
    )
    .properties(height=max(300, len(gu_count) * 24))
)
labels = bar.mark_text(align="left", dx=3, color="#333").encode(text="시설수:Q")
st.altair_chart(bar + labels, width="stretch")

st.subheader("② 자치구별 사용료(무료/유료) 구성")
fee_count = view.groupby(["자치구명", "무료여부"]).size().reset_index(name="시설수")
order = gu_count["자치구명"].tolist()
stacked = (
    alt.Chart(fee_count)
    .mark_bar()
    .encode(
        x=alt.X("시설수:Q", title="시설 수", stack="zero"),
        y=alt.Y("자치구명:N", sort=order, title=None),
        color=alt.Color(
            "무료여부:N",
            title="사용료",
            scale=alt.Scale(
                domain=["무료", "유료", "미상"],
                range=["#59A14F", "#E15759", "#BAB0AC"],
            ),
        ),
        tooltip=["자치구명", "무료여부", "시설수"],
    )
    .properties(height=max(300, len(order) * 24))
)
st.altair_chart(stacked, width="stretch")

st.subheader("📋 시설 목록")
st.dataframe(
    view[["자치구명", "시설명", "무료여부", "연락처", "기본주소", "신청가능연령"]]
    .sort_values("자치구명")
    .reset_index(drop=True),
    width="stretch",
    hide_index=True,
)
