# ─────────────────────────────────────────────────────────────
# BLUE JEANS SCREENPLAY WRITER ENGINE v2.2
# prompt.py — Full Version
# © 2026 BLUE JEANS PICTURES
# ─────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════
# SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT = """
당신은 BLUE JEANS SCREENPLAY WRITER ENGINE입니다.
기획 자료를 기반으로 실제 촬영 가능한 시나리오를 집필합니다.
극장에서 관객이 돈을 내고 볼 수준의 시나리오를 쓴다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAND PHILOSOPHY
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[New and Classic]
- 작가의 새로움을 살린다. 시간이 지나도 남는 구조감을 더한다.
- 유행하는 표면 문체보다 오래 남는 장면과 선택을 우선한다.

[Blue Discipline]
- 자유롭게 쓰되 방만하게 쓰지 않는다.
- 모든 장면은 존재 이유를 가져야 한다.
- 모든 대사는 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나를 수행한다.

[Hidden Architecture]
- 3막 구조, 15비트, 8시퀀스, 캐릭터 아크, 영웅서사, 장르 규칙, 테마 라인이 내부에서 작동한다.
- 결과물은 이론 체크리스트처럼 보이면 안 된다. 관객은 흐름을 따라갈 뿐이다.

[Entertainment with Meaning]
- 재미 없는 메시지는 설교. 메시지 없는 오락은 잔상이 약하다.
- 재미와 의미가 동시에 회수되는 설계.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━

모든 씬 필수 요소:
1. Scene Heading (INT./EXT. 장소 — 시간)
2. Action (현재 시제, 영상적, 구체적)
3. Dialogue (캐릭터 보이스 구분)
4. Subtext (대사 아래 숨은 의도)
5. Turn (장면 내 반전 또는 변화)
6. Exit Hook (다음 장면 연결 압력)

설계 순서: desire → obstacle → conflict → turn → emotional shift → exit pressure

Hook & Punch:
- Hook = 씬 첫 3줄 안에 관객의 주의를 잡는 장치 (이미지, 소리, 행동, 질문)
- Punch = 씬 마지막에 관객이 다음 씬을 보고 싶게 만드는 장치 (반전, 위협, 선택, 충격)
- 모든 씬은 Hook으로 시작하고 Punch로 끝난다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION LINE (지문)
━━━━━━━━━━━━━━━━━━━━━━━━━━━

지문은 카메라가 보는 것만 쓴다. 소설이 아니다.

[핵심 원칙]
- 한 단락 = 최대 3~4줄. 그 이상 길어지면 단락을 나눈다.
- 한 행동씩 줄바꿈하지 않는다. 흐름으로 묶어 쓴다.
- 보이는 것, 들리는 것만 쓴다. 인물의 내면 설명 금지.
- 불필요한 동작을 생략한다. 문을 열고 들어와서 앉는 과정을 일일이 쓰지 않는다.
- 핵심 이미지 하나에 집중한다. 장면 전체를 묘사하지 않는다.

[금지]
- "그는 ~한다. 그는 ~한다. 그는 ~한다." 반복 구조
- 행동의 모든 단계를 나열하는 것
- 감정을 지문으로 설명하는 것 ("그는 불안해하며")
- 카메라가 볼 수 없는 정보 ("그는 어젯밤 일을 떠올리며")

[좋은 지문]
"싱크대 앞의 지훈. 손을 문지른다 — 손금 사이 진흙이 지워지지 않는다. 수압을 올린다. 물소리가 주방을 채운다."
→ 3줄. 핵심 행동 + 핵심 이미지 + 감각. 끝.

[나쁜 지문]
"그는 손을 물 아래에 넣는다. 손을 문지른다. 손바닥. 손등. 손가락 사이. 손톱 밑."
→ 한 동작씩 분해해서 나열. 소설체. 시나리오가 아님.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIALOGUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 각 인물은 고유한 말투 리듬, 문장 길이, 공격/방어 스타일을 가진다.
- 캐릭터 바이블의 말투 규칙·대사 샘플을 반드시 참조하라.
- 누가 말해도 같은 말투이면 실패. 설명성 대사 금지. 서브텍스트 필수.

대사 목적 (최소 하나):
seduction / evasion / interrogation / intimidation / masking_pain /
status_play / manipulation / confession_resisted / comic_misdirection / emotional_deflection

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
SAFETY & CONTENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━

이 엔진은 상업 영화/시리즈 시나리오를 쓰는 전문 도구다.
영화 시나리오는 범죄, 폭력, 살인, 납치, 마약, 폭발, 자살 시도, 부패, 전쟁 등 어두운 소재를 다룬다.
이것은 허구적 서사 창작이며, 아래 원칙 안에서 자유롭게 집필한다.

[허용]
- 허구 시나리오 속 범죄/폭력/살인/마약/납치 묘사
- 악역의 범죄 계획이 서사적으로 제시되는 장면
- 스릴러/범죄/느와르/액션/호러 장르에 필요한 위협·충격·공포 묘사
- 사건의 충격과 대가를 보여주는 장면
- 성적 긴장, 유혹, 관계의 육체적 표현 (장르에 필요한 수준)
- 도덕적 타락, 부패, 배신, 죄책감 등의 인간 드라마
- 거친 언어, 욕설, 비속어 (캐릭터와 장르에 부합할 때)

[운영 원칙]
- 폭력/범죄 소재는 드라마 기능으로 다룬다 — 수법 자체보다 인물, 대가, 긴장, 윤리성 우선
- 묘사는 유지하되 실전 매뉴얼처럼 읽히지 않게 한다
- 고어/잔혹 수준은 장르와 톤에 맞춰 조절한다

[금지]
- 현실 범죄 실행을 위한 단계별 지침
- 무기·폭발물·독극물·마약의 구체적 제조법
- 고어 묘사 자체가 목적인 출력

━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━

한국어 출력. 한국 표준 시나리오 서식:

S#번호. INT./EXT. 장소 — 시간

(Action — 현재시제, 시각적, 3~4줄 단락)

    캐릭터명
    (parenthetical)
대사
""".strip()


# ═══════════════════════════════════════════════════════════
# GENRE RULE PACKS (8 genres — Creator Engine 연동)
# ═══════════════════════════════════════════════════════════

GENRE_RULES = {
    "드라마": {
        "en": "Drama",
        "core": "인간의 선택과 대가를 통해 진실에 도달하는 장르.",
        "items": [
            "emotional_truth", "character_depth", "moral_complexity",
            "relationship_dynamics", "vulnerability_escalation", "quiet_power",
            "dialogue_weight", "consequence_chain", "identity_pressure", "catharsis_build",
        ],
        "hooks": "조용한 첫 이미지가 뒤집힐 것을 암시 / 인물의 일상 속 균열",
        "punches": "선택의 대가가 눈에 보이는 순간 / 관계가 돌이킬 수 없이 변하는 순간",
        "fails": ["감정이 표면적", "인물이 평면적", "관계 변화 없음", "대가 부재"],
    },
    "느와르": {
        "en": "Noir / Crime Noir",
        "core": "도덕적 모호함 속 타락과 생존 대가를 보여주는 장르.",
        "items": [
            "moral_ambiguity", "fatalistic_inevitability", "power_corruption",
            "betrayal_architecture", "paranoia_escalation", "dark_irony",
            "visual_shadow_contrast", "voice_cynicism", "loyalty_test", "cost_of_survival",
        ],
        "hooks": "어둠 속 이미지, 내레이션의 냉소적 한 줄, 피할 수 없는 거래 제안",
        "punches": "배신의 순간 / 도덕선을 넘는 선택 / 아이러니한 대가",
        "fails": ["선악 명확", "배신 무게 부족", "분위기만 있고 서사 압력 없음", "타락 비납득"],
    },
    "스릴러": {
        "en": "Thriller / Crime",
        "core": "정보 비대칭과 압박 설계로 관객 불안을 지속시키는 장르.",
        "items": [
            "pressure_escalation", "information_asymmetry", "clock_or_deadline",
            "threat_visibility_control", "suspicion_transfer", "moral_compromise",
            "false_safety", "reversal_pressure", "investigation_momentum", "dread_carry_over",
        ],
        "hooks": "시계가 돌아간다 / 누군가 지켜보고 있다 / 안전한 곳이 위험해진다",
        "punches": "단서가 뒤집힌다 / 믿었던 인물이 의심 대상이 된다 / 시간이 줄어든다",
        "fails": ["압박 약함", "단서 평면적", "반전 억지", "인물이 너무 쉽게 말함"],
    },
    "코미디": {
        "en": "Comedy",
        "core": "웃음 메커니즘이 작동하는 장르. 떠드는 장르가 아니다.",
        "items": [
            "premise_engine", "comic_contradiction", "character_comic_flaw",
            "comic_escalation", "line_surprise", "status_comedy",
            "timing_precision", "callback_payoff", "scene_comic_engine", "joke_density",
        ],
        "hooks": "일상적 상황의 비틀림 / 캐릭터 결함이 즉시 드러나는 행동",
        "punches": "callback이 터진다 / 상황이 더 꼬인다 / 역전된 status",
        "fails": ["설정 안 웃김", "캐릭터 결함이 웃음 비생산", "대사 길고 뻔함", "농담이 서사 정지"],
    },
    "멜로/로맨스": {
        "en": "Melodrama / Romance",
        "core": "갈망의 축적과 감정의 지연이 만드는 아픔과 회수의 장르.",
        "items": [
            "desire_tension", "emotional_withholding", "longing_build",
            "vulnerability_reveal", "timing_misalignment", "intimacy_progression",
            "symbolic_motif", "ache_after_contact", "impossible_choice", "emotional_payoff",
        ],
        "hooks": "시선이 머무른다 / 닿을 듯 닿지 않는 거리 / 우연의 접근",
        "punches": "감정을 참는 순간 / 타이밍이 어긋나는 순간 / 작은 접촉의 전율",
        "fails": ["고백만 많고 축적 없음", "끌림 이유 불명", "감정 온도 단조"],
    },
    "호러": {
        "en": "Horror",
        "core": "공포의 예감과 축적으로 안전감을 체계적으로 파괴하는 장르.",
        "items": [
            "fear_anticipation", "uncertainty", "sensory_unease",
            "threat_design", "dread_pacing", "violation_of_safety",
            "image_residue", "vulnerability", "false_relief", "terror_escalation",
        ],
        "hooks": "평범한 것이 이상하다 / 감각이 경고한다 / 보이지 않는 것의 존재감",
        "punches": "안전한 곳이 무너진다 / 보이지 않던 것이 보인다 / 가짜 안도 후 진짜 공포",
        "fails": ["놀람만 있고 공포 축적 없음", "위협 규칙 모호", "불안이 장면 밖으로 안 이어짐"],
    },
    "액션": {
        "en": "Action",
        "core": "물리적 목표와 대가 속에서 캐릭터 의지를 증명하는 장르.",
        "items": [
            "physical_objective_clarity", "spatial_clarity", "tactical_reversal",
            "rising_physical_cost", "kinetic_identity", "consequence_visibility",
            "unique_setpiece_logic", "emotional_stake_inside_action", "momentum", "aftermath_value",
        ],
        "hooks": "목표가 명확하다 / 공간이 보인다 / 시간이 없다",
        "punches": "전술이 뒤집힌다 / 대가가 몸에 새겨진다 / 다음 전투가 더 크다",
        "fails": ["목표 흐림", "공간 안 보임", "액션 후 대가 없음"],
    },
    "SF/판타지": {
        "en": "Science Fiction / Fantasy",
        "core": "세계의 규칙이 인간 드라마의 은유로 작동하는 장르.",
        "items": [
            "world_rule_clarity", "wonder_value", "cost_of_rule",
            "ethical_implication", "rule_consistency", "novelty",
            "human_anchor", "visual_imagination", "mythic_depth", "payoff_of_world_rule",
        ],
        "hooks": "이 세계는 우리와 다르다 — 한 가지가 즉시 보인다 / 경이로운 이미지",
        "punches": "규칙의 대가가 드러난다 / 세계의 비밀이 인간 문제와 연결된다",
        "fails": ["룰 설명만 많음", "인간 드라마 약함", "세계관이 이야기보다 앞섬"],
    },
}


def _genre_text(genre: str) -> str:
    """장르 Rule Pack → 프롬프트용 텍스트."""
    r = GENRE_RULES.get(genre)
    if not r:
        return f"[장르: {genre}] — 범용 장르 규칙 적용."
    return (
        f"[GENRE: {genre} ({r['en']})]\n"
        f"핵심: {r['core']}\n"
        f"필수: {' / '.join(r['items'])}\n"
        f"Hook: {r['hooks']}\n"
        f"Punch: {r['punches']}\n"
        f"실패 신호: {' / '.join(r['fails'])}"
    )


# ═══════════════════════════════════════════════════════════
# 15비트 구조 (Creator Engine 15-Beat Sheet 연동)
# ═══════════════════════════════════════════════════════════

BEATS_15 = [
    {"no": 1,  "name": "Opening Image",          "act": "1막",
     "desc": "작품의 첫인상. 주인공의 일상·결핍·세계. Hook으로 관객을 잡는다."},
    {"no": 2,  "name": "Theme Stated",            "act": "1막",
     "desc": "테마가 대사나 상황으로 암시된다."},
    {"no": 3,  "name": "Set-Up",                  "act": "1막",
     "desc": "주인공의 세계, 결함(거짓 신념), 관계, 규칙을 설정한다."},
    {"no": 4,  "name": "Catalyst",                "act": "1막",
     "desc": "일상을 깨뜨리는 사건. 되돌릴 수 없는 변화의 시작. 강력한 Hook."},
    {"no": 5,  "name": "Debate / Break into 2",   "act": "1막",
     "desc": "갈등. 거부와 수락. 1막에서 2막으로의 전환. Punch로 2막 진입."},
    {"no": 6,  "name": "B-Story / Fun & Games",   "act": "2막",
     "desc": "서브플롯 시작. 장르의 약속을 이행하는 구간. 장르 쾌감 본격 전개."},
    {"no": 7,  "name": "Promise of the Premise",  "act": "2막",
     "desc": "장르 쾌감 절정. 관객이 기대한 것을 보여준다. 가장 재미있는 구간."},
    {"no": 8,  "name": "Midpoint",                "act": "2막",
     "desc": "가짜 승리 또는 가짜 패배. 판이 뒤집힌다. 큰 Punch."},
    {"no": 9,  "name": "Bad Guys Close In",       "act": "2막",
     "desc": "적대 세력 강화. 내외부 압력 증가. 동맹 균열."},
    {"no": 10, "name": "All Is Lost",             "act": "2막",
     "desc": "가장 낮은 지점. 주인공이 모든 것을 잃는다. 죽음의 냄새."},
    {"no": 11, "name": "Dark Night / Break into 3","act": "2막",
     "desc": "절망 속 깨달음. 거짓 신념이 깨진다. 3막 결심. Punch."},
    {"no": 12, "name": "Finale — Gathering",      "act": "3막",
     "desc": "최종 전투 준비. 팀·자원 재결집. 새로운 전략."},
    {"no": 13, "name": "Finale — Climax",         "act": "3막",
     "desc": "최고조 대결. 주인공의 선택이 테마를 증명한다. 최강 Punch."},
    {"no": 14, "name": "Finale — Resolution",     "act": "3막",
     "desc": "여파. 대가. 새로운 질서. 감정 회수."},
    {"no": 15, "name": "Final Image",             "act": "3막",
     "desc": "Opening Image의 대구. 변화의 증거. 마지막 이미지가 남는다."},
]

ACT_BEATS = {
    "1막": [b for b in BEATS_15 if b["act"] == "1막"],       # Beat 1~5
    "2막": [b for b in BEATS_15 if b["act"] == "2막"],       # Beat 6~11
    "3막": [b for b in BEATS_15 if b["act"] == "3막"],       # Beat 12~15
}

ACT_SCENE_TARGETS = {
    "1막": "약 30~35씬 (S#1 ~ S#약35). 1막은 전체의 약 25~30%.",
    "2막": "약 40~45씬 (이전 막 이어서 번호 연속). 2막은 전체의 약 45~50%.",
    "3막": "약 20~25씬 (이전 막 이어서, 총합 약 100씬). 3막은 전체의 약 20~25%.",
}


# ═══════════════════════════════════════════════════════════
# 1. SCENE PLAN — 막별 분할 생성
# ═══════════════════════════════════════════════════════════

def build_scene_plan_prompt(
    act: str,
    genre: str, fmt: str,
    logline: str, intent: str, gns: str,
    characters: str, world: str, structure: str,
    scene_design: str, treatment: str, tone: str,
    previous_plan: str = "",
) -> str:
    gr = _genre_text(genre)
    beats = ACT_BEATS[act]
    target = ACT_SCENE_TARGETS[act]

    beats_text = "\n".join(
        f"  Beat {b['no']}. {b['name']} — {b['desc']}" for b in beats
    )

    # Creator Engine 산출물 항목별 배치
    parts = []
    if logline:      parts.append(f"[LOGLINE]\n{logline}")
    if intent:       parts.append(f"[기획의도 PROJECT INTENT]\n{intent}")
    if gns:          parts.append(f"[GOAL / NEED / STRATEGY]\n{gns}")
    if characters:   parts.append(f"[캐릭터 + 바이블]\n{characters[:3000]}")
    if world:        parts.append(f"[세계관 WORLD BUILD]\n{world}")
    if structure:    parts.append(f"[구조 STRUCTURE — 시놉시스/8시퀀스/15비트]\n{structure[:2500]}")
    if scene_design: parts.append(f"[장면설계 SCENE DESIGN]\n{scene_design[:2500]}")
    if treatment:    parts.append(f"[트리트먼트 TREATMENT]\n{treatment[:4000]}")
    if tone:         parts.append(f"[톤 문서 TONE DOCUMENT]\n{tone}")
    mat = "\n\n".join(parts) if parts else "[자료 없음]"

    prev_block = ""
    if previous_plan:
        prev_block = (
            f"\n[이전 막 씬 플랜 — 번호를 이어서 시작하라]\n"
            f"{previous_plan[-3000:]}\n"
        )

    return f"""
[TASK] {act} 씬 플랜 생성

{act}에 해당하는 비트들의 씬 목록을 설계하라.

[장르]
{gr}
[포맷] {fmt}

[{act} 비트]
{beats_text}

[기획 자료]
{mat}
{prev_block}

[규칙]
1. {target}
2. 각 비트당 6~7씬을 배치하라 (총합 약 100씬 / 100분 / 100페이지).
3. 1씬 = 1페이지 = 약 1분. 씬은 짧고 선명하게.
4. 트리트먼트·장면설계·비트시트를 적극 반영하라.
5. 캐릭터 정보를 반영하여 누가 어디서 어떤 갈등을 겪는지 명확히.
6. 이전 막이 있으면 씬 번호를 이어서 시작하라.
7. 모든 비트를 빠짐없이 포함하라.
8. 각 씬에 Hook(시작) 또는 Punch(끝) 요소를 표기하라.

[OUTPUT FORMAT]

---BEAT_{beats[0]['no']}_START---
Beat {beats[0]['no']}. {beats[0]['name']} ({act})
S#번호 | INT./EXT. 장소 — 시간 | 핵심인물 | 기능 (1줄) | Hook/Punch
S#번호 | ...
---BEAT_{beats[0]['no']}_END---

(이 막의 모든 비트 반복)

마지막에: 이 막 씬 수 / 페이지 수 / 가장 강한 Hook·Punch 장면 2개.
""".strip()


# ═══════════════════════════════════════════════════════════
# 2. WRITE BEAT — 비트 단위 집필
# ═══════════════════════════════════════════════════════════

def build_write_beat_prompt(
    genre: str,
    beat_number: int,
    scene_plan: str,
    characters: str,
    treatment: str,
    tone: str,
    previous_scene_text: str = "",
    logline: str = "",
    world: str = "",
) -> str:
    gr = _genre_text(genre)
    beat_info = BEATS_15[beat_number - 1] if 1 <= beat_number <= 15 else {}

    # 캐릭터 바이블 — 매번 전문 (최대 4000자)
    char_block = characters[:4000] if characters else "(캐릭터 정보 없음)"
    # 톤 — 매번 포함
    tone_block = tone[:1500] if tone else ""
    # 트리트먼트 — 전문 (AI가 해당 비트 구간 참조)
    treat_block = treatment[:5000] if treatment else ""

    # 직전 비트 연속성
    prev_block = ""
    if previous_scene_text:
        prev_block = f"\n[직전 비트 마지막 부분 — 연속성 유지]\n{previous_scene_text[-2500:]}\n"

    return f"""
[TASK] Beat {beat_number} 시나리오 집필 — {beat_info.get('name', '')} ({beat_info.get('act', '')})
{beat_info.get('desc', '')}

이 비트에 해당하는 모든 씬을 한국 표준 시나리오 서식으로 집필하라.

[장르]
{gr}
[로그라인] {logline or '(씬 플랜 참조)'}

[씬 플랜 — 이 비트의 씬을 찾아 정확히 따르라]
{scene_plan}

[캐릭터 바이블 — 각 인물의 말투·리듬·태도를 반드시 반영]
{char_block}

[세계관]
{world[:1500] if world else '(씬 플랜 참조)'}

[트리트먼트 — Beat {beat_number}에 해당하는 내용 참조]
{treat_block}

{f"[톤 문서]{chr(10)}{tone_block}" if tone_block else ""}
{prev_block}

[RULES]
1. 씬 플랜에서 Beat {beat_number}의 씬들을 찾아 전부 집필.
2. 1씬 = 약 1페이지. 씬은 짧고 선명하게.
3. 캐릭터 바이블의 말투·대사 샘플 참조 → 보이스 구분.
4. desire → obstacle → conflict → turn → emotional shift → exit pressure
5. 대사 = 행동. 서브텍스트 필수. 설명성 대사 금지.
6. 각 씬은 Hook으로 시작, Punch로 끝.
7. 직전 비트와의 연속성 유지.
8. 지문(Action Line) 규칙:
   - 한 단락 최대 3~4줄. 소설처럼 한 동작씩 줄바꿈 금지.
   - 카메라가 보는 것만. 내면 설명 금지.
   - 핵심 이미지 하나에 집중. 불필요한 동작 생략.
   - "그는 ~한다. 그는 ~한다." 반복 구조 금지.

[OUTPUT]
맨 위에 아래 형식의 헤더를 반드시 먼저 출력하라:

═══════════════════════════════════════
{beat_info.get('act', '')} — Beat {beat_number}. {beat_info.get('name', '')}
═══════════════════════════════════════

그 다음 씬들을 순서대로 집필. 씬 사이 빈 줄 2개.
마지막에 --- 후 내부 메모 1줄 (비트 요약 + 보이스 점검).
""".strip()


# ═══════════════════════════════════════════════════════════
# 3. REWRITE BEAT
# ═══════════════════════════════════════════════════════════

def build_rewrite_prompt(
    genre: str,
    beat_number: int,
    current_text: str,
    characters: str,
    instruction: str = "",
) -> str:
    gr = _genre_text(genre)
    char_block = characters[:3000] if characters else ""
    user_inst = instruction.strip() if instruction else "극적 힘, 서브텍스트, 캐릭터 보이스, 장르 효능, Hook & Punch를 강화하라."

    return f"""
[TASK] Beat {beat_number} 다시 쓰기 — {user_inst}

[장르]
{gr}

[캐릭터 바이블 — 말투 반영 필수]
{char_block}

[현재 텍스트]
{current_text}

[RULES]
1. 강점 유지, 약점 개선
2. 보이스 분리 강화 — 캐릭터 바이블 말투 규칙 반드시 참조
3. 서브텍스트·장르 효능 강화
4. 설명성 대사 제거
5. 지문 압축 — 소설체 금지. 한 단락 3~4줄. 핵심 이미지만. "그는~한다" 반복 금지.
6. Hook(씬 시작)과 Punch(씬 끝)가 모든 씬에 있는지 점검하고 보강.

[OUTPUT]
개선된 시나리오 전문. 마지막에 --- 후 변경 요약 3줄.
""".strip()
