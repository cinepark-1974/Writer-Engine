import os
import streamlit as st
from anthropic import Anthropic

from prompt import (
    SYSTEM_PROMPT,
    build_input_summary_prompt,
    build_scene_draft_prompt,
    build_dialogue_polish_prompt,
    build_qc_prompt,
)

ANTHROPIC_MODEL = "claude-sonnet-4-6"

# 고정값
GENRE = "느와르"
FORMAT = "시리즈"

st.set_page_config(
    page_title="BLUE JEANS · Writer Engine",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────
# API
# ─────────────────────────────
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
    if not api_key:
        return None
    return Anthropic(api_key=api_key)


def run_ai(prompt):
    client = get_client()

    if not client:
        return "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return "".join([b.text for b in response.content if hasattr(b, "text")])


# ─────────────────────────────
# HEADER
# ─────────────────────────────
st.markdown(
"""
### BLUE JEANS PICTURES
# WRITER ENGINE
""")

st.info(f"장르: {GENRE}  |  포맷: {FORMAT}")

# ─────────────────────────────
# MODE
# ─────────────────────────────
MODE = st.selectbox(
    "작업 모드",
    [
        "입력 정리 (Input Summary)",
        "씬 작성 (Scene Draft)",
        "대사 다듬기 (Dialogue Polish)",
        "품질 점검 (Quality Control)",
    ],
)

# ─────────────────────────────
# INPUT
# ─────────────────────────────
title = st.text_input("프로젝트 제목")
logline = st.text_area("Logline")
intent = st.text_area("Project Intent")
gns = st.text_area("Goal / Need / Strategy")
characters = st.text_area("Character")
world = st.text_area("World Build")
structure = st.text_area("Structure")
scene_design = st.text_area("Scene Design")
treatment = st.text_area("Treatment")
tone = st.text_area("Tone Document")

# ─────────────────────────────
# PROMPT BUILD
# ─────────────────────────────
prompt = ""

if MODE.startswith("입력 정리"):
    prompt = build_input_summary_prompt(
        title,
        GENRE,
        FORMAT,
        logline,
        intent,
        gns,
        characters,
        world,
        structure,
        scene_design,
        treatment,
        tone,
    )

elif MODE.startswith("씬 작성"):
    scene_request = st.text_area("어떤 장면을 쓸지")
    prompt = build_scene_draft_prompt(
        title,
        GENRE,
        FORMAT,
        logline,
        characters,
        structure,
        scene_design,
        treatment,
        tone,
        scene_request,
    )

elif MODE.startswith("대사"):
    dialogue_notes = st.text_area("캐릭터 보이스")
    scene_text = st.text_area("씬 텍스트")

    prompt = build_dialogue_polish_prompt(
        GENRE,
        dialogue_notes,
        scene_text,
    )

elif MODE.startswith("품질"):
    qc_text = st.text_area("검토할 텍스트")

    prompt = build_qc_prompt(
        GENRE,
        logline,
        qc_text,
    )

# ─────────────────────────────
# RUN
# ─────────────────────────────
if st.button("실행"):
    result = run_ai(prompt)
    st.session_state["result"] = result

# ─────────────────────────────
# OUTPUT
# ─────────────────────────────
if "result" in st.session_state:
    text = st.text_area(
        "결과 (수정 가능)",
        value=st.session_state["result"],
        height=500,
    )

    st.download_button(
        "TXT 다운로드",
        text,
        file_name="writer_output.txt",
    )
