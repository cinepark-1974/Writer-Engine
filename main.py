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

ANTHROPIC_MODEL_WRITE = "claude-opus-4-6"      # 집필 (비트 쓰기, 다시 쓰기) — 최고 품질
ANTHROPIC_MODEL_PLAN  = "claude-sonnet-4-6"    # 구조 작업 (씬 플랜, 요소 추출) — 비용 효율

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
    "fact_based": False,
    "historical": False,
    "historical_type": "팩션",
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

def stream_ai(prompt: str, tokens: int = 16000, model: str = ""):
    """스트리밍 제너레이터. model 미지정 시 WRITE 모델 사용."""
    use_model = model or ANTHROPIC_MODEL_WRITE
    client = get_client()
    if not client:
        yield "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다."
        return
    try:
        with client.messages.stream(
            model=use_model, max_tokens=tokens,
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

def make_docx_bytes(genre: str, beats_done: dict, title: str = "",
                    fact_based: bool = False,
                    historical: bool = False,
                    historical_type: str = "") -> bytes:
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

    # ── 커스텀 Word 스타일 생성 (나중에 Word 스타일 패널에서 일괄 수정 가능) ──
    from docx.enum.style import WD_STYLE_TYPE
    from docx.shared import Cm

    def _set_eastasia_font(style_or_run_element, font_name='함초롬바탕'):
        """rPr에 eastAsia 폰트 설정."""
        rpr_elem = style_or_run_element
        rf = rpr_elem.find(qn('w:rFonts'))
        if rf is None:
            rf = rpr_elem.makeelement(qn('w:rFonts'), {})
            rpr_elem.append(rf)
        rf.set(qn('w:eastAsia'), font_name)

    # [스타일 1] 씬번호 — Bold, 위 24pt / 아래 6pt, 1.5줄 간격
    style_scene = doc.styles.add_style('씬번호', WD_STYLE_TYPE.PARAGRAPH)
    style_scene.base_style = doc.styles['Normal']
    style_scene.font.name = '함초롬바탕'
    style_scene.font.size = Pt(11)
    style_scene.font.bold = True
    style_scene.paragraph_format.space_before = Pt(24)
    style_scene.paragraph_format.space_after = Pt(6)
    style_scene.paragraph_format.line_spacing = 1.5
    _set_eastasia_font(style_scene.element.get_or_add_rPr())

    # [스타일 2] 대사 — Bold, 왼쪽 들여쓰기 1.25cm, 위 8pt / 아래 2pt
    style_dialogue = doc.styles.add_style('대사', WD_STYLE_TYPE.PARAGRAPH)
    style_dialogue.base_style = doc.styles['Normal']
    style_dialogue.font.name = '함초롬바탕'
    style_dialogue.font.size = Pt(10)
    style_dialogue.font.bold = True
    style_dialogue.paragraph_format.left_indent = Cm(1.25)
    style_dialogue.paragraph_format.space_before = Pt(8)
    style_dialogue.paragraph_format.space_after = Pt(2)
    style_dialogue.paragraph_format.line_spacing = 1.5
    _set_eastasia_font(style_dialogue.element.get_or_add_rPr())

    # [스타일 3] 대사연속 — 대사 이어쓰기 (캐릭터명 없이)
    style_dialogue_cont = doc.styles.add_style('대사연속', WD_STYLE_TYPE.PARAGRAPH)
    style_dialogue_cont.base_style = style_dialogue
    style_dialogue_cont.paragraph_format.space_before = Pt(0)
    style_dialogue_cont.paragraph_format.space_after = Pt(0)

    # [스타일 4] 지문 — 일반 텍스트, 들여쓰기 없음
    style_action = doc.styles.add_style('지문', WD_STYLE_TYPE.PARAGRAPH)
    style_action.base_style = doc.styles['Normal']
    style_action.font.name = '함초롬바탕'
    style_action.font.size = Pt(10)
    style_action.font.bold = False
    style_action.paragraph_format.space_before = Pt(2)
    style_action.paragraph_format.space_after = Pt(2)
    _set_eastasia_font(style_action.element.get_or_add_rPr())

    # ── 헬퍼 함수 (스타일 기반) ──
    def add_text(text, bold=False, size=None, color=None, align=None):
        """커버 페이지용 범용 텍스트."""
        p = doc.add_paragraph()
        if align:
            p.alignment = align
        r = p.add_run(text)
        r.font.name = "함초롬바탕"
        _set_eastasia_font(r._element.get_or_add_rPr())
        if bold:
            r.bold = True
        if size:
            r.font.size = size
        if color:
            r.font.color.rgb = color
        return p

    def add_scene_heading(text):
        """씬 헤딩 — '씬번호' 스타일 적용."""
        p = doc.add_paragraph(style='씬번호')
        r = p.add_run(text)
        r.font.name = "함초롬바탕"
        _set_eastasia_font(r._element.get_or_add_rPr())
        return p

    def add_dialogue(char_name, parenthetical, line, continuation=False):
        """대사 — '대사'/'대사연속' 스타일 적용.
        continuation=True이면 캐릭터명 생략."""
        if continuation:
            p = doc.add_paragraph(style='대사연속')
            paren = f"({parenthetical}) " if parenthetical else ""
            full = f"\t\t{paren}{line}"
        else:
            p = doc.add_paragraph(style='대사')
            paren = f"({parenthetical}) " if parenthetical else ""
            full = f"{char_name}\t\t{paren}{line}"
        r = p.add_run(full)
        r.font.name = "함초롬바탕"
        _set_eastasia_font(r._element.get_or_add_rPr())
        return p

    def add_action(text):
        """지문 — '지문' 스타일 적용."""
        p = doc.add_paragraph(style='지문')
        r = p.add_run(text)
        r.font.name = "함초롬바탕"
        _set_eastasia_font(r._element.get_or_add_rPr())
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
    add_text(f"Writer Engine v3.0  ·  {len(beats_done)}/15 비트",
             size=Pt(9), align=WD_ALIGN_PARAGRAPH.CENTER,
             color=RGBColor(0x8E, 0x8E, 0x99))
    doc.add_page_break()

    # ── 면책 자막 페이지 ──
    # 적용 조건:
    #   (1) 실화 배경 기반 작품 (fact_based)
    #   (2) 팩션·퓨전 역사영화 (정통은 실존 사건·인물 중심이라 면책 문구가 맞지 않음)
    _need_disclaimer = fact_based or (
        historical and ("팩션" in (historical_type or "") or "퓨전" in (historical_type or "")
                        or "faction" in (historical_type or "").lower()
                        or "fusion" in (historical_type or "").lower())
    )
    if _need_disclaimer:
        for _ in range(10):
            doc.add_paragraph("")
        add_text("본 작품에 등장하는 인물, 단체, 지명, 상호, 사건은",
                 size=Pt(11), align=WD_ALIGN_PARAGRAPH.CENTER)
        add_text("모두 허구이며, 실존하는 것과 관련이 있더라도",
                 size=Pt(11), align=WD_ALIGN_PARAGRAPH.CENTER)
        add_text("극적 구성을 위해 각색되었습니다.",
                 size=Pt(11), align=WD_ALIGN_PARAGRAPH.CENTER)
        doc.add_paragraph("")
        add_text("All characters, organizations, places, and events in this work",
                 size=Pt(9), align=WD_ALIGN_PARAGRAPH.CENTER,
                 color=RGBColor(0x8E, 0x8E, 0x99))
        add_text("are fictional. Any resemblance to actual persons or events is",
                 size=Pt(9), align=WD_ALIGN_PARAGRAPH.CENTER,
                 color=RGBColor(0x8E, 0x8E, 0x99))
        add_text("dramatized for narrative purposes.",
                 size=Pt(9), align=WD_ALIGN_PARAGRAPH.CENTER,
                 color=RGBColor(0x8E, 0x8E, 0x99))
        doc.add_page_break()

    # ── 본문 파싱 + 변환 ──
    # 씬 헤딩 패턴: S#숫자. INT./EXT. 또는 그냥 INT./EXT.
    heading_re = re.compile(r'^S?#?\d*\.?\s*(INT\.|EXT\.|INT\./EXT\.)\s*(.+)', re.IGNORECASE)
    # 캐릭터명 패턴: 2칸+ 들여쓰기 + 이름 (1~15자) + 선택적 (V.O.) / (O.S.) / (CONT'D)
    char_re = re.compile(
        r'^\s{2,}([가-힣a-zA-Z\s]{1,15}?)\s*'
        r'(?:\((V\.O\.|O\.S\.|CONT\'D|cont\'d|v\.o\.|o\.s\.)\))?\s*$',
        re.IGNORECASE
    )
    # 인라인 대사 패턴: "캐릭터명\t\t(지시)대사" 또는 "캐릭터명 (V.O.)\t\t대사"
    inline_dialogue_re = re.compile(
        r'^([가-힣a-zA-Z\s]{1,15}?)\s*'
        r'(?:\((V\.O\.|O\.S\.|CONT\'D|cont\'d|v\.o\.|o\.s\.)\))?\s*'
        r'\t{1,}\s*(?:\(([^)]*)\)\s*)?(.+)',
        re.IGNORECASE
    )
    # 괄호 지시
    paren_re = re.compile(r'^\s{2,}\((.+?)\)\s*$')
    # 구분선/내부메모 (출력 제외)
    divider_re = re.compile(r'^(═{3,}|─{3,}|---)')

    # ═══════════════════════════════════════════════════════════
    # 메타데이터 유출 차단 — 강화된 필터 (v3.4)
    # Writer Engine 프롬프트가 요구하는 "내부 메모" 항목이 본문에 유출되는 버그 차단.
    # 아래 키워드 중 하나라도 매칭되면 해당 라인은 DOCX 본문에서 제외.
    # ═══════════════════════════════════════════════════════════
    META_PREFIX_PATTERNS = [
        # 장르 장치 메타 (10개 장치 x 9장르)
        "premise_engine", "comic_contradiction", "character_comic_flaw",
        "comic_escalation", "line_surprise", "status_comedy",
        "timing_precision", "callback_payoff", "scene_comic_engine",
        "joke_density",
        "fear_anticipation", "uncertainty", "sensory_unease",
        "threat_design", "dread_pacing", "violation_of_safety",
        "image_residue", "vulnerability", "false_relief",
        "terror_escalation",
        "information_asymmetry", "escalation", "clock_device",
        "suspense_peak", "plot_twist", "investigator_obstacle",
        "villain_intelligence", "moral_ambiguity", "red_herring",
        "irreversible_stakes",
        "action_spark", "physical_choreography", "setpiece_scale",
        "hero_signature", "obstacle_escalation", "stakes_personal",
        "counter_attack", "low_point", "final_confrontation",
        "kinetic_rhythm",
        "longing_distance", "touch_hesitation", "romantic_specificity",
        "emotional_subtext", "miscommunication", "emotional_reversal",
        "vulnerability_moment", "physical_chemistry", "obstacle_internal",
        "payoff_emotional",
        "world_rule", "tech_showcase", "awe_moment", "info_drip",
        "human_anchor", "rule_consequence", "visual_wonder",
        "scale_shift", "philosophical_stakes", "discovery_rhythm",
        "magic_rule", "mythic_echo", "threshold_crossing",
        "wonder_image", "sacrifice_price", "prophecy_twist",
        # 비트 메타 공통
        "writer_notes", "plant_payoff_tag", "plant_payoff",
        "scene_meta", "quality_check",
        # 한글 메타 헤더
        "맥거핀", "캐릭터 비밀", "핵심 장소", "모티프", "모티프:",
        "Plant:", "Plant/Payoff", "Payoff:", "Payoff :",
        "서브플롯", "관객 심리", "열린 질문", "Dramatic Irony",
        "Zeigarnik", "보이스 점검", "보이스점검",
        "비트 요약", "비트요약", "비트 구조 유형", "액션 아이디어",
        "서사동력", "작동한 장르", "작동 장르", "핵심 요소",
        "장르 드라이브", "캐릭터 전술", "캐릭터 아크",
        "서브플롯 진행", "강회장 B-Story", "B-Story",
        "민준 서브플롯", "민준 아크",
        # 장르 드라이브 5점 체크 항목 (① ② ③ ④ ⑤ 뒤에 오는 메타 키워드)
        "정보 비대칭", "정보비대칭", "에스컬레이션",
        "적대자", "타이머", "장르 쾌감", "장르쾌감",
        # 추가 메타 헤더 (v3.4.1 보강)
        "캐릭터 전술", "캐릭터전술", "Payoff 회수", "Payoff회수",
        "Plant 유지", "Plant유지", "비밀",
    ]
    # 줄의 시작 부분에 대한 매칭 (불릿/기호 뒤 텍스트)
    META_LINE_RE = re.compile(
        r'^(?:[\s•·\-*⭐★─═]+\**)*(?:[①②③④⑤⑥⑦⑧⑨⑩]\s*)?'
        r'(' + '|'.join(re.escape(p) for p in META_PREFIX_PATTERNS) + r')'
        r'(?:\s|[:\-—.(]|$)',
        re.IGNORECASE
    )

    # (Beat N plant → S#NN payoff) / (S#NN → S#NN) / (전체 plant → S#NN payoff) 같은 개발자 표기
    META_DEV_NOTATION_RE = re.compile(
        r'\((?:Beat\s*\d+|S#\s*\d+|전체|전반|후반)[^)]*(?:plant|payoff|→|->)[^)]*\)',
        re.IGNORECASE
    )
    # "- 설명(S#NN) — 미공개/미등장/공개/열린 채" 같은 단독 dev 코멘트
    META_DEV_COMMENT_RE = re.compile(
        r'^[\s•·\-*]+.*?\(S#\s*\d+(?:[/,]\s*\d+)*\)\s*(?:—|-|–)\s*(?:미공개|미등장|미해결|공개|폭로|열린|유지|부재)',
        re.IGNORECASE
    )
    # "(관객 O, 유진 X) — 미공개/유지" 같은 Dramatic Irony 메타 주석
    META_IRONY_COMMENT_RE = re.compile(
        r'\(관객\s*[OX].*?(?:유진|주인공|캐릭터)\s*[OX][^)]*\)\s*(?:—|-|–)\s*(?:미공개|미등장|미해결|공개|유지)',
    )
    # "· 캐릭터명:" 또는 "- 캐릭터명:" 으로 시작하는 서브플롯 요약
    # (본문 대사와 구분: 대사는 "캐릭터\t\t대사", 요약은 불릿+콜론)
    META_CHARACTER_SUMMARY_RE = re.compile(
        r'^[\s•·\-*]+\s*([가-힣]+(?:[·∙・]\s*[가-힣]+)*(?:\s*커플)?)\s*:',
    )
    # "- 설명 (Beat N plant → S#NN payoff): 내용" — 불릿 + 설명 + 괄호 dev notation + 콜론
    META_BULLET_DEV_RE = re.compile(
        r'^[\s•·\-*]+.*?\((?:Beat\s*\d+|S#\s*\d+)[^)]*\)\s*:',
        re.IGNORECASE
    )

    def is_meta_line(s: str) -> bool:
        """메타데이터 라인 여부 판정."""
        if not s:
            return False
        # 1차: 메타 키워드 직접 매칭
        if META_LINE_RE.match(s):
            return True
        # 2차: snake_case 장르 장치명 (· premise_engine ...)
        m = re.match(r'^[\s•·\-*⭐★─═]+\s*([a-z]+_[a-z_]+)', s)
        if m:
            return True
        # 3차: 개발자 표기 괄호 + 콜론 (- 간판 케이블타이(Beat 1 plant → S#95 payoff):)
        if META_BULLET_DEV_RE.match(s):
            return True
        # 4차: 캐릭터명 + 콜론 서브플롯 요약 (· 오현수·박지영 커플: ...)
        # 주의: 본문 대사는 "캐릭터\t\t대사"이고 불릿 없음 → 오차단 안 됨
        if META_CHARACTER_SUMMARY_RE.match(s):
            return True
        # 5차: 줄 전체에 개발자 표기가 있으면 메타 (예: "... (Beat 3 plant → S#45 payoff) ...")
        if META_DEV_NOTATION_RE.search(s):
            return True
        # 6차: 개발자 코멘트 라인 (예: "- 진호 도면 메모(S#91) — 미공개.")
        if META_DEV_COMMENT_RE.match(s):
            return True
        # 7차: Dramatic Irony 메타 주석 (예: "- 건물 강회장 소유(관객 O, 유진 X) — 미공개.")
        if META_IRONY_COMMENT_RE.search(s):
            return True
        return False

    current_act = ""
    for b_no in sorted(beats_done.keys()):
        b_info = BEATS_15[b_no - 1]

        # ACT 전환
        if b_info["act"] != current_act:
            if current_act:
                doc.add_page_break()
            current_act = b_info["act"]

        text = beats_done[b_no]

        # ═══════════════════════════════════════════════════════════
        # 대사 형식 붕괴 자동 복구 (v3.4 신규)
        # 버그: 긴 컨텍스트에서 AI가 대사 포맷 규칙을 잊고
        #       "캐릭터\n\n대사" 형식으로 출력 (S#89~ 에서 발견됨)
        # 복구: "캐릭터" 단독 라인 + 빈 라인 + 대사 라인 → "캐릭터\t\t대사"
        # ═══════════════════════════════════════════════════════════
        _CHAR_NAMES = {
            '유진', '진호', '세웅', '다은', '강회장', '민준', '박지영', '오현수',
            '이진호', '반세웅', '김사장', '비서', '편집자', '기사', '배달 기사',
            '사장', '민준 엄마', '박씨', '엄마', '아빠', '형', '누나', '아들', '딸',
        }
        _broken_lines = text.split("\n")
        _fixed_lines = []
        _j = 0
        while _j < len(_broken_lines):
            _cur = _broken_lines[_j].strip()
            # 패턴 A: "캐릭터명" 단독 + 빈줄 + 대사 → "캐릭터\t\t대사"
            if (_cur in _CHAR_NAMES and
                _j + 2 < len(_broken_lines) and
                _broken_lines[_j + 1].strip() == "" and
                _broken_lines[_j + 2].strip() and
                not _broken_lines[_j + 2].strip().startswith("S#") and
                _broken_lines[_j + 2].strip() not in _CHAR_NAMES):
                _next_content = _broken_lines[_j + 2].strip()
                # 괄호 지시(예: "(잠깐 생각하고)")가 있으면 다음 줄이 진짜 대사
                if _next_content.startswith("(") and _next_content.endswith(")") and \
                   _j + 4 < len(_broken_lines) and _broken_lines[_j + 3].strip() == "" and \
                   _broken_lines[_j + 4].strip():
                    _fixed_lines.append(f"{_cur}\t\t{_next_content} {_broken_lines[_j + 4].strip()}")
                    _j += 5
                    continue
                _fixed_lines.append(f"{_cur}\t\t{_next_content}")
                _j += 3
                continue
            _fixed_lines.append(_broken_lines[_j])
            _j += 1
        lines = _fixed_lines

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 빈 줄
            if not stripped:
                i += 1
                continue

            # ★ WRITER_NOTES 마커 블록 스킵 (v3.4 신규)
            # 프롬프트가 "<WRITER_NOTES_BEGIN>...<WRITER_NOTES_END>" 마커로
            # 메타 블록을 감싸도록 지시. 이 마커 안쪽 전체를 차단.
            if "<WRITER_NOTES_BEGIN>" in stripped or "WRITER_NOTES_BEGIN" in stripped:
                i += 1
                while i < len(lines):
                    if ("<WRITER_NOTES_END>" in lines[i] or
                        "WRITER_NOTES_END" in lines[i]):
                        i += 1
                        break
                    i += 1
                continue
            # BLOCK 2 헤더 (메타 블록 시작 신호) 감지 — 마커를 잊어도 차단
            if stripped.startswith("[BLOCK 2:") or stripped.startswith("[BLOCK 2 "):
                # 파일 끝까지 스킵
                i = len(lines)
                continue
            if stripped == "[BLOCK 1: 시나리오 본문]" or stripped.startswith("[BLOCK 1:"):
                i += 1
                continue
            if stripped.startswith("━━━"):
                i += 1
                continue

            # 구분선/내부메모 스킵 (--- 또는 ═══ 이후 블록 전체)
            if divider_re.match(stripped):
                i += 1
                # 내부메모 블록 스킵 (다음 씬 헤딩이나 Beat 헤더까지)
                while i < len(lines):
                    memo_line = lines[i].strip()
                    if heading_re.match(memo_line):
                        break
                    if "Beat " in memo_line and "—" in memo_line:
                        break
                    i += 1
                continue

            # 내부 메모 블록 감지 — "**내부 메모**" / "내부 메모:" / "내부 메모" 등
            if "내부 메모" in stripped:
                i += 1
                # 내부 메모 블록 전체 스킵 (다음 씬 헤딩까지)
                while i < len(lines):
                    memo_line = lines[i].strip()
                    if heading_re.match(memo_line):
                        break
                    i += 1
                continue

            # ★ 메타데이터 개별 줄 차단 (v3.4 신규 강화 필터)
            # 장르 장치 이름, 비트 메타 항목, 한글 메타 헤더 등을
            # 광범위하게 매칭하여 본문 유출 차단
            if is_meta_line(stripped):
                i += 1
                continue

            # Beat 헤더 스킵 (프롬프트가 넣는 ACT — Beat 헤더)
            if stripped.startswith("═") or "Beat " in stripped and "—" in stripped:
                i += 1
                continue

            # 씬 헤딩
            m = heading_re.match(stripped)
            if m:
                # S#번호 포함 전체 텍스트 사용
                add_scene_heading(stripped)
                i += 1
                continue

            # 인라인 대사 감지: "캐릭터명\t\t(지시) 대사" 형식 (V.O./O.S. 포함)
            im = inline_dialogue_re.match(stripped)
            if im:
                char_name = im.group(1).strip()
                vo_marker = im.group(2) or ""  # V.O., O.S. 등
                inline_paren = im.group(3) or ""  # (부드럽게) 등
                inline_text = im.group(4).strip()
                # V.O./O.S.를 캐릭터명에 포함
                if vo_marker:
                    char_name = f"{char_name} ({vo_marker})"
                add_dialogue(char_name, inline_paren, inline_text)
                i += 1
                continue

            # 캐릭터명 + 대사 감지 (들여쓰기 형식)
            cm = char_re.match(line)
            if cm:
                char_name = cm.group(1).strip()
                vo_marker = cm.group(2) or ""  # V.O., O.S. 등
                if vo_marker:
                    char_name = f"{char_name} ({vo_marker})"
                parenthetical = ""
                dialogue_lines = []
                i += 1

                # 괄호 지시 확인
                if i < len(lines):
                    pm = paren_re.match(lines[i])
                    if pm:
                        parenthetical = pm.group(1)
                        i += 1

                # 대사 수집
                while i < len(lines):
                    dl = lines[i]
                    ds = dl.strip()
                    if not ds:
                        break
                    if heading_re.match(ds):
                        break
                    if char_re.match(dl):
                        break
                    if inline_dialogue_re.match(ds):
                        break
                    dialogue_lines.append(ds)
                    i += 1

                # 대사 출력 — 한 캐릭터의 연속 대사를 하나로 병합
                # AI가 한 발화 안에서 줄바꿈을 넣으면 여러 줄로 쪼개지는 문제 해결
                if dialogue_lines:
                    # 괄호 지시문 (행동 지시)을 감지해서 분리 처리
                    # 예: "(결제 페이지를 본다)" 같은 줄은 대사와 분리
                    merged_parts = []  # [(type, text)] — type은 "dialogue" 또는 "action"
                    current_dialogue = []
                    for dl in dialogue_lines:
                        dl_stripped = dl.strip()
                        # 줄 전체가 괄호로 시작해서 괄호로 끝나면 행동 지시
                        if (dl_stripped.startswith("(") and dl_stripped.endswith(")")
                            and len(dl_stripped) > 2):
                            # 지금까지 모은 대사를 먼저 합치기
                            if current_dialogue:
                                merged_parts.append(("dialogue", " ".join(current_dialogue)))
                                current_dialogue = []
                            merged_parts.append(("action", dl_stripped))
                        else:
                            current_dialogue.append(dl_stripped)
                    if current_dialogue:
                        merged_parts.append(("dialogue", " ".join(current_dialogue)))

                    # 출력
                    first = True
                    for part_type, part_text in merged_parts:
                        if part_type == "dialogue":
                            if first:
                                add_dialogue(char_name, parenthetical, part_text)
                                parenthetical = ""
                                first = False
                            else:
                                add_dialogue(char_name, "", part_text, continuation=True)
                        else:
                            # 행동 지시는 지문으로 표시 (대사 사이에 끼워 넣기)
                            add_action(part_text)
                            # 행동 지시 뒤 대사는 다시 캐릭터명 표시
                            first = True
                    # 처음부터 모두 행동 지시만 있던 경우 fallback
                    if first:
                        add_dialogue(char_name, parenthetical, "")
                else:
                    add_dialogue(char_name, parenthetical, "")
                continue

            # 그 외 = 지문
            add_action(stripped)
            i += 1

    # ── 푸터 ──
    doc.add_page_break()
    add_text(f"© 2026 BLUE JEANS PICTURES · Writer Engine v3.0",
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
    # Creator Engine과 동일한 장르 목록 (로맨틱 코미디 포함)
    # _is_comedy/_is_romance가 "로맨틱 코미디"를 자동 감지해 COMEDY+ROMANCE 둘 다 주입
    genre_list = [
        "미지정", "범죄/스릴러", "드라마", "액션", "로맨스", "코미디",
        "로맨틱 코미디", "호러/공포", "SF", "판타지",
        "시대극/사극", "느와르", "미스터리", "전쟁", "뮤지컬", "다큐/논픽션"
    ]
    current_genre = st.session_state.get("genre", "범죄/스릴러")
    if current_genre not in genre_list:
        current_genre = "미지정"
    genre = st.selectbox("장르", genre_list,
                          index=genre_list.index(current_genre))
    st.session_state["genre"] = genre
with col_g2:
    fmt = "영화 (장편)"
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

# ── 실화 배경 기반 작품 체크 ──
st.session_state["fact_based"] = st.checkbox(
    "실화 배경 기반 작품 (실명 비사용 + 사실성 확보 규칙 적용)",
    value=st.session_state.get("fact_based", False),
    help="체크하면 집필 시 실명·특정 가능 디테일 회피 규칙이 적용되고, "
         "DOCX에 각색 고지 자막이 자동 삽입됩니다. "
         "실제 지명·시대 사건·공적 직함은 사용 가능합니다."
)

# ── 역사영화 체크 + 유형 선택 ──
_hist_col1, _hist_col2 = st.columns([2, 3])
with _hist_col1:
    st.session_state["historical"] = st.checkbox(
        "역사영화 (시대 고증 + 유형별 규칙 적용)",
        value=st.session_state.get("historical", False),
        help="체크하면 시대감 구체화·시대 언어 균형·공간 설계 등 역사영화 공통 규칙이 적용되고, "
             "선택한 유형(정통/팩션/퓨전)에 따라 세부 집필 철학이 분기됩니다."
    )
with _hist_col2:
    if st.session_state.get("historical", False):
        st.session_state["historical_type"] = st.selectbox(
            "역사영화 유형",
            options=["정통역사영화", "팩션역사영화", "퓨전역사영화"],
            index=["정통역사영화", "팩션역사영화", "퓨전역사영화"].index(
                st.session_state.get("historical_type", "팩션")
                if st.session_state.get("historical_type", "팩션") in ["정통역사영화", "팩션역사영화", "퓨전역사영화"]
                else ("정통역사영화" if "정통" in st.session_state.get("historical_type", "팩션")
                      else "팩션역사영화" if "팩션" in st.session_state.get("historical_type", "팩션")
                      else "퓨전역사영화")
            ),
            help="정통: 실재 사건·인물 중심, 사료 존중, 감정 과잉 회피 (남한산성·1987)  |  "
                 "팩션: 실재 시대+가공 드라마, 재미 코드 자유 (왕의 남자·암살·밀정)  |  "
                 "퓨전: 시대 차용+자유 서사, 장르 재미 우선 (조선명탐정·전우치)"
        )

# API 상태
if get_client():
    st.success(f"API 준비 완료 — 집필: {ANTHROPIC_MODEL_WRITE} · 구조: {ANTHROPIC_MODEL_PLAN}")
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
        fact_based=st.session_state.get("fact_based", False),
        historical=st.session_state.get("historical", False),
        historical_type=st.session_state.get("historical_type", "팩션"),
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
        result = st.write_stream(stream_ai(prompt, model=ANTHROPIC_MODEL_PLAN))
        st.session_state["plan_1막"] = result
        st.session_state["plan_2막"] = ""
        st.session_state["plan_3막"] = ""
        st.session_state["beats_done"] = {}
        st.session_state["current_beat"] = 1
        st.rerun()

    if btn2:
        prompt = build_scene_plan_prompt(act="2막", **plan_kw, previous_plan=st.session_state["plan_1막"])
        st.markdown('<div class="act-tag">2막 씬 플랜 생성 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt, model=ANTHROPIC_MODEL_PLAN))
        st.session_state["plan_2막"] = result
        st.session_state["plan_3막"] = ""
        st.rerun()

    if btn3:
        prev = st.session_state["plan_1막"] + "\n\n" + st.session_state["plan_2막"]
        prompt = build_scene_plan_prompt(act="3막", **plan_kw, previous_plan=prev)
        st.markdown('<div class="act-tag">3막 씬 플랜 생성 중…</div>', unsafe_allow_html=True)
        result = st.write_stream(stream_ai(prompt, model=ANTHROPIC_MODEL_PLAN))
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
            result = st.write_stream(stream_ai(extract_prompt, model=ANTHROPIC_MODEL_PLAN))
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
            fact_based=st.session_state.get("fact_based", False),
            historical=st.session_state.get("historical", False),
            historical_type=st.session_state.get("historical_type", "팩션"),
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
                                         title=st.session_state.get("title", ""),
                                         fact_based=st.session_state.get("fact_based", False),
                                         historical=st.session_state.get("historical", False),
                                         historical_type=st.session_state.get("historical_type", "팩션"))
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

st.caption("© 2026 BLUE JEANS PICTURES · Writer Engine v3.0")
