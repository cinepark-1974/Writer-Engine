# =================================================================
# 👖 BLUE JEANS REVISE ENGINE
# prompt.py — System Prompt + AI ESCAPE + Genre Rules + 3-Stage Builders
# =================================================================
# © 2026 BLUE JEANS PICTURES. All rights reserved.
#
# v1.0 (2026-04-21)
# - 영화 시나리오 전용 각색(Revision) 엔진
# - Writer Engine 결과물 DOCX + 수정 지시문 + LOCKED 요소 입력
# - 3-Stage: DIAGNOSE (지시 해석) → REVISE (실제 집필) → VERIFY (검증)
# - 듀얼 모델: Opus 4.6 (집필) / Sonnet 4.6 (분석)
# - Writer Engine v3.5 룰팩 내장 (AI ESCAPE A1~A20, 장르 Override)
# - Profession Pack v2.3.9 연동 (직업 전문성 블록 자동 주입)
# =================================================================

# ─────────────────────────────────────────────────────────────────
# Profession Pack 연동 (선택적 — 없어도 엔진은 정상 동작)
# ─────────────────────────────────────────────────────────────────
try:
    from profession_pack import (
        build_profession_block as _build_profession_block,
        detect_profession_category as _detect_profession_category,
    )
    PROFESSION_PACK_AVAILABLE = True
except ImportError:
    PROFESSION_PACK_AVAILABLE = False
    def _build_profession_block(text, character_name=""):
        return ""
    def _detect_profession_category(text):
        return []


# ─────────────────────────────────────────────────────────────────
# Period Pack 연동 (사극·시대극 — 선택적)
# ─────────────────────────────────────────────────────────────────
try:
    from period_pack import (
        build_period_block as _build_period_block,
        get_all_period_keys as _get_all_period_keys,
        get_period_label as _get_period_label,
    )
    PERIOD_PACK_AVAILABLE = True
except ImportError:
    PERIOD_PACK_AVAILABLE = False
    def _build_period_block(locked_text="", period_keys=None, max_periods=2):
        return ""
    def _get_all_period_keys():
        return []
    def _get_period_label(key):
        return key


# ─────────────────────────────────────────────────────────────────
# Writer Modules 연동 (Fact-Based + Historical + Genre Override/Enforcement)
# ─────────────────────────────────────────────────────────────────
try:
    from writer_modules import (
        get_fact_based_rules as _get_fact_based_rules,
        get_historical_film_rules as _get_historical_film_rules,
        get_genre_override as _get_genre_override,
        get_genre_enforcement as _get_genre_enforcement,
    )
    WRITER_MODULES_AVAILABLE = True
except ImportError:
    WRITER_MODULES_AVAILABLE = False
    def _get_fact_based_rules(b):
        return ""
    def _get_historical_film_rules(b, t=""):
        return ""
    def _get_genre_override(g):
        return ""
    def _get_genre_enforcement(g):
        return ""


def get_period_keys_for_ui() -> list:
    """UI 드롭다운용 시대 키 목록. (현대) 옵션을 첫 항목으로 추가."""
    if not PERIOD_PACK_AVAILABLE:
        return ["(현대)"]
    keys = _get_all_period_keys()
    return ["(현대)"] + list(keys)


def get_period_labels_for_ui() -> dict:
    """UI 표시용 키→라벨 매핑."""
    labels = {"(현대)": "현대 (사극·시대극이 아닌 경우 선택)"}
    if PERIOD_PACK_AVAILABLE:
        for k in _get_all_period_keys():
            labels[k] = _get_period_label(k)
    return labels


def build_profession_context(
    profession_input: str,
    raw_text: str = "",
    max_auto_detect_chars: int = 30000
) -> str:
    """Revise Engine 전용: 사용자 명시 직업 + 원본 자동 추출을 조합.

    우선순위:
    1. 사용자가 명시 입력한 직업 문자열을 파싱
       - 형식: "유진=쇼핑 호스트, 진호=변호사" 또는 "쇼핑 호스트, 변호사"
    2. 입력이 비어있으면 원본 DOCX 본문에서 자동 추출
       - 앞 30,000자만 검색 (속도·토큰 절약)

    감지 실패 시 빈 문자열 반환 → REVISE 빌더가 직업 블록 없이 진행.
    """
    if not PROFESSION_PACK_AVAILABLE:
        return ""

    blocks = []
    seen_categories = set()

    # 1. 명시 입력 파싱
    if profession_input and profession_input.strip():
        # "이름=직업, 이름=직업" 또는 "직업, 직업" 두 형식 모두 지원
        entries = [e.strip() for e in profession_input.replace(";", ",").split(",") if e.strip()]
        for entry in entries:
            if "=" in entry:
                name, prof = entry.split("=", 1)
                name, prof = name.strip(), prof.strip()
            else:
                name, prof = "", entry.strip()
            cats = _detect_profession_category(prof)
            for cat in cats:
                if cat in seen_categories:
                    continue
                seen_categories.add(cat)
                block = _build_profession_block(prof, character_name=name)
                if block:
                    blocks.append(block)

    # 2. 원본 자동 추출 (명시 입력이 없거나, 명시 입력이 있어도 추가로 감지)
    if raw_text:
        sample = raw_text[:max_auto_detect_chars]
        auto_cats = _detect_profession_category(sample)
        # 카테고리 → 대표 키워드 매핑 (자동 추출 시 블록 생성용)
        try:
            from profession_pack import PROFESSION_KEYWORDS as _PROF_KW
        except ImportError:
            _PROF_KW = {}
        for cat in auto_cats:
            if cat in seen_categories:
                continue
            seen_categories.add(cat)
            # 해당 카테고리의 첫 번째 키워드를 대표 직업으로 사용
            rep_keyword = _PROF_KW.get(cat, [cat])[0] if _PROF_KW.get(cat) else cat
            block = _build_profession_block(rep_keyword, character_name="(자동 추출)")
            if block:
                blocks.append(block)

    if not blocks:
        return ""

    return "\n\n".join(blocks)


# =================================================================
# [1] SYSTEM PROMPT — 전 단계 공통 주입
# =================================================================
SYSTEM_PROMPT = """당신은 블루진픽처스(Blue Jeans Pictures)의 수석 각색 작가(Senior Revision Writer)이다.
글로벌 메이저 스튜디오에서 20년 이상 각색·리비전을 전담해온 베테랑 각본가의 감각을 지녔다.

[블루진 철학 — Indigo Spirit]
1. New and Classic: 작가의 젊고 자유로운 상상력(New)을 존중하되, 시간이 지나도 남는 깊이(Classic)를 더한다.
2. Freedom Fit: 규칙 강요가 아닌, 작품이 가장 자연스럽게 숨 쉴 수 있는 방향(Fit)을 제안한다.
3. Innovative Washing: 표면적 문장 손질보다, 서사의 불순물(인과·욕망·대가·장면기능)을 먼저 걷어낸다.

[Revise Engine의 핵심 원칙 — Voice First]
1. 각색은 "원본의 강점을 보존하면서 약점만 교체"하는 작업이다. 재창작이 아니다.
2. 작가가 이미 잘 쓴 디테일(사물, 공간, 미세 행동, 리듬, 고유 어휘)은 절대 삭제하지 않는다.
3. 인물의 능동적 선택을 수동적 반응으로 바꾸지 않는다.
4. 감정을 형용사로 설명하지 않는다. 행동으로 보여준다.
5. LOCKED 요소는 어떤 경우에도 건드리지 않는다. 지시문이 LOCKED와 충돌하면 LOCKED가 우선한다.

[출력 규칙]
1. 한국어로 작성. 전문 용어는 한글용어(English Term) 병기.
2. 마크다운 강조 기호(**) 사용 금지.
3. 리스트는 번호를 붙이고 한 줄에 하나씩.
4. 불필요한 수사·감탄·칭찬 금지.
5. JSON 출력 시 단일 JSON 객체만 반환. 마크다운 코드블록 금지.
6. 줄바꿈은 JSON 내부에서 \\n 처리.
7. Key/Value는 쌍따옴표("). Value 내부 대사/지문은 홑따옴표(').
8. 마지막 닫는 괄호까지 완결된 JSON만 출력.

[안전 규칙]
허용: 허구 속 범죄/폭력/살인/마약/납치, 성적 긴장, 거친 언어.
운영: 드라마 기능 우선. 수법보다 인물·대가·윤리성.
금지: 현실 범죄 실행 지침, 제조법, 고어 자체 목적.
"""

# =================================================================
# [2] AI SCREENPLAY ESCAPE — Writer Engine v3.5 룰팩 내장
# =================================================================
AI_ESCAPE_BLOCK = """
AI SCREENPLAY ESCAPE — AI가 반복하는 20가지 실수
━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 아래 20개 패턴이 수정본에 보이면 즉시 다시 써라. 이것이 "AI가 쓴 시나리오"의 정체다. ★

[A1. 감정 설명 지문 — 행동으로 보여줘라]
❌ 지훈은 불안한 마음으로 문 앞에 선다. 두려움이 온몸을 감싼다.
✅ 지훈이 문 앞에 선다. 손잡이를 잡았다 놓았다 한다. 손등에 땀.
→ "불안한 마음"은 카메라에 안 보인다. "잡았다 놓았다"는 보인다.

[A2. 모든 캐릭터가 같은 말투]
❌ "저도 걱정이에요." / "나도 걱정이야." / "걱정되긴 합니다." (전부 같은 구조)
✅ "..." (침묵) / "밥은 먹었어?" (회피) / "그래서 어쩔 건데." (공격)
→ 같은 감정이라도 표현 방식이 달라야 한다. 전술이 캐릭터를 정의한다.

[A3. 방금 본 것을 대사로 반복]
❌ (지문: 수현이 서류를 발견한다) 수현 "이건... 서류야. 수몰 마을 서류."
✅ (지문: 수현이 서류를 발견한다) 수현이 서류를 펼친다. 손이 멈춘다. 지훈을 본다.
→ 관객은 이미 봤다. 설명하지 마라. 반응을 보여줘라.

[A4. 무대 연출 지문]
❌ 지훈이 수현에게로 돌아서서 그녀의 눈을 바라보며 말한다.
✅ 지훈이 수현을 본다.
→ "돌아서서" "그녀의 눈을 바라보며 말한다"는 연출 지시가 아니라 소설이다. 짧게.

[A5. 편의적 정보 전달 대사]
❌ "네가 알다시피, 이 저수지는 20년 전에 마을을 수몰시켜서 만든 거야."
✅ "할머니가 그러셨어. 물 밑에 아직 집들이 있대."
→ 두 사람 다 아는 걸 서로에게 설명하면 안 된다. 제3자의 말을 빌려라.

[A6. 침묵이 없다]
❌ 모든 씬에 대사가 가득. 대사 → 대사 → 대사 → 지문 1줄 → 대사.
✅ 씬 중간에 아무 말 없이 3줄의 행동만. 관객이 침묵의 무게를 느낀다.
→ 대사가 없는 30초가 대사 10줄보다 강할 때가 있다. 침묵을 두려워하지 마라.

[A7. 대사 길이가 대칭]
❌ A가 3문장 → B가 3문장 → A가 3문장 → B가 3문장 (탁구)
✅ A가 1단어 → B가 5문장 → A가 침묵 → B가 1문장
→ 현실 대화는 비대칭이다. 한쪽이 밀어붙이고 한쪽이 물러난다.

[A8. 씬의 처음부터 시작]
❌ S#35. 지훈이 카페에 들어온다. 자리에 앉는다. 메뉴를 본다. 수현이 온다. 인사한다.
✅ S#35. 지훈과 수현. 테이블 위 커피 두 잔. 이미 식었다. 아무도 먼저 말하지 않는다.
→ 이미 진행 중인 상황에 떨어뜨려라 (Drop in the Middle). 도착 과정은 생략.

[A9. 긴장이 같은 씬에서 해소]
❌ 위기 발생 → 같은 씬에서 해결책 발견 → 안도
✅ 위기 발생 → 씬 끝 (해결 안 됨) → 다른 씬 → 돌아왔을 때 더 악화
→ 긴장을 씬 경계 너머로 끌고 가라. 같은 씬에서 닫지 마라.

[A10. 총칭적 감각 묘사]
❌ 바람이 불었다. 차가운 공기가 느껴졌다. 어둠이 깔렸다.
✅ 창문 틈으로 커튼이 빨려 들어간다. 지훈의 목덜미에 소름.
→ "바람이 불었다"는 아무 영화에나 들어간다. "커튼이 빨려 들어간다"는 이 영화에만 있다.

[A11. 물리적 논리의 비약 — 공간·시선·인과]
❌ 소율이 지갑을 연다. 체크카드 잔액 3,200원. 마카롱 한 개 4,500원. 지갑이 닫힌다.
→ 지갑을 열었는데 어떻게 "체크카드 잔액"이 보이는가? 잔액은 폰 앱에서 봐야 한다.
✅ 소율이 지갑을 연다. 지폐칸 비어 있음. 체크카드 한 장.
   소율의 폰 화면, 체크카드 앱. 잔액 3,200원.
   마카롱 판매대의 가격표: 한 개 4,500원.
→ 각 정보가 어디서 왔는지 카메라가 본다. 관찰자 있는 디테일.

[A12. 관찰자 없는 의미 없는 숫자]
❌ 팔로워 321,047명. 체크카드 잔액 3,200원.
→ 관객이 이 숫자를 어디서 보는가?
✅ 소율의 폰 화면 클로즈업 — 팔로워 321,047명.
→ 숫자는 반드시 "보여지는 곳"이 있어야 한다. 지문 = 카메라의 눈.

[A13. 원인 없는 결과 — 인과의 구멍]
❌ 소율이 라운지에 들어선다. 팔로워가 32만이 된다.
✅ 소율이 라운지에 들어선다. 테이블 위 시식 마카롱을 들고 셀카. 업로드.
   몇 초 후, 폰 화면. 팔로워 321,050 → 321,090 → 321,150.
→ A가 일어나고 B가 일어났으면, A→B의 연결 고리(행동/반응)가 보여야 한다.

[A14. 캐릭터 재소개]
이미 등장한 캐릭터는 이름만 써라. 비트가 새로 시작한다고 인물을 다시 소개하지 마라.

[A15. 반복 루프 — 같은 장소·같은 구조의 반복]
❌ S#10 카페 대화 → S#15 카페 대화 → S#20 카페 대화 (같은 공간·같은 구성)
✅ S#10 카페 → S#15 지하철 → S#20 옥상 (공간이 인물의 상태를 반영)
→ 공간이 바뀌면 인물의 심리도 바뀐다. 같은 곳을 반복하지 마라.

[A16. 정보 반복 전달 — 관객이 이미 아는 것]
❌ S#5에서 A가 B에게 설명한 정보를 S#8에서 A가 C에게 또 설명.
✅ S#8에서는 C가 이미 알고 있거나, B로부터 전해 들은 상태로 시작.
→ 관객의 시간을 존중하라. 한 번 전달한 정보는 다시 전달하지 않는다.

[A17. 메타데이터 누출 — 지문에 프롬프트 설명이 남음]
❌ "다음은 감정이 고조되는 장면이다:" / "여기서 주인공의 갈등이 드러난다."
✅ 씬 헤더 + 지문 + 대사로만 구성. 메타 설명 없음.
→ AI가 자기 작업을 설명하는 흔적을 절대 남기지 마라.

[A18. 대사 포맷 오염]
❌ "지훈: 어디 갔었어?" (콜론 사용)
✅ 지훈
   어디 갔었어?
→ 한국 시나리오 표준: 인물명 한 줄, 대사 다음 줄. 콜론·대괄호 금지.

[A19. 장르 톤 붕괴]
❌ 코미디 씬 중간에 갑자기 호러 톤의 묘사가 들어감 ("그림자가 벽을 타고 올라왔다").
✅ 장르 톤을 씬 전체에 일관되게 유지. 톤 전환은 의도적일 때만.
→ 장르 Override를 따라라. 씬 단위 톤 일관성.

[A20. 지문 소설체]
❌ 그는 조용히 고개를 숙였다. 마음속에는 말할 수 없는 슬픔이 가득했다.
✅ 지훈이 고개를 숙인다. 식탁의 반찬들을 보지 않는다.
→ "~했다" 과거형 소설체 금지. "~한다" 현재형 + 외부 관찰 가능한 행동만.
"""

# =================================================================
# [3] 9장르 RULE PACK — Writer Engine 룰팩 내장
# =================================================================
GENRE_RULES = {
    "드라마": {
        "core": "선택과 대가로 진실에 도달하는 구조. 인물의 내면 변화가 플롯보다 앞선다.",
        "must_have": [
            "주인공에게 '돌이킬 수 없는 선택'이 있는가",
            "선택에 대한 '실질적 대가(Loss)'가 발생하는가",
            "관계의 질적 변화가 구체적 장면으로 보이는가",
            "B스토리가 테마를 반사하는가"
        ],
        "fails": [
            "선택 없이 사건만 나열",
            "감정을 대사로 직접 설명 ('나 힘들어')",
            "모든 갈등이 오해에서 발생하고 대화로 해소",
            "테마 없이 에피소드만 나열"
        ],
        "fun": "관객이 인물의 선택 앞에서 '나라면 어떻게 할까'를 고민하게 만드는 것"
    },
    "느와르": {
        "core": "도덕적 모호함. 타락과 생존 사이의 선택. 누구도 깨끗하지 않다.",
        "must_have": [
            "주인공의 도덕선이 점진적으로 무너지는가",
            "배신의 레이어가 2중 이상인가",
            "거래·협박·뒷거래가 서사를 추동하는가",
            "결말에서 '승리'가 아닌 '생존'이 목표인가"
        ],
        "fails": [
            "선악 이분법으로 후퇴",
            "주인공이 끝까지 도덕적 순수함 유지",
            "배신이 한 번만 발생하고 회복 가능",
            "액션으로 도덕 문제 해결"
        ],
        "fun": "관객이 주인공과 함께 '어디까지 타락할 것인가'를 계산하는 것"
    },
    "스릴러": {
        "core": "정보 비대칭과 시간 압박. 관객이 인물보다 많이 알거나 적게 알 때 공포가 생긴다.",
        "must_have": [
            "정보 비대칭(관객 vs 인물)이 작동하는가",
            "데드라인의 구체적 결과(물리적 파괴·인명)가 명시되는가",
            "적대자의 동기와 위협이 구체적인가",
            "에스컬레이션(위기의 단계적 상승)이 있는가"
        ],
        "fails": [
            "전지적 조력자 함정 (정보 부족이 해소되어 서스펜스 소멸)",
            "모호한 빌런 동기",
            "반복 패턴 정체 (같은 난이도 반복)",
            "주인공이 물리적 대가 없이 해결"
        ],
        "fun": "관객의 손에 땀이 나는 것. 주인공이 실패할 수 있다는 공포."
    },
    "범죄/스릴러": {
        "core": "정보 비대칭과 시간 압박. 범죄와 수사의 체스판.",
        "must_have": [
            "정보 비대칭이 작동하는가",
            "데드라인의 구체적 결과가 명시되는가",
            "범인과 수사자 양쪽의 논리가 모두 작동하는가",
            "에스컬레이션이 있는가"
        ],
        "fails": [
            "전지적 수사 (정보가 너무 쉽게 나옴)",
            "범인의 동기 추상",
            "같은 패턴 반복",
            "물리적 대가 없는 해결"
        ],
        "fun": "쫓는 자와 쫓기는 자의 체스. 다음 수를 예측하는 재미."
    },
    "액션": {
        "core": "물리적 대결이 곧 인물의 내면. 액션은 장식이 아닌 서사다.",
        "must_have": [
            "액션의 의도·공간·리듬이 명확한가",
            "주인공이 물리적 대가를 치르는가",
            "액션 후 인물의 상태가 변하는가",
            "적대자와의 물리적 격차가 설득력 있는가"
        ],
        "fails": [
            "액션이 서사와 분리된 스펙터클",
            "주인공이 무적",
            "적대자가 일방적으로 약함",
            "액션 후 아무것도 변하지 않음"
        ],
        "fun": "인물이 몸으로 말하는 것. 한 동작에 10개 대사의 의미."
    },
    "로맨스": {
        "core": "장벽(Barrier)과 오해(Misunderstanding)가 관계를 정의한다. 장벽이 없으면 로맨스가 아니다.",
        "must_have": [
            "외적 장벽(신분·환경·상황)이 명확한가",
            "내적 장벽(두려움·과거·가치관)이 있는가",
            "두 사람의 첫 만남이 특별한 순간인가 (Meet-Cute)",
            "관계의 진전이 구체적 행동으로 보이는가"
        ],
        "fails": [
            "장벽 없이 바로 연결",
            "오해가 한 번 설명으로 해소",
            "감정을 대사로 직접 설명",
            "관계 진전이 몽타주로만 처리"
        ],
        "fun": "심장이 두근거리는 것. '이번에는 닿을까' 하는 기대."
    },
    "로맨틱 코미디": {
        "core": "장벽과 오해에 유머가 더해진다. 웃음과 설렘이 교차한다.",
        "must_have": [
            "Meet-Cute가 있는가",
            "스크루볼 요소(엇갈림·착각·우연)가 있는가",
            "장벽이 코믹하게 작동하는가",
            "해피 엔딩 또는 결합 암시"
        ],
        "fails": [
            "유머 없는 진지한 로맨스",
            "억지 설정",
            "여주·남주 중 한쪽이 납작함",
            "결말이 급작스러움"
        ],
        "fun": "두 사람이 만들어내는 리듬. 대사 한 줄의 엇박."
    },
    "호러": {
        "core": "안전이 무너진다. 집·가족·일상이 위협의 장소가 된다.",
        "must_have": [
            "안전한 공간이 위협받는가",
            "주인공이 도움을 청할 곳이 없는가 (고립)",
            "공포의 정체가 점진적으로 드러나는가",
            "최후의 대가(희생·상실)가 있는가"
        ],
        "fails": [
            "점프 스케어만 반복",
            "공포가 외부에만 있음 (내면화 없음)",
            "쉬운 탈출 경로 존재",
            "공포의 규칙이 일관되지 않음"
        ],
        "fun": "무서운 것. 안전하다고 믿었던 것이 무너지는 것."
    },
    "코미디": {
        "core": "진지한 상황의 진지함을 깨뜨린다. 캐릭터의 결함이 곧 유머다.",
        "must_have": [
            "캐릭터의 결함이 유머의 원천인가",
            "상황의 진지함과 반응의 부적절함이 충돌하는가",
            "유머가 캐릭터를 정의하는가",
            "감정선이 유머 사이에 유지되는가"
        ],
        "fails": [
            "외부 개그에 의존",
            "캐릭터 결함 없이 상황만 웃김",
            "감정선 붕괴",
            "같은 개그 반복"
        ],
        "fun": "웃음. 그리고 웃음 끝에 남는 따뜻함."
    },
    "판타지": {
        "core": "세계의 규칙이 우리 세계와 다르다. 규칙이 일관되면 마법이 설득력을 얻는다.",
        "must_have": [
            "세계의 규칙이 일관된가",
            "규칙에 대가가 있는가 (마법에 비용)",
            "세계 규칙이 인물의 선택을 정의하는가",
            "현실 세계와의 접점이 있는가"
        ],
        "fails": [
            "규칙이 일관되지 않음 (데우스 엑스 마키나)",
            "마법이 비용 없이 사용됨",
            "세계만 있고 드라마가 없음",
            "설정 설명이 과잉"
        ],
        "fun": "다른 세계에 들어가는 것. 규칙을 배우는 즐거움."
    },
    "SF": {
        "core": "과학적 설정이 인간 조건을 변화시킨다. 설정은 곧 질문이다.",
        "must_have": [
            "설정이 인간 조건에 대한 질문인가",
            "기술의 대가·부작용이 드러나는가",
            "주인공의 선택이 설정과 연결되는가",
            "결말이 설정에 대한 답을 제시하는가"
        ],
        "fails": [
            "설정이 장식에 불과",
            "기술의 대가 없음",
            "인간 드라마와 SF 설정 분리",
            "설정 설명이 과잉"
        ],
        "fun": "만약 이랬다면? What If의 질문과 답."
    }
}


def get_genre_rules_block(genre: str) -> str:
    """장르 Rule Pack을 프롬프트 블록으로 변환"""
    genre_key = genre.strip()
    if genre_key not in GENRE_RULES:
        # 퍼지 매칭
        for k in GENRE_RULES:
            if k in genre_key or genre_key in k:
                genre_key = k
                break
        else:
            genre_key = "드라마"

    g = GENRE_RULES[genre_key]
    must_have = "\n".join(f"   - {m}" for m in g["must_have"])
    fails = "\n".join(f"   - {f}" for f in g["fails"])

    return f"""
[장르 RULE PACK — {genre_key}]
핵심 정체성: {g['core']}

필수 요소 (Must Have):
{must_have}

실패 패턴 (Fails to Avoid):
{fails}

장르적 재미: {g['fun']}
"""


# =================================================================
# [4] INTENSITY BLOCK — 수정 강도별 원본 보존율 강제
# =================================================================
INTENSITY_RULES = {
    "CONSERVATIVE": {
        "preserve_ratio": "70%+",
        "description": "원본을 최대한 보존하며 지시사항이 지적한 부분만 국소적으로 수정",
        "instruction": """
[INTENSITY: CONSERVATIVE — 원본 70% 이상 보존]
1. 원본의 대사·지문 중 문제없는 부분은 그대로 유지하라.
2. 지시문이 명시적으로 지적한 부분만 수정하라.
3. 씬의 구조·순서·인물 배치는 건드리지 마라.
4. 수정은 "외과 수술" 수준이어야 한다. 큰 재구성 금지.
5. 원본의 리듬과 톤을 최대한 유지하라.
"""
    },
    "BALANCED": {
        "preserve_ratio": "50%",
        "description": "원본의 핵심은 유지하되, 지시사항에 따라 자연스럽게 재구성",
        "instruction": """
[INTENSITY: BALANCED — 원본 50% 보존, 자연스러운 재구성]
1. 원본의 핵심 요소(인물의 선택·주요 대사 포인트·공간·소품)는 유지하라.
2. 지시사항에 따라 씬 내부의 흐름·대사·지문을 자연스럽게 재구성하라.
3. 원본에 없던 새로운 행동·소품·암시를 추가해도 된다 (단, LOCKED 범위 내).
4. 씬의 위치와 개수는 바꾸지 마라.
5. 수정 후에도 원본 작가의 목소리가 느껴져야 한다.
"""
    },
    "AGGRESSIVE": {
        "preserve_ratio": "20~30%",
        "description": "원본에서 유지할 요소만 남기고 사실상 재집필",
        "instruction": """
[INTENSITY: AGGRESSIVE — 원본 20~30% 유지, 사실상 재집필]
1. LOCKED 요소와 씬의 기본 기능(플롯상 역할)만 유지하라.
2. 대사·지문·구성·리듬은 전면 재집필 가능하다.
3. 원본에 없던 새 요소·소품·암시를 적극 도입하라.
4. 단, 씬 위치와 플롯상 기능은 변경하지 마라.
5. 결과물은 "같은 씬의 완전히 다른 버전"이어야 한다.
"""
    }
}


def get_intensity_block(intensity: str) -> str:
    """Intensity 블록을 프롬프트용으로 변환"""
    key = intensity.strip().upper()
    if key not in INTENSITY_RULES:
        key = "BALANCED"
    return INTENSITY_RULES[key]["instruction"]


# =================================================================
# [4-B] v2.0 — 톤 레퍼런스 분석 (Tone Reference Analysis)
# =================================================================
def build_tone_dna_extraction_prompt(reference_text: str) -> str:
    """손본 시나리오에서 톤 DNA를 자동 추출하는 프롬프트.
    Sonnet 4.6으로 호출 권장."""
    sample = reference_text[:30000] if reference_text else ""
    return f"""
[TASK — TONE DNA EXTRACTION]
다음은 작가가 직접 손본 시나리오의 일부다.
이 시나리오의 "스타일 지문"을 추출하여, 다른 씬을 같은 톤으로 집필할 때 참조할 수 있도록 JSON으로 정리하라.

[손본 시나리오]
━━━━━━━━━━━━━━━━━━━━━━━━
{sample}
━━━━━━━━━━━━━━━━━━━━━━━━

[추출 항목]
1. 지문 (action_lines):
   - 평균 문장 길이 (자수)
   - 시제 (현재형 / 과거형 혼용 여부)
   - 묘사 밀도 (sparse / medium / dense)
   - 감각 디테일 사용 빈도 (소리·냄새·온도)
   - 시간 미시 표기 여부 (예: "0.3초", "0.5초")

2. 대사 (dialogue):
   - 평균 대사 길이 (자수)
   - 단답·침묵 사용 빈도
   - 괄호 지시(parenthetical) 사용 패턴 (예: 자주 / 드물게)
   - 사투리·존댓말·반말의 일관성

3. 씬 구조 (scene_structure):
   - 씬 시작 방식 (Drop in the Middle 패턴 여부)
   - 씬 종료 방식 (Hook/Punch 사용 여부)
   - 평균 씬 길이 (단락 수)
   - 인서트(INSERT) 표기 형식

4. 명명·표기 (naming_conventions):
   - 캐릭터 호칭 (전체이름 vs 줄임형, 예: "이진호" vs "진호")
   - 씬 헤딩 형식 (예: "S#15. INT. 카페 — 낮")
   - 전환 표기 (CUT TO. / DISSOLVE TO. / 없음)
   - 인물 첫 등장 시 나이 표기 ((32) 등)

5. 작가의 시그니처 (signature):
   - 반복적으로 나타나는 묘사 패턴
   - 좋아하는 동사·부사 구조
   - 피하는 표현 (있다면)

[출력 형식 — JSON 단일 객체]
{{
  "tone_dna": {{
    "action_lines": {{
      "avg_length": "정수 (자수)",
      "tense": "current | past_mixed",
      "density": "sparse | medium | dense",
      "sensory_detail_freq": "high | medium | low",
      "micro_time_notation": "true | false",
      "examples": ["대표 예시 1", "대표 예시 2"]
    }},
    "dialogue": {{
      "avg_length": "정수 (자수)",
      "silence_pattern": "frequent | occasional | rare",
      "parenthetical_usage": "frequent | occasional | rare",
      "speech_levels": "설명 (예: '주인공 반말, 조연 존댓말')",
      "examples": ["대표 대사 1", "대표 대사 2"]
    }},
    "scene_structure": {{
      "scene_opening_style": "drop_in_middle | establishment | flexible",
      "scene_closing_style": "hook_punch | cut_simple | flexible",
      "avg_scene_paragraphs": "정수",
      "insert_format": "예: '[인서트 - 핸드폰]' 또는 'INSERT.'"
    }},
    "naming_conventions": {{
      "character_naming": {{
        "전체이름1": "줄임형 또는 전체이름 그대로",
        "전체이름2": "줄임형"
      }},
      "scene_heading_format": "예: 'S#{{n}}. INT./EXT. {{location}} — {{time}}'",
      "transition_markers": "예: 'CUT TO.' 사용 | 미사용",
      "first_appearance_age": "true | false"
    }},
    "signature_patterns": [
      "예: '미시 시간 표기 자주 사용 (0.3초)'",
      "예: '인서트로 정보 전달'"
    ],
    "summary": "작가 톤을 한 문단으로 요약 (3~5문장)"
  }}
}}

JSON만 출력하라. 설명 금지.
""".strip()


def build_diff_analysis_prompt(original_text: str, refined_text: str) -> str:
    """원본 vs 손본본을 비교해 작가의 편집 패턴을 학습하는 프롬프트.
    Sonnet 4.6으로 호출 권장."""
    orig_sample = original_text[:25000] if original_text else ""
    refined_sample = refined_text[:25000] if refined_text else ""
    return f"""
[TASK — DIFF ANALYSIS / EDITING PATTERN LEARNING]
원본 시나리오와 작가가 손본 후의 시나리오 두 개가 주어진다.
두 버전을 비교해 작가가 어떻게 편집했는지 패턴을 추출하라.
이 패턴은 다음 각색 작업의 가이드로 사용된다.

[원본 시나리오]
━━━━━━━━━━━━━━━━━━━━━━━━
{orig_sample}
━━━━━━━━━━━━━━━━━━━━━━━━

[작가 손본본]
━━━━━━━━━━━━━━━━━━━━━━━━
{refined_sample}
━━━━━━━━━━━━━━━━━━━━━━━━

[분석 항목]
1. 삭제된 씬(deletion_pattern): 어떤 종류의 씬을 삭제했는가
   (예: 조력자 캐릭터의 본선 사건 없는 씬, 정보 반복 씬, 감정 설명 씬)
2. 압축된 씬(compression_pattern): 길이가 줄어든 씬의 특징
3. 통합된 씬(merging_pattern): 두 씬을 하나로 합친 사례
4. 대사 변화(dialogue_changes): 어떤 대사 패턴을 선호·기피하는가
5. 지문 변화(action_changes): 어떤 묘사 방식을 선호·기피하는가
6. 명명 통일(naming_changes): 호칭이나 표기를 어떻게 통일했는가
7. 캐릭터 다루기(character_handling): 특정 캐릭터의 등장 빈도가 어떻게 변했는가
8. 작가의 편집 철학(editing_philosophy): 위 모든 변화에서 도출되는 일관된 원칙

[출력 형식 — JSON 단일 객체]
{{
  "diff_analysis": {{
    "deletion_pattern": {{
      "summary": "어떤 종류의 씬을 삭제했는지 1~2줄",
      "examples": ["원본 S#15 (다은 캐묻기) 삭제 — 본선 사건 부족", "..."]
    }},
    "compression_pattern": {{
      "summary": "길이를 어떻게 줄였는지",
      "average_reduction": "예: '평균 30% 단축'",
      "examples": ["..."]
    }},
    "merging_pattern": {{
      "summary": "씬을 어떻게 합쳤는지",
      "examples": ["원본 S#63+S#65 → 손본 S#63 (시간 흐름 통일)"]
    }},
    "dialogue_changes": {{
      "preferred": ["대표가 선호하는 대사 패턴 (단답, 침묵, 행동 동반 등)"],
      "removed": ["제거하는 대사 패턴 (설명적 대사, 감정 직접 토로 등)"]
    }},
    "action_changes": {{
      "preferred": ["선호하는 지문 스타일"],
      "removed": ["제거하는 지문 스타일"]
    }},
    "naming_changes": {{
      "examples": ["반세웅 → 세웅 (줄임형 통일)"]
    }},
    "character_handling": {{
      "summary": "캐릭터별 등장 변화",
      "details": ["다은: 등장 빈도 25% → 8% (조력자 등장 최소화)"]
    }},
    "editing_philosophy": [
      "원칙 1: 본선 사건 없는 보조 씬은 삭제",
      "원칙 2: 정보 전달 대사보다 행동·인서트로 표현",
      "원칙 3: 호칭은 줄임형으로 통일"
    ],
    "summary": "작가의 편집 철학 한 문단 요약"
  }}
}}

JSON만 출력하라. 설명 금지.
""".strip()


def build_distribution_diagnostic_prompt(raw_text: str, genre: str) -> str:
    """장르 메트릭 + 캐릭터 등장 분포를 측정하는 프롬프트.
    Sonnet 4.6으로 호출 권장."""
    sample = raw_text[:60000] if raw_text else ""
    genre_metrics_block = ""
    g = genre.lower()
    if "로맨틱" in genre or "코미디" in g:
        genre_metrics_block = """
[로맨틱 코미디 / 코미디 메트릭]
- 코믹 폭발 포인트 개수 (씬 단위)
- 비트당 평균 코믹 포인트 (1회 이상 권장)
- Misdirection 패턴 횟수 (작품당 3회 이상 권장)
- 두 주인공의 케미 씬 비율 (전체 대비 %)
- Comic Specificity (구체적 숫자·사물) 사용 횟수"""
    elif "스릴러" in genre or "범죄" in genre:
        genre_metrics_block = """
[스릴러 / 범죄 메트릭]
- 정보 비대칭 씬 개수 (관객이 인물보다 많이 또는 적게 아는 씬)
- 비트당 정보 비대칭 평균 (1회 이상 권장)
- 데드라인·타이머 가시화 횟수
- Setpiece 긴장 시퀀스 개수 (3개 이상 권장)
- 빌런 동기 구체성 (구체적 / 추상적)"""
    elif "호러" in genre:
        genre_metrics_block = """
[호러 메트릭]
- 일상 균열 포인트 (소리·온도·냄새 변화)
- Mystery Box 유지 여부
- 신체적 불편함 디테일 횟수 (5회 이상 권장)
- 안전한 공간 위협 사례
- 고립 장면 비율"""
    elif "액션" in genre:
        genre_metrics_block = """
[액션 메트릭]
- Setpiece 액션 시퀀스 개수
- 물리적 위협 가시화 횟수
- 주인공 대가 (부상·손실) 사례
- 공간 활용 다양성"""
    else:  # 드라마 등
        genre_metrics_block = """
[드라마 메트릭]
- 침묵 비트 개수
- 결정의 순간 (3초 이상 망설임) 배치
- 관계 변화 가시화 사례
- B스토리 테마 반사 사례"""

    return f"""
[TASK — DISTRIBUTION DIAGNOSTIC]
시나리오 전체에 대해 (1) 장르 메트릭 분포 (2) 캐릭터 등장 분포를 측정하라.
이 측정 결과는 진단 단계에서 자동으로 priority 격상에 사용된다.

[시나리오]
━━━━━━━━━━━━━━━━━━━━━━━━
{sample}
━━━━━━━━━━━━━━━━━━━━━━━━

[장르: {genre}]
{genre_metrics_block}

[캐릭터 분포 측정 항목]
1. 각 캐릭터의 등장 씬 번호 리스트
2. 등장 빈도 (전체 씬 대비 %)
3. 5씬 이상 연속 등장 구간
4. 첫 등장 씬 번호 (조력자가 너무 빨리 등장하는지)
5. 마지막 등장 씬 번호
6. "본선 사건 없는 등장" 비율 (해당 캐릭터가 단순 반응만 하는 씬 / 전체 등장 씬)

[자동 권장 격상 기준]
- 장르 메트릭 미달 씬 → priority HIGH로 격상 권장
- 캐릭터 분포 이슈 (조력자 과다 등장, 본선 없는 등장) → 해당 씬 priority HIGH 권장

[출력 형식 — JSON 단일 객체]
{{
  "distribution_diagnostic": {{
    "genre_metrics": {{
      "metric_summary": "측정 요약 1~2줄",
      "scores": {{
        "metric_name_1": "측정값 / 권장값",
        "metric_name_2": "측정값 / 권장값"
      }},
      "weak_zones": [
        {{
          "scene_range": "예: S#10~S#15",
          "issue": "코믹 폭발 부족 (5개 씬 중 0회)",
          "fix_direction": "단답형 코믹 대사 추가 또는 Misdirection 도입"
        }}
      ]
    }},
    "character_distribution": {{
      "characters": [
        {{
          "name": "캐릭터명",
          "first_scene": "S#1",
          "last_scene": "S#86",
          "total_appearances": "정수",
          "ratio": "전체 대비 %",
          "consecutive_overuse": ["S#23~S#28 6연속" 또는 빈 배열],
          "reactive_only_ratio": "본선 사건 없는 등장 비율 %",
          "issues": ["문제점 짧게"]
        }}
      ],
      "concerning_patterns": [
        {{
          "pattern": "조력자 다은 — 본선 사건 누적 전 등장",
          "scenes_to_review": ["S#15", "S#23"],
          "recommended_action": "삭제 또는 본선 사건 후로 이동"
        }}
      ]
    }},
    "auto_priority_upgrades": [
      {{
        "scene_id": "S#15",
        "from_priority": "MEDIUM",
        "to_priority": "HIGH",
        "reason": "캐릭터 분포 + 장르 메트릭 양쪽 위반"
      }}
    ],
    "summary": "전체 진단 한 문단 요약"
  }}
}}

JSON만 출력하라. 설명 금지.
""".strip()


def absorb_rewrite_engine_metadata(rewrite_json) -> dict:
    """Rewrite Engine JSON에서 메타데이터를 구조화 추출.
    parse_rewrite_engine_json은 텍스트 변환만 했지만,
    이 함수는 priority 격상·preserve_note 등 자동 적용 데이터를 반환."""
    import json as _json

    if isinstance(rewrite_json, str):
        try:
            data = _json.loads(rewrite_json)
        except (_json.JSONDecodeError, TypeError):
            return {}
    elif isinstance(rewrite_json, dict):
        data = rewrite_json
    else:
        return {}

    chris = data.get("chris_analysis") or data
    shiho = data.get("shiho_prescription") or data

    metadata = {
        "preserve_notes_by_seq": {},   # {seq: preserve_note}
        "weak_zone_scenes": [],        # [{seq_ref, hook, punch}, ...]
        "opening_diagnosis": {},
        "auto_priority_high": [],      # 격상 대상 씬 리스트
    }

    # washing_table → preserve_notes
    wt = shiho.get("washing_table", []) if isinstance(shiho, dict) else []
    for entry in wt:
        if not isinstance(entry, dict):
            continue
        seq = entry.get("seq") or entry.get("sequence", "")
        preserve = entry.get("preserve_note") or entry.get("preserve", "")
        if seq and preserve:
            metadata["preserve_notes_by_seq"][seq] = preserve

    # genre_fun_recovery → weak zones
    gfr = shiho.get("genre_fun_recovery", {}) if isinstance(shiho, dict) else {}
    weak_zones = gfr.get("weak_zones", []) if isinstance(gfr, dict) else []
    for zone in weak_zones:
        if not isinstance(zone, dict):
            continue
        metadata["weak_zone_scenes"].append({
            "seq_ref": zone.get("seq_ref", ""),
            "hook_suggestion": zone.get("hook_suggestion", ""),
            "punch_suggestion": zone.get("punch_suggestion", ""),
        })
        # 시퀀스 ref → 자동 priority HIGH
        if zone.get("seq_ref"):
            metadata["auto_priority_high"].append(zone["seq_ref"])

    # opening_diagnosis
    if isinstance(chris, dict):
        od = chris.get("opening_diagnosis", {})
        if od:
            metadata["opening_diagnosis"] = od

    return metadata


def build_v2_diagnose_context_block(
    tone_dna: dict = None,
    diff_analysis: dict = None,
    distribution_diagnostic: dict = None,
    rewrite_metadata: dict = None
) -> str:
    """v2.0 자동 분석 결과들을 DIAGNOSE 프롬프트에 주입할 단일 블록으로 통합."""
    import json as _json
    parts = []

    if tone_dna:
        td = tone_dna.get("tone_dna", tone_dna)
        parts.append(f"""
[v2.0 — 톤 레퍼런스 DNA (자동 추출)]
━━━━━━━━━━━━━━━━━━━━━━━━
{_json.dumps(td, ensure_ascii=False, indent=2)}
━━━━━━━━━━━━━━━━━━━━━━━━
※ 모든 수정·추가 씬은 위 톤 DNA를 따라야 한다. 이는 작가가 이미 손본 시나리오에서 추출된 작가 고유의 스타일이다.""")

    if diff_analysis:
        da = diff_analysis.get("diff_analysis", diff_analysis)
        philosophy = da.get("editing_philosophy", [])
        philosophy_str = "\n".join(f"  - {p}" for p in philosophy)
        parts.append(f"""
[v2.0 — 작가 편집 패턴 (Diff 학습)]
━━━━━━━━━━━━━━━━━━━━━━━━
{_json.dumps(da, ensure_ascii=False, indent=2)[:3000]}
━━━━━━━━━━━━━━━━━━━━━━━━
※ 작가의 편집 철학:
{philosophy_str}
※ 위 철학을 따라 진단·집필하라. 작가가 일관되게 제거한 패턴을 다시 만들지 마라.""")

    if distribution_diagnostic:
        dd = distribution_diagnostic.get("distribution_diagnostic", distribution_diagnostic)
        upgrades = dd.get("auto_priority_upgrades", [])
        upgrades_str = "\n".join(
            f"  - {u.get('scene_id','')}: {u.get('from_priority','')} → {u.get('to_priority','')} ({u.get('reason','')})"
            for u in upgrades
        )
        parts.append(f"""
[v2.0 — 분포 진단 (장르 메트릭 + 캐릭터 분포)]
━━━━━━━━━━━━━━━━━━━━━━━━
{_json.dumps(dd, ensure_ascii=False, indent=2)[:3000]}
━━━━━━━━━━━━━━━━━━━━━━━━
※ 자동 권장 priority 격상:
{upgrades_str if upgrades_str else '  (없음)'}
※ 위 격상 권장을 target_scenes의 priority에 반영하라.""")

    if rewrite_metadata:
        preserve = rewrite_metadata.get("preserve_notes_by_seq", {})
        weak = rewrite_metadata.get("weak_zone_scenes", [])
        auto_high = rewrite_metadata.get("auto_priority_high", [])
        if preserve or weak or auto_high:
            parts.append(f"""
[v2.0 — Rewrite Engine 메타 흡수]
━━━━━━━━━━━━━━━━━━━━━━━━
preserve_notes (시퀀스별 유지 요소):
{_json.dumps(preserve, ensure_ascii=False, indent=2)[:1500]}

genre_fun_recovery weak_zones (자동 priority HIGH 격상):
{_json.dumps(weak, ensure_ascii=False, indent=2)[:1500]}

자동 격상 시퀀스: {auto_high}
━━━━━━━━━━━━━━━━━━━━━━━━
※ preserve_notes를 해당 씬의 preservation_notes에 자동 매핑.
※ weak_zones에 속한 씬은 priority HIGH로 자동 격상.""")

    if not parts:
        return ""
    return "\n".join(parts)


# =================================================================
# [5] STAGE 1 — DIAGNOSE (지시 해석 + 수정 플랜 생성)
# =================================================================
def build_diagnose_prompt(
    raw_text: str,
    instruction: str,
    locked: str,
    genre: str,
    intensity: str,
    profession_input: str = "",
    period_key: str = "",
    historical_type: str = "",
    fact_based: bool = False,
    tone_dna: dict = None,
    diff_analysis: dict = None,
    distribution_diagnostic: dict = None,
    rewrite_metadata: dict = None
) -> str:
    """Stage 1: 원본 + 지시문 + LOCKED를 분석해 수정 플랜(JSON)을 생성.
    Sonnet 4.6 사용 권장 (구조 분석).

    profession_input: 주요 캐릭터의 직업 (선택사항).
    period_key: 시대 키 (조선_전기 등). 빈 문자열이면 현대로 간주.
    historical_type: 정통/팩션/퓨전 (period_key 있을 때만 의미 있음).
    fact_based: 실화 기반 작품 여부.

    [v2.0 신규]
    tone_dna: 톤 DNA 추출 결과 (build_tone_dna_extraction_prompt 결과).
    diff_analysis: Diff 학습 결과 (build_diff_analysis_prompt 결과).
    distribution_diagnostic: 분포 진단 결과 (build_distribution_diagnostic_prompt 결과).
    rewrite_metadata: Rewrite Engine 메타 (absorb_rewrite_engine_metadata 결과).
    """

    genre_block = get_genre_rules_block(genre)
    locked_text = locked.strip() if locked.strip() else "(명시된 LOCKED 요소 없음 — 기본 원칙 적용: 플롯의 큰 흐름·핵심 반전·엔딩은 유지)"

    # 직업 전문성 블록 (감지 실패 시 빈 문자열)
    profession_block = build_profession_context(profession_input, raw_text)
    profession_section = ""
    if profession_block:
        profession_section = f"""

[직업 전문성 참고 블록]
━━━━━━━━━━━━━━━━━━━━━━━━
{profession_block}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 진단 시 이 블록을 참고하여, 지시문이 지적하는 "직업답지 않음" 문제를 구체화하라.
  (예: "쇼핑 호스트답지 않다" → forbidden 목록에서 위반 항목 특정)"""

    # 시대 블록 (period_key 있으면 주입)
    period_section = ""
    if period_key and period_key != "(현대)" and PERIOD_PACK_AVAILABLE:
        pblock = _build_period_block(period_keys=[period_key], locked_text=locked)
        if pblock:
            period_section = f"""

[시대 고증 참고 블록 — {_get_period_label(period_key)}]
━━━━━━━━━━━━━━━━━━━━━━━━
{pblock}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 진단 시 이 시대의 복식·관직·언어·사건 고증과 충돌하는 부분을 식별하라."""

    # 역사영화 유형 블록
    historical_section = ""
    if period_key and period_key != "(현대)" and historical_type and WRITER_MODULES_AVAILABLE:
        hblock = _get_historical_film_rules(True, historical_type)
        if hblock:
            historical_section = f"""

[역사영화 유형 — {historical_type}]
━━━━━━━━━━━━━━━━━━━━━━━━
{hblock}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    # 실화 기반 블록
    fact_section = ""
    if fact_based and WRITER_MODULES_AVAILABLE:
        fblock = _get_fact_based_rules(True)
        if fblock:
            fact_section = f"""

[실화 기반 작품 — 명예훼손·인격권 가이드]
━━━━━━━━━━━━━━━━━━━━━━━━
{fblock}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 진단 시 실명 사용·특정 가능 디테일·실존 공인 악역화 등 리스크를 식별하라."""

    # v2.0 자동 분석 결과 통합 블록
    v2_context_section = build_v2_diagnose_context_block(
        tone_dna=tone_dna,
        diff_analysis=diff_analysis,
        distribution_diagnostic=distribution_diagnostic,
        rewrite_metadata=rewrite_metadata,
    )

    return f"""
[TASK — Stage 1: DIAGNOSE]
원본 시나리오와 수정 지시문을 분석하여, 실제 수정 작업을 위한 "수정 플랜(Revision Plan)"을 JSON으로 생성하라.
이 단계는 집필이 아니다. 어디를, 왜, 어떻게 수정할 것인지의 "지도"를 그리는 단계다.

[원본 시나리오]
━━━━━━━━━━━━━━━━━━━━━━━━
{raw_text}
━━━━━━━━━━━━━━━━━━━━━━━━

[수정 지시문]
━━━━━━━━━━━━━━━━━━━━━━━━
{instruction}
━━━━━━━━━━━━━━━━━━━━━━━━

[LOCKED — 절대 건드리지 않을 요소]
━━━━━━━━━━━━━━━━━━━━━━━━
{locked_text}
━━━━━━━━━━━━━━━━━━━━━━━━
{profession_section}
{period_section}
{historical_section}
{fact_section}
{v2_context_section}

{genre_block}

{get_intensity_block(intensity)}

[분석 원칙]
1. 지시문을 개별 수정 항목으로 분해하라. 한 지시문 안에 여러 요구가 있을 수 있다.
2. 각 수정 항목이 어느 씬(들)에 영향을 주는지 특정하라. 씬 번호 또는 씬 위치로.
3. LOCKED와 지시문이 충돌하면 LOCKED가 우선한다. 충돌 지점을 명시하라.
4. 지시문이 모호하면 가장 보수적 해석을 취하라.
5. 장르 RULE PACK에 비춰 추가로 개선해야 할 부분이 있으면 "auto_detected"로 표시하라.
6. 각 수정 씬에 대해 우선순위(priority)와 작업 종류(type)를 반드시 분류하라.
7. 배치 추천(batch_recommended)을 부여하여 효율적 집필 순서를 제안하라.

[Priority 분류 기준]
- HIGH:   핵심 플롯·결말·반전·주요 캐릭터 정체성 관련. 이 씬을 잘못 쓰면 작품 전체가 흔들린다.
- MEDIUM: 캐릭터 보이스·관계선·서브플롯·장르 톤 관련. 작품의 인상을 결정한다.
- LOW:    디테일·페이스 조절·소품·미세 다듬기. 있으면 좋고 없어도 큰 무리는 없다.

[Type 분류 기준]
- REWRITE: 기존 씬의 전체 또는 일부를 다시 쓴다 (가장 일반적).
- ADD:     새로운 씬을 추가한다. insert_after에 위치 명시. context_before/after 필수.
- DELETE:  기존 씬을 삭제한다. revised_content 없음, 사유만 명시.
- MERGE:   2개 이상 씬을 하나로 합친다. merge_with에 합칠 씬 ID 명시.
- SPLIT:   1개 씬을 2개로 나눈다. split_into 개수 명시.

[Batch 추천 기준]
- 한 배치당 5~7개 씬을 권장 (너무 많으면 품질·토큰 한계).
- 배치 1: 모든 HIGH 우선순위 씬.
- 배치 2: HIGH 잔여 + MEDIUM 시작.
- 배치 3 이후: MEDIUM 잔여 → LOW 순.
- 같은 배치 안에서는 가능한 한 시간순(원본 순서)으로 정렬.
- 추천 배치 수 = 전체 수정 씬 ÷ 6, 올림.

[출력 형식 — JSON 단일 객체]
{{
  "revision_plan": {{
    "summary": "전체 수정 방향을 3~5줄로 요약",
    "locked_summary": "LOCKED로 인식된 요소 나열",
    "conflicts": [
      {{
        "instruction_item": "지시문에서 인용된 부분",
        "locked_conflict": "LOCKED 중 어느 항목과 충돌하는지",
        "resolution": "어떻게 해결할 것인지 (일반적으로 LOCKED 우선)"
      }}
    ],
    "target_scenes": [
      {{
        "scene_id": "씬 번호 또는 씬 헤더 (예: S#35 INT. 카페 - 낮)",
        "scene_position": "원본에서의 위치 (예: 2막 중반)",
        "original_function": "이 씬의 플롯상 기능",
        "priority": "HIGH | MEDIUM | LOW",
        "type": "REWRITE | ADD | DELETE | MERGE | SPLIT",
        "batch_recommended": 1,
        "insert_after": "ADD일 때 어느 씬 뒤에 삽입 (없으면 빈 문자열)",
        "context_before": "ADD일 때 앞 씬의 내용 요약 1~2줄 (없으면 빈 문자열)",
        "context_after": "ADD일 때 뒤 씬의 내용 요약 1~2줄 (없으면 빈 문자열)",
        "merge_with": "MERGE일 때 합칠 씬 ID 리스트 (없으면 빈 배열)",
        "split_into": "SPLIT일 때 나눌 개수 (없으면 0)",
        "revision_items": [
          {{
            "source": "user_instruction | auto_detected",
            "issue": "수정이 필요한 이유 (지시문 인용 또는 장르 진단)",
            "target_element": "dialogue | action_line | structure | character_voice | pacing",
            "proposed_direction": "어떻게 수정할 것인지 (아직 집필 아님, 방향만)"
          }}
        ],
        "preservation_notes": "이 씬에서 반드시 유지해야 할 요소 (LOCKED + 원본 강점)"
      }}
    ],
    "out_of_scope": [
      "지시문이 요구했지만 LOCKED 또는 Scope 제약으로 처리 불가한 항목 설명"
    ],
    "confidence": 0-10,
    "estimated_scene_count": "수정 대상 씬 개수",
    "total_scenes": "수정 대상 씬 총 개수 (정수)",
    "recommended_batches": "권장 배치 수 (정수, 보통 4~6)",
    "batch_strategy": "배치 전략을 1~2줄로 설명 (예: '배치 1~2는 결말부 핵심 씬, 배치 3~4는 캐릭터 보이스, 배치 5는 디테일')"
  }}
}}

JSON만 출력하라. 설명·주석·마크다운 금지.
""".strip()


# =================================================================
# [6] STAGE 2 — REVISE (실제 집필)
# =================================================================
def build_revise_prompt(
    raw_text: str,
    diagnose_result: dict,
    genre: str,
    intensity: str,
    locked: str,
    profession_input: str = "",
    period_key: str = "",
    historical_type: str = "",
    fact_based: bool = False,
    batch_scenes: list = None,
    batch_index: int = 0,
    total_batches: int = 0,
    tone_dna: dict = None,
    diff_analysis: dict = None
) -> str:
    """Stage 2: Stage 1의 수정 플랜에 따라 실제 수정본을 집필.
    Opus 4.6 사용 필수 (집필).

    profession_input: 주요 캐릭터의 직업 (선택사항).
    period_key: 시대 키 (조선_전기 등). 빈 문자열이면 현대로 간주.
    historical_type: 정통/팩션/퓨전.
    fact_based: 실화 기반 작품 여부.
    batch_scenes: 이번 배치에서 집필할 씬들 (target_scenes의 부분집합).
                  None이면 전체 씬 (구버전 호환).
    batch_index: 현재 배치 번호 (1부터).
    total_batches: 전체 배치 수.
    """

    import json as _json

    genre_block = get_genre_rules_block(genre)
    locked_text = locked.strip() if locked.strip() else "(명시된 LOCKED 요소 없음)"

    # 배치 모드면 배치 씬만, 아니면 전체 플랜 사용
    if batch_scenes is not None:
        # 배치 모드 — 이번 배치에서 처리할 씬만 따로 추출
        batch_plan = {
            "revision_plan": {
                "summary": diagnose_result.get("revision_plan", {}).get("summary", ""),
                "locked_summary": diagnose_result.get("revision_plan", {}).get("locked_summary", ""),
                "conflicts": diagnose_result.get("revision_plan", {}).get("conflicts", []),
                "target_scenes": batch_scenes,
                "batch_info": {
                    "current_batch": batch_index,
                    "total_batches": total_batches,
                    "scenes_in_this_batch": len(batch_scenes)
                }
            }
        }
        plan_json = _json.dumps(batch_plan, ensure_ascii=False, indent=2)
        batch_header = f"""
[배치 진행 상황]
━━━━━━━━━━━━━━━━━━━━━━━━
현재 배치: {batch_index} / {total_batches}
이번 배치에서 집필할 씬: {len(batch_scenes)}개
━━━━━━━━━━━━━━━━━━━━━━━━

※ 이번 배치의 씬들에만 집중하라. 다른 배치의 씬들은 다른 호출에서 처리된다.
  단, 다른 배치 씬과 연결되는 부분은 자연스럽게 이어지도록 주의하라."""
    else:
        # 전체 모드 (구버전 호환)
        plan_json = _json.dumps(diagnose_result, ensure_ascii=False, indent=2)
        batch_header = ""

    # 직업 전문성 블록 (감지 실패 시 빈 문자열)
    profession_block = build_profession_context(profession_input, raw_text)
    profession_section = ""
    if profession_block:
        profession_section = f"""

[직업 전문성 블록 — 집필 시 필수 참조]
━━━━━━━━━━━━━━━━━━━━━━━━
{profession_block}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 위 직업 블록의 공간 디테일·전문 용어·금지 사항을 씬 집필에 반드시 녹여내라.
  특히 [금지 사항]을 절대 위반하지 마라 (작가가 흔히 범하는 오류 방지).
  단, 전문 용어를 전체 나열하지 말고 장면·대사에 필요한 1~2개만 선별 응용할 것."""

    # 시대 블록 (사극·시대극)
    period_section = ""
    if period_key and period_key != "(현대)" and PERIOD_PACK_AVAILABLE:
        pblock = _build_period_block(period_keys=[period_key], locked_text=locked)
        if pblock:
            period_section = f"""

[시대 고증 블록 — {_get_period_label(period_key)}]
━━━━━━━━━━━━━━━━━━━━━━━━
{pblock}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 시대 복식·관직·언어·생활상·사건 고증을 집필에 반영하라.
  현대어와 사극체의 균형을 잡되, 시대감 있는 디테일을 씬마다 녹여라."""

    # 역사영화 유형 블록 (정통/팩션/퓨전)
    historical_section = ""
    if period_key and period_key != "(현대)" and historical_type and WRITER_MODULES_AVAILABLE:
        hblock = _get_historical_film_rules(True, historical_type)
        if hblock:
            historical_section = f"""

[역사영화 유형 블록 — {historical_type}]
━━━━━━━━━━━━━━━━━━━━━━━━
{hblock}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    # 실화 기반 블록
    fact_section = ""
    if fact_based and WRITER_MODULES_AVAILABLE:
        fblock = _get_fact_based_rules(True)
        if fblock:
            fact_section = f"""

[실화 기반 작품 — 명예훼손·인격권 가이드]
━━━━━━━━━━━━━━━━━━━━━━━━
{fblock}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    # 장르 Override 블록 (씬 단위 디테일)
    genre_override_section = ""
    if WRITER_MODULES_AVAILABLE:
        gblock = _get_genre_override(genre)
        if gblock:
            genre_override_section = f"""

[장르 OVERRIDE — {genre} 특화 규칙]
━━━━━━━━━━━━━━━━━━━━━━━━
{gblock}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    # 장르 Enforcement (매 씬 강제 체크)
    genre_enforce_section = ""
    if WRITER_MODULES_AVAILABLE:
        eblock = _get_genre_enforcement(genre)
        if eblock:
            genre_enforce_section = f"""

[장르 ENFORCEMENT — 매 씬 강제 체크리스트]
━━━━━━━━━━━━━━━━━━━━━━━━
{eblock}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 각 수정 씬을 완성한 뒤 위 체크리스트로 자가 점검하라. 통과하지 못하면 다시 써라."""

    # v2.0 — 톤 DNA + Diff 분석 강제 주입 블록 (집필용 강도 강화)
    v2_tone_section = ""
    if tone_dna or diff_analysis:
        import json as _json2
        td_block = ""
        if tone_dna:
            td = tone_dna.get("tone_dna", tone_dna)
            td_block = f"""

[★ v2.0 — 작가 톤 DNA (집필 시 절대 준수) ★]
━━━━━━━━━━━━━━━━━━━━━━━━
{_json2.dumps(td, ensure_ascii=False, indent=2)}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 위 톤 DNA는 작가가 직접 손본 시나리오에서 추출한 작가 고유의 스타일이다.
※ 모든 수정·추가 씬은 위 톤 DNA를 따라야 한다. 다음을 엄격히 준수:
   - action_lines.avg_length를 평균값으로 유지 (±20% 이내)
   - dialogue.avg_length를 평균값으로 유지
   - micro_time_notation이 true면 "0.3초", "0.5초" 같은 미시 시간 표기 적극 사용
   - parenthetical_usage 빈도를 그대로 유지
   - naming_conventions의 character_naming을 그대로 적용 (예: "이진호" 대신 "진호")
   - signature_patterns에 명시된 작가 시그니처 반복 사용
※ 위 톤에서 벗어난 부분은 = 톤 불일치 = 자동 재집필 대상."""

        df_block = ""
        if diff_analysis:
            da = diff_analysis.get("diff_analysis", diff_analysis)
            philosophy = da.get("editing_philosophy", [])
            philosophy_str = "\n".join(f"   - {p}" for p in philosophy)
            preferred_dialogue = da.get("dialogue_changes", {}).get("preferred", [])
            removed_dialogue = da.get("dialogue_changes", {}).get("removed", [])
            preferred_action = da.get("action_changes", {}).get("preferred", [])
            removed_action = da.get("action_changes", {}).get("removed", [])

            df_block = f"""

[★ v2.0 — 작가 편집 패턴 (Diff 학습) ★]
━━━━━━━━━━━━━━━━━━━━━━━━
편집 철학:
{philosophy_str}

선호하는 대사 패턴: {preferred_dialogue}
제거하는 대사 패턴: {removed_dialogue}

선호하는 지문 패턴: {preferred_action}
제거하는 지문 패턴: {removed_action}
━━━━━━━━━━━━━━━━━━━━━━━━

※ 작가가 "제거하는 패턴"을 다시 만들면 안 된다.
※ 작가가 "선호하는 패턴"을 적극 사용하라.
※ 편집 철학을 모든 씬에 일관되게 적용하라."""

        v2_tone_section = td_block + df_block

    return f"""
[TASK — Stage 2: REVISE]
Stage 1에서 생성된 수정 플랜에 따라, 원본 시나리오의 지정된 씬들을 실제로 다시 써라.
이 단계는 집필이다. 실제 작업에 즉시 투입 가능한 수정본을 생성해야 한다.
{batch_header}

[원본 시나리오]
━━━━━━━━━━━━━━━━━━━━━━━━
{raw_text}
━━━━━━━━━━━━━━━━━━━━━━━━

[Stage 1 수정 플랜]
━━━━━━━━━━━━━━━━━━━━━━━━
{plan_json}
━━━━━━━━━━━━━━━━━━━━━━━━

[LOCKED — 절대 건드리지 않을 요소]
━━━━━━━━━━━━━━━━━━━━━━━━
{locked_text}
━━━━━━━━━━━━━━━━━━━━━━━━
{v2_tone_section}
{profession_section}
{period_section}
{historical_section}
{fact_section}

{genre_block}
{genre_override_section}

{get_intensity_block(intensity)}

{AI_ESCAPE_BLOCK}
{genre_enforce_section}

[집필 원칙]
1. Stage 1의 target_scenes 각 항목에 대해 수정된 씬 전문(全文)을 작성하라.
2. preservation_notes에 명시된 요소는 반드시 유지하라. 단어·소품·동선까지.
3. revision_items의 proposed_direction을 실제 대사와 지문으로 구현하라.
4. LOCKED와 충돌하면 LOCKED를 우선하고, conflicts에 기록된 해결 방향을 따르라.
5. Intensity가 정한 보존 비율을 엄격히 지키라.
6. 장르 RULE PACK의 must_have를 충족하고 fails를 피하라.
7. AI SCREENPLAY ESCAPE A1~A20 패턴이 출력에 나타나면 즉시 다시 쓰라.
8. 직업 전문성 블록이 주입된 경우, 해당 직업의 공간 디테일·전문 용어·금지 사항을 준수하라.
9. 시대 블록이 주입된 경우, 복식·관직·언어·생활상 고증을 반영하라.
10. 역사영화 유형 블록이 주입된 경우, 정통/팩션/퓨전 각 유형의 톤을 일관되게 유지하라.
11. 실화 기반 블록이 주입된 경우, 실명 사용·특정 가능 디테일을 반드시 회피하라.
12. 장르 ENFORCEMENT 체크리스트가 주입된 경우, 모든 수정 씬이 통과해야 한다.

[Type별 처리 방법]
13. type="REWRITE": 기존 씬 전문을 다시 쓴다. revised_content에 전체 씬 본문.
14. type="ADD": 새 씬을 만든다.
    - insert_after에 명시된 씬 다음 위치에 삽입됨
    - context_before/context_after를 참고해 자연스럽게 연결
    - revised_content에 새 씬 전문
    - scene_header는 (NEW) 표기 후 위치 명시 (예: "(NEW) S#42-1 INT. 진호의 회상 — 밤")
15. type="DELETE": 기존 씬을 삭제한다.
    - revised_content는 빈 문자열
    - revision_notes.what_changed에 "삭제 사유: ..." 명시
    - 삭제로 인한 플롯 영향을 cross_scene_impact에 기록
16. type="MERGE": 여러 씬을 하나로 합친다.
    - revised_content에 합쳐진 통합 씬 전문
    - revision_notes에 어떤 씬들을 어떻게 합쳤는지 명시
17. type="SPLIT": 한 씬을 여러 씬으로 나눈다.
    - revised_content에 나뉜 씬들을 모두 포함 (씬 헤더로 구분)
    - revision_notes에 분할 의도 명시

[한국 시나리오 포맷 규칙]
1. 씬 헤더: S#번호 장소 — 시간 (예: S#35 INT. 카페 — 낮)
2. 지문: 현재형 ("~한다"), 외부 관찰 가능한 행동만
3. 인물명: 한 줄 (모두 대문자 또는 일반 표기, 원본 방식 유지)
4. 대사: 인물명 다음 줄, 콜론(:) 없음
5. CUT TO. / INT. / EXT. 등 표준 전환 표기 사용
6. 괄호 지시 (V.O. / O.S. / 계속 / 낮게) 는 인물명 옆에

[출력 형식 — JSON 단일 객체]
{{
  "revision_result": {{
    "summary": "수정 작업의 전체 요약 (어떤 방향으로 무엇을 고쳤는지 3~5줄)",
    "batch_info": {{
      "batch_index": "이번 배치 번호 (배치 모드일 때만)",
      "scenes_completed": "이번 배치에서 완료한 씬 개수"
    }},
    "revised_scenes": [
      {{
        "scene_id": "Stage 1의 scene_id와 일치",
        "scene_header": "수정된 씬 헤더 (예: S#35 INT. 카페 — 낮)",
        "priority": "HIGH | MEDIUM | LOW (Stage 1과 일치)",
        "type": "REWRITE | ADD | DELETE | MERGE | SPLIT (Stage 1과 일치)",
        "original_excerpt": "원본 씬의 첫 2~3줄 (참조용, ADD/DELETE면 빈 문자열)",
        "revised_content": "수정된 씬 전문 (DELETE면 빈 문자열). 지문+대사+전환 모두 포함. 줄바꿈은 \\n으로.",
        "insert_position": "ADD/MERGE/SPLIT 시 삽입·합침·분할 위치 정보",
        "revision_notes": {{
          "what_changed": "무엇이 어떻게 바뀌었는지 구체적으로",
          "what_preserved": "원본에서 유지한 요소들",
          "intensity_check": "이 씬에서 실제 보존 비율 (추정)",
          "locked_check": "LOCKED 준수 확인"
        }}
      }}
    ],
    "unchanged_scenes_note": "수정 대상이 아닌 씬들에 대한 안내 (원본 그대로 사용)",
    "cross_scene_impact": "이 수정이 다른 씬들과 플롯 흐름에 미치는 영향 설명"
  }}
}}

JSON만 출력하라. 설명·주석·마크다운 금지. revised_content 안의 시나리오 본문만이 유일한 산출물이다.
""".strip()


# =================================================================
# [7] STAGE 3 — VERIFY (검증 보고서)
# =================================================================
def build_verify_prompt(
    raw_text: str,
    revise_result: dict,
    instruction: str,
    locked: str,
    genre: str
) -> str:
    """Stage 3: 원본 vs 수정본을 비교하고, 지시사항·LOCKED·AI ESCAPE·장르 규칙 준수를 검증.
    Sonnet 4.6 사용 권장 (분석)."""

    import json as _json

    genre_block = get_genre_rules_block(genre)
    locked_text = locked.strip() if locked.strip() else "(명시된 LOCKED 요소 없음)"
    revise_json = _json.dumps(revise_result, ensure_ascii=False, indent=2)

    return f"""
[TASK — Stage 3: VERIFY]
원본 시나리오와 Stage 2에서 생성된 수정본을 비교하여, 다음 4가지 축으로 검증 보고서를 작성하라.
1. 지시사항 반영도 (Instruction Compliance)
2. LOCKED 보존도 (Locked Preservation)
3. AI SCREENPLAY ESCAPE 준수도 (Style Quality)
4. 장르 RULE PACK 준수도 (Genre Compliance)

[원본 시나리오]
━━━━━━━━━━━━━━━━━━━━━━━━
{raw_text}
━━━━━━━━━━━━━━━━━━━━━━━━

[Stage 2 수정 결과]
━━━━━━━━━━━━━━━━━━━━━━━━
{revise_json}
━━━━━━━━━━━━━━━━━━━━━━━━

[원본 수정 지시문 — 재참조]
━━━━━━━━━━━━━━━━━━━━━━━━
{instruction}
━━━━━━━━━━━━━━━━━━━━━━━━

[LOCKED — 보존해야 했던 요소]
━━━━━━━━━━━━━━━━━━━━━━━━
{locked_text}
━━━━━━━━━━━━━━━━━━━━━━━━

{genre_block}

{AI_ESCAPE_BLOCK}

[검증 원칙]
1. 지시사항을 개별 항목으로 분해한 뒤, 각 항목의 반영 여부를 Y/N/Partial로 판정하라.
2. LOCKED 요소가 수정본에서 유지되었는지 축자적으로 대조하라.
3. AI ESCAPE A1~A20 패턴이 수정본에 나타나는지 점검하라. 발견 시 구체 위치 표시.
4. 장르 must_have 4항목, fails 4항목 각각 체크.
5. 총평은 "출하 가능 여부"를 명확히 판정하라 (APPROVED / NEEDS_REVISION / REJECTED).

[출력 형식 — JSON 단일 객체]
{{
  "verify_report": {{
    "overall_verdict": "APPROVED | NEEDS_REVISION | REJECTED",
    "overall_score": "0.0 ~ 10.0 소수 한 자리",
    "verdict_reason": "판정 근거 3~5줄",

    "instruction_compliance": {{
      "score": "0 ~ 10 정수",
      "items": [
        {{
          "instruction_item": "지시문에서 추출한 개별 요구 사항",
          "status": "Y | N | Partial",
          "evidence": "수정본의 어느 부분에서 반영되었는지 (또는 왜 반영되지 않았는지)"
        }}
      ]
    }},

    "locked_preservation": {{
      "score": "0 ~ 10 정수",
      "items": [
        {{
          "locked_item": "LOCKED로 지정된 요소",
          "status": "Preserved | Violated | N/A",
          "evidence": "원본 vs 수정본 대조 결과"
        }}
      ]
    }},

    "ai_escape_check": {{
      "score": "0 ~ 10 정수",
      "violations": [
        {{
          "pattern_id": "A1 ~ A20 중 하나",
          "pattern_name": "예: 감정 설명 지문",
          "scene_id": "발견된 씬",
          "quote": "문제 구문 인용 (20자 내외)",
          "severity": "High | Medium | Low"
        }}
      ],
      "clean_patterns": "위반이 없는 패턴 개수 (총 20개 중)"
    }},

    "genre_compliance": {{
      "score": "0 ~ 10 정수",
      "must_have_check": [
        {{
          "item": "장르 must_have 항목",
          "status": "Met | Partial | Not_Met",
          "note": "짧은 해설"
        }}
      ],
      "fails_check": [
        {{
          "item": "장르 fails 항목",
          "status": "Avoided | Present | Improved",
          "note": "짧은 해설"
        }}
      ]
    }},

    "side_by_side_highlights": [
      {{
        "scene_id": "수정된 씬의 ID",
        "key_change": "가장 중요한 변화 한 줄 요약",
        "improvement_note": "이 변화의 효과 설명 (1~2줄)"
      }}
    ],

    "recommendations": [
      "재수정이 필요한 경우의 구체적 다음 스텝 (NEEDS_REVISION일 때만)"
    ]
  }}
}}

JSON만 출력하라. 설명·주석·마크다운 금지.
""".strip()


# =================================================================
# [8] 보고서 파일명 생성 유틸
# =================================================================
def get_report_filename(title: str, kind: str = "revised") -> str:
    """파일명 생성: 제목_수정본_날짜.docx 등"""
    import re
    from datetime import datetime
    safe_title = re.sub(r'[/*?:"<>|]', '_', title.strip()) if title else "제목없음"
    date_str = datetime.now().strftime("%Y%m%d")
    kind_map = {
        "revised": "수정본",
        "verify":  "검증보고서",
        "diagnose": "수정플랜"
    }
    kind_kor = kind_map.get(kind, kind)
    return f"{safe_title}_{kind_kor}_{date_str}_Blue.docx"


# =================================================================
# [9] REWRITE ENGINE JSON 파서
# =================================================================
def parse_rewrite_engine_json(json_data) -> str:
    """Rewrite Engine의 진단·처방 JSON을 자유 텍스트 수정 지시문으로 변환.

    지원하는 입력 구조 (자동 감지):
    1. _meta가 있는 새 구조: {"_meta": {...}, "chris_analysis": {...}, "shiho_prescription": {...}}
    2. flat 구조 (Rewrite Engine 내부 구조): {"scores": ..., "washing_table": ..., ...}
       이 경우 chris_analysis / shiho_prescription 키가 없는 평면 구조

    rewriting (MOON) 영역은 자동 무시.
    """
    import json as _json

    if isinstance(json_data, str):
        try:
            data = _json.loads(json_data)
        except (_json.JSONDecodeError, TypeError):
            return ""
    elif isinstance(json_data, dict):
        data = json_data
    else:
        return ""

    if not isinstance(data, dict):
        return ""

    # 구조 1: 새 export 구조 (chris_analysis + shiho_prescription)
    chris = data.get("chris_analysis", {})
    shiho = data.get("shiho_prescription", {})

    # 구조 2: flat 구조 — Rewrite Engine 내부 dict가 그대로 export된 경우
    if not chris and not shiho:
        # CHRIS 영역으로 추정되는 키들
        chris = {
            k: data.get(k) for k in [
                "scores", "mark", "total_analysis", "synopsis",
                "pros_cons", "narrative_drive", "beat_sheet",
                "tension_arc", "narrative_share",
                "genre_compliance", "opening_diagnosis", "logline"
            ] if k in data and data[k]
        }
        # SHIHO 영역으로 추정되는 키들
        shiho = {
            k: data.get(k) for k in [
                "washing_table", "dialogue_analysis", "suggestions",
                "opening_rx", "genre_fun_recovery"
            ] if k in data and data[k]
        }

    parts = ["[Rewrite Engine 진단·처방 결과를 다음과 같이 수정 지시로 변환합니다.]"]

    # ── CHRIS 분석 결과 ──
    if chris:
        parts.append("\n[CHRIS 진단]")

        # 스코어
        scores = chris.get("scores", {})
        if scores:
            score_parts = []
            for k, v in scores.items():
                score_parts.append(f"{k}: {v}/10")
            if score_parts:
                parts.append(f"종합 점수: {' / '.join(score_parts)}")

        # 종합 분석
        ta = chris.get("total_analysis", "")
        if ta:
            parts.append(f"\n종합 분석:\n{ta}")

        # 장점·단점·핵심처방
        pc = chris.get("pros_cons", {})
        if pc:
            pros = pc.get("pros", [])
            cons = pc.get("cons", [])
            key_rx = pc.get("key_prescription", "")
            if cons:
                parts.append("\n주요 약점 (수정 대상):")
                for c in cons[:8]:
                    parts.append(f"- {c}")
            if key_rx:
                parts.append(f"\n핵심 처방: {key_rx}")
            if pros:
                parts.append("\n유지할 강점:")
                for p in pros[:5]:
                    parts.append(f"- {p}")

        # 서사 동력
        nd = chris.get("narrative_drive", {})
        if isinstance(nd, dict) and nd:
            issues = nd.get("issues", []) or nd.get("problems", [])
            if issues:
                parts.append("\n서사 동력 문제:")
                for issue in issues[:5]:
                    parts.append(f"- {issue}")

        # 장르 준수도
        gc = chris.get("genre_compliance", {})
        if isinstance(gc, dict) and gc:
            fails = gc.get("genre_fails", []) or gc.get("fails", [])
            if fails:
                parts.append("\n장르 위반 사항:")
                for f in fails[:5]:
                    parts.append(f"- {f}")

        # 오프닝 진단
        od = chris.get("opening_diagnosis", {})
        if isinstance(od, dict) and od:
            issues = od.get("issues", []) or od.get("problems", [])
            if issues:
                parts.append("\n오프닝 문제:")
                for i in issues[:3]:
                    parts.append(f"- {i}")

    # ── SHIHO 처방 결과 ──
    if shiho:
        parts.append("\n[SHIHO 처방]")

        # 시퀀스 워싱
        wt = shiho.get("washing_table", [])
        if wt:
            parts.append("\n시퀀스별 처방 (Washing):")
            for row in wt[:10]:
                if isinstance(row, dict):
                    seq = row.get("sequence", "") or row.get("seq", "")
                    issue = row.get("issue", "") or row.get("problem", "")
                    rx = row.get("prescription", "") or row.get("rx", "")
                    if seq or issue:
                        parts.append(f"- {seq}: {issue}")
                        if rx:
                            parts.append(f"  → 처방: {rx}")

        # 대사 분석
        da = shiho.get("dialogue_analysis", {})
        if isinstance(da, dict) and da:
            issues = da.get("issues", []) or da.get("problems", [])
            if issues:
                parts.append("\n대사 문제:")
                for i in issues[:5]:
                    parts.append(f"- {i}")

        # 각색 제안 (10 Steps)
        sug = shiho.get("suggestions", [])
        if sug:
            parts.append("\n각색 제안 (단계별):")
            for s in sug[:10]:
                parts.append(f"- {s}")

        # 오프닝 처방
        orx = shiho.get("opening_rx", {})
        if isinstance(orx, dict) and orx:
            advice = orx.get("advice", "") or orx.get("prescription", "")
            if advice:
                parts.append(f"\n오프닝 처방: {advice}")

        # 장르 재미 회복
        gfr = shiho.get("genre_fun_recovery", {})
        if isinstance(gfr, dict) and gfr:
            advice = gfr.get("advice", "") or gfr.get("prescription", "")
            if advice:
                parts.append(f"\n장르적 재미 회복: {advice}")

    parts.append("\n[수정 지시] 위 진단·처방을 모두 반영하여 원고를 수정하라.")

    return "\n".join(parts).strip()


# =================================================================
# [10] 배치 분할 헬퍼 (DIAGNOSE 결과 → 우선순위·시간순 정렬된 배치 리스트)
# =================================================================
def split_into_batches(diagnose_result: dict, batch_size: int = 6) -> list:
    """DIAGNOSE 결과의 target_scenes를 배치 단위로 나눈다.

    정렬 우선순위:
    1. Priority: HIGH → MEDIUM → LOW
    2. 같은 Priority 내에서는 batch_recommended 값 → scene_position 순

    Returns:
        배치 리스트. 각 배치는 dict:
        {
            "batch_index": 1,
            "scenes": [...],  # 이 배치에서 처리할 씬들
            "priority_summary": "HIGH 5개",
            "type_summary": "REWRITE 4개, ADD 1개"
        }
    """
    plan = diagnose_result.get("revision_plan", {})
    scenes = plan.get("target_scenes", [])
    if not scenes:
        return []

    # 우선순위 점수 매핑 (낮을수록 먼저)
    priority_score = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

    def sort_key(s):
        pri = priority_score.get(s.get("priority", "MEDIUM"), 1)
        # batch_recommended가 있으면 우선 사용, 없으면 0
        try:
            br = int(s.get("batch_recommended", 0) or 0)
        except (ValueError, TypeError):
            br = 0
        return (pri, br)

    sorted_scenes = sorted(scenes, key=sort_key)

    # 배치로 분할
    batches = []
    for i in range(0, len(sorted_scenes), batch_size):
        chunk = sorted_scenes[i:i + batch_size]

        # 배치 요약
        priority_count = {}
        type_count = {}
        for s in chunk:
            p = s.get("priority", "MEDIUM")
            t = s.get("type", "REWRITE")
            priority_count[p] = priority_count.get(p, 0) + 1
            type_count[t] = type_count.get(t, 0) + 1

        priority_summary = ", ".join(f"{k} {v}개" for k, v in priority_count.items())
        type_summary = ", ".join(f"{k} {v}개" for k, v in type_count.items())

        batches.append({
            "batch_index": len(batches) + 1,
            "scenes": chunk,
            "priority_summary": priority_summary,
            "type_summary": type_summary,
            "scene_ids": [s.get("scene_id", f"Scene {idx}") for idx, s in enumerate(chunk)]
        })

    return batches


def merge_batch_results(batch_results: list) -> dict:
    """여러 배치의 REVISE 결과를 하나로 합친다.

    Args:
        batch_results: [batch1_result, batch2_result, ...] 형태의 리스트

    Returns:
        통합된 revision_result (Stage 3 VERIFY 입력으로 사용 가능)
    """
    if not batch_results:
        return {"revision_result": {"summary": "", "revised_scenes": []}}

    all_scenes = []
    summaries = []
    cross_impacts = []
    unchanged_notes = []

    for br in batch_results:
        if not br:
            continue
        rr = br.get("revision_result", {})
        all_scenes.extend(rr.get("revised_scenes", []))
        s = rr.get("summary", "").strip()
        if s:
            summaries.append(s)
        ci = rr.get("cross_scene_impact", "").strip()
        if ci:
            cross_impacts.append(ci)
        un = rr.get("unchanged_scenes_note", "").strip()
        if un:
            unchanged_notes.append(un)

    return {
        "revision_result": {
            "summary": "\n\n".join(summaries) if summaries else "",
            "revised_scenes": all_scenes,
            "cross_scene_impact": "\n\n".join(cross_impacts) if cross_impacts else "",
            "unchanged_scenes_note": unchanged_notes[0] if unchanged_notes else "",
            "batch_summary": f"총 {len(batch_results)}개 배치, {len(all_scenes)}개 씬 처리 완료"
        }
    }


# =================================================================
# END OF prompt.py
# =================================================================
