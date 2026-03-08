import os
from datetime import datetime

import streamlit as st
from anthropic import Anthropic

from prompt import (
    SYSTEM_PROMPT,
    GENRE_RULES,
    build_input_summary_prompt,
    build_story_matrix_prompt,
    build_unit_blueprint_prompt,
    build_section_draft_prompt,
    build_dialogue_polish_prompt,
    build_ending_control_prompt,
    build_qc_prompt,
)

ANTHROPIC_MODEL = "claude-sonnet-4-6"

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
# Custom CSS  (Creator Engine 동일)
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
.stMarkdown, .stText, .stCode { color: var(--t) !important; }
h1, h2, h3, h4, h5, h6 {
    color: var(--navy) !important;
    font-family: var(--heading) !important;
}
p, span, label, div, li { color: inherit; }

section[data-testid="stSidebar"] { display: none; }

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
    color: var(--dim) !important; font-size: 0.85rem !important;
}

.stSelectbox > div > div, [data-baseweb="select"] > div, [data-baseweb="select"] input {
    background-color: var(--card) !important;
    color: var(--t) !important;
    border-color: var(--card-border) !important;
    border-radius: 8px !important;
}
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"], [role="option"] {
    background-color: var(--card) !important; color: var(--t) !important;
}
[role="option"]:hover { background-color: var(--light-bg) !important; }

.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--t) !important; font-weight: 600 !important;
    font-size: 0.82rem !important; margin-bottom: 0.3rem !important;
}

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

.stExpander, details, details summary {
    background-color: var(--card) !important;
    color: var(--t) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 8px !important;
}
details[open] > div { background-color: var(--card) !important; }
.stExpander summary, .stExpander summary span { color: var(--t) !important; }

.stAlert { color: var(--t) !important; border-radius: 8px !important; }

[data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"],
[data-testid="stColumn"] { background-color: transparent !important; }

.header {
    font-size: 0.85rem; font-weight: 700; color: var(--navy);
    letter-spacing: 0.15em; margin-bottom: 0; font-family: var(--heading);
}
.brand-title {
    font-size: 2.6rem; font-weight: 900; color: var(--navy);
    font-family: var(--display); letter-spacing: -0.02em;
    margin-bottom: 0.15rem; position: relative; display: inline-block;
}
.brand-title::after {
    content: ''; position: absolute; bottom: 2px; left: 0;
    width: 100%; height: 4px; background: var(--y); border-radius: 2px;
}
.sub {
    font-size: 0.7rem; color: var(--dim); letter-spacing: 0.15em;
    margin-top: 0.5rem; margin-bottom: 1.5rem;
}
.card {
    background: var(--card); border: 1px solid var(--card-border);
    border-radius: 10px; padding: 1.2rem; margin-bottom: 0.8rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
.callout {
    background: var(--light-bg); border-left: 4px solid var(--navy);
    padding: 0.9rem 1.1rem; margin: 0.5rem 0;
    border-radius: 0 8px 8px 0; font-size: 0.88rem; color: var(--t);
}
.cl {
    color: var(--navy); font-weight: 700; font-size: 0.72rem;
    letter-spacing: 0.03em; margin-bottom: 0.3rem; text-transform: uppercase;
}
.section-header {
    background: var(--y); color: var(--navy);
    padding: 0.6rem 1rem; border-radius: 6px;
    font-weight: 800; font-size: 1rem; font-family: var(--heading);
    margin: 1.5rem 0 0.8rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.section-header .en {
    font-family: var(--display); font-size: 0.75rem;
    font-weight: 700; letter-spacing: 0.05em; opacity: 0.7;
}
.small-meta {
    font-size: 0.78rem; color: var(--dim);
    margin-top: -0.2rem; margin-bottom: 0.5rem;
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
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────
# Helpers
# ─────────────────────────────────────
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
    if not api_key:
        return None
    return Anthropic(api_key=api_key)


def run_ai(prompt_text: str, tokens: int = 4000) -> str:
    client = get_client()
    if not client:
        return "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."
    try:
        resp = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt_text}],
        )
        parts = [b.text for b in resp.content if hasattr(b, "text")]
        return "\n".join(parts).strip() if parts else "[EMPTY RESPONSE]"
    except Exception as e:
        return f"❌ 오류: {e}"


def build_revision_prompt(base: str, draft: str) -> str:
    return (
        f"{base}\n\n"
        "[REVISION]\n"
        "아래 수정본을 기반으로 개선하라. "
        "극적 힘, 서브텍스트, 캐릭터 보이스, 장르 효능을 강화하라.\n\n"
        f"[CURRENT DRAFT]\n{draft}"
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
    unsafe_allow_html=True,
)

# ─────────────────────────────────────
# 장르 / 포맷 선택
# ─────────────────────────────────────
col_g1, col_g2 = st.columns(2)
with col_g1:
    genre = st.selectbox("장르", list(GENRE_RULES.keys()), index=1)   # 기본 느와르
with col_g2:
    fmt = st.selectbox("포맷", ["영화 (장편)", "시리즈", "단편", "웹드라마"])

st.markdown(
    f'<div class="callout"><div class="cl">PROJECT META</div>'
    f'장르: {genre} | 포맷: {fmt}</div>',
    unsafe_allow_html=True,
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
    unsafe_allow_html=True,
)

MODE_LIST = [
    "① 입력 정리 (Input Summary)",
    "② 스토리 매트릭스 (Story Matrix)",
    "③ 유닛 설계 (Unit Blueprint)",
    "④ 섹션 집필 (Section Draft)",
    "⑤ 대사 다듬기 (Dialogue Polish)",
    "⑥ 엔딩 점검 (Ending Control)",
    "⑦ 품질 점검 (Quality Control)",
]

mode = st.selectbox("작업 모드", MODE_LIST, index=0)

st.markdown(
    '<div class="small-meta">'
    '권장 순서: ① 입력 정리 → ② Matrix → ③ Unit Blueprint ×8 → '
    '④ Section Draft ×16 → ⑤ 대사 → ⑥ 엔딩 → ⑦ QC'
    '</div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────
# 기획 자료 입력 (붙여넣기)
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">📥 기획 자료 입력 <span class="en">PASTE MATERIAL</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="small-meta">'
    'Creator Engine 결과 또는 기존 기획안을 복사해 붙여넣습니다. '
    '필요한 칸만 채워도 작동합니다.'
    '</div>',
    unsafe_allow_html=True,
)

title      = st.text_input("프로젝트 제목", placeholder="예: 폭립군")
logline    = st.text_area("Logline", height=80, placeholder="로그라인")
intent     = st.text_area("기획의도", height=100, placeholder="소재 / 장르 / 시장 / Pitch / Theme")
gns        = st.text_area("Goal / Need / Strategy", height=100, placeholder="GNS")
characters = st.text_area("캐릭터", height=180, placeholder="캐릭터 정보 — 바이블 포함")
world      = st.text_area("세계관", height=100, placeholder="세계관")
structure  = st.text_area("구조 / 시놉시스 / 비트", height=180, placeholder="시놉시스, 15비트, 8시퀀스 등")
scene_design = st.text_area("장면 설계", height=160, placeholder="핵심 장면 설계")
treatment  = st.text_area("트리트먼트", height=200, placeholder="16비트 줄글 트리트먼트")
tone       = st.text_area("톤 문서", height=100, placeholder="톤 / 연출 문서")


# ─────────────────────────────────────
# 기획 자료 → 텍스트 모아두기
# ─────────────────────────────────────
def _gather_material() -> str:
    """기획 자료 중 입력된 것만 모아서 하나의 텍스트로."""
    pairs = [
        ("제목", title), ("장르", genre), ("포맷", fmt),
        ("로그라인", logline), ("기획의도", intent), ("GNS", gns),
        ("캐릭터", characters), ("세계관", world),
        ("구조", structure), ("장면설계", scene_design),
        ("트리트먼트", treatment), ("톤 문서", tone),
    ]
    parts = []
    for lab, val in pairs:
        v = (val or "").strip()
        if v:
            parts.append(f"[{lab}]\n{v}")
    txt = "\n\n".join(parts)
    # 토큰 제한 대비 — 약 12000자 컷
    if len(txt) > 12000:
        txt = txt[:12000] + "\n\n[... 12,000자 초과분 생략]"
    return txt


# ─────────────────────────────────────
# 모드별 추가 입력 + 프롬프트 생성
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">✍️ 모드별 설정 <span class="en">MODE INPUT</span></div>',
    unsafe_allow_html=True,
)

prompt_text = ""
mat = _gather_material()

# ── ① 입력 정리 ──
if mode.startswith("①"):
    st.markdown(
        '<div class="small-meta">'
        '위 기획 자료를 분석하여 집필 준비 상태를 진단합니다.'
        '</div>',
        unsafe_allow_html=True,
    )
    prompt_text = build_input_summary_prompt(
        title=title, genre=genre, fmt=fmt, logline=logline,
        intent=intent, gns=gns, characters=characters,
        world=world, structure=structure,
        scene_design=scene_design, treatment=treatment, tone=tone,
    )

# ── ② Story Matrix ──
elif mode.startswith("②"):
    theme = st.text_area("테마 / 메시지", height=80, placeholder="이 이야기가 결국 무엇을 말하는가")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        protagonist = st.text_input("주인공 이름", placeholder="예: 정섬")
        flaw = st.text_input("결함 / 거짓 신념", placeholder="예: 타인을 절대 믿지 않는다")
    with col_m2:
        need = st.text_input("진짜 필요 / 진실", placeholder="예: 혼자서는 끝까지 못 간다")
        ending_goal = st.text_input("엔딩 목표", placeholder="예: 행동으로 테마를 증명")

    prompt_text = build_story_matrix_prompt(
        title=title, genre=genre, logline=logline, theme=theme,
        protagonist=protagonist, flaw=flaw, need=need,
        ending_goal=ending_goal, material_text=mat,
    )

# ── ③ Unit Blueprint ──
elif mode.startswith("③"):
    st.markdown(
        '<div class="small-meta">'
        'Unit 하나를 골라 상세 설계합니다. 8번 반복하면 전체 골격 완성.'
        '</div>',
        unsafe_allow_html=True,
    )
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        act_label = st.selectbox("Act", ["Act 1", "Act 2A", "Act 2B", "Act 3"])
        unit_no = st.number_input("Unit 번호", 1, 8, 1, step=1)
        section_count = st.number_input("Section 수", 1, 4, 2, step=1)
    with col_u2:
        unit_goal = st.text_area("Unit 목표", height=90, placeholder="이 Unit의 서사적 역할")
        beat_links = st.text_area("16비트 연결", height=90, placeholder="예: Catalyst, Debate")

    arc_links = st.text_area("아크 연결", height=80, placeholder="주인공 변화 / 관계 변화")
    genre_goal = st.text_area("장르 효능 목표", height=80, placeholder="긴장 상승 / 웃음 장치 등")
    ending_connection = st.text_area("엔딩 연결", height=80, placeholder="이 Unit이 엔딩에 기여하는 방식")

    prompt_text = build_unit_blueprint_prompt(
        act_label=act_label, unit_no=int(unit_no), unit_goal=unit_goal,
        section_count=int(section_count), beat_links=beat_links,
        arc_links=arc_links, genre_goal=genre_goal,
        ending_connection=ending_connection, material_text=mat,
    )

# ── ④ Section Draft ──
elif mode.startswith("④"):
    st.markdown(
        '<div class="small-meta">'
        '한 Section씩 시나리오를 집필합니다. '
        '전체를 한 번에 쓰지 않고, Section 단위로 쪼개서 출력합니다.'
        '</div>',
        unsafe_allow_html=True,
    )
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        act_label = st.selectbox("Act", ["Act 1", "Act 2A", "Act 2B", "Act 3"])
    with col_s2:
        unit_no = st.number_input("Unit", 1, 8, 1, step=1)
    with col_s3:
        section_no = st.number_input("Section", 1, 4, 1, step=1)

    section_goal = st.text_area("Section 목표", height=80, placeholder="이 Section의 극적 목적")
    previous_context = st.text_area("이전 맥락", height=80, placeholder="직전 Section 요약")
    character_notes = st.text_area("캐릭터 메모", height=100, placeholder="보이스·욕망·갈등·숨기는 정보")
    tone_notes = st.text_area("톤 메모", height=80, placeholder="리듬·분위기·시각적 질감")
    genre_notes = st.text_area("장르 규칙 메모", height=80, placeholder="이 장르에서 반드시 작동해야 하는 것")
    theme_line = st.text_area("테마 라인", height=60, placeholder="이 Section에서 테마가 어떻게 작동하는가")
    ending_line = st.text_area("엔딩 라인", height=60, placeholder="엔딩 방향과의 연결")

    prompt_text = build_section_draft_prompt(
        title=title, genre=genre, act_label=act_label,
        unit_no=int(unit_no), section_no=int(section_no),
        section_goal=section_goal, previous_context=previous_context,
        character_notes=character_notes, tone_notes=tone_notes,
        genre_notes=genre_notes, theme_line=theme_line,
        ending_line=ending_line, material_text=mat,
    )

# ── ⑤ Dialogue Polish ──
elif mode.startswith("⑤"):
    character_voice_notes = st.text_area(
        "캐릭터 보이스 메모", height=120,
        placeholder="인물별 말투 / 리듬 / 감정 표현 규칙",
    )
    scene_text = st.text_area(
        "다듬을 씬 텍스트", height=280,
        placeholder="기존 씬을 붙여넣기",
    )
    prompt_text = build_dialogue_polish_prompt(
        genre=genre,
        character_voice_notes=character_voice_notes,
        scene_text=scene_text,
    )

# ── ⑥ Ending Control ──
elif mode.startswith("⑥"):
    theme = st.text_area("테마", height=60, placeholder="이 이야기가 결국 무엇을 말하는가")
    protagonist_arc = st.text_area("주인공 아크", height=90, placeholder="시작→위기→선택→변화")
    setup_payoffs = st.text_area("복선 / 회수", height=90, placeholder="반드시 회수할 복선과 감정")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        desired_emotion = st.text_input("원하는 최종 감정", placeholder="먹먹함 / 카타르시스 / 잔상")
    with col_e2:
        ending_type = st.text_input("엔딩 유형", placeholder="비극적 승리 / 열린 결말 / 아이러니")

    prompt_text = build_ending_control_prompt(
        title=title, theme=theme,
        protagonist_arc=protagonist_arc, setup_payoffs=setup_payoffs,
        desired_emotion=desired_emotion, ending_type=ending_type,
        material_text=mat,
    )

# ── ⑦ Quality Control ──
elif mode.startswith("⑦"):
    theme_qc = st.text_input("테마", placeholder="이 작품의 테마")
    qc_text = st.text_area(
        "검토할 텍스트", height=320,
        placeholder="씬 / 시퀀스 / 섹션 / 대본 일부를 붙여넣기",
    )
    prompt_text = build_qc_prompt(
        genre=genre, theme=theme_qc,
        scene_or_section_text=qc_text,
    )

st.session_state["last_prompt"] = prompt_text

# ─────────────────────────────────────
# 실행
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">⚙️ 실행 <span class="en">RUN</span></div>',
    unsafe_allow_html=True,
)

col_r1, col_r2 = st.columns(2)

with col_r1:
    if st.button("프롬프트 보기", use_container_width=True):
        pass  # expander에서 표시

with col_r2:
    if st.button("실행", type="primary", use_container_width=True):
        with st.spinner("Writer Engine 생성 중…"):
            st.session_state["result_text"] = run_ai(prompt_text)
        st.session_state["saved_label"] = ""

with st.expander("현재 프롬프트 보기", expanded=False):
    st.code(st.session_state["last_prompt"] or "")

# ─────────────────────────────────────
# 결과
# ─────────────────────────────────────
st.markdown(
    '<div class="section-header">📝 결과 <span class="en">OUTPUT</span></div>',
    unsafe_allow_html=True,
)

result_value = st.text_area(
    "결과 (직접 수정 가능)",
    value=st.session_state["result_text"],
    height=520,
    key="result_editor",
)
st.session_state["result_text"] = result_value

col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    st.download_button(
        label="TXT 다운로드",
        data=st.session_state["result_text"],
        file_name=f"writer_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

with col_d2:
    if st.button("수정본 확인", use_container_width=True):
        st.session_state["saved_label"] = (
            f"확인: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

with col_d3:
    if st.button("수정본 기준 재실행", use_container_width=True):
        rev = build_revision_prompt(
            st.session_state["last_prompt"],
            st.session_state["result_text"],
        )
        with st.spinner("재생성 중…"):
            st.session_state["result_text"] = run_ai(rev)
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
