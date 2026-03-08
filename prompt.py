# ─────────────────────────────────────────────────────────────
# BLUE JEANS SCREENPLAY WRITER ENGINE v2.2
# prompt.py — Act-Split Scene Plan + Beat-by-Beat Writing
# © 2026 BLUE JEANS PICTURES
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 BLUE JEANS SCREENPLAY WRITER ENGINE입니다.
기획 자료를 기반으로 실제 촬영 가능한 시나리오를 집필합니다.

━━ BRAND ━━
- 모든 장면은 존재 이유를 가져야 한다.
- 모든 대사는 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나를 수행한다.
- 3막/16비트/캐릭터아크/장르규칙이 내부에서 작동하되 이론 용어를 노출하지 않는다.
- 재미와 의미가 동시에 회수되는 설계.

━━ SCENE RULES ━━
모든 씬: Scene Heading → Action → Dialogue → Subtext → Turn → Exit Hook
설계: desire → obstacle → conflict → turn → emotional shift → exit pressure

━━ DIALOGUE ━━
- 각 인물은 고유한 말투 리듬, 문장 길이, 공격/방어 스타일을 가진다.
- 캐릭터 바이블의 말투 규칙·대사 샘플을 반드시 참조하라.
- 누가 말해도 같은 말투이면 실패. 설명성 대사 금지. 서브텍스트 필수.

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

# ─── 비트 정의 (15비트) ──────────────────

BEATS_15 = [
    {"no": 1,  "name": "Opening Image",          "act": "1막"},
    {"no": 2,  "name": "Theme Stated",            "act": "1막"},
    {"no": 3,  "name": "Set-Up",                  "act": "1막"},
    {"no": 4,  "name": "Catalyst",                "act": "1막"},
    {"no": 5,  "name": "Debate / Break into 2",   "act": "1막"},
    {"no": 6,  "name": "B-Story / Fun & Games",   "act": "2막"},
    {"no": 7,  "name": "Promise of the Premise",  "act": "2막"},
    {"no": 8,  "name": "Midpoint",                "act": "2막"},
    {"no": 9,  "name": "Bad Guys Close In",       "act": "2막"},
    {"no": 10, "name": "All Is Lost",             "act": "2막"},
    {"no": 11, "name": "Dark Night / Break into 3", "act": "2막"},
    {"no": 12, "name": "Finale — Gathering",      "act": "3막"},
    {"no": 13, "name": "Finale — Climax",         "act": "3막"},
    {"no": 14, "name": "Finale — Resolution",     "act": "3막"},
    {"no": 15, "name": "Final Image",             "act": "3막"},
]

# 막별 비트 분류
ACT_BEATS = {
    "1막": [b for b in BEATS_15 if b["act"] == "1막"],       # Beat 1~5
    "2막": [b for b in BEATS_15 if b["act"] == "2막"],       # Beat 6~11
    "3막": [b for b in BEATS_15 if b["act"] == "3막"],       # Beat 12~15
}

ACT_SCENE_TARGETS = {
    "1막": "약 30~35씬 (S#1 ~ S#약35)",
    "2막": "약 40~45씬 (이전 막 이어서 번호 연속)",
    "3막": "약 25~30씬 (이전 막 이어서 번호 연속, 총합 약 100씬)",
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
    gr = GENRE_RULES.get(genre, "")
    beats = ACT_BEATS[act]
    target = ACT_SCENE_TARGETS[act]

    beats_text = "\n".join(
        f"  Beat {b['no']}. {b['name']}" for b in beats
    )

    # 자료 조립
    parts = []
    if logline:      parts.append(f"[LOGLINE]\n{logline}")
    if intent:       parts.append(f"[기획의도]\n{intent}")
    if gns:          parts.append(f"[GNS]\n{gns}")
    if characters:   parts.append(f"[캐릭터]\n{characters[:3000]}")
    if world:        parts.append(f"[세계관]\n{world}")
    if structure:    parts.append(f"[구조]\n{structure[:2000]}")
    if scene_design: parts.append(f"[장면설계]\n{scene_design[:2000]}")
    if treatment:    parts.append(f"[트리트먼트]\n{treatment[:4000]}")
    if tone:         parts.append(f"[톤]\n{tone}")
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

[장르] {genre} — {gr}
[포맷] {fmt}

[{act} 비트]
{beats_text}

[기획 자료]
{mat}
{prev_block}

[규칙]
1. {target}.
2. 각 비트당 6~7씬을 배치하라.
3. 1씬 = 1페이지 = 약 1분. 씬은 짧고 선명하게.
4. 트리트먼트·장면설계·비트시트를 적극 반영하라.
5. 캐릭터 정보를 반영하여 누가 어디서 어떤 갈등을 겪는지 명확히.
6. 이전 막이 있으면 씬 번호를 이어서 시작하라.
7. 모든 비트를 빠짐없이 포함하라.

[OUTPUT FORMAT]

---BEAT_{beats[0]['no']}_START---
Beat {beats[0]['no']}. {beats[0]['name']} ({act})
S#번호 | INT./EXT. 장소 — 시간 | 핵심인물 | 기능 (1줄)
S#번호 | ...
---BEAT_{beats[0]['no']}_END---

(이 막의 모든 비트 반복)

마지막에: 이 막 씬 수 / 페이지 수.
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
    gr = GENRE_RULES.get(genre, "")
    beat_info = BEATS_15[beat_number - 1] if 1 <= beat_number <= 15 else {}

    char_block = characters[:4000] if characters else "(캐릭터 정보 없음)"
    tone_block = tone[:1500] if tone else ""
    treat_block = treatment[:5000] if treatment else ""

    prev_block = ""
    if previous_scene_text:
        prev_block = f"\n[직전 비트 마지막 부분 — 연속성 유지]\n{previous_scene_text[-2500:]}\n"

    return f"""
[TASK] Beat {beat_number} 시나리오 집필 — {beat_info.get('name', '')} ({beat_info.get('act', '')})

이 비트에 해당하는 모든 씬을 한국 표준 시나리오 서식으로 집필하라.

[장르] {genre} — {gr}
[로그라인] {logline or '(씬 플랜 참조)'}

[씬 플랜 — 이 비트의 씬을 찾아 정확히 따르라]
{scene_plan}

[캐릭터 바이블 — 각 인물의 말투·리듬·태도를 반드시 반영]
{char_block}

[세계관]
{world[:1500] if world else '(씬 플랜 참조)'}

[트리트먼트 — Beat {beat_number}에 해당하는 내용 참조]
{treat_block}

{f"[톤]{chr(10)}{tone_block}" if tone_block else ""}
{prev_block}

[RULES]
1. 씬 플랜에서 Beat {beat_number}의 씬들을 찾아 전부 집필.
2. 1씬 = 약 1페이지. 씬은 짧고 선명하게.
3. 캐릭터 바이블의 말투·대사 샘플 참조 → 보이스 구분.
4. desire → obstacle → conflict → turn → emotional shift → exit pressure
5. 대사 = 행동. 서브텍스트 필수. 설명성 대사 금지.
6. 각 씬 끝에 exit hook.
7. 직전 비트와의 연속성 유지.

[OUTPUT]
Beat {beat_number}의 씬들을 순서대로 집필. 씬 사이 빈 줄 2개.
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
    gr = GENRE_RULES.get(genre, "")
    char_block = characters[:3000] if characters else ""
    user_inst = instruction.strip() if instruction else "극적 힘, 서브텍스트, 캐릭터 보이스, 장르 효능을 강화하라."

    return f"""
[TASK] Beat {beat_number} 다시 쓰기 — {user_inst}

[장르] {genre} — {gr}

[캐릭터 바이블 — 말투 반영 필수]
{char_block}

[현재 텍스트]
{current_text}

[RULES]
1. 강점 유지, 약점 개선  2. 보이스 분리 강화  3. 서브텍스트·장르 효능 강화  4. 설명성 대사 제거

[OUTPUT]
개선된 시나리오 전문. 마지막에 --- 후 변경 요약 3줄.
""".strip()
