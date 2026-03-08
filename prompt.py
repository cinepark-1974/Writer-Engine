# ─────────────────────────────────────────────────────────────
# BLUE JEANS SCREENPLAY WRITER ENGINE v1.0
# prompt.py — System Prompt · Genre Rules · Prompt Builders
# © 2026 BLUE JEANS PICTURES
# ─────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════
# SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
당신은 BLUE JEANS SCREENPLAY WRITER ENGINE의 핵심 AI입니다.
영화·시리즈의 기획 자료, 트리트먼트, 줄거리, 초고를 입력받아
실제 촬영 가능한 시나리오 초고를 생성하는 전문 집필 엔진입니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND PHILOSOPHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[New and Classic]
- 작가의 새로움을 살린다. 시간이 지나도 남는 구조감을 더한다.
- 유행하는 표면 문체보다 오래 남는 장면과 선택을 우선한다.

[Blue Discipline]
- 자유롭게 쓰되 방만하게 쓰지 않는다.
- 모든 장면은 존재 이유를 가져야 한다.
- 모든 대사는 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나 이상을 수행해야 한다.

[Hidden Architecture]
- 3막 구조, 16비트, 캐릭터 아크, 영웅서사, 장르 규칙, 테마 라인이 내부에서 작동한다.
- 결과물은 이론 체크리스트처럼 보이면 안 된다. 관객은 흐름을 따라갈 뿐이다.

[Entertainment with Meaning]
- 재미 없는 메시지는 설교. 메시지 없는 오락은 잔상이 약하다.
- 재미와 의미가 동시에 회수되는 설계를 지향한다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Act → Unit → Section → Scene

- Act 1 = Unit 1, 2    |  Act 2A = Unit 3, 4
- Act 2B = Unit 5, 6   |  Act 3  = Unit 7, 8

분량 감각:
- 1 Scene ≈ 0.75~1.25 page
- 1 Section = 2~3 Scenes
- 1 Unit = 2 Sections = 4~6 Scenes ≈ 5~8 pages
- 8 Units = 장편 기본 골격

핵심 원칙: 전체를 한 번에 쓰지 않는다. Section 단위로 생성하고 Unit 단위로 점검한다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE WRITING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━

모든 Scene 필수 요소:
1. Scene Heading (INT./EXT. 장소 — 시간)
2. Action (현재 시제, 영상적, 구체적)
3. Dialogue (캐릭터 보이스 구분)
4. Subtext (대사 아래 숨은 의도)
5. Turn (장면 내 반전 또는 변화)
6. Exit Hook (다음 장면 연결 압력)

Scene 설계 순서:
desire → obstacle → conflict → turn → emotional shift → exit pressure

━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIALOGUE RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━

대사 목적 (최소 하나):
seduction / evasion / interrogation / intimidation / masking_pain /
status_play / manipulation / confession_resisted / comic_misdirection / emotional_deflection

실패 신호: 말투 구분 불가 / 설명성 대사 / 행동 없는 감정 / 권력 변화 없음 / 빈 리액션

━━━━━━━━━━━━━━━━━━━━━━━━━━━
NONSENSE FILTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━

절대 출력 금지:
목적 없는 장면 / 갈등 없는 대화 / 장르 효능 없는 장면 / 보이스 중복 /
전환 없는 장면 / 설명성 대사 과다 / 엔딩 무관 가지치기 / 설교 대사

━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENDING 10 CONTROL
━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. inevitability  2. surprise  3. thematic_proof  4. emotional_payoff
5. character_truth  6. cost_visibility  7. image_memory
8. unresolved_noise_control  9. aftertaste_design  10. sequel_or_closure_balance

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCORING — 10점 만점 통일
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Global Gate: Concept Strength / Theme Clarity / Character Potential / Genre Promise / Ending Potential
Unit Gate: Structural Fit / Conflict Density / Emotional Flow / Character Voice / Genre Pleasure / Originality / Ending Setup
Scene Gate: Scene Function / Conflict / Turn / Emotional Shift / Dialogue Subtext / Character Voice / Genre Effect / Visual Memory / Necessity / Nonsense Risk Inverse

경고: 6.0 미만 → 재검토 / 5.0 미만 → 재생성 권장

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAFETY
━━━━━━━━━━━━━━━━━━━━━━━━━━━

허용: 허구 서사 속 범죄/폭력, 장르에 필요한 위협·결과, 윤리적 갈등 드라마.
금지: 현실 범죄 실행 지침, 무기·마약 제조 정보, 고어 자체 목적 출력.
운영: 수법보다 인물·대가·윤리성 우선. 실전 매뉴얼 금지.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 한국어 출력
- 한국 표준 시나리오 서식 (Scene Heading, Action, Dialogue, Parenthetical)
- 점수 테이블: 항목 | 점수 | 코멘트
""".strip()


# ═══════════════════════════════════════════════════════════
# GENRE RULE PACKS
# ═══════════════════════════════════════════════════════════

GENRE_RULES = {
    "드라마": {
        "en": "Drama",
        "items": [
            "emotional_truth", "character_depth", "moral_complexity",
            "relationship_dynamics", "vulnerability_escalation", "quiet_power",
            "dialogue_weight", "consequence_chain", "identity_pressure", "catharsis_build",
        ],
        "fails": ["감정이 표면적", "인물이 평면적", "관계 변화 없음", "대가 부재"],
        "core": "인간의 선택과 대가를 통해 진실에 도달하는 장르.",
    },
    "느와르": {
        "en": "Noir / Crime Noir",
        "items": [
            "moral_ambiguity", "fatalistic_inevitability", "power_corruption",
            "betrayal_architecture", "paranoia_escalation", "dark_irony",
            "visual_shadow_contrast", "voice_cynicism", "loyalty_test", "cost_of_survival",
        ],
        "fails": ["선악 명확", "배신 무게 부족", "분위기만 있고 서사 압력 없음", "타락 비납득"],
        "core": "도덕적 모호함 속 타락과 생존 대가를 보여주는 장르.",
    },
    "스릴러": {
        "en": "Thriller / Crime",
        "items": [
            "pressure_escalation", "information_asymmetry", "clock_or_deadline",
            "threat_visibility_control", "suspicion_transfer", "moral_compromise",
            "false_safety", "reversal_pressure", "investigation_momentum", "dread_carry_over",
        ],
        "fails": ["압박 약함", "단서 평면적", "반전 억지", "인물이 너무 쉽게 말함"],
        "core": "정보 비대칭과 압박 설계로 관객 불안을 지속시키는 장르.",
    },
    "코미디": {
        "en": "Comedy",
        "items": [
            "premise_engine", "comic_contradiction", "character_comic_flaw",
            "comic_escalation", "line_surprise", "status_comedy",
            "timing_precision", "callback_payoff", "scene_comic_engine", "joke_density",
        ],
        "fails": ["설정 안 웃김", "캐릭터 결함이 웃음 비생산", "대사 길고 뻔함", "농담이 서사 정지"],
        "core": "웃음 메커니즘이 작동하는 장르. 떠드는 장르가 아니다.",
    },
    "멜로/로맨스": {
        "en": "Melodrama / Romance",
        "items": [
            "desire_tension", "emotional_withholding", "longing_build",
            "vulnerability_reveal", "timing_misalignment", "intimacy_progression",
            "symbolic_motif", "ache_after_contact", "impossible_choice", "emotional_payoff",
        ],
        "fails": ["고백만 많고 축적 없음", "끌림 이유 불명", "감정 온도 단조"],
        "core": "갈망의 축적과 감정의 지연이 만드는 아픔과 회수의 장르.",
    },
    "호러": {
        "en": "Horror",
        "items": [
            "fear_anticipation", "uncertainty", "sensory_unease",
            "threat_design", "dread_pacing", "violation_of_safety",
            "image_residue", "vulnerability", "false_relief", "terror_escalation",
        ],
        "fails": ["놀람만 있고 공포 축적 없음", "위협 규칙 모호", "불안이 장면 밖으로 안 이어짐"],
        "core": "공포의 예감과 축적으로 안전감을 체계적으로 파괴하는 장르.",
    },
    "액션": {
        "en": "Action",
        "items": [
            "physical_objective_clarity", "spatial_clarity", "tactical_reversal",
            "rising_physical_cost", "kinetic_identity", "consequence_visibility",
            "unique_setpiece_logic", "emotional_stake_inside_action", "momentum", "aftermath_value",
        ],
        "fails": ["목표 흐림", "공간 안 보임", "액션 후 대가 없음"],
        "core": "물리적 목표와 대가 속에서 캐릭터 의지를 증명하는 장르.",
    },
    "SF/판타지": {
        "en": "Science Fiction / Fantasy",
        "items": [
            "world_rule_clarity", "wonder_value", "cost_of_rule",
            "ethical_implication", "rule_consistency", "novelty",
            "human_anchor", "visual_imagination", "mythic_depth", "payoff_of_world_rule",
        ],
        "fails": ["룰 설명만 많음", "인간 드라마 약함", "세계관이 이야기보다 앞섬"],
        "core": "세계의 규칙이 인간 드라마의 은유로 작동하는 장르.",
    },
}


def _genre_text(genre: str) -> str:
    """장르 Rule Pack → 프롬프트용 텍스트."""
    r = GENRE_RULES.get(genre)
    if not r:
        return f"[장르: {genre}] — 범용 장르 규칙 적용."
    return (
        f"[GENRE RULE: {genre} ({r['en']})]\n"
        f"핵심: {r['core']}\n"
        f"필수: {' / '.join(r['items'])}\n"
        f"실패 신호: {' / '.join(r['fails'])}"
    )


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def _material_block(**kw) -> str:
    """공통 기획 자료 블록 — 값이 있는 것만 포함."""
    fields = [
        ("제목", "title"), ("장르", "genre"), ("포맷", "fmt"),
        ("로그라인", "logline"), ("기획의도", "intent"),
        ("GNS", "gns"), ("캐릭터", "characters"),
        ("세계관", "world"), ("구조/시놉시스/비트", "structure"),
        ("장면설계", "scene_design"), ("트리트먼트", "treatment"),
        ("톤 문서", "tone"),
    ]
    parts = []
    for label, key in fields:
        v = (kw.get(key) or "").strip()
        if v:
            parts.append(f"[{label}]\n{v}")
    return "\n\n".join(parts) if parts else ""


# ═══════════════════════════════════════════════════════════
# PROMPT BUILDERS
# ═══════════════════════════════════════════════════════════

# ── 1. 입력 정리 ──────────────────────────────

def build_input_summary_prompt(**kw) -> str:
    mat = _material_block(**kw)
    gr  = _genre_text(kw.get("genre", ""))
    return f"""
[TASK] 입력 정리 — Writer Engine 시나리오 집필 사전 분석

아래 기획 자료를 분석하여 집필에 필요한 핵심 정보를 정리하라.
부족한 항목은 "보완 필요"로 표시하고 추가 제안을 하라.

{mat}

{gr}

[OUTPUT]
1. PROJECT OVERVIEW (제목/장르/포맷/로그라인/테마)
2. CHARACTER SUMMARY (주요인물 — 결함·거짓신념·진짜필요·보이스)
3. STRUCTURE STATUS (3막/16비트/8시퀀스/아크/서브플롯 — 있음/약함/없음)
4. GENRE CONTRACT (장르가 관객에게 약속하는 것)
5. ENDING DIRECTION (명확/모호/미정)
6. MATERIAL GAP (부족 자료 + 보완 제안)
7. WRITER ENGINE READINESS (집필 진입 가능 여부 + 권장 시작점)
8. GLOBAL GATE (5항목 × 10점)
""".strip()


# ── 2. Story Matrix ──────────────────────────

def build_story_matrix_prompt(
    title="", genre="", logline="", theme="",
    protagonist="", flaw="", need="",
    ending_goal="", material_text="",
) -> str:
    gr = _genre_text(genre)
    return f"""
[TASK] Story Matrix 생성

Story Matrix는 Writer Engine의 핵심 내부 제어 시스템이다.
장면 존재 이유, 구조 위치, 캐릭터 변화, 장르 효능, 엔딩 회수를 동시에 관리한다.

[PROJECT]
- 제목: {title or '미정'}  /  장르: {genre}
- 로그라인: {logline or '미입력'}
- 테마: {theme or '미입력'}
- 주인공: {protagonist or '미입력'}
- 결함: {flaw or '미입력'}  /  진짜 필요: {need or '미입력'}
- 엔딩 목표: {ending_goal or '미입력'}

{gr}
{f"{chr(10)}[기획 자료]{chr(10)}{material_text}" if material_text else ""}

[OUTPUT]

A. GLOBAL STORY LAYER
core_premise / theme_statement / message_intent / central_dramatic_question
audience_promise / tone_mode / ending_target / emotional_aftertaste

B. STRUCTURAL LAYER
- three_act_map: 각 Act 서사 목표
- beat16_map: 16비트 각 1~2문장
- hero_journey_map: 12단계
- character_arc_map: 거짓신념→위기→선택→변화
- genre_arc_map: 장르 쾌감 곡선
- subplot_map / payoff_map / ending_proof_map

C. UNIT LAYER (8 Units)
unit_purpose / dramatic_pressure / dominant_conflict
emotional_band / beat_range / character_arc_shift
genre_promise_target / ending_setup_value

구체적으로 — 추상 선언이 아니라 집필 기준으로 작성.
""".strip()


# ── 3. Unit Blueprint ────────────────────────

def build_unit_blueprint_prompt(
    act_label="", unit_no=1, unit_goal="",
    section_count=2, beat_links="", arc_links="",
    genre_goal="", ending_connection="",
    material_text="",
) -> str:
    return f"""
[TASK] Unit Blueprint — Unit {unit_no} 상세 설계

[UNIT INFO]
Act: {act_label}  /  Unit: {unit_no}  /  Sections: {section_count}
목표: {unit_goal or '미입력'}
16비트: {beat_links or '미입력'}
아크: {arc_links or '미입력'}
장르 효능: {genre_goal or '미입력'}
엔딩 연결: {ending_connection or '미입력'}
{f"{chr(10)}[기획 자료]{chr(10)}{material_text}" if material_text else ""}

[OUTPUT]
1. UNIT OVERVIEW (purpose / pressure / conflict / emotional_band / rhythm)
2. SECTION BLUEPRINTS (각 Section):
   goal / scene_count / page_est / required_turn / info_release
   tension(1~10) / emotional_shift / genre_device / exit_hook
3. SCENE OUTLINE (scene_no / heading / function / character / turn)
4. UNIT GATE (7항목 × 10점, 6.0 미만 보완)
""".strip()


# ── 4. Section Draft (시나리오 집필) ─────────

def build_section_draft_prompt(
    title="", genre="", act_label="",
    unit_no=1, section_no=1,
    section_goal="", previous_context="",
    character_notes="", tone_notes="",
    genre_notes="", theme_line="", ending_line="",
    material_text="",
) -> str:
    gr = _genre_text(genre)
    return f"""
[TASK] Section Draft — 시나리오 집필 (Act {act_label} / Unit {unit_no} / Section {section_no})

이 Section의 실제 시나리오를 집필하라.
줄거리가 아니라 촬영 가능한 시나리오 초고다.

[SECTION]
제목: {title or '미정'}  /  장르: {genre}
Section 목표: {section_goal or '미입력'}
이전 맥락: {previous_context or '없음'}
캐릭터: {character_notes or '없음'}
톤: {tone_notes or '없음'}
장르 규칙: {genre_notes or '없음'}
테마 라인: {theme_line or '없음'}
엔딩 라인: {ending_line or '없음'}

{gr}
{f"{chr(10)}[기획 자료]{chr(10)}{material_text}" if material_text else ""}

[FORMAT — 한국 표준 시나리오]
S#번호. INT./EXT. 장소 — 시간
(Action — 현재시제, 시각적)
    캐릭터명
    (Parenthetical)
대사

[RULES]
1. desire→obstacle→conflict→turn→emotional shift→exit pressure
2. 대사 = 행동 (욕망/방어/회피/공격/유혹/압박)
3. 보이스 분리 필수  4. 장르 효능 작동  5. 설명성 대사 금지  6. exit hook

[OUTPUT]
1. 시나리오 본문 (2~3 Scenes)
2. 장면별 메모 (function / genre_effect / turn)
3. Section 자가 채점 (Scene Gate 평균)
""".strip()


# ── 5. Dialogue Polish ───────────────────────

def build_dialogue_polish_prompt(
    genre="", character_voice_notes="", scene_text="",
) -> str:
    gr = _genre_text(genre)
    return f"""
[TASK] Dialogue Polish — 대사 고도화

[GENRE] {genre}
{gr}

[CHARACTER VOICE]
{character_voice_notes or '없음'}

[SCENE TEXT]
{scene_text or '미입력'}

[RULES]
1. 말투 분리  2. 대사 목적  3. 서브텍스트  4. 설명성 제거
5. 권력 변화  6. 리액션(침묵/행동/표정)  7. 장르 효능

[OUTPUT]
1. POLISHED SCENE
2. CHANGE LOG
3. VOICE CHECK (캐릭터 | 말투 | 분리도/10)
4. DIALOGUE GATE (5항목 × 10점)
""".strip()


# ── 6. Ending Control ────────────────────────

def build_ending_control_prompt(
    title="", theme="",
    protagonist_arc="", setup_payoffs="",
    desired_emotion="", ending_type="",
    material_text="",
) -> str:
    return f"""
[TASK] Ending Control — 엔딩 설계·점검

[PROJECT]
제목: {title or '미정'}  /  테마: {theme or '미입력'}
주인공 아크: {protagonist_arc or '미입력'}
복선/회수: {setup_payoffs or '미입력'}
최종 감정: {desired_emotion or '미입력'}
엔딩 유형: {ending_type or '미입력'}
{f"{chr(10)}[기획 자료]{chr(10)}{material_text}" if material_text else ""}

[ENDING 10 CONTROL]
1. INEVITABILITY  2. SURPRISE  3. THEMATIC PROOF  4. EMOTIONAL PAYOFF
5. CHARACTER TRUTH  6. COST VISIBILITY  7. IMAGE MEMORY
8. UNRESOLVED NOISE  9. AFTERTASTE  10. CLOSURE BALANCE

[OUTPUT]
1. ENDING DESIGN (10항목 상세)
2. ENDING SCENE SKETCH (마지막 2~3장면)
3. PAYOFF CHECKLIST
4. FAILURE CHECK
5. ENDING GATE (10항목 × 10점)
""".strip()


# ── 7. Quality Control ───────────────────────

def build_qc_prompt(
    genre="", theme="", scene_or_section_text="",
) -> str:
    gr = _genre_text(genre)
    return f"""
[TASK] Quality Control — 품질 점검

[GENRE] {genre}   [THEME] {theme or '미입력'}
{gr}

[TEXT]
{scene_or_section_text or '미입력'}

[CHECKLIST]
A. NONSENSE FILTER (why_now / what_changes / why_not_cut / subtext / genre_effect / ending)
B. SCENE GATE (10항목 × 10점)
C. DIALOGUE CHECK (분리도/설명성/서브텍스트/권력이동)
D. GENRE EFFECTIVENESS (장치/쾌감/실패신호)
E. STRUCTURAL CHECK (위치/리듬/정보타이밍)

[OUTPUT]
1. QC SUMMARY (강점3 + 약점3)
2. SCENE-BY-SCENE REPORT
3. PRIORITY FIX LIST
4. REWRITE RECOMMENDATIONS
5. OVERALL SCORE TABLE
""".strip()
