import os
from datetime import datetime

import streamlit as st
from anthropic import Anthropic

from prompt import (
    SYSTEM_PROMPT,
    build_project_brief_prompt,
    build_story_matrix_prompt,
    build_unit_blueprint_prompt,
    build_section_screenplay_prompt,
    build_dialogue_polish_prompt,
    build_ending_control_prompt,
    build_qc_prompt,
)

# ─────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────
ANTHROPIC_MODEL = "claude-sonnet-4-6"

# 장르 / 포맷 고정
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
# Custom CSS
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
    --display: 'Playfair Display', 'Paperlogy', 'Georgia', serif;
    --body: 'Pretendard', -apple-system, sans-serif;
    --heading: 'Paperlogy', 'Pretendard', sans-serif;
}

/* 기본 */
html, body, [class*="css"] {
    font-family: var(--body);
    color: var(--t);
    -webkit-font-smoothing: antialiased;
}

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

/* 사이드바 숨김 */
section[data-testid="stSidebar"] {
    display: none;
}

/* 입력 */
.stTextInput input, .stTextArea textarea,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background-color: var(--card) !important;
    color: var(--t) !important;
    border: 1.5px solid var(--card-border) !important;
    border-radius: 8px !important;
    font-family: var(--body) !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 0.8rem !important;
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
    font-weight: 700 !important;
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

/* Header */
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

/* UI blocks */
.callout {
    background: var(--light-bg);
    border-left: 4px solid var(--navy);
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.88rem;
    color: var(--t);
}

.card {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Session State
# ─────────────────────────────────────
def init_session_state():
    defaults = {
        "generated_text": "",
        "edited_text": "",
        "last_prompt": "",
        "last_mode": "",
        "saved_label": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ─────────────────────────────────────
# Helpers
# ─────────────────────────────────────
def get_api_key():
    secret_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    if secret_key:
        return secret_key
    return os.getenv("ANTHROPIC_API_KEY")

def get_client():
    api_key = get_api_key()
    if not api_key:
        return None
    return Anthropic(api_key=api_key)

def generate_with_anthropic(user_prompt, max_tokens=4000):
    client = get_client()
    if client is None:
        return (
            "[ERROR]\n"
            "ANTHROPIC_API_KEY가 설정되지 않았습니다.\n"
            "Streamlit Secrets 또는 환경변수에 API 키를 등록해주세요."
        )

    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
        )

        parts = []
        for block in response.content:
            if hasattr(block, "text"):
                parts.append(block.text)

        if not parts:
            return "[EMPTY RESPONSE]"
        return "\n".join(parts).strip()

    except Exception as e:
        return f"[ERROR]\n{str(e)}"

def build_revision_prompt(base_prompt, edited_text):
    return (
        f"{base_prompt}\n\n"
        "[REVISION INSTRUCTION]\n"
        "Use the revised text below as the current working draft. "
        "Preserve its strengths, improve clarity, dramatic force, cinematic precision, "
        "character voice, subtext, and genre effectiveness.\n\n"
        "[CURRENT DRAFT]\n"
        f"{edited_text}"
    )

# ─────────────────────────────────────
# Brand Header
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
    f'<div class="callout">'
    f'<div class="cl">PROJECT META</div>'
    f'장르: {FIXED_GENRE} · 포맷: {FIXED_FORMAT}'
    f'</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────
# API Status
# ─────────────────────────────────────
if get_api_key():
    st.success("Anthropic API 연결 준비 완료")
else:
    st.warning("ANTHROPIC_API_KEY가 아직 설정되지 않았습니다.")

# ─────────────────────────────────────
# Mode Select
# ─────────────────────────────────────
MODE_OPTIONS = {
    "프로젝트 브리프 (Project Brief)": "Project Brief",
    "스토리 매트릭스 (Story Matrix)": "Story Matrix",
    "유닛 설계 (Unit Blueprint)": "Unit Blueprint",
    "섹션 집필 (Section Draft)": "Section Draft",
    "대사 다듬기 (Dialogue Polish)": "Dialogue Polish",
    "엔딩 점검 (Ending Control)": "Ending Control",
    "품질 점검 (Quality Control)": "Quality Control",
}

st.markdown(
    '<div class="section-header">🧭 작업 모드 <span class="en">MODE</span></div>',
    unsafe_allow_html=True
)

selected_label = st.selectbox(
    "작업 모드 (Mode)",
    list(MODE_OPTIONS.keys()),
    index=0,
)

mode = MODE_OPTIONS[selected_label]
st.session_state["last_mode"] = mode

# ─────────────────────────────────────
# Common Inputs
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">📌 프로젝트 입력 <span class="en">PROJECT INPUT</span></div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    project_title = st.text_input(
        "프로젝트 제목",
        placeholder="예: 폭립군"
    )
    logline = st.text_area(
        "로그라인",
        height=100,
        placeholder="한 줄 핵심 로그라인"
    )
    theme = st.text_area(
        "테마 / 메시지",
        height=100,
        placeholder="이 이야기가 결국 무엇을 말하는가"
    )

with col2:
    tone = st.text_input(
        "톤",
        placeholder="예: 차갑고 건조한 리얼리즘"
    )
    audience = st.text_input(
        "타깃 관객",
        placeholder="예: 한국 30~50대 관객"
    )
    protagonist_name = st.text_input(
        "주인공 이름",
        placeholder="예: 정섬"
    )

# ─────────────────────────────────────
# Mode-specific Inputs
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">🛠️ 모드별 입력 <span class="en">MODE INPUT</span></div>',
    unsafe_allow_html=True
)

user_prompt = ""

if mode == "Project Brief":
    user_prompt = build_project_brief_prompt(
        title=project_title,
        genre=FIXED_GENRE,
        format_type=FIXED_FORMAT,
        logline=logline,
        theme=theme,
        tone=tone,
        audience=audience,
    )

elif mode == "Story Matrix":
    flaw = st.text_input(
        "주인공의 결함 / 거짓 신념",
        placeholder="예: 타인을 절대 믿지 않는다"
    )
    need = st.text_input(
        "주인공의 진짜 필요 / 진실",
        placeholder="예: 혼자서는 끝까지 갈 수 없다는 사실"
    )
    ending_goal = st.text_input(
        "엔딩 목표",
        placeholder="예: 행동으로 테마를 증명하는 결말"
    )

    user_prompt = build_story_matrix_prompt(
        title=project_title,
        genre=FIXED_GENRE,
        logline=logline,
        theme=theme,
        protagonist=protagonist_name,
        flaw=flaw,
        need=need,
        ending_goal=ending_goal,
    )

elif mode == "Unit Blueprint":
    col_u1, col_u2 = st.columns(2)

    with col_u1:
        act_label = st.selectbox(
            "Act",
            ["Act 1", "Act 2A", "Act 2B", "Act 3"]
        )
        unit_no = st.number_input(
            "Unit 번호",
            min_value=1,
            max_value=8,
            value=1,
            step=1
        )
        section_count = st.number_input(
            "Section 수",
            min_value=1,
            max_value=4,
            value=2,
            step=1
        )

    with col_u2:
        unit_goal = st.text_area(
            "Unit 목표",
            height=100,
            placeholder="이 Unit이 서사적으로 해야 할 일"
        )
        beat_links = st.text_area(
            "16비트 연결",
            height=100,
            placeholder="예: Catalyst, Debate, Break into 2"
        )

    arc_links = st.text_area(
        "아크 연결",
        height=100,
        placeholder="주인공 변화 / 관계 변화"
    )
    genre_goal = st.text_area(
        "장르 효능 목표",
        height=100,
        placeholder="예: 긴장 상승, 웃음 장치, 갈망 심화"
    )
    ending_connection = st.text_area(
        "엔딩 연결",
        height=100,
        placeholder="이 Unit이 엔딩에 어떻게 기여하는가"
    )

    user_prompt = build_unit_blueprint_prompt(
        act_label=act_label,
        unit_no=int(unit_no),
        unit_goal=unit_goal,
        section_count=int(section_count),
        beat_links=beat_links,
        arc_links=arc_links,
        genre_goal=genre_goal,
        ending_connection=ending_connection,
    )

elif mode == "Section Draft":
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        act_label = st.selectbox(
            "Act",
            ["Act 1", "Act 2A", "Act 2B", "Act 3"]
        )
    with col_s2:
        unit_no = st.number_input(
            "Unit 번호",
            min_value=1,
            max_value=8,
            value=1,
            step=1
        )
    with col_s3:
        section_no = st.number_input(
            "Section 번호",
            min_value=1,
            max_value=4,
            value=1,
            step=1
        )

    section_goal = st.text_area(
        "Section 목표",
        height=90,
        placeholder="이 Section이 달성해야 할 극적 목적"
    )
    previous_context = st.text_area(
        "이전 맥락",
        height=90,
        placeholder="직전 장면 / 직전 Section 요약"
    )
    character_notes = st.text_area(
        "캐릭터 메모",
        height=100,
        placeholder="보이스, 욕망, 갈등, 숨기는 정보"
    )
    tone_notes = st.text_area(
        "톤 메모",
        height=90,
        placeholder="리듬, 분위기, 시각적 질감"
    )
    genre_rule = st.text_area(
        "장르 규칙",
        height=90,
        placeholder="이 장르에서 반드시 작동해야 하는 것"
    )
    theme_line = st.text_area(
        "테마 라인",
        height=80,
        placeholder="이 Section에서 테마가 어떻게 작동하는가"
    )
    ending_line = st.text_area(
        "엔딩 라인",
        height=80,
        placeholder="엔딩 방향과의 연결"
    )

    user_prompt = build_section_screenplay_prompt(
        title=project_title,
        genre=FIXED_GENRE,
        act_label=act_label,
        unit_no=int(unit_no),
        section_no=int(section_no),
        section_goal=section_goal,
        previous_context=previous_context,
        character_notes=character_notes,
        tone_notes=tone_notes,
        genre_rule=genre_rule,
        theme_line=theme_line,
        ending_line=ending_line,
    )

elif mode == "Dialogue Polish":
    character_voice_notes = st.text_area(
        "캐릭터 보이스 메모",
        height=120,
        placeholder="인물별 말투 규칙 / 태도 / 감정"
    )
    scene_text = st.text_area(
        "수정할 장면 텍스트",
        height=320,
        placeholder="여기에 기존 장면 텍스트를 붙여넣기"
    )

    user_prompt = build_dialogue_polish_prompt(
        genre=FIXED_GENRE,
        character_voice_notes=character_voice_notes,
        scene_text=scene_text,
    )

elif mode == "Ending Control":
    protagonist_arc = st.text_area(
        "주인공 아크",
        height=100,
        placeholder="시작 → 위기 → 선택 → 변화"
    )
    setup_payoffs = st.text_area(
        "복선 / 회수",
        height=100,
        placeholder="반드시 회수해야 할 복선과 감정"
    )
    desired_emotion = st.text_input(
        "원하는 최종 감정",
        placeholder="예: 먹먹함, 카타르시스, 잔상"
    )
    ending_type = st.text_input(
        "엔딩 유형",
        placeholder="예: 비극적 승리 / 열린 결말 / 아이러니"
    )

    user_prompt = build_ending_control_prompt(
        title=project_title,
        theme=theme,
        protagonist_arc=protagonist_arc,
        setup_payoffs=setup_payoffs,
        desired_emotion=desired_emotion,
        ending_type=ending_type,
    )

elif mode == "Quality Control":
    scene_or_section_text = st.text_area(
        "점검할 텍스트",
        height=320,
        placeholder="QC할 장면 또는 섹션 전체 텍스트"
    )

    user_prompt = build_qc_prompt(
        genre=FIXED_GENRE,
        theme=theme,
        scene_or_section_text=scene_or_section_text,
    )

# ─────────────────────────────────────
# Prompt Actions
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">⚙️ 실행 <span class="en">ACTIONS</span></div>',
    unsafe_allow_html=True
)

col_a1, col_a2 = st.columns(2)

with col_a1:
    if st.button("프롬프트 보기", use_container_width=True):
        st.session_state["last_prompt"] = user_prompt

with col_a2:
    if st.button("생성 실행", type="primary", use_container_width=True):
        st.session_state["last_prompt"] = user_prompt
        result = generate_with_anthropic(
            user_prompt=user_prompt,
            max_tokens=4000
        )
        st.session_state["generated_text"] = result
        st.session_state["edited_text"] = result
        st.session_state["saved_label"] = ""

# ─────────────────────────────────────
# Prompt Preview
# ─────────────────────────────────────
if st.session_state["last_prompt"]:
    with st.expander("현재 프롬프트 보기", expanded=False):
        st.code(st.session_state["last_prompt"])

# ─────────────────────────────────────
# Output
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">✍️ 결과 <span class="en">OUTPUT</span></div>',
    unsafe_allow_html=True
)

if st.session_state["edited_text"]:
    st.markdown(
        '<div class="card"><div class="cl">생성 결과 / 직접 수정</div></div>',
        unsafe_allow_html=True
    )

    st.text_area(
        "생성 결과 / 직접 수정",
        key="edited_text",
        height=520,
        label_visibility="collapsed",
    )

    edited_text = st.session_state["edited_text"]

    st.download_button(
        label="TXT 다운로드",
        data=edited_text,
        file_name=f"blue_jeans_writer_{mode.lower().replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        if st.button("수정본 상태 표시", use_container_width=True):
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state["saved_label"] = f"수정본 확인 시각: {stamp}"

    with col_b2:
        if st.button("수정본 기준 재실행", use_container_width=True):
            revised_prompt = build_revision_prompt(
                st.session_state["last_prompt"],
                st.session_state["edited_text"]
            )
            result = generate_with_anthropic(
                user_prompt=revised_prompt,
                max_tokens=4000
            )
            st.session_state["generated_text"] = result
            st.session_state["edited_text"] = result
            st.session_state["saved_label"] = ""

    if st.session_state["saved_label"]:
        st.info(st.session_state["saved_label"])

else:
    st.markdown(
        '<div class="callout"><div class="cl">OUTPUT</div>아직 생성된 결과가 없습니다. 입력 후 생성 실행을 눌러주세요.</div>',
        unsafe_allow_html=True
    )

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
