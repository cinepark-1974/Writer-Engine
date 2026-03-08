import os
from datetime import datetime

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

# ─────────────────────────────────────
# 고정값
# ─────────────────────────────────────
FIXED_GENRE = "느와르"
FIXED_FORMAT = "시리즈"

# ─────────────────────────────────────
# Page Config
# ─────────────────────────────────────
st.set_page_config(
    page_title="BLUE JEANS · Writer Engine",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────
# Custom CSS  (Creator Engine 톤 유지)
# ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/2408-3@latest/Paperlogy.css');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');

:root {
    --navy: #191970;
    --y: #FFCB05;
    --bg: #F7F7F5;
    --card: #FFFFFF;
    --card-border: #E2E2E0;
    --t: #1A1A2E;
    --r: #D32F2F;
    --g: #2EC484;
    --dim: #8E8E99;
    --light-bg: #EEEEF6;
    --serif: 'Paperlogy', 'Noto Serif KR', 'Georgia', serif;
    --display: 'Playfair Display', 'Paperlogy', 'Georgia', serif;
    --body: 'Pretendard', -apple-system, sans-serif;
    --heading: 'Paperlogy', 'Pretendard', sans-serif;
}

/* 기본 타이포 */
html, body, [class*="css"] {
    font-family: var(--body);
    color: var(--t);
    -webkit-font-smoothing: antialiased;
}

/* 라이트모드 강제 */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], [data-testid="stHeader"],
[data-testid="stBottom"] {
    background-color: var(--bg) !important;
    color: var(--t) !important;
}
.stMarkdown, .stText, .stCode {
    color: var(--t) !important;
}
h1, h2, h3, h4, h5, h6 {
    color: var(--navy) !important;
    font-family: var(--heading) !important;
}
p, span, label, div, li {
    color: inherit;
}

/* 사이드바 숨김 */
section[data-testid="stSidebar"] {
    display: none;
}

/* 입력 위젯 */
.stTextInput input, .stTextArea textarea,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background-color: var(--card) !important;
    color: var(--t) !important;
    border: 1.5px solid var(--card-border) !important;
    border-radius: 8px !important;
    font-family: var(--body) !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 0.85rem !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus, .stTextArea textarea:focus,
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
    border-color: var(--navy) !important;
    box-shadow: 0 0 0 2px rgba(25,25,112,0.08) !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder,
[data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder {
    color: var(--dim) !important;
    font-size: 0.85rem !important;
}

/* selectbox */
.stSelectbox > div > div, [data-baseweb="select"] > div, [data-baseweb="select"] input {
    background-color: var(--card) !important;
    color: var(--t) !important;
    border-color: var(--card-border) !important;
    border-radius: 8px !important;
}
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"], [role="option"] {
    background-color: var(--card) !important;
    color: var(--t) !important;
}
[role="option"]:hover {
    background-color: var(--light-bg) !important;
}

/* label */
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--t) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    margin-bottom: 0.3rem !important;
}

/* 버튼 */
.stButton > button {
    color: var(--t) !important;
    border: 1.5px solid var(--card-border) !important;
    background-color: var(--card) !important;
    border-radius: 8px !important;
    font-family: var(--body) !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    border-color: var(--navy) !important;
    box-shadow: 0 2px 8px rgba(25,25,112,0.08) !important;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background-color: var(--y) !important;
    color: var(--navy) !important;
    border-color: var(--y) !important;
    font-weight: 800 !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background-color: #E8B800 !important;
    box-shadow: 0 2px 12px rgba(255,203,5,0.3) !important;
}

/* 다운로드 버튼 */
.stDownloadButton > button {
    color: var(--navy) !important;
    border: 1.5px solid var(--y) !important;
    background-color: var(--y) !important;
    border-radius: 8px !important;
    font-family: var(--body) !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.2rem !important;
}

/* Expander */
.stExpander, details, details summary {
    background-color: var(--card) !important;
    color: var(--t) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 8px !important;
}
details[open] > div {
    background-color: var(--card) !important;
}
.stExpander summary, .stExpander summary span {
    color: var(--t) !important;
}

/* Alert */
.stAlert {
    color: var(--t) !important;
    border-radius: 8px !important;
}

/* 내부 컨테이너 */
[data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"],
[data-testid="stColumn"] {
    background-color: transparent !important;
}

/* 커스텀 UI */
.header {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.15em;
    margin-bottom: 0;
    font-family: var(--heading);
}

.brand-title {
    font-size: 2.6rem;
    font-weight: 900;
    color: var(--navy);
    font-family: var(--display);
    letter-spacing: -0.02em;
    margin-bottom: 0.15rem;
    position: relative;
    display: inline-block;
}
.brand-title::after {
    content: '';
    position: absolute;
    bottom: 2px;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--y);
    border-radius: 2px;
}

.sub {
    font-size: 0.7rem;
    color: var(--dim);
    letter-spacing: 0.15em;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}

.card {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}

.callout {
    background: var(--light-bg);
    border-left: 4px solid var(--navy);
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.88rem;
    color: var(--t);
}

.cl {
    color: var(--navy);
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.03em;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
}

.section-header {
    background: var(--y);
    color: var(--navy);
    padding: 0.6rem 1rem;
    border-radius: 6px;
    font-weight: 800;
    font-size: 1rem;
    font-family: var(--heading);
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.section-header .en {
    font-family: var(--display);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    opacity: 0.7;
}
.small-meta {
    font-size: 0.78rem;
    color: var(--dim);
    margin-top: -0.2rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Session State
# ─────────────────────────────────────
defaults = {
    "result_text": "",
    "saved_label": "",
    "last_prompt": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ─────────────────────────────────────
# Helpers
# ─────────────────────────────────────
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
    if not api_key:
        return None
    return Anthropic(api_key=api_key)

def run_ai(prompt_text: str) -> str:
    client = get_client()
    if not client:
        return "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."

    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt_text}],
        )

        parts = []
        for block in response.content:
            if hasattr(block, "text"):
                parts.append(block.text)

        if not parts:
            return "[EMPTY RESPONSE]"

        return "\n".join(parts).strip()

    except Exception as e:
        return f"❌ 오류: {str(e)}"

def build_revision_prompt(base_prompt: str, current_text: str) -> str:
    return (
        f"{base_prompt}\n\n"
        "[REVISION INSTRUCTION]\n"
        "Use the current draft below as the base text. "
        "Improve clarity, dramatic force, subtext, character distinction, and cinematic readability "
        "without losing the existing strengths.\n\n"
        "[CURRENT DRAFT]\n"
        f"{current_text}"
    )

# ─────────────────────────────────────
# Header
# ─────────────────────────────────────
st.markdown(
    '<div style="text-align:center;padding:1rem 0 0 0">'
    '<div class="header">B L U E &nbsp; J E A N S &nbsp; P I C T U R E S</div>'
    '<div class="brand-title">WRITER ENGINE</div>'
    '<div class="sub">Y O U N G &nbsp; · &nbsp; V I N T A G E &nbsp; · &nbsp; F R E E &nbsp; · &nbsp; I N N O V A T I V E</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="callout"><div class="cl">PROJECT META</div>'
    f'장르: {FIXED_GENRE} | 포맷: {FIXED_FORMAT}'
    f'</div>',
    unsafe_allow_html=True
)

if get_client():
    st.success("Anthropic API 연결 준비 완료")
else:
    st.warning("ANTHROPIC_API_KEY가 아직 설정되지 않았습니다.")

# ─────────────────────────────────────
# 작업 모드
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">🧭 작업 모드 <span class="en">MODE</span></div>',
    unsafe_allow_html=True
)

MODE_OPTIONS = [
    "입력 정리 (Input Summary)",
    "씬 작성 (Scene Draft)",
    "대사 다듬기 (Dialogue Polish)",
    "품질 점검 (Quality Control)",
]

mode = st.selectbox("작업 모드", MODE_OPTIONS, index=0)

# ─────────────────────────────────────
# 공통 입력
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">📥 기획안 입력 <span class="en">PASTE DEVELOPMENT MATERIAL</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="small-meta">Creator Engine 결과 또는 기존 기획안의 내용을 그대로 복사해서 붙여넣습니다.</div>',
    unsafe_allow_html=True
)

title = st.text_input("프로젝트 제목", placeholder="예: 폭립군")
logline = st.text_area("Logline", height=90, placeholder="로그라인")
project_intent = st.text_area("Project Intent", height=130, placeholder="기획의도")
gns = st.text_area("Goal / Need / Strategy", height=130, placeholder="Goal / Need / Strategy")
characters = st.text_area("Character", height=220, placeholder="캐릭터 정보")
world_build = st.text_area("World Build", height=140, placeholder="세계관")
structure = st.text_area("Structure", height=220, placeholder="구조 / 시놉시스 / 비트시트")
scene_design = st.text_area("Scene Design", height=220, placeholder="장면 설계")
treatment = st.text_area("Treatment", height=260, placeholder="트리트먼트")
tone_document = st.text_area("Tone Document", height=140, placeholder="톤 문서 / 연출 문서")

# ─────────────────────────────────────
# 모드별 추가 입력 + 프롬프트 생성
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">✍️ 생성 설정 <span class="en">WRITE / POLISH / QC</span></div>',
    unsafe_allow_html=True
)

prompt_text = ""

if mode.startswith("입력 정리"):
    prompt_text = build_input_summary_prompt(
        title=title,
        genre=FIXED_GENRE,
        format_type=FIXED_FORMAT,
        logline=logline,
        project_intent=project_intent,
        gns=gns,
        characters=characters,
        world_build=world_build,
        structure=structure,
        scene_design=scene_design,
        treatment=treatment,
        tone_document=tone_document,
    )

elif mode.startswith("씬 작성"):
    target_scene = st.text_area(
        "어떤 장면을 쓸지",
        height=140,
        placeholder="예: 1화 오프닝 장면 / 주인공 첫 등장 / 적대자와 첫 대면 / 3막 클라이맥스 직전"
    )

    prompt_text = build_scene_draft_prompt(
        title=title,
        genre=FIXED_GENRE,
        format_type=FIXED_FORMAT,
        logline=logline,
        characters=characters,
        structure=structure,
        scene_design=scene_design,
        treatment=treatment,
        tone_document=tone_document,
        target_scene=target_scene,
    )

elif mode.startswith("대사 다듬기"):
    character_voice_notes = st.text_area(
        "캐릭터 보이스",
        height=120,
        placeholder="인물별 말투 / 리듬 / 숨기는 방식 / 감정 표현 규칙"
    )
    scene_text = st.text_area(
        "다듬을 씬 텍스트",
        height=260,
        placeholder="기존 씬을 붙여넣기"
    )

    prompt_text = build_dialogue_polish_prompt(
        genre=FIXED_GENRE,
        character_voice_notes=character_voice_notes,
        scene_text=scene_text,
    )

elif mode.startswith("품질 점검"):
    qc_text = st.text_area(
        "검토할 텍스트",
        height=280,
        placeholder="씬 / 시퀀스 / 섹션 / 일부 대본을 붙여넣기"
    )

    prompt_text = build_qc_prompt(
        genre=FIXED_GENRE,
        theme=logline,
        scene_or_section_text=qc_text,
    )

st.session_state["last_prompt"] = prompt_text

# ─────────────────────────────────────
# 실행 버튼
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">⚙️ 실행 <span class="en">RUN</span></div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button("프롬프트 보기", use_container_width=True):
        pass

with col2:
    if st.button("실행", type="primary", use_container_width=True):
        st.session_state["result_text"] = run_ai(prompt_text)
        st.session_state["saved_label"] = ""

with st.expander("현재 프롬프트 보기", expanded=False):
    st.code(st.session_state["last_prompt"] or "")

# ─────────────────────────────────────
# 결과
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">📝 결과 <span class="en">OUTPUT</span></div>',
    unsafe_allow_html=True
)

result_value = st.text_area(
    "결과 (직접 수정 가능)",
    value=st.session_state["result_text"],
    height=520,
    key="result_editor",
)

# 최신 수정값 반영
st.session_state["result_text"] = result_value

col3, col4, col5 = st.columns(3)

with col3:
    st.download_button(
        label="TXT 다운로드",
        data=st.session_state["result_text"],
        file_name=f"writer_output_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

with col4:
    if st.button("수정본 확인", use_container_width=True):
        st.session_state["saved_label"] = f"확인 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

with col5:
    if st.button("수정본 기준 재실행", use_container_width=True):
        revised_prompt = build_revision_prompt(
            st.session_state["last_prompt"],
            st.session_state["result_text"],
        )
        st.session_state["result_text"] = run_ai(revised_prompt)
        st.session_state["saved_label"] = ""

if st.session_state["saved_label"]:
    st.info(st.session_state["saved_label"])

# ─────────────────────────────────────
# System Prompt
# ─────────────────────────────────────
with st.expander("System Prompt 보기", expanded=False):
    st.code(SYSTEM_PROMPT)

# ─────────────────────────────────────
# Footer
# ─────────────────────────────────────
st.markdown("---")
st.caption("© 2026 BLUE JEANS PICTURES · Writer Engine v1.0")
