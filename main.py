import os
from datetime import datetime

import streamlit as st
from anthropic import Anthropic

from prompt import (
    SYSTEM_PROMPT,
    GENRE_RULES,
    BEATS_15,
    ACT_BEATS,
    build_scene_plan_prompt,
    build_extract_elements_prompt,
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
# Custom CSS (Creator Engine 동일 톤)
# ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/2408-3@latest/Paperlogy.css');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');

:root {
    --navy: #191970; --y: #FFCB05; --bg: #F7F7F5;
    --card: #FFFFFF; --card-border: #E2E2E0; --t: #1A1A2E;
    --g: #2EC484; --dim: #8E8E99; --light-bg: #EEEEF6;
    --serif: 'Paperlogy', 'Noto Serif KR', 'Georgia', serif;
    --display: 'Playfair Display', 'Paperlogy', 'Georgia', serif;
    --body: 'Pretendard', -apple-system, sans-serif;
    --heading: 'Paperlogy', 'Pretendard', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--body); color: var(--t); -webkit-font-smoothing: antialiased;
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
    position: relative; display: inline-block;
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
.act-tag {
    background: var(--navy); color: #fff;
    display: inline-block; padding: 0.25rem 0.8rem;
    border-radius: 4px; font-size: 0.82rem; font-weight: 800;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# Session State
# ─────────────────────────────────────
FIELDS = ["title", "logline", "intent", "gns", "characters", "world",
          "structure", "scene_design", "treatment", "tone"]

for k, v in {
    "plan_1막": "", "plan_2막": "", "plan_3막": "",
    "story_elements": "",
    "beats_done": {},
    "current_beat": 1,
    "genre": "범죄/스릴러",
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

def stream_ai(prompt: str, tokens: int = 16000):
    """스트리밍 제너레이터 — st.write_stream에 직접 전달."""
    client = get_client()
    if not client:
        yield "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."
        return
    try:
        with client.messages.stream(
            model=ANTHROPIC_MODEL, max_tokens=tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        yield f"\n\n❌ 오류: {e}"

def full_plan() -> str:
    """3막 플랜 합침."""
    return "\n\n".join(
        st.session_state.get(f"plan_{a}", "")
        for a in ["1막", "2막", "3막"]
        if st.session_state.get(f"plan_{a}", "")
    )

def plan_ready() -> bool:
    return all(st.session_state.get(f"plan_{a}", "").strip() for a in ["1막", "2막", "3막"])

def make_docx_bytes(genre: str, beats_done: dict, title: str = "") -> bytes:
    """시나리오 DOCX — 한국 표준 시나리오 서식."""
    import re
    from docx import Document as DocxDocument
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from io import BytesIO

    doc = DocxDocument()

    # ── 페이지 설정 (A4, 20mm 마진) ──
    from docx.shared import Mm
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(20)
    section.right_margin = Mm(20)

    # ── 기본 스타일: 함초롬바탕 10pt ──
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "함초롬바탕"
    style_normal.font.size = Pt(10)
    style_normal.paragraph_format.space_after = Pt(2)
    style_normal.paragraph_format.space_before = Pt(0)
    # 한글 폰트 설정
    rpr = style_normal.element.rPr
    if rpr is None:
        rpr = style_normal.element.makeelement(qn('w:rPr'), {})
        style_normal.element.append(rpr)
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rfonts)
    rfonts.set(qn('w:eastAsia'), '함초롬바탕')

    def add_text(text, bold=False, size=None, color=None, align=None):
        p = doc.add_paragraph()
        if align:
            p.alignment = align
        r = p.add_run(text)
        r.font.name = "함초롬바탕"
        rpr_elem = r._element.get_or_add_rPr()
        rf = rpr_elem.find(qn('w:rFonts'))
        if rf is None:
            rf = rpr_elem.makeelement(qn('w:rFonts'), {})
            rpr_elem.append(rf)
        rf.set(qn('w:eastAsia'), '함초롬바탕')
        if bold:
            r.bold = True
        if size:
            r.font.size = size
        if color:
            r.font.color.rgb = color
        return p

    def add_scene_heading(text):
        """씬 헤딩 — 볼드."""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.bold = True
        r.font.name = "함초롬바탕"
        r.font.size = Pt(10)
        return p

    def add_dialogue(char_name, parenthetical, line):
        """대사 — 캐릭터명 + 탭 + (지시) + 대사."""
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        paren = f"({parenthetical})" if parenthetical else ""
        full = f"{char_name}\t\t{paren}{line}"
        r = p.add_run(full)
        r.font.name = "함초롬바탕"
        r.font.size = Pt(10)
        return p

    def add_action(text):
        """지문 — 일반 텍스트."""
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = "함초롬바탕"
        r.font.size = Pt(10)
        return p

    # ── 커버 페이지 ──
    for _ in range(6):
        doc.add_paragraph("")
    add_text("시나리오", size=Pt(11), align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph("")
    proj_title = title or f"<{genre}>"
    add_text(proj_title, bold=True, size=Pt(24), align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph("")
    doc.add_paragraph("")
    add_text("기획/제작 | 블루진픽처스", size=Pt(10), align=WD_ALIGN_PARAGRAPH.CENTER,
             color=RGBColor(0x8E, 0x8E, 0x99))
    add_text(f"Writer Engine v2.2  ·  {len(beats_done)}/15 비트",
             size=Pt(9), align=WD_ALIGN_PARAGRAPH.CENTER,
             color=RGBColor(0x8E, 0x8E, 0x99))
    doc.add_page_break()

    # ── 본문 파싱 + 변환 ──
    # 씬 헤딩 패턴: S#숫자. INT./EXT. 또는 그냥 INT./EXT.
    heading_re = re.compile(r'^S?#?\d*\.?\s*(INT\.|EXT\.|INT\./EXT\.)\s*(.+)', re.IGNORECASE)
    # 캐릭터명 패턴: 4칸 들여쓰기 + 짧은 이름 (2~10자)
    char_re = re.compile(r'^\s{2,}([가-힣a-zA-Z\s]{1,15})\s*$')
    # 괄호 지시
    paren_re = re.compile(r'^\s{2,}\((.+?)\)\s*$')
    # 구분선/내부메모 (출력 제외)
    divider_re = re.compile(r'^(═{3,}|─{3,}|---)')

    current_act = ""
    for b_no in sorted(beats_done.keys()):
        b_info = BEATS_15[b_no - 1]

        # ACT 전환
        if b_info["act"] != current_act:
            if current_act:
                doc.add_page_break()
            current_act = b_info["act"]

        text = beats_done[b_no]
        lines = text.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 빈 줄
            if not stripped:
                i += 1
                continue

            # 구분선/내부메모 스킵
            if divider_re.match(stripped):
                i += 1
                # 내부메모 블록 스킵
                while i < len(lines) and lines[i].strip():
                    i += 1
                continue

            # Beat 헤더 스킵 (프롬프트가 넣는 ACT — Beat 헤더)
            if stripped.startswith("═") or "Beat " in stripped and "—" in stripped:
                i += 1
                continue

            # 씬 헤딩
            m = heading_re.match(stripped)
            if m:
                heading_text = m.group(1) + " " + m.group(2)
                add_scene_heading(heading_text)
                i += 1
                continue

            # 캐릭터명 + 대사 감지
            cm = char_re.match(line)
            if cm:
                char_name = cm.group(1).strip()
                parenthetical = ""
                dialogue_lines = []
                i += 1

                # 괄호 지시 확인
                if i < len(lines):
                    pm = paren_re.match(lines[i])
                    if pm:
                        parenthetical = pm.group(1)
                        i += 1

                # 대사 수집 (들여쓰기 없거나 일반 텍스트)
                while i < len(lines):
                    dl = lines[i]
                    ds = dl.strip()
                    if not ds:
                        break
                    # 다음 씬헤딩이면 멈춤
                    if heading_re.match(ds):
                        break
                    # 다음 캐릭터명이면 멈춤
                    if char_re.match(dl):
                        break
                    dialogue_lines.append(ds)
                    i += 1

                # 대사 출력
                if dialogue_lines:
                    for dl in dialogue_lines:
                        add_dialogue(char_name, parenthetical, dl)
                        parenthetical = ""  # 첫 줄에만
                else:
                    add_dialogue(char_name, parenthetical, "")
                continue

            # 그 외 = 지문
            add_action(stripped)
            i += 1

    # ── 푸터 ──
    doc.add_page_break()
    add_text(f"© 2026 BLUE JEANS PICTURES · Writer Engine v2.2",
             size=Pt(8), align=WD_ALIGN_PARAGRAPH.CENTER,
             color=RGBColor(0x8E, 0x8E, 0x99))

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.getvalue()


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
# STEP 1 — 자료 입력 (Creator Engine 9개 항목)
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header">📥 STEP 1 · 자료 입력 <span class="en">PASTE FROM CREATOR ENGINE</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="small-meta">Creator Engine 결과를 항목별로 복사해서 붙여넣으세요. 필요한 칸만 채워도 됩니다.</div>',
    unsafe_allow_html=True,
)

col_g1, col_g2 = st.columns(2)
with col_g1:
    genre_list = list(GENRE_RULES.keys())
    current_genre = st.session_state.get("genre", "범죄/스릴러")
    if current_genre not in genre_list:
        current_genre = "미지정"
    genre = st.selectbox("장르", genre_list,
                          index=genre_list.index(current_genre))
    st.session_state["genre"] = genre
with col_g2:
    fmt = st.selectbox("포맷", ["영화 (장편)", "시리즈", "단편", "웹드라마"])
    st.session_state["fmt"] = fmt

st.session_state["title"] = st.text_input(
    "프로젝트 제목", value=st.session_state.get("title", ""),
    placeholder="예: 물귀신")

st.session_state["logline"] = st.text_area(
    "Logline", value=st.session_state["logline"],
    height=60, placeholder="Logline Pack (5종 중 택1 또는 전체)")

col_i1, col_i2 = st.columns(2)
with col_i1:
    st.session_state["intent"] = st.text_area(
        "기획의도 (Project Intent)", value=st.session_state["intent"],
        height=100, placeholder="소재 / 장르 / 시장 / Pitch / Theme")
    st.session_state["gns"] = st.text_area(
        "Goal / Need / Strategy", value=st.session_state["gns"],
        height=100, placeholder="Goal / Need / Strategy")
    st.session_state["world"] = st.text_area(
        "세계관 (World Build)", value=st.session_state["world"],
        height=100, placeholder="시간 / 공간 / 규칙 / 금기 / 권력구조")
with col_i2:
    st.session_state["characters"] = st.text_area(
        "캐릭터 + 바이블 ← 가장 중요", value=st.session_state["characters"],
        height=300, placeholder="캐릭터(4인) + 바이블(백스토리/말투규칙/대사샘플/관계태도/변화궤적)")

st.session_state["structure"] = st.text_area(
    "구조 (Synopsis + Storyline + Beat Sheet)", value=st.session_state["structure"],
    height=120, placeholder="Synopsis 1P / Storyline 8시퀀스 / 15-Beat Sheet / 3막 진단")

st.session_state["scene_design"] = st.text_area(
    "장면 설계 (Scene Design)", value=st.session_state["scene_design"],
    height=120, placeholder="핵심 장면 15~18개 + Scene Map")

st.session_state["treatment"] = st.text_area(
    "트리트먼트 (Treatment)", value=st.session_state["treatment"],
    height=160, placeholder="16비트 줄글 (1막/2막/3막)")

st.session_state["tone"] = st.text_area(
    "톤 문서 (Tone Document)", value=st.session_state["tone"],
    height=80, placeholder="비주얼/페이싱/대사규칙/모티프/사운드/금기/Writer지시")

# API 상태
if get_client():
    st.success("API 연결 준비 완료")
else:
    st.warning("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

has_material = any(st.session_state[f].strip() for f in FIELDS)

# ═══════════════════════════════════════════════════════════
# SCENE PLAN — 3막 분할 (100씬 / 100분)
# ═══════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-header">🗺️ 씬 플랜 <span class="en">SCENE PLAN · 100 SCENES / 3-ACT SPLIT</span></div>',
    unsafe_allow_html=True,
)

if has_material:
    st.markdown(
        '<div class="small-meta">'
        '100씬/100분 기준. 1막 → 2막 → 3막 순서로 생성합니다.'
        '</div>',
        unsafe_allow_html=True,
    )

    plan_kw = dict(
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

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        done1 = bool(st.session_state["plan_1막"])
        btn1 = st.button(
            f"{'✅ ' if done1 else ''}1막 플랜 (Beat 1~5)",
            type="primary" if not done1 else "secondary",
            use_container_width=True,
        )
    with col_p2:
        done2 = bool(st.session_state["plan_2막"])
        btn2 = st.button(
            f"{'✅ ' if done2 else ''}2막 플랜 (Beat 6~11)",
            type="primary" if done1 and not done2 else "secondary",
            use_container_width=True,
            disabled=not done1,
        )
    with col_p3:
        done3 = bool(st.session_state["plan_3막"])
        btn3 = st.button(
            f"{'✅ ' if done3 else ''}3막 플랜 (Beat 12~15)",
            type="primary" if done2 and not done3 else "secondary",
            use_container_width=True,
            disabled=not done2,
        )

    if btn1:
        prompt = build_scene_plan_prompt(act="1막", **plan_kw, previous_plan="")
        st.markdown('<div class="act-tag">1막 씬 플랜 생성 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt))
        st.session_state["plan_1막"] = result
        st.session_state["plan_2막"] = ""
        st.session_state["plan_3막"] = ""
        st.session_state["beats_done"] = {}
        st.session_state["current_beat"] = 1
        st.rerun()

    if btn2:
        prompt = build_scene_plan_prompt(act="2막", **plan_kw, previous_plan=st.session_state["plan_1막"])
        st.markdown('<div class="act-tag">2막 씬 플랜 생성 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt))
        st.session_state["plan_2막"] = result
        st.session_state["plan_3막"] = ""
        st.rerun()

    if btn3:
        prev = st.session_state["plan_1막"] + "\n\n" + st.session_state["plan_2막"]
        prompt = build_scene_plan_prompt(act="3막", **plan_kw, previous_plan=prev)
        st.markdown('<div class="act-tag">3막 씬 플랜 생성 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt))
        st.session_state["plan_3막"] = result
        st.rerun()

    # 플랜 표시
    for act in ["1막", "2막", "3막"]:
        p = st.session_state.get(f"plan_{act}", "")
        if p:
            with st.expander(f"{act} 씬 플랜 ✅", expanded=False):
                st.text(p)

    if plan_ready():
        st.markdown(
            '<div class="callout"><div class="cl">PLAN COMPLETE</div>'
            '3막 씬 플랜 완성. 아래에서 비트별 집필을 시작하세요.</div>',
            unsafe_allow_html=True,
        )
        plan_all = full_plan()
        st.download_button(
            label="씬 플랜 TXT 저장",
            data=plan_all,
            file_name=f"scene_plan_{genre}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        # ── 핵심 요소 추출 ──
        st.markdown(
            '<div class="section-header">🔍 핵심 요소 추출 <span class="en">STORY ELEMENTS</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="small-meta">'
            '기획 자료에서 맥거핀·캐릭터 비밀·핵심 장소·모티프·클라이맥스 설계를 추출합니다. '
            '추출 결과는 매 비트 집필 시 자동으로 주입되어 누락을 방지합니다.'
            '</div>',
            unsafe_allow_html=True,
        )

        elements_done = bool(st.session_state.get("story_elements", ""))

        if st.button(
            f"{'✅ ' if elements_done else ''}핵심 요소 추출",
            type="primary" if not elements_done else "secondary",
            use_container_width=True,
        ):
            extract_prompt = build_extract_elements_prompt(
                genre=genre,
                logline=st.session_state["logline"],
                characters=st.session_state["characters"],
                structure=st.session_state["structure"],
                scene_design=st.session_state["scene_design"],
                treatment=st.session_state["treatment"],
                tone=st.session_state["tone"],
                world=st.session_state["world"],
            )
            st.markdown('<div class="beat-tag">핵심 요소 추출 중…</div>', unsafe_allow_html=True)
            result = st.write_stream(stream_ai(extract_prompt))
            st.session_state["story_elements"] = result
            st.rerun()

        if elements_done:
            with st.expander("핵심 요소 보기 ✅", expanded=False):
                st.text(st.session_state["story_elements"])
else:
    st.markdown(
        '<div class="callout"><div class="cl">WAITING</div>'
        '위에 기획 자료를 붙여넣으면 시작할 수 있습니다.</div>',
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════
# STEP 2 — 비트별 집필
# ═══════════════════════════════════════════════════════════
if plan_ready():
    st.markdown(
        '<div class="section-header">✍️ STEP 2 · 비트별 집필 <span class="en">WRITE BY BEAT</span></div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.get("story_elements"):
        st.warning("⚠️ 핵심 요소 추출을 먼저 실행하세요. 맥거핀·비밀·모티프가 누락될 수 있습니다.")

    cur = st.session_state["current_beat"]
    done = st.session_state["beats_done"]
    combined_plan = full_plan()

    # 완료 비트 표시
    for b_no in sorted(done.keys()):
        b_info = BEATS_15[b_no - 1]
        with st.expander(
            f"{b_info['act']} — Beat {b_no}. {b_info['name']} ✅",
            expanded=(b_no == max(done.keys())),
        ):
            st.text(done[b_no])

    # 현재 비트 정보
    if cur <= 15:
        b_info = BEATS_15[cur - 1]
        st.markdown(
            f'<div class="beat-tag">Beat {cur} / 15</div> '
            f'<span style="font-weight:700">{b_info["name"]}</span> '
            f'<span style="color:var(--dim)">({b_info["act"]})</span>',
            unsafe_allow_html=True,
        )

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        write_btn = st.button(
            f"Beat {cur} 집필" if cur <= 15 else "전체 완료 ✅",
            type="primary", use_container_width=True,
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
            placeholder="예: 대사를 더 차갑게 / 긴장감 올려줘 / Hook 강화",
        )

    # 집필
    if write_btn and cur <= 15:
        prev_text = done[cur - 1] if (cur > 1 and (cur - 1) in done) else ""
        prompt = build_write_beat_prompt(
            genre=genre, beat_number=cur,
            scene_plan=combined_plan,
            characters=st.session_state["characters"],
            treatment=st.session_state["treatment"],
            tone=st.session_state["tone"],
            previous_scene_text=prev_text,
            logline=st.session_state["logline"],
            world=st.session_state["world"],
            story_elements=st.session_state.get("story_elements", ""),
        )
        st.markdown(f'<div class="beat-tag">Beat {cur} 집필 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt, tokens=16000))
        st.session_state["beats_done"][cur] = result
        st.session_state["current_beat"] = cur + 1
        st.rerun()

    # 다시 쓰기
    if rewrite_btn and done:
        last_beat = max(done.keys())
        prompt = build_rewrite_prompt(
            genre=genre, beat_number=last_beat,
            current_text=done[last_beat],
            characters=st.session_state["characters"],
            instruction=rewrite_note,
        )
        st.markdown(f'<div class="beat-tag">Beat {last_beat} 다시 쓰는 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt, tokens=16000))
        st.session_state["beats_done"][last_beat] = result
        st.rerun()

# ═══════════════════════════════════════════════════════════
# DOWNLOAD — TXT + DOCX (수시 저장)
# ═══════════════════════════════════════════════════════════
if st.session_state.get("beats_done"):
    st.markdown(
        '<div class="section-header">📄 다운로드 <span class="en">EXPORT · SAVE ANYTIME</span></div>',
        unsafe_allow_html=True,
    )

    done_count = len(st.session_state["beats_done"])
    st.markdown(
        f'<div class="callout"><div class="cl">DATA</div>'
        f'{done_count}/15 비트 완료. 새로고침하면 데이터가 사라집니다. 수시로 저장하세요.</div>',
        unsafe_allow_html=True,
    )

    # TXT
    parts = []
    for b_no in sorted(st.session_state["beats_done"].keys()):
        b_info = BEATS_15[b_no - 1]
        parts.append(
            f"{'='*60}\n{b_info['act']} — Beat {b_no}. {b_info['name']}\n{'='*60}\n\n"
            f"{st.session_state['beats_done'][b_no]}"
        )
    all_text = "\n\n\n".join(parts)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label=f"TXT 저장 ({done_count}/15)",
            data=all_text,
            file_name=f"screenplay_{genre}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_dl2:
        try:
            docx_bytes = make_docx_bytes(genre, st.session_state["beats_done"],
                                         title=st.session_state.get("title", ""))
            st.download_button(
                label=f"DOCX 저장 ({done_count}/15)",
                data=docx_bytes,
                file_name=f"screenplay_{genre}_{datetime.now().strftime('%Y%m%d_%H%M')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        except ImportError:
            st.caption("DOCX: python-docx 미설치 — pip install python-docx")

# ═══════════════════════════════════════════════════════════
# RESET
# ═══════════════════════════════════════════════════════════
st.markdown("---")
col_r1, col_r2 = st.columns([3, 1])
with col_r2:
    if st.button("전체 초기화", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

st.caption("© 2026 BLUE JEANS PICTURES · Writer Engine v2.2")
