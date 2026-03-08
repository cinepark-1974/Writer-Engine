# ─────────────────────────────────────────────────────────────
# BLUE JEANS SCREENPLAY WRITER ENGINE v2.1
# prompt.py — Beat-by-Beat Scene Writing
# © 2026 BLUE JEANS PICTURES
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 BLUE JEANS SCREENPLAY WRITER ENGINE입니다.
기획 자료를 기반으로 실제 촬영 가능한 시나리오를 집필합니다.

━━ BRAND ━━
- 모든 장면은 존재 이유를 가져야 한다.
- 모든 대사는 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나를 수행한다.
- 3막/16비트/캐릭터아크/장르규칙이 내부에서 작동하되 결과물에 이론 용어를 노출하지 않는다.
- 재미와 의미가 동시에 회수되는 설계.

━━ SCENE RULES ━━
모든 씬: Scene Heading → Action → Dialogue → Subtext → Turn → Exit Hook
설계: desire → obstacle → conflict → turn → emotional shift → exit pressure

━━ DIALOGUE ━━
- 각 인물은 고유한 말투 리듬, 문장 길이, 공격/방어 스타일을 가진다.
- 캐릭터 바이블의 말투 규칙과 대사 샘플을 반드시 참조하라.
- 누가 말해도 같은 말투이면 실패.
- 설명성 대사 금지. 서브텍스트 필수.

━━ FORMAT ━━
한국어. 한국 표준 시나리오 서식:

S#번호. INT./EXT. 장소 — 시간

(Action — 현재시제, 시각적)

    캐릭터명
    (parenthetical)
대사

━━ SAFETY ━━
허구 서사 속 범죄/폭력 허용. 현실 실행 지침/제조법 금지.
""".strip()


GENRE_RULES = {
    "드라마":      "인간의 선택과 대가를 통해 진실에 도달. 감정 깊이·관계 변화·대가 필수.",
    "느와르":      "도덕적 모호함 속 타락과 생존 대가. 배신 설계·편집증·어둠의 아이러니.",
    "스릴러":      "정보 비대칭과 압박으로 불안 지속. 시계장치·위협 제어·반전 압력.",
    "코미디":      "웃음 메커니즘 작동. premise engine·status comedy·callback payoff.",
    "멜로/로맨스":  "갈망 축적과 감정 지연. 타이밍 어긋남·취약성 노출·감정 회수.",
    "호러":        "공포 예감과 축적. 안전 위반·감각 불안·공포 이월.",
    "액션":        "물리적 목표와 대가. 공간 선명·전술 반전·액션 후 대가.",
    "SF/판타지":   "세계 규칙이 인간 드라마의 은유. 경이감·규칙 대가·인간 앵커.",
}


# ─── 비트 정의 ───────────────────────────────

BEATS_15 = [
    {"no": 1,  "name": "Opening Image",     "act": "1막", "desc": "작품의 첫인상. 주인공의 일상·결핍·세계를 보여준다."},
    {"no": 2,  "name": "Theme Stated",       "act": "1막", "desc": "테마가 대사나 상황으로 암시된다."},
    {"no": 3,  "name": "Set-Up",             "act": "1막", "desc": "주인공의 세계, 결함, 관계, 규칙을 설정한다."},
    {"no": 4,  "name": "Catalyst",           "act": "1막", "desc": "일상을 깨뜨리는 사건. 되돌릴 수 없는 변화 시작."},
    {"no": 5,  "name": "Debate / Break into 2", "act": "1막→2막", "desc": "갈등. 거부와 수락. 2막으로의 전환."},
    {"no": 6,  "name": "B-Story / Fun & Games", "act": "2막 전반", "desc": "서브플롯 시작. 장르의 약속을 이행하는 구간."},
    {"no": 7,  "name": "Promise of the Premise", "act": "2막 전반", "desc": "장르 쾌감 본격 전개. 관객이 기대한 것을 보여준다."},
    {"no": 8,  "name": "Midpoint",           "act": "2막 중간", "desc": "가짜 승리 또는 가짜 패배. 판이 뒤집힌다."},
    {"no": 9,  "name": "Bad Guys Close In",  "act": "2막 후반", "desc": "적대 세력 강화. 내외부 압력 증가."},
    {"no": 10, "name": "All Is Lost",        "act": "2막 후반", "desc": "가장 낮은 지점. 주인공이 모든 것을 잃는다."},
    {"no": 11, "name": "Dark Night / Break into 3", "act": "2막→3막", "desc": "절망 속 깨달음. 3막 결심."},
    {"no": 12, "name": "Finale — Gathering",  "act": "3막", "desc": "최종 전투 준비. 팀/자원 재결집."},
    {"no": 13, "name": "Finale — Climax",     "act": "3막", "desc": "최고조 대결. 주인공의 선택이 테마를 증명한다."},
    {"no": 14, "name": "Finale — Resolution",  "act": "3막", "desc": "여파. 대가. 새로운 질서."},
    {"no": 15, "name": "Final Image",        "act": "3막", "desc": "Opening Image의 대구. 변화의 증거."},
]


# ═══════════════════════════════════════════════════════════
# 1. SCENE PLAN — 비트 기반 60~80씬 플랜
# ═══════════════════════════════════════════════════════════

def build_scene_plan_prompt(
    genre: str, fmt: str,
    logline: str, intent: str, gns: str,
    characters: str, world: str, structure: str,
    scene_design: str, treatment: str, tone: str,
) -> str:
    gr = GENRE_RULES.get(genre, "")
    beats_text = "\n".join(
        f"  Beat {b['no']}. {b['name']} ({b['act']}) — {b['desc']}"
        for b in BEATS_15
    )

    # 각 자료를 역할별로 명확히 배치
    parts = []
    if logline:    parts.append(f"[LOGLINE]\n{logline}")
    if intent:     parts.append(f"[기획의도]\n{intent}")
    if gns:        parts.append(f"[GOAL/NEED/STRATEGY]\n{gns}")
    if characters: parts.append(f"[캐릭터]\n{characters[:3000]}")
    if world:      parts.append(f"[세계관]\n{world}")
    if structure:  parts.append(f"[구조/시놉시스/비트시트]\n{structure}")
    if scene_design: parts.append(f"[장면설계]\n{scene_design}")
    if treatment:  parts.append(f"[트리트먼트]\n{treatment[:4000]}")
    if tone:       parts.append(f"[톤 문서]\n{tone}")
    mat = "\n\n".join(parts) if parts else "[자료 없음]"

    return f"""
[TASK] 비트 기반 씬 플랜 생성

아래 기획 자료를 분석하고, 15비트 구조에 맞춰 전체 씬 목록을 설계하라.

[장르] {genre} — {gr}
[포맷] {fmt}

[15비트 구조]
{beats_text}

[기획 자료]
{mat}

[규칙]
1. 영화 장편은 총 100씬 / 100분 / 100페이지 기준. 시리즈는 1화 기준 30~40씬.
2. 각 비트당 6~7씬을 배치하라 (15비트 × 6~7씬 ≈ 100씬).
3. 1씬 = 1페이지 = 약 1분. 씬은 짧고 선명하게.
4. 기획 자료의 트리트먼트·장면설계·비트시트를 적극 반영하라.
5. 캐릭터 정보를 반영하여 누가 어디서 어떤 갈등을 겪는지 명확히 하라.

[OUTPUT FORMAT]

먼저 1~2줄 핵심 요약 (테마·주인공아크·엔딩방향).

그 다음 비트별 씬 목록:

---BEAT_1_START---
Beat 1. Opening Image (1막)
S#1 | INT./EXT. 장소 — 시간 | 핵심인물 | 기능 (1줄)
S#2 | INT./EXT. 장소 — 시간 | 핵심인물 | 기능 (1줄)
...
---BEAT_1_END---

---BEAT_2_START---
Beat 2. Theme Stated (1막)
S#3 | ...
...
---BEAT_2_END---

(Beat 15까지 반복)

마지막에: 총 씬 수 / 예상 러닝타임 / 가장 강한 장면 3개.
""".strip()


# ═══════════════════════════════════════════════════════════
# 2. WRITE BEAT — 비트 단위 씬 집필 (핵심)
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
    gr = GENRE_RULES.get(genre, "")
    beat_info = BEATS_15[beat_number - 1] if 1 <= beat_number <= 15 else {}

    # 캐릭터 바이블 — 매번 전문 포함 (최대 4000자)
    char_block = characters[:4000] if characters else "(캐릭터 정보 없음)"

    # 톤 — 매번 포함
    tone_block = tone[:1500] if tone else ""

    # 트리트먼트 — 전문 포함 (AI가 해당 비트에 맞는 부분을 참조)
    treat_block = treatment[:5000] if treatment else ""

    # 직전 씬 — 연속성
    prev_block = ""
    if previous_scene_text:
        prev_block = f"\n[직전 씬 — 연속성 유지]\n{previous_scene_text[-2500:]}\n"

    return f"""
[TASK] Beat {beat_number} 시나리오 집필 — {beat_info.get('name', '')} ({beat_info.get('act', '')})

비트 설명: {beat_info.get('desc', '')}

이 비트에 해당하는 모든 씬을 한국 표준 시나리오 서식으로 집필하라.

[장르] {genre} — {gr}
[로그라인] {logline or '(참조)'}

[씬 플랜 — 이 비트의 씬 목록을 확인하고 정확히 따르라]
{scene_plan}

[캐릭터 바이블 — 각 인물의 말투·리듬·태도를 반드시 반영하라]
{char_block}

[세계관]
{world[:1500] if world else '(씬 플랜 참조)'}

[트리트먼트 — Beat {beat_number}에 해당하는 내용을 찾아 참조하라]
{treat_block}

{f"[톤 문서]{chr(10)}{tone_block}" if tone_block else ""}
{prev_block}

[RULES]
1. 씬 플랜에서 Beat {beat_number}에 해당하는 씬들을 찾아 전부 집필하라.
2. 각 씬은 독립적 장면이다 — 1씬 = 약 1페이지.
3. 캐릭터 바이블의 말투 규칙·대사 샘플을 참조하여 각 인물의 보이스를 구분하라.
4. desire → obstacle → conflict → turn → emotional shift → exit pressure
5. 대사는 설명이 아니라 행동. 서브텍스트 필수.
6. 각 씬 끝에 exit hook (다음 씬 연결 압력).
7. 직전 씬과의 연속성을 유지하라.

[OUTPUT]
씬 플랜의 Beat {beat_number} 씬들을 순서대로 집필.
각 씬 사이에 빈 줄 2개.
마지막에 --- 후 내부 메모 (비트 요약 1줄 + 캐릭터 보이스 점검 1줄).
""".strip()


# ═══════════════════════════════════════════════════════════
# 3. REWRITE BEAT — 비트 다시 쓰기
# ═══════════════════════════════════════════════════════════

def build_rewrite_prompt(
    genre: str,
    beat_number: int,
    current_text: str,
    characters: str,
    instruction: str = "",
) -> str:
    gr = GENRE_RULES.get(genre, "")
    char_block = characters[:3000] if characters else ""
    user_inst = instruction.strip() if instruction else "극적 힘, 서브텍스트, 캐릭터 보이스, 장르 효능을 강화하라."

    return f"""
[TASK] Beat {beat_number} 다시 쓰기

지시: {user_inst}

[장르] {genre} — {gr}

[캐릭터 바이블 — 말투 반영 필수]
{char_block}

[현재 텍스트]
{current_text}

[RULES]
1. 강점 유지, 약점 개선
2. 캐릭터 보이스 분리 강화
3. 서브텍스트·장르 효능 강화
4. 설명성 대사 제거

[OUTPUT]
개선된 시나리오 전문.
마지막에 --- 후 변경 요약 (3줄).
""".strip()
