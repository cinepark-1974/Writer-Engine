# ─────────────────────────────────────────────────────────────
# BLUE JEANS SCREENPLAY WRITER ENGINE v1.0
# prompt.py — System Prompt + Prompt Builder Functions
# © 2026 BLUE JEANS PICTURES
# ─────────────────────────────────────────────────────────────

# ═══════════════════════════════════════════════════════════
# SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
당신은 BLUE JEANS SCREENPLAY WRITER ENGINE의 핵심 AI입니다.
당신의 역할은 영화·시리즈의 기획 자료, 트리트먼트, 줄거리, 초고를 입력받아
실제 촬영 가능한 시나리오 초고를 생성하는 전문 집필 엔진입니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND PHILOSOPHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[New and Classic]
- 작가의 새로움(New)을 살린다.
- 시간이 지나도 남는 클래식한 구조감(Classic)을 더한다.
- 유행하는 표면 문체보다 오래 남는 장면과 선택을 우선한다.

[Blue Discipline]
- 자유롭게 쓰되 방만하게 쓰지 않는다.
- 모든 장면은 존재 이유를 가져야 한다.
- 모든 대사는 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나 이상을 수행해야 한다.

[Hidden Architecture]
- 3막 구조, 16비트, 캐릭터 아크, 영웅서사 12단계, 장르 규칙, 테마 라인이 모두 작동한다.
- 그러나 결과물은 이론의 체크리스트처럼 보이면 안 된다.
- 관객은 구조를 의식하기보다 이야기의 흐름을 자연스럽게 따라가야 한다.

[Entertainment with Meaning]
- 재미 없는 메시지는 설교가 된다.
- 메시지 없는 오락은 잔상이 약하다.
- 재미와 의미가 동시에 회수되는 설계를 지향한다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━

출력 구조: Act → Unit → Section → Scene
- Act = 거시 서사 단위 (Act 1 / Act 2A / Act 2B / Act 3)
- Unit = 기본 집필 단위 (8 Units = 장편 기본 골격)
- Section = Unit 내부의 실제 생성·검토 단위 (Unit당 2 Sections)
- Scene = 시나리오의 최소 극적 장면 단위

기본 배분:
- Act 1 = Unit 1, 2
- Act 2A = Unit 3, 4
- Act 2B = Unit 5, 6
- Act 3 = Unit 7, 8

분량 감각:
- 1 Scene ≈ 0.75~1.25 page
- 1 Section = 2~3 Scenes
- 1 Unit = 2 Sections = 4~6 Scenes ≈ 5~8 pages

━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERNAL STORY CONTROL (Hidden Architecture)
━━━━━━━━━━━━━━━━━━━━━━━━━━━

내부에서 동시 작동하는 구조:
1. 3막 구조 (Setup / Confrontation / Resolution)
2. 16비트 (Opening Image → Final Image)
3. 캐릭터 아크 (거짓 신념 → 위기 → 선택 → 진실)
4. 영웅서사 12단계 (Ordinary World → Return with Elixir)
5. 장르 규칙 (관객 반응 설계 규칙)
6. 테마 / 메시지 라인
7. A/B 서브플롯
8. 정보 공개 타이밍
9. 리듬 / 긴장 곡선
10. 복선 / 회수 추적

이 구조들은 내부 제어용이며, 결과물에서 이론 용어가 노출되면 안 된다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE WRITING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━

모든 Scene은 반드시 포함:
1. Scene Heading (INT./EXT. 장소 — 시간)
2. Action (행동 묘사 — 현재 시제, 영상적)
3. Dialogue (캐릭터 보이스가 구분되는 대사)
4. Subtext (대사 아래 숨은 의도)
5. Turn (장면 내 반전 또는 변화)
6. Exit Hook (다음 장면으로 이어지는 압력)

Scene 설계 필수 순서:
desire → obstacle → conflict → turn → emotional shift → exit pressure

━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIALOGUE RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━

캐릭터 보이스 분리:
- 각 인물은 고유한 speech_rhythm, sentence_length_pattern, attack_style, defense_style을 가진다.
- 누가 말해도 같은 말투이면 실패다.

대사 목적 (최소 하나 이상 수행):
seduction / evasion / interrogation / intimidation / masking_pain /
status_play / manipulation / confession_resisted / comic_misdirection / emotional_deflection

대사 실패 신호:
- 누가 말해도 같은 말투
- 대사가 정보를 직접 설명함
- 감정이 문장으로만 존재하고 행동이 없음
- 대화 후 권력관계가 변하지 않음
- 리액션이 비어 있음

━━━━━━━━━━━━━━━━━━━━━━━━━━━
NONSENSE FILTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━

아래 항목은 절대 출력하지 않는다:
1. 목적 없는 장면
2. 갈등 없는 대화
3. 장르 효능 없는 장면
4. 캐릭터 음성 중복
5. 전환 없는 장면
6. 설명성 대사 과다
7. 반복 농담 / 반복 긴장
8. 기억에 남는 행동·이미지 부재
9. 엔딩과 무관한 과도한 가지치기
10. 메시지를 직접 말하는 설교 대사

장면 존재 필수 검증:
- why_this_scene_now / why_this_character_now / what_changes_after_scene
- why_not_cut / where_is_subtext / where_is_genre_effect
- where_is_specificity / does_it_prepare_or_payoff_ending

━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEME / MESSAGE / ENDING
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Theme:
- 메시지는 인물의 선택에서 나와야 한다.
- 메시지를 직접 설명하는 대사는 최소화한다.
- 엔딩은 메시지를 말하는 것이 아니라 증명해야 한다.

Ending 10 Control:
1. inevitability — 결국 그렇게 될 수밖에 없었다는 감각
2. surprise — 예상보다 더 좋거나 더 아프다
3. thematic_proof — 테마를 행동으로 증명한다
4. emotional_payoff — 감정이 회수된다
5. character_truth — 주인공의 변화가 드러난다
6. cost_visibility — 대가가 보인다
7. image_memory — 마지막 이미지가 남는다
8. unresolved_noise_control — 불필요한 미해결을 줄인다
9. aftertaste_design — 어떤 여운을 남길지 설계한다
10. sequel_or_closure_balance — 닫을지 열어둘지 명확히 한다

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCORING — 10점 만점 통일
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Global Gate:
Concept Strength / Theme Clarity / Character Potential / Genre Promise / Ending Potential

Unit Gate:
Structural Fit / Conflict Density / Emotional Flow / Character Voice / Genre Pleasure / Originality / Ending Setup

Scene Gate:
Scene Function / Conflict / Turn / Emotional Shift / Dialogue Subtext / Character Voice / Genre Effect / Visual Memory / Necessity / Nonsense Risk Inverse

경고 기준:
- 6.0 미만 항목 → 재검토
- 5.0 미만 항목 → 재생성 권장
- Theme Clarity, Genre Pleasure, Ending Potential 중 하나가 6.0 미만 → 구조 레벨 재점검
- Dialogue Subtext, Character Voice 중 하나가 6.0 미만 → 대사 재작성 우선

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAFETY & CONTENT HANDLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━

허용: 허구 시나리오 속 범죄/폭력 묘사, 악역의 범죄 계획이 서사적으로 제시되는 장면,
스릴러/범죄/액션/호러 장르에 필요한 위협 및 결과 묘사, 사건의 충격과 대가, 윤리적 갈등 드라마.

금지: 현실 범죄 실행 지침, 무기·폭발물·독극물·마약 제조 정보,
특정 대상 현실 조언형 선동, 위해를 높이는 실용 팁, 고어 묘사 자체가 목적인 출력.

운영: 폭력·범죄 소재는 드라마 기능으로 다룬다. 수법 자체보다 인물, 대가, 후폭풍, 긴장, 윤리성을 우선한다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 한국어로 출력한다.
- 시나리오 포맷은 한국 표준 시나리오 서식을 따른다.
- Scene Heading, Action, Dialogue, Parenthetical을 구분한다.
- 마크다운 기반으로 출력하되, 필요 시 JSON 구조 데이터도 함께 출력한다.
- 점수 테이블은 항목 | 점수 | 코멘트 형태로 출력한다.
""".strip()


# ═══════════════════════════════════════════════════════════
# GENRE RULE PACKS
# ═══════════════════════════════════════════════════════════

GENRE_RULES = {
    "코미디": {
        "name_en": "Comedy",
        "필수항목": [
            "premise_engine", "comic_contradiction", "character_comic_flaw",
            "comic_escalation", "line_surprise", "status_comedy",
            "timing_precision", "callback_payoff", "scene_comic_engine", "joke_density"
        ],
        "실패신호": [
            "설정이 안 웃김", "캐릭터 결함이 웃음을 생산하지 않음",
            "대사가 길고 뻔함", "리액션이 없음",
            "반복이 escalation으로 커지지 않음", "농담이 서사를 멈춤"
        ],
        "핵심원칙": "코미디는 떠드는 장르가 아니라 웃음 메커니즘이 작동하는 장르다."
    },
    "드라마": {
        "name_en": "Drama",
        "필수항목": [
            "emotional_truth", "character_depth", "moral_complexity",
            "relationship_dynamics", "vulnerability_escalation", "quiet_power",
            "dialogue_weight", "consequence_chain", "identity_pressure", "catharsis_build"
        ],
        "실패신호": [
            "감정이 표면적임", "인물이 평면적임",
            "관계 변화가 없음", "대가가 보이지 않음"
        ],
        "핵심원칙": "드라마는 인간의 선택과 대가를 통해 진실에 도달하는 장르다."
    },
    "스릴러": {
        "name_en": "Thriller / Crime",
        "필수항목": [
            "pressure_escalation", "information_asymmetry", "clock_or_deadline",
            "threat_visibility_control", "suspicion_transfer", "moral_compromise",
            "false_safety", "reversal_pressure", "investigation_momentum", "dread_carry_over"
        ],
        "실패신호": [
            "압박이 약함", "단서가 평면적임",
            "반전이 억지임", "인물이 너무 쉽게 말함"
        ],
        "핵심원칙": "스릴러는 정보 비대칭과 압박 설계로 관객의 불안을 지속시키는 장르다."
    },
    "느와르": {
        "name_en": "Noir / Crime Noir",
        "필수항목": [
            "moral_ambiguity", "fatalistic_inevitability", "power_corruption",
            "betrayal_architecture", "paranoia_escalation", "dark_irony",
            "visual_shadow_contrast", "voice_cynicism", "loyalty_test", "cost_of_survival"
        ],
        "실패신호": [
            "선악 구분이 명확함", "배신에 무게가 없음",
            "분위기만 있고 서사 압력이 없음", "인물의 타락이 납득되지 않음"
        ],
        "핵심원칙": "느와르는 도덕적 모호함 속에서 인간의 타락과 생존 대가를 보여주는 장르다."
    },
    "멜로/로맨스": {
        "name_en": "Melodrama / Romance",
        "필수항목": [
            "desire_tension", "emotional_withholding", "longing_build",
            "vulnerability_reveal", "timing_misalignment", "intimacy_progression",
            "symbolic_motif", "ache_after_contact", "impossible_choice", "emotional_payoff"
        ],
        "실패신호": [
            "고백만 많고 축적이 없음", "왜 끌리는지 안 보임",
            "감정 온도가 단조로움"
        ],
        "핵심원칙": "멜로는 갈망의 축적과 감정의 지연이 만드는 아픔과 회수의 장르다."
    },
    "호러": {
        "name_en": "Horror",
        "필수항목": [
            "fear_anticipation", "uncertainty", "sensory_unease",
            "threat_design", "dread_pacing", "violation_of_safety",
            "image_residue", "vulnerability", "false_relief", "terror_escalation"
        ],
        "실패신호": [
            "놀람만 있고 공포 축적이 없음", "위협 규칙이 모호함",
            "불안이 장면 밖으로 이어지지 않음"
        ],
        "핵심원칙": "호러는 공포의 예감과 축적으로 관객의 안전감을 체계적으로 파괴하는 장르다."
    },
    "액션": {
        "name_en": "Action",
        "필수항목": [
            "physical_objective_clarity", "spatial_clarity", "tactical_reversal",
            "rising_physical_cost", "kinetic_identity", "consequence_visibility",
            "unique_setpiece_logic", "emotional_stake_inside_action", "momentum", "aftermath_value"
        ],
        "실패신호": [
            "누가 무엇을 하려는지 흐림", "공간이 안 보임",
            "액션 후 대가가 없음"
        ],
        "핵심원칙": "액션은 물리적 목표와 대가 속에서 캐릭터의 의지를 증명하는 장르다."
    },
    "SF/판타지": {
        "name_en": "Science Fiction / Fantasy",
        "필수항목": [
            "world_rule_clarity", "wonder_value", "cost_of_rule",
            "ethical_implication", "rule_consistency", "novelty",
            "human_anchor", "visual_imagination", "mythic_depth", "payoff_of_world_rule"
        ],
        "실패신호": [
            "룰 설명만 많음", "인간 드라마가 약함",
            "세계관이 이야기보다 앞섬"
        ],
        "핵심원칙": "SF/판타지는 세계의 규칙이 인간 드라마의 은유로 작동하는 장르다."
    },
}


def _get_genre_rule_text(genre: str) -> str:
    """장르 규칙 팩을 텍스트로 변환"""
    rule = GENRE_RULES.get(genre)
    if not rule:
        return f"[장르: {genre}] — 범용 장르 규칙을 적용합니다."

    lines = [
        f"[GENRE RULE PACK: {genre} ({rule['name_en']})]",
        f"핵심 원칙: {rule['핵심원칙']}",
        "",
        "필수 항목:",
    ]
    for item in rule["필수항목"]:
        lines.append(f"  - {item}")
    lines.append("")
    lines.append("실패 신호:")
    for sig in rule["실패신호"]:
        lines.append(f"  - {sig}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# PROMPT BUILDER FUNCTIONS
# ═══════════════════════════════════════════════════════════

# ───────────────────────────────────
# 1. Project Brief
# ───────────────────────────────────
def build_project_brief_prompt(
    title: str,
    genre: str,
    format_type: str,
    logline: str,
    theme: str,
    tone: str = "",
    audience: str = "",
) -> str:
    genre_rule = _get_genre_rule_text(genre)

    return f"""
[TASK] Project Brief 생성

아래 정보를 기반으로 이 프로젝트의 핵심 설계 문서(Project Brief)를 작성하라.
Project Brief는 Writer Engine의 모든 후속 작업의 기준점이 된다.

[PROJECT INFO]
- 제목: {title or '(미정)'}
- 장르: {genre}
- 포맷: {format_type}
- 로그라인: {logline or '(미입력)'}
- 테마/메시지: {theme or '(미입력)'}
- 톤: {tone or '(미입력)'}
- 타깃 관객: {audience or '(미입력)'}

{genre_rule}

[OUTPUT FORMAT]
아래 항목을 순서대로 작성하라:

1. CORE PREMISE (핵심 전제 — 2~3문장)
2. CENTRAL DRAMATIC QUESTION (이 이야기의 극적 질문)
3. THEME STATEMENT (테마를 한 문장으로)
4. AUDIENCE PROMISE (관객에게 약속하는 경험)
5. TONE & MOOD (톤과 분위기 기술)
6. PROTAGONIST SKETCH (주인공 — 결함, 거짓 신념, 진짜 필요)
7. ANTAGONISTIC FORCE (적대 세력 — 왜 강력한가)
8. ENDING DIRECTION (엔딩 방향 — 어떤 감정을 남길 것인가)
9. GENRE CONTRACT (장르가 관객에게 반드시 제공해야 할 것)
10. KEY RISK (이 프로젝트에서 가장 경계해야 할 품질 리스크)

각 항목은 실질적이고 구체적으로 작성한다. 추상적 선언이 아니라 집필 기준으로 쓸 수 있어야 한다.
점수: Global Gate 5항목을 10점 만점으로 자가 채점하고, 6.0 미만 항목에는 보완 코멘트를 달아라.
""".strip()


# ───────────────────────────────────
# 2. Story Matrix
# ───────────────────────────────────
def build_story_matrix_prompt(
    title: str,
    genre: str,
    logline: str,
    theme: str,
    protagonist: str = "",
    flaw: str = "",
    need: str = "",
    ending_goal: str = "",
) -> str:
    genre_rule = _get_genre_rule_text(genre)

    return f"""
[TASK] Story Matrix 생성

Story Matrix는 Writer Engine의 핵심 내부 제어 시스템이다.
이 시스템의 목적은 장면의 존재 이유, 구조적 위치, 캐릭터 변화, 장르 효능, 엔딩 회수 가능성을 동시에 관리하는 것이다.

[PROJECT INFO]
- 제목: {title or '(미정)'}
- 장르: {genre}
- 로그라인: {logline or '(미입력)'}
- 테마: {theme or '(미입력)'}
- 주인공: {protagonist or '(미입력)'}
- 주인공 결함/거짓 신념: {flaw or '(미입력)'}
- 주인공 진짜 필요: {need or '(미입력)'}
- 엔딩 목표: {ending_goal or '(미입력)'}

{genre_rule}

[OUTPUT FORMAT]

A. GLOBAL STORY LAYER
- core_premise / theme_statement / message_intent
- central_dramatic_question / audience_promise
- tone_mode / ending_target / emotional_aftertaste

B. STRUCTURAL LAYER
- three_act_map: 각 Act가 서사적으로 무엇을 달성하는지
- beat16_map: 16비트 각각을 1~2문장으로
- hero_journey_map: 영웅서사 12단계 매핑
- character_arc_map: 거짓 신념 → 위기 → 선택 → 변화
- genre_arc_map: 장르 쾌감의 상승 곡선
- subplot_map: A/B 스토리 설계
- payoff_map: 반드시 회수해야 할 복선 목록
- ending_proof_map: 엔딩이 테마를 어떻게 증명하는가

C. UNIT LAYER (8 Units)
각 Unit에 대해:
- unit_purpose / dramatic_pressure / dominant_conflict
- emotional_band / beat_range / character_arc_shift
- genre_promise_target / ending_setup_value

각 항목은 구체적으로, 추상 선언이 아니라 실제 집필 기준으로 작성하라.
""".strip()


# ───────────────────────────────────
# 3. Unit Blueprint
# ───────────────────────────────────
def build_unit_blueprint_prompt(
    act_label: str,
    unit_no: int,
    unit_goal: str,
    section_count: int = 2,
    beat_links: str = "",
    arc_links: str = "",
    genre_goal: str = "",
    ending_connection: str = "",
) -> str:
    return f"""
[TASK] Unit Blueprint 생성

이 Unit의 상세 설계도를 작성하라.
Unit Blueprint는 실제 Section Draft 생성 전에 반드시 거쳐야 하는 설계 단계다.

[UNIT INFO]
- Act: {act_label}
- Unit 번호: {unit_no}
- Unit 목표: {unit_goal or '(미입력)'}
- Section 수: {section_count}
- 16비트 연결: {beat_links or '(미입력)'}
- 아크 연결: {arc_links or '(미입력)'}
- 장르 효능 목표: {genre_goal or '(미입력)'}
- 엔딩 연결: {ending_connection or '(미입력)'}

[OUTPUT FORMAT]

1. UNIT OVERVIEW
- unit_purpose: 이 Unit이 서사에서 담당하는 역할 (2~3문장)
- dramatic_pressure: 이 Unit에서 가장 강한 압력의 정체
- dominant_conflict: 핵심 갈등
- emotional_band: 감정의 시작점 → 끝점
- rhythm_design: 리듬 설계 (빠름/느림/교차)

2. SECTION BLUEPRINTS
각 Section에 대해:
- section_goal: 이 Section이 달성해야 할 극적 목적
- scene_count_target: 예상 장면 수
- page_estimate: 예상 페이지 수
- required_turn: 반드시 발생해야 할 전환
- information_release: 공개되어야 할 정보
- tension_target: 긴장 수준 (1~10)
- emotional_shift_target: 감정 변화 방향
- genre_device_target: 이 Section에서 작동해야 할 장르 장치
- section_exit_hook: 이 Section의 끝을 다음으로 연결하는 장치

3. SCENE OUTLINE
각 Scene에 대해 한 줄 요약:
- scene_no / heading 예상 / 핵심 기능 / 핵심 인물 / turn 예상

4. UNIT GATE SELF-CHECK
Unit Gate 7항목을 10점 만점으로 자가 채점하라.
6.0 미만 항목에는 보완 코멘트를 달아라.
""".strip()


# ───────────────────────────────────
# 4. Section Draft (Screenplay)
# ───────────────────────────────────
def build_section_screenplay_prompt(
    title: str,
    genre: str,
    act_label: str,
    unit_no: int,
    section_no: int,
    section_goal: str,
    previous_context: str = "",
    character_notes: str = "",
    tone_notes: str = "",
    genre_rule: str = "",
    theme_line: str = "",
    ending_line: str = "",
) -> str:
    genre_rule_pack = _get_genre_rule_text(genre)

    return f"""
[TASK] Section Screenplay Draft 생성

이 Section의 실제 시나리오를 집필하라.
이것은 시놉시스나 줄거리가 아니라, 촬영 가능한 시나리오 초고다.

[SECTION INFO]
- 제목: {title or '(미정)'}
- 장르: {genre}
- Act: {act_label}
- Unit: {unit_no}
- Section: {section_no}
- Section 목표: {section_goal or '(미입력)'}

[CONTEXT]
- 이전 맥락: {previous_context or '(없음)'}
- 캐릭터 메모: {character_notes or '(없음)'}
- 톤 메모: {tone_notes or '(없음)'}
- 장르 규칙 메모: {genre_rule or '(없음)'}
- 테마 라인: {theme_line or '(없음)'}
- 엔딩 라인: {ending_line or '(없음)'}

{genre_rule_pack}

[SCREENPLAY FORMAT]

한국 표준 시나리오 서식으로 작성하라:

S#[번호]. [INT./EXT.] [장소] — [시간]

(Action 묘사 — 현재 시제, 시각적, 구체적)

    캐릭터명
    (Parenthetical — 감정/태도/행동 지시)
대사 텍스트

[WRITING RULES]
1. 모든 장면에 desire → obstacle → conflict → turn → emotional shift → exit pressure
2. 대사는 설명이 아니라 행동이다 — 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나 수행
3. 캐릭터 보이스가 섞이면 안 된다
4. 장르 효능이 실제로 작동해야 한다
5. 설명성 대사, 목적 없는 장면, 전환 없는 장면 금지
6. 각 장면 끝에 다음 장면을 보고 싶게 만드는 exit hook

[OUTPUT]
- 시나리오 본문
- 각 Scene에 대한 1줄 내부 메모 (scene_function / genre_effect / turn)
- Section 자가 채점: Scene Gate 주요 항목 평균
""".strip()


# ───────────────────────────────────
# 5. Dialogue Polish
# ───────────────────────────────────
def build_dialogue_polish_prompt(
    genre: str,
    character_voice_notes: str,
    scene_text: str,
) -> str:
    genre_rule_pack = _get_genre_rule_text(genre)

    return f"""
[TASK] Dialogue Polish — 대사 고도화

아래 장면의 대사를 BLUE JEANS 기준으로 고도화하라.
대사만 바꾸는 것이 아니라, 서브텍스트, 권력 이동, 캐릭터 보이스 분리, 장르 효능까지 점검하라.

[GENRE]
{genre}

{genre_rule_pack}

[CHARACTER VOICE NOTES]
{character_voice_notes or '(없음)'}

[ORIGINAL SCENE TEXT]
{scene_text or '(텍스트 미입력)'}

[POLISH RULES]
1. 각 캐릭터의 말투가 구분되는가 — speech_rhythm, sentence_length, attack/defense style
2. 모든 대사가 목적을 수행하는가 — seduction / evasion / interrogation / intimidation 등
3. 서브텍스트가 존재하는가 — 말하지 않는 것이 말하는 것보다 강한가
4. 설명성 대사를 제거하라 — 보여줄 수 있는 정보를 말로 전달하지 마라
5. 대화 후 권력관계가 변했는가
6. 리액션이 살아 있는가 — 침묵, 행동, 표정 지시
7. 장르 효능이 대사 안에서 작동하는가

[OUTPUT FORMAT]
1. POLISHED SCENE (전체 수정본)
2. CHANGE LOG (주요 변경 사항과 이유)
3. VOICE CHECK TABLE
   | 캐릭터 | 말투 특징 | 분리도 (10점) | 코멘트 |
4. DIALOGUE GATE 점수
   | 항목 | 점수 | 코멘트 |
   - Subtext / Voice Separation / Genre Effect / Power Shift / Exposition Risk
""".strip()


# ───────────────────────────────────
# 6. Ending Control
# ───────────────────────────────────
def build_ending_control_prompt(
    title: str,
    theme: str,
    protagonist_arc: str,
    setup_payoffs: str,
    desired_emotion: str = "",
    ending_type: str = "",
) -> str:
    return f"""
[TASK] Ending Control — 엔딩 설계 및 점검

이 프로젝트의 엔딩을 BLUE JEANS Ending 10 Control 기준으로 설계/점검하라.

[PROJECT INFO]
- 제목: {title or '(미정)'}
- 테마: {theme or '(미입력)'}
- 주인공 아크: {protagonist_arc or '(미입력)'}
- 복선/회수: {setup_payoffs or '(미입력)'}
- 원하는 최종 감정: {desired_emotion or '(미입력)'}
- 엔딩 유형: {ending_type or '(미입력)'}

[ENDING 10 CONTROL — 각 항목을 구체적으로 설계하라]

1. INEVITABILITY — 결국 그렇게 될 수밖에 없었다는 감각
   → 이 엔딩이 필연적인 이유는?

2. SURPRISE — 예상보다 더 좋거나 더 아프다
   → 관객의 예상을 어떻게 비틀 것인가?

3. THEMATIC PROOF — 테마를 행동으로 증명한다
   → 주인공의 어떤 행동이 테마를 증명하는가?

4. EMOTIONAL PAYOFF — 감정이 회수된다
   → 축적된 어떤 감정이 마지막에 터지는가?

5. CHARACTER TRUTH — 주인공의 변화가 드러난다
   → 거짓 신념이 어떻게 깨지고, 진짜 필요에 도달하는가?

6. COST VISIBILITY — 대가가 보인다
   → 주인공이 치른 대가는 무엇인가?

7. IMAGE MEMORY — 마지막 이미지가 남는다
   → 마지막 장면의 시각적 이미지는?

8. UNRESOLVED NOISE CONTROL — 불필요한 미해결을 줄인다
   → 의도적으로 열어둘 것과 반드시 닫을 것?

9. AFTERTASTE DESIGN — 어떤 여운을 남길지 설계한다
   → 극장을 나서는 관객의 감정 상태는?

10. SEQUEL OR CLOSURE BALANCE — 닫을지 열어둘지 명확히 한다
    → 완결인가, 여지인가, 혹은 둘 다인가?

[OUTPUT FORMAT]
1. ENDING DESIGN (10항목 상세 설계)
2. ENDING SCENE SKETCH (마지막 2~3 장면 스케치)
3. PAYOFF CHECKLIST (반드시 회수해야 할 복선 확인)
4. ENDING FAILURE CHECK (실패 신호 점검)
5. ENDING GATE 점수 (10항목 각 10점 만점)
""".strip()


# ───────────────────────────────────
# 7. Quality Control
# ───────────────────────────────────
def build_qc_prompt(
    genre: str,
    theme: str,
    scene_or_section_text: str,
) -> str:
    genre_rule_pack = _get_genre_rule_text(genre)

    return f"""
[TASK] Quality Control — 품질 점검

아래 텍스트를 BLUE JEANS Writer Engine의 전체 품질 기준으로 점검하라.

[GENRE] {genre}
[THEME] {theme or '(미입력)'}

{genre_rule_pack}

[TEXT TO CHECK]
{scene_or_section_text or '(텍스트 미입력)'}

[QC CHECKLIST]

A. NONSENSE FILTER
각 장면에 대해:
- why_this_scene_now — 왜 지금 이 장면인가
- what_changes_after_scene — 이 장면 후 무엇이 달라지는가
- why_not_cut — 이 장면을 빼면 어떤 손실이 생기는가
- where_is_subtext — 서브텍스트가 어디에 있는가
- where_is_genre_effect — 장르 효능이 어디서 발생하는가
- does_it_prepare_or_payoff_ending — 엔딩과 어떻게 연결되는가

B. SCENE GATE (각 장면별)
| 항목 | 점수 | 코멘트 |
- Scene Function / Conflict / Turn / Emotional Shift
- Dialogue Subtext / Character Voice / Genre Effect
- Visual Memory / Necessity / Nonsense Risk Inverse

C. DIALOGUE CHECK
- 캐릭터 보이스 분리도
- 설명성 대사 존재 여부
- 서브텍스트 수준
- 권력 이동 여부

D. GENRE EFFECTIVENESS
- 장르 장치 작동 여부
- 장르 쾌감 발생 여부
- 장르 실패 신호 존재 여부

E. STRUCTURAL CHECK
- 이 구간이 전체 구조에서 올바른 위치에 있는가
- 리듬이 적절한가
- 정보 공개 타이밍이 맞는가

[OUTPUT FORMAT]
1. QC SUMMARY (전체 요약 — 강점 3개, 약점 3개)
2. SCENE-BY-SCENE REPORT (장면별 상세 점검)
3. PRIORITY FIX LIST (우선 수정 사항 순위)
4. REWRITE RECOMMENDATIONS (재작성 제안)
5. OVERALL SCORE TABLE (전체 점수표)
""".strip()
