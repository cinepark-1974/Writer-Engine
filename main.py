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

ANTHROPIC_MODEL = "claude-sonnet-4-6"


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="BLUE JEANS WRITER ENGINE",
    page_icon="🟦",
    layout="centered",
)


# -----------------------------
# Helpers
# -----------------------------
def get_api_key() -> str | None:
    """Load API key from Streamlit secrets first, then environment variable."""
    key = st.secrets.get("ANTHROPIC_API_KEY", None)
    if key:
        return key
    return os.getenv("ANTHROPIC_API_KEY")


def get_client() -> Anthropic | None:
    api_key = get_api_key()
    if not api_key:
        return None
    return Anthropic(api_key=api_key)


def generate_with_anthropic(user_prompt: str, max_tokens: int = 4000) -> str:
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

        return "\n".join(parts).strip() if parts else "[EMPTY RESPONSE]"
    except Exception as e:
        return f"[ERROR]\n{str(e)}"


def init_session_state():
    defaults = {
        "generated_text": "",
        "edited_text": "",
        "last_prompt": "",
        "last_mode": "Project Brief",
        "save_message": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def save_current_text() -> None:
    text = st.session_state.get("edited_text", "").strip()
    if not text:
        st.session_state["save_message"] = "저장할 내용이 없습니다."
        return

    filename = f"writer_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    st.session_state["save_message"] = f"저장 준비 완료: {filename}"


# -----------------------------
# Init
# -----------------------------
init_session_state()


# -----------------------------
# Header
# -----------------------------
st.title("BLUE JEANS WRITER ENGINE")
st.caption("Young · Vintage · Free · Innovative")

api_key_exists = get_api_key() is not None
if api_key_exists:
    st.success("Anthropic API 연결 준비 완료")
else:
    st.warning("ANTHROPIC_API_KEY가 아직 설정되지 않았습니다.")


# -----------------------------
# Mode Select
# -----------------------------
mode = st.selectbox(
    "작업 모드",
    [
        "Project Brief",
        "Story Matrix",
        "Unit Blueprint",
        "Section Draft",
        "Dialogue Polish",
        "Ending Control",
        "Quality Control",
    ],
    index=0,
)

st.session_state["last_mode"] = mode

st.divider()

# -----------------------------
# Common Inputs
# -----------------------------
project_title = st.text_input("프로젝트 제목", placeholder="예: 폭립군")
genre = st.text_input("장르", placeholder="예: 느와르, 스릴러, 멜로, 코미디")
format_type = st.text_input("포맷", placeholder="예: 장편영화 / 시리즈 / 파일럿")
logline = st.text_area("로그라인", placeholder="한 줄 핵심 로그라인")
theme = st.text_area("테마 / 메시지", placeholder="이 이야기가 결국 무엇을 말하는가")
tone = st.text_input("톤", placeholder="예: 차갑고 건조한 리얼리즘")
audience = st.text_input("타깃 관객", placeholder="예: 한국 30~50대 관객")

st.divider()

# -----------------------------
# Mode-specific Inputs
# -----------------------------
user_prompt = ""

if mode == "Project Brief":
    user_prompt = build_project_brief_prompt(
        title=project_title,
        genre=genre,
        format_type=format_type,
        logline=logline,
        theme=theme,
        tone=tone,
        audience=audience,
    )

elif mode == "Story Matrix":
    protagonist = st.text_input("주인공", placeholder="예: 정섬")
    flaw = st.text_input("주인공의 결함 / 거짓 신념", placeholder="예: 타인을 절대 믿지 않는다")
    need = st.text_input("주인공의 진짜 필요 / 진실", placeholder="예: 혼자서는 끝까지 갈 수 없다는 사실")
    ending_goal = st.text_input("엔딩 목표", placeholder="예: 행동으로 테마를 증명하는 결말")

    user_prompt = build_story_matrix_prompt(
        title=project_title,
        genre=genre,
        logline=logline,
        theme=theme,
        protagonist=protagonist,
        flaw=flaw,
        need=need,
        ending_goal=ending_goal,
    )

elif mode == "Unit Blueprint":
    act_label = st.selectbox("Act", ["Act 1", "Act 2A", "Act 2B", "Act 3"])
    unit_no = st.number_input("Unit 번호", min_value=1, max_value=8, value=1, step=1)
    unit_goal = st.text_area("Unit 목표", placeholder="이 Unit이 서사적으로 해야 할 일")
    section_count = st.number_input("Section 수", min_value=1, max_value=4, value=2, step=1)
    beat_links = st.text_area("16비트 연결", placeholder="예: Catalyst, Debate, Break into 2")
    arc_links = st.text_area("아크 연결", placeholder="주인공 변화 / 관계 변화")
    genre_goal = st.text_area("장르 효능 목표", placeholder="예: 긴장 상승, 웃음 장치, 갈망 심화")
    ending_connection = st.text_area("엔딩 연결", placeholder="이 Unit이 엔딩에 어떻게 기여하는가")

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
    act_label = st.selectbox("Act", ["Act 1", "Act 2A", "Act 2B", "Act 3"])
    unit_no = st.number_input("Unit 번호", min_value=1, max_value=8, value=1, step=1)
    section_no = st.number_input("Section 번호", min_value=1, max_value=4, value=1, step=1)

    section_goal = st.text_area("Section 목표", placeholder="이 Section이 달성해야 할 극적 목적")
    previous_context = st.text_area("이전 맥락", placeholder="직전 장면 / 직전 Section 요약")
    character_notes = st.text_area("캐릭터 메모", placeholder="보이스, 욕망, 갈등, 숨기는 정보")
    tone_notes = st.text_area("톤 메모", placeholder="리듬, 분위기, 시각적 질감")
    genre_rule = st.text_area("장르 규칙", placeholder="이 장르에서 반드시 작동해야 하는 것")
    theme_line = st.text_area("테마 라인", placeholder="이 Section에서 테마가 어떻게 작동하는가")
    ending_line = st.text_area("엔딩 라인", placeholder="엔딩 방향과의 연결")

    user_prompt = build_section_screenplay_prompt(
        title=project_title,
        genre=genre,
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
    character_voice_notes = st.text_area("캐릭터 보이스 메모", placeholder="인물별 말투 규칙 / 태도 / 감정")
    scene_text = st.text_area("수정할 장면 텍스트", height=300, placeholder="여기에 기존 장면 텍스트를 붙여넣기")

    user_prompt = build_dialogue_polish_prompt(
        genre=genre,
        character_voice_notes=character_voice_notes,
        scene_text=scene_text,
    )

elif mode == "Ending Control":
    protagonist_arc = st.text_area("주인공 아크", placeholder="시작 → 위기 → 선택 → 변화")
    setup_payoffs = st.text_area("복선 / 회수", placeholder="반드시 회수해야 할 복선과 감정")
    desired_emotion = st.text_input("원하는 최종 감정", placeholder="예: 먹먹함, 카타르시스, 잔상")
    ending_type = st.text_input("엔딩 유형", placeholder="예: 비극적 승리 / 열린 결말 / 아이러니")

    user_prompt = build_ending_control_prompt(
        title=project_title,
        theme=theme,
        protagonist_arc=protagonist_arc,
        setup_payoffs=setup_payoffs,
        desired_emotion=desired_emotion,
        ending_type=ending_type,
    )

elif mode == "Quality Control":
    scene_or_section_text = st.text_area("점검할 텍스트", height=300, placeholder="QC할 장면 또는 섹션 전체 텍스트")

    user_prompt = build_qc_prompt(
        genre=genre,
        theme=theme,
        scene_or_section_text=scene_or_section_text,
    )

st.divider()

# -----------------------------
# Action Buttons
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("프롬프트 미리보기", use_container_width=True):
        st.session_state["last_prompt"] = user_prompt

with col2:
    if st.button("생성 실행", use_container_width=True):
        st.session_state["last_prompt"] = user_prompt
        result = generate_with_anthropic(user_prompt=user_prompt, max_tokens=4000)
        st.session_state["generated_text"] = result
        st.session_state["edited_text"] = result

# -----------------------------
# Prompt Preview
# -----------------------------
if st.session_state["last_prompt"]:
    with st.expander("현재 프롬프트 보기"):
        st.code(st.session_state["last_prompt"])

# -----------------------------
# Output
# -----------------------------
st.subheader("결과")

if st.session_state["edited_text"]:
    edited = st.text_area(
        "생성 결과 / 직접 수정",
        value=st.session_state["edited_text"],
        height=500,
        key="edited_text",
    )

    st.download_button(
        label="TXT 다운로드",
        data=edited,
        file_name=f"blue_jeans_writer_{mode.lower().replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    col3, col4 = st.columns(2)

    with col3:
        if st.button("수정본 저장", use_container_width=True):
            save_current_text()

    with col4:
        if st.button("수정본 기준 재실행", use_container_width=True):
            revised_prompt = (
                f"{st.session_state['last_prompt']}\n\n"
                "[REVISION INSTRUCTION]\n"
                "Use the following revised text as the current working draft and improve it without losing its strengths.\n\n"
                f"{st.session_state['edited_text']}"
            )
            result = generate_with_anthropic(user_prompt=revised_prompt, max_tokens=4000)
            st.session_state["generated_text"] = result
            st.session_state["edited_text"] = result

    if st.session_state["save_message"]:
        st.info(st.session_state["save_message"])
else:
    st.caption("아직 생성된 결과가 없습니다.")

st.divider()

with st.expander("System Prompt 보기"):
    st.code(SYSTEM_PROMPT)
