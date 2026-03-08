import os
from datetime import datetime

import streamlit as st
from anthropic import Anthropic

from prompt import (
    SYSTEM_PROMPT,
    GENRE_RULES,
    BEATS_15,
    build_scene_plan_prompt,
    build_write_beat_prompt,
    build_rewrite_prompt,
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
# CSS
# ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/2408-3@latest/Paperlogy.css');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');

:root {
    --navy: #191970; --y: #FFCB05; --bg: #F7F7F5;
    --card: #FFFFFF; --card-border: #E2E2E0; --t: #1A1A2E;
    --r: #D32F2F; --g: #2EC484; --dim: #8E8E99; --light-bg: #EEEEF6;
    --display: 'Playfair Display', 'Paperlogy', 'Georgia', serif;
    --body: 'Pretendard', -apple-system, sans-serif;
    --heading: 'Paperlogy', 'Pretendard', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--body); color: var(--t);
    -webkit-font-smoothing: antialiased;
}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], [data-testid="stHeader"],
[data-testid="stBottom"] {
    background-color: var(--bg) !important; color: var(--t) !important;
}
.stMarkdown, .stText, .stCode { color: var(--t) !important; }
h1,h2,h3,h4,h5,h6 { color: var(--navy) !important; font-family: var(--heading) !important; }
p, span, label, div, li { color: inherit; }
section[data-testid="stSidebar"] { display: none; }

.stTextInput input, .stTextArea textarea,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background-color: var(--card) !important; color: var(--t) !important;
    border: 1.5px solid var(--card-border) !important; border-radius: 8px !important;
    font-family: var(--body) !important; font-size: 0.92rem !important;
    padding: 0.65rem 0.85rem !important;
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
    background-color: var(--card) !important; color: var(--t) !important;
    border-color: var(--card-border) !important; border-radius: 8px !important;
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
    color: var(--t) !important; border: 1.5px solid var(--card-border) !important;
    background-color: var(--card) !important; border-radius: 8px !important;
    font-family: var(--body) !important; font-weight: 700 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1.2rem !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    border-color: var(--navy) !important;
    box-shadow: 0 2px 8px rgba(25,25,112,0.08) !important;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background-color: var(--y) !important; color: var(--navy) !important;
    border-color: var(--y) !important; font-weight: 800 !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background-color: #E8B800 !important;
    box-shadow: 0 2px 12px rgba(255,203,5,0.3) !important;
}
.stDownloadButton > button {
    color: var(--navy) !important; border: 1.5px solid var(--y) !important;
    background-color: var(--y) !important; border-radius: 8px !important;
    font-family: var(--body) !important; font-weight: 800 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1.2rem !important;
}
.stExpander, details, details summary {
    background-color: var(--card) !important; color: var(--t) !important;
    border: 1px solid var(--card-border) !important; border-radius: 8px !important;
}
details[open] > div { background-color: var(--card) !important; }
.stExpander summary, .stExpander summary span { color: var(--t) !important; }
.stAlert { color: var(--t) !important; border-radius: 8px !important; }
[data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"],
[data-testid="stColumn"] { background-color: transparent !important; }

.header {
    font-size: 0.85rem; font-weight: 700; color: var(--navy);
    letter-spacing: 0.15em; font-family: var(--heading);
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
.beat-tag {
    background: var(--navy); color: var(--y);
    display: inline-block; padding: 0.2rem 0.7rem;
    border-radius: 4px; font-size: 0.78rem; font-weight: 800;
    letter-spacing: 0.04em; margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Session State
# ─────────────────────────────────────
FIELDS = ["logline", "intent", "gns", "characters", "world",
          "structure", "scene_design", "treatment", "tone"]

for k, v in {
    "scene_plan": "",
    "beats_done": {},      # {1: "text...", 2: "text...", ...}
    "current_beat": 1,
    "genre": "느와르",
    "fmt": "영화 (장편)",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

for f in FIELDS:
    if f not in st.session_state:
        st.session_state[f] = ""

# ─────────────────────────────────────
# Helpers
# ─────────────────────────────────────
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
    return Anthropic(api_key=api_key) if api_key else None


def stream_ai(prompt: str, tokens: int = 8000):
    """스트리밍 제너레이터."""
    client = get_client()
    if not client:
        yield "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."
        return
    try:
        with client.messages.stream(
            model=ANTHROPIC_MODEL,
            max_tokens=tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        yield f"\n\n❌ 오류: {e}"


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div style="text-align:center;padding:1rem 0 0 0">'
    '<div class="header">B L U E &nbsp; J E A N S &nbsp; P I C T U R E S</div>'
    '<div class="brand-title">WRITER ENGINE</div>'
    '<div class="sub">Y O U N G &nbsp; · &nbsp; V I N T A G E &nbsp; · &nbsp; F R E E &nbsp; · &nbsp; I N N O V A T I V E</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════
# STEP 1 — 자료 입력 (9칸 붙여넣기)
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header">📥 STEP 1 · 자료 입력 <span class="en">PASTE FROM CREATOR ENGINE</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="small-meta">'
    'Creator Engine 결과를 항목별로 복사해서 붙여넣으세요. 필요한 칸만 채워도 됩니다.'
    '</div>',
    unsafe_allow_html=True,
)

col_g1, col_g2 = st.columns(2)
with col_g1:
    genre = st.selectbox("장르", list(GENRE_RULES.keys()),
                          index=list(GENRE_RULES.keys()).index(st.session_state["genre"]))
    st.session_state["genre"] = genre
with col_g2:
    fmt = st.selectbox("포맷", ["영화 (장편)", "시리즈", "단편", "웹드라마"])
    st.session_state["fmt"] = fmt

# ── 9개 입력 칸 ──
st.session_state["logline"] = st.text_area(
    "Logline", value=st.session_state["logline"],
    height=60, placeholder="Creator Engine → Logline 복사")

col_i1, col_i2 = st.columns(2)
with col_i1:
    st.session_state["intent"] = st.text_area(
        "기획의도", value=st.session_state["intent"],
        height=100, placeholder="Creator Engine → 기획의도 복사")
    st.session_state["gns"] = st.text_area(
        "Goal / Need / Strategy", value=st.session_state["gns"],
        height=100, placeholder="GNS 복사")
    st.session_state["world"] = st.text_area(
        "세계관", value=st.session_state["world"],
        height=100, placeholder="World Building 복사")
with col_i2:
    st.session_state["characters"] = st.text_area(
        "캐릭터 (바이블 포함)", value=st.session_state["characters"],
        height=300, placeholder="캐릭터 + 바이블 전체 복사 ← 가장 중요!")

st.session_state["structure"] = st.text_area(
    "구조 / 시놉시스 / 비트시트", value=st.session_state["structure"],
    height=120, placeholder="Synopsis, Storyline, Beat Sheet 복사")

st.session_state["scene_design"] = st.text_area(
    "장면 설계", value=st.session_state["scene_design"],
    height=120, placeholder="Scene Design 복사")

st.session_state["treatment"] = st.text_area(
    "트리트먼트", value=st.session_state["treatment"],
    height=160, placeholder="Treatment (1막/2막/3막) 복사")

st.session_state["tone"] = st.text_area(
    "톤 문서", value=st.session_state["tone"],
    height=80, placeholder="Tone Document 복사")

# API 상태
if get_client():
    st.success("API 연결 준비 완료")
else:
    st.warning("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

# ═══════════════════════════════════════════════════════════
# SCENE PLAN — 15비트 씬 플랜
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header">🗺️ 씬 플랜 <span class="en">SCENE PLAN · 15 BEATS</span></div>',
    unsafe_allow_html=True,
)

has_material = any(st.session_state[f].strip() for f in FIELDS)

if has_material:
    if st.button("씬 플랜 생성", type="primary", use_container_width=True):
        prompt = build_scene_plan_prompt(
            genre=genre, fmt=fmt,
            logline=st.session_state["logline"],
            intent=st.session_state["intent"],
            gns=st.session_state["gns"],
            characters=st.session_state["characters"],
            world=st.session_state["world"],
            structure=st.session_state["structure"],
            scene_design=st.session_state["scene_design"],
            treatment=st.session_state["treatment"],
            tone=st.session_state["tone"],
        )
        result = st.write_stream(stream_ai(prompt, tokens=8000))
        st.session_state["scene_plan"] = result
        st.session_state["beats_done"] = {}
        st.session_state["current_beat"] = 1

    if st.session_state["scene_plan"]:
        done_count = len(st.session_state["beats_done"])
        st.markdown(
            f'<div class="callout"><div class="cl">PLAN STATUS</div>'
            f'15비트 중 {done_count}비트 집필 완료'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander("씬 플랜 보기", expanded=False):
            st.text(st.session_state["scene_plan"])
else:
    st.markdown(
        '<div class="callout"><div class="cl">WAITING</div>'
        '위에 기획 자료를 붙여넣으면 시작할 수 있습니다.'
        '</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════
# STEP 2 — 비트별 집필
# ═══════════════════════════════════════════════════════════
if st.session_state["scene_plan"]:
    st.markdown(
        '<div class="section-header">✍️ STEP 2 · 비트별 집필 <span class="en">WRITE BY BEAT</span></div>',
        unsafe_allow_html=True,
    )

    cur = st.session_state["current_beat"]
    done = st.session_state["beats_done"]

    # ── 완료된 비트 표시 ──
    for b_no in sorted(done.keys()):
        b_info = BEATS_15[b_no - 1]
        label = f"Beat {b_no}. {b_info['name']} ({b_info['act']}) ✅"
        with st.expander(label, expanded=(b_no == max(done.keys()))):
            st.text(done[b_no])

    # ── 현재 비트 정보 ──
    if cur <= 15:
        b_info = BEATS_15[cur - 1]
        st.markdown(
            f'<div class="beat-tag">Beat {cur} / 15</div> '
            f'<span style="font-weight:700">{b_info["name"]}</span> '
            f'<span style="color:var(--dim)">({b_info["act"]})</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="small-meta">{b_info["desc"]}</div>',
            unsafe_allow_html=True,
        )

    # ── 버튼 ──
    col_b1, col_b2 = st.columns(2)

    with col_b1:
        write_btn = st.button(
            f"Beat {cur} 집필" if cur <= 15 else "전체 완료 ✅",
            type="primary",
            use_container_width=True,
            disabled=(cur > 15),
        )

    with col_b2:
        rewrite_btn = st.button(
            "마지막 비트 다시",
            use_container_width=True,
            disabled=(len(done) == 0),
        )

    rewrite_note = ""
    if rewrite_btn:
        rewrite_note = st.text_input(
            "수정 지시 (비워두면 전체 강화)",
            placeholder="예: 캐릭터 대사를 더 차갑게 / 긴장감 올려줘",
        )

    # ── Beat 집필 ──
    if write_btn and cur <= 15:
        # 직전 비트의 마지막 부분
        prev_text = ""
        if cur > 1 and (cur - 1) in done:
            prev_text = done[cur - 1]

        prompt = build_write_beat_prompt(
            genre=genre,
            beat_number=cur,
            scene_plan=st.session_state["scene_plan"],
            characters=st.session_state["characters"],
            treatment=st.session_state["treatment"],
            tone=st.session_state["tone"],
            previous_scene_text=prev_text,
            logline=st.session_state["logline"],
            world=st.session_state["world"],
        )

        st.markdown(
            f'<div class="beat-tag">Beat {cur} 집필 중…</div>',
            unsafe_allow_html=True,
        )
        result = st.write_stream(stream_ai(prompt, tokens=8000))

        st.session_state["beats_done"][cur] = result
        st.session_state["current_beat"] = cur + 1
        st.rerun()

    # ── Beat 다시 쓰기 ──
    if rewrite_btn and done:
        last_beat = max(done.keys())

        prompt = build_rewrite_prompt(
            genre=genre,
            beat_number=last_beat,
            current_text=done[last_beat],
            characters=st.session_state["characters"],
            instruction=rewrite_note,
        )

        b_info = BEATS_15[last_beat - 1]
        st.markdown(
            f'<div class="beat-tag">Beat {last_beat} 다시 쓰는 중…</div>',
            unsafe_allow_html=True,
        )
        result = st.write_stream(stream_ai(prompt, tokens=8000))

        st.session_state["beats_done"][last_beat] = result
        st.rerun()

# ═══════════════════════════════════════════════════════════
# DOWNLOAD
# ═══════════════════════════════════════════════════════════
if st.session_state["beats_done"]:
    st.markdown(
        '<div class="section-header">📄 다운로드 <span class="en">EXPORT</span></div>',
        unsafe_allow_html=True,
    )

    all_parts = []
    for b_no in sorted(st.session_state["beats_done"].keys()):
        b_info = BEATS_15[b_no - 1]
        all_parts.append(
            f"{'='*60}\n"
            f"Beat {b_no}. {b_info['name']} ({b_info['act']})\n"
            f"{'='*60}\n\n"
            f"{st.session_state['beats_done'][b_no]}"
        )

    all_text = "\n\n\n".join(all_parts)
    done_count = len(st.session_state["beats_done"])

    st.download_button(
        label=f"시나리오 TXT ({done_count}/15 비트)",
        data=all_text,
        file_name=f"screenplay_{genre}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

# ═══════════════════════════════════════════════════════════
# RESET
# ═══════════════════════════════════════════════════════════
st.markdown("---")

col_r1, col_r2 = st.columns([3, 1])
with col_r2:
    if st.button("전체 초기화", use_container_width=True):
        for k in ["scene_plan", "beats_done", "current_beat"] + FIELDS:
            if k == "beats_done":
                st.session_state[k] = {}
            elif k == "current_beat":
                st.session_state[k] = 1
            else:
                st.session_state[k] = ""
        st.rerun()

st.caption("© 2026 BLUE JEANS PICTURES · Writer Engine v2.1")
