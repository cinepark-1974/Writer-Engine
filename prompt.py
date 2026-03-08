# ─────────────────────────────────────────────────────────────
# BLUE JEANS SCREENPLAY WRITER ENGINE v2.0
# prompt.py — 2-Step Architecture
# © 2026 BLUE JEANS PICTURES
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
당신은 BLUE JEANS SCREENPLAY WRITER ENGINE입니다.
기획 자료를 기반으로 실제 촬영 가능한 시나리오를 씬 단위로 집필합니다.

━━ BRAND ━━
- 모든 장면은 존재 이유를 가져야 한다.
- 모든 대사는 욕망, 방어, 회피, 공격, 유혹, 압박 중 하나를 수행한다.
- 3막/16비트/캐릭터아크/장르규칙이 내부에서 작동하되 결과물에 이론 용어를 노출하지 않는다.
- 재미와 의미가 동시에 회수되는 설계.

━━ SCENE RULES ━━
모든 씬 필수: Scene Heading → Action → Dialogue → Subtext → Turn → Exit Hook
설계 순서: desire → obstacle → conflict → turn → emotional shift → exit pressure
대사: 말투 분리 필수 / 설명성 대사 금지 / 서브텍스트 필수

━━ NONSENSE FILTER ━━
금지: 목적 없는 장면 / 갈등 없는 대화 / 보이스 중복 / 전환 없는 장면 / 설교 대사

━━ FORMAT ━━
한국어 출력. 한국 표준 시나리오 서식:

S#번호. INT./EXT. 장소 — 시간

(Action — 현재시제, 시각적, 구체적)

    캐릭터명
    (parenthetical)
대사

━━ SAFETY ━━
허구 서사 속 범죄/폭력 허용. 현실 실행 지침/제조법/고어 자체 목적 금지.
""".strip()


# ═══════════════════════════════════════════════════════════
# GENRE RULES
# ═══════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════
# 1. SCENE PLAN — 자료 분석 + 씬 목록 생성
# ═══════════════════════════════════════════════════════════

def build_scene_plan_prompt(material: str, genre: str, fmt: str) -> str:
    genre_rule = GENRE_RULES.get(genre, "")
    return f"""
[TASK] 씬 플랜 생성

아래 기획 자료를 분석하고, 이 작품의 전체 씬 목록을 설계하라.

[장르] {genre}
[장르 규칙] {genre_rule}
[포맷] {fmt}

[기획 자료]
{material[:10000]}

[OUTPUT 형식]

먼저 2~3줄로 작품 핵심을 요약하라 (테마, 주인공 아크, 엔딩 방향).

그 다음 아래 형식으로 씬 목록을 작성하라.
영화는 20~30씬, 시리즈는 1화 기준 15~20씬.

---SCENE_PLAN_START---
S#1 | INT./EXT. 장소 — 시간 | 핵심인물 | 핵심기능 (1줄)
S#2 | INT./EXT. 장소 — 시간 | 핵심인물 | 핵심기능 (1줄)
S#3 | ...
---SCENE_PLAN_END---

각 씬은 반드시:
- 존재 이유가 명확할 것
- 이전 씬에서 다음 씬으로 연결 압력이 있을 것
- 장르 효능이 작동할 것

씬 목록 후 1줄 코멘트: 전체 씬 수, 예상 러닝타임(페이지), 가장 강한 장면 3개.
""".strip()


# ═══════════════════════════════════════════════════════════
# 2. WRITE SCENE — 다음 씬 생성
# ═══════════════════════════════════════════════════════════

def build_write_scene_prompt(
    material: str,
    genre: str,
    scene_plan: str,
    scene_number: int,
    previous_scene_text: str = "",
    total_scenes_written: int = 0,
) -> str:
    genre_rule = GENRE_RULES.get(genre, "")

    context_block = ""
    if previous_scene_text:
        # 직전 씬만 전문 포함 (토큰 절약)
        context_block = (
            f"\n[직전 씬 — 연속성 유지 필수]\n"
            f"{previous_scene_text[-3000:]}\n"
        )

    return f"""
[TASK] 씬 #{scene_number} 집필

아래 자료와 씬 플랜을 기반으로 S#{scene_number}의 시나리오를 집필하라.
지금까지 {total_scenes_written}개의 씬이 완료되었다. 다음 씬을 써라.

[장르] {genre}
[장르 규칙] {genre_rule}

[씬 플랜]
{scene_plan}

[기획 자료 (핵심)]
{material[:6000]}
{context_block}

[RULES]
1. S#{scene_number}에 해당하는 씬을 정확히 집필하라.
2. 한국 표준 시나리오 서식으로 작성하라.
3. desire → obstacle → conflict → turn → emotional shift → exit pressure
4. 대사: 캐릭터 보이스 분리, 서브텍스트, 설명성 대사 금지
5. 장면 끝에 다음 장면을 보고 싶게 만드는 exit hook
6. 직전 씬과의 연속성을 유지하라.

[OUTPUT]
1. 시나리오 본문 (S#{scene_number})
2. --- 아래에 내부 메모 1줄: [기능] / [장르효능] / [turn]
""".strip()


# ═══════════════════════════════════════════════════════════
# 3. REWRITE SCENE — 이 씬 다시 쓰기
# ═══════════════════════════════════════════════════════════

def build_rewrite_scene_prompt(
    genre: str,
    scene_plan: str,
    scene_number: int,
    current_scene_text: str,
    instruction: str = "",
) -> str:
    genre_rule = GENRE_RULES.get(genre, "")
    user_instruction = instruction.strip() if instruction else "극적 힘, 서브텍스트, 캐릭터 보이스, 장르 효능을 강화하라."

    return f"""
[TASK] 씬 #{scene_number} 다시 쓰기

아래 씬을 개선하라: {user_instruction}

[장르] {genre}
[장르 규칙] {genre_rule}

[씬 플랜 참고]
{scene_plan}

[현재 씬 텍스트]
{current_scene_text}

[RULES]
1. 한국 표준 시나리오 서식 유지
2. 강점은 유지하고 약점만 개선
3. 캐릭터 보이스 분리 / 서브텍스트 / 장르 효능 강화
4. 설명성 대사 제거

[OUTPUT]
1. 개선된 시나리오 본문
2. --- 아래에 변경 사항 요약 (2~3줄)
""".strip()


# ═══════════════════════════════════════════════════════════
# 4. DIALOGUE POLISH — 대사 다듬기
# ═══════════════════════════════════════════════════════════

def build_polish_prompt(genre: str, scene_text: str) -> str:
    genre_rule = GENRE_RULES.get(genre, "")
    return f"""
[TASK] 대사 다듬기

아래 씬의 대사를 고도화하라.

[장르] {genre}
[장르 규칙] {genre_rule}

[씬 텍스트]
{scene_text}

[RULES]
1. 말투 분리 강화 (각 인물의 speech rhythm, attack/defense style)
2. 서브텍스트 강화 (말하지 않는 것이 더 강하게)
3. 설명성 대사 제거
4. 권력관계 변화 반영
5. 리액션 살리기 (침묵, 행동, 표정)

[OUTPUT]
1. 다듬어진 씬 전문
2. --- 아래에 주요 변경 사항 (3줄)
""".strip()
