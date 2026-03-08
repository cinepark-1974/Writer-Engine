import os
from datetime import datetime

import streamlit as st
from anthropic import Anthropic

from prompt import (
    SYSTEM_PROMPT,
    GENRE_RULES,
    build_scene_plan_prompt,
    build_write_scene_prompt,
    build_rewrite_scene_prompt,
    build_polish_prompt,
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
# CSS (Creator Engine 동일)
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

.scene-card {
    background: var(--card); border: 1px solid var(--card-border);
    border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
.scene-num {
    background: var(--navy); color: var(--y);
    display: inline-block; padding: 0.15rem 0.6rem;
    border-radius: 4px; font-size: 0.75rem; font-weight: 800;
    letter-spacing: 0.05em; margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Session State
# ─────────────────────────────────────
for k, v in {
    "material": "",
    "scene_plan": "",
    "scenes": [],           # [{"num":1, "text":"..."}, ...]
    "genre": "느와르",
    "fmt": "영화 (장편)",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────
# Helpers
# ─────────────────────────────────────
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
    return Anthropic(api_key=api_key) if api_key else None


def stream_generate(prompt: str, max_tokens: int = 4000):
    """제너레이터 — st.write_stream 에 직접 전달."""
    client = get_client()
    if not client:
        yield "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."
        return
    try:
        with client.messages.stream(
            model=ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        yield f"\n\n❌ 오류: {e}"


def count_plan_scenes(plan_text: str) -> int:
    """씬 플랜에서 S# 라인 수를 센다."""
    return sum(1 for line in plan_text.splitlines() if line.strip().startswith("S#"))


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
# STEP 1 — 자료 입력
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header">📥 STEP 1 · 자료 입력 <span class="en">PASTE MATERIAL</span></div>',
    unsafe_allow_html=True,
)

col_g1, col_g2 = st.columns(2)
with col_g1:
    genre = st.selectbox("장르", list(GENRE_RULES.keys()), index=list(GENRE_RULES.keys()).index(st.session_state["genre"]))
    st.session_state["genre"] = genre
with col_g2:
    fmt = st.selectbox("포맷", ["영화 (장편)", "시리즈", "단편", "웹드라마"])
    st.session_state["fmt"] = fmt

st.markdown(
    '<div class="small-meta">'
    'Creator Engine 결과를 통째로 복사해서 아래에 붙여넣으세요. '
    '또는 기존 기획서·시놉시스·트리트먼트를 붙여넣어도 됩니다.'
    '</div>',
    unsafe_allow_html=True,
)

material = st.text_area(
    "기획 자료 (전체 붙여넣기)",
    value=st.session_state["material"],
    height=300,
    placeholder=(
        "여기에 Creator Engine 결과 전체를 붙여넣으세요.\n\n"
        "로그라인, 기획의도, GNS, 캐릭터 바이블, 세계관, 시놉시스, "
        "비트시트, 장면설계, 트리트먼트, 톤 문서 등 — 전부 한 번에."
    ),
    key="material_input",
)
st.session_state["material"] = material

if get_client():
    st.success("API 연결 준비 완료")
else:
    st.warning("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

# ═══════════════════════════════════════════════════════════
# SCENE PLAN — 씬 플랜 생성
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header">🗺️ 씬 플랜 <span class="en">SCENE PLAN</span></div>',
    unsafe_allow_html=True,
)

if material.strip():
    if st.button("씬 플랜 생성", type="primary", use_container_width=True):
        prompt = build_scene_plan_prompt(material, genre, fmt)
        result = st.write_stream(stream_generate(prompt))
        st.session_state["scene_plan"] = result
        st.session_state["scenes"] = []   # 새 플랜이면 씬 초기화

    # 기존 플랜 표시
    if st.session_state["scene_plan"]:
        total = count_plan_scenes(st.session_state["scene_plan"])
        done = len(st.session_state["scenes"])

        st.markdown(
            f'<div class="callout"><div class="cl">PLAN STATUS</div>'
            f'전체 {total}씬 중 {done}씬 완료'
            f'</div>',
            unsafe_allow_html=True,
        )

        with st.expander(f"씬 플랜 보기 ({total}씬)", expanded=False):
            st.text(st.session_state["scene_plan"])
else:
    st.markdown(
        '<div class="callout"><div class="cl">WAITING</div>'
        '위에 기획 자료를 붙여넣으면 씬 플랜을 생성할 수 있습니다.'
        '</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════
# STEP 2 — 씬 집필
# ═══════════════════════════════════════════════════════════
if st.session_state["scene_plan"]:
    st.markdown(
        '<div class="section-header">✍️ STEP 2 · 씬 집필 <span class="en">WRITE SCENES</span></div>',
        unsafe_allow_html=True,
    )

    total = count_plan_scenes(st.session_state["scene_plan"])
    done = len(st.session_state["scenes"])
    next_num = done + 1

    # ── 완료된 씬 표시 ──
    if st.session_state["scenes"]:
        for sc in st.session_state["scenes"]:
            with st.expander(f"S#{sc['num']} ✅", expanded=(sc == st.session_state["scenes"][-1])):
                st.text(sc["text"])

    # ── 액션 버튼 ──
    if next_num <= total:
        st.markdown(
            f'<div class="small-meta">다음: S#{next_num} / 전체 {total}씬</div>',
            unsafe_allow_html=True,
        )

    col_w1, col_w2, col_w3 = st.columns(3)

    with col_w1:
        write_next = st.button(
            f"S#{next_num} 쓰기" if next_num <= total else "전체 완료",
            type="primary",
            use_container_width=True,
            disabled=(next_num > total),
        )

    with col_w2:
        rewrite_last = st.button(
            "마지막 씬 다시",
            use_container_width=True,
            disabled=(done == 0),
        )

    with col_w3:
        polish_last = st.button(
            "대사 다듬기",
            use_container_width=True,
            disabled=(done == 0),
        )

    # 다시쓰기 지시 (선택)
    rewrite_note = ""
    if rewrite_last or polish_last:
        rewrite_note = st.text_input(
            "수정 지시 (선택 — 비워두면 전체 강화)",
            placeholder="예: 주인공 대사를 더 차갑게 / 긴장감 올려줘",
        )

    # ── 다음 씬 쓰기 ──
    if write_next and next_num <= total:
        prev_text = st.session_state["scenes"][-1]["text"] if st.session_state["scenes"] else ""

        prompt = build_write_scene_prompt(
            material=material,
            genre=genre,
            scene_plan=st.session_state["scene_plan"],
            scene_number=next_num,
            previous_scene_text=prev_text,
            total_scenes_written=done,
        )

        st.markdown(f'<div class="scene-num">S#{next_num} 집필 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_generate(prompt))

        st.session_state["scenes"].append({"num": next_num, "text": result})
        st.rerun()

    # ── 마지막 씬 다시 ──
    if rewrite_last and done > 0:
        last = st.session_state["scenes"][-1]

        prompt = build_rewrite_scene_prompt(
            genre=genre,
            scene_plan=st.session_state["scene_plan"],
            scene_number=last["num"],
            current_scene_text=last["text"],
            instruction=rewrite_note,
        )

        st.markdown(f'<div class="scene-num">S#{last["num"]} 다시 쓰는 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_generate(prompt))

        st.session_state["scenes"][-1]["text"] = result
        st.rerun()

    # ── 대사 다듬기 ──
    if polish_last and done > 0:
        last = st.session_state["scenes"][-1]

        prompt = build_polish_prompt(
            genre=genre,
            scene_text=last["text"],
        )

        st.markdown(f'<div class="scene-num">S#{last["num"]} 대사 다듬는 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_generate(prompt))

        st.session_state["scenes"][-1]["text"] = result
        st.rerun()

# ═══════════════════════════════════════════════════════════
# DOWNLOAD
# ═══════════════════════════════════════════════════════════
if st.session_state["scenes"]:
    st.markdown(
        '<div class="section-header">📄 다운로드 <span class="en">EXPORT</span></div>',
        unsafe_allow_html=True,
    )

    all_text = "\n\n".join(
        f"{'='*50}\nS#{sc['num']}\n{'='*50}\n\n{sc['text']}"
        for sc in st.session_state["scenes"]
    )

    done = len(st.session_state["scenes"])
    total = count_plan_scenes(st.session_state["scene_plan"])

    st.download_button(
        label=f"전체 시나리오 TXT ({done}/{total}씬)",
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
        for k in ["material", "scene_plan", "scenes"]:
            st.session_state[k] = "" if k != "scenes" else []
        st.rerun()

st.caption("© 2026 BLUE JEANS PICTURES · Writer Engine v2.0")
