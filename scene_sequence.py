# ─────────────────────────────────────────────────────────────
# BLUE JEANS Story Engine — Scene Sequence Pack v1.0.0
# scene_sequence.py — 씬 시퀀스 레이어 (권역·시간대·장르 1막 셋업)
# © 2026 BLUE JEANS PICTURES
#
# v1.0.0 (2026-08-06):
# - Mr. MOON 진단: "Writer Engine에 씬 순서 설계가 없다. 비트 단위로는
#   정확한데 비트 사이의 교대가 설계되지 않는다. 공간 교대·시점 교대·
#   두 주인공 세계의 병렬 제시는 비트 레벨이 아니라 씬 시퀀스 레벨의
#   판단인데 그 층이 비어 있다. 시간대 연속성 검증도 없다."
# - Mr. MOON 추가 진단: "권역이 한 군데면 공포영화가 아닌 이상 문제가
#   생긴다. 그래서 장르규칙이 제일 중요하다."
# - Mr. MOON 추가 진단: "로맨틱 코미디면 주인공이 티키타카 하면서
#   캐릭터 셋업이 1막에 설치되어야 한다."
#
# [설계 원칙]
# 1) 이 모듈의 검증은 AI가 아니라 파이썬이 수행한다.
#    기존 v3.5 공간 분산 룰은 AI에게 "세어보라"고 지시하는 구조였고,
#    실측 결과 AI가 하위 공간(선셋홀 사무실 / 선셋홀 복도)을 서로 다른
#    장소로 세어 룰을 우회했다. 세는 주체와 어기는 주체가 같으면 안 된다.
# 2) 권역(VENUE) 개념 도입 — 장소가 아니라 건물·구역 단위로 센다.
# 3) 모든 임계값은 장르에서 끌어온다. 같은 수치가 호러에서는 문법이고
#    로코에서는 결함이다.
# 4) prompt.py를 import 하지 않는다 (순환 참조 방지).
#    장르 판별 키워드는 prompt.py의 _is_* 함수군과 동일하게 유지한다.
#    ★ prompt.py의 판별 키워드가 바뀌면 이 파일도 함께 고쳐야 한다.
# ─────────────────────────────────────────────────────────────

import re
from collections import Counter, OrderedDict

MODULE_NAME = "BLUE JEANS Story Engine — Scene Sequence Pack"
MODULE_VERSION = "v1.0.0"
MODULE_BUILD_DATE = "2026-08-06"


# ═══════════════════════════════════════════════════════════
# 1. 장르 판별 — prompt.py _is_* 함수군과 키워드 동기화
# ═══════════════════════════════════════════════════════════

def _g(genre: str) -> str:
    return (genre or "").lower()


def is_horror(genre: str) -> bool:
    g = _g(genre)
    return "호러" in g or "공포" in g or "horror" in g


def is_comedy(genre: str) -> bool:
    g = _g(genre)
    return "코미디" in g or "comedy" in g or "롬코" in g or "스크루볼" in g or "screwball" in g


def is_romance(genre: str) -> bool:
    g = _g(genre)
    return ("로맨스" in g or "멜로" in g or "romance" in g
            or "롬코" in g or "로맨틱" in g)


def is_romcom(genre: str) -> bool:
    g = _g(genre)
    if "로맨틱 코미디" in g or "로맨틱코미디" in g or "롬코" in g:
        return True
    if "romcom" in g or "rom-com" in g or "romantic comedy" in g:
        return True
    return is_comedy(genre) and is_romance(genre)


def is_screwball(genre: str) -> bool:
    """스크루볼 코미디 판별 (v1.0.0 신규).
    권역 정책은 코미디(재방문 공간에서 상황이 누적되는 구조)를 따르고,
    1막 셋업 정책은 로코(티키타카)를 따른다 — 두 축이 분리된다."""
    g = _g(genre)
    return "스크루볼" in g or "screwball" in g


def is_action(genre: str) -> bool:
    g = _g(genre)
    return "액션" in g or "action" in g


def is_thriller(genre: str) -> bool:
    g = _g(genre)
    if is_horror(genre):
        return False
    kws = ["스릴러", "thriller", "범죄", "crime",
           "누아르", "느와르", "noir",
           "조폭", "갱스터", "gangster", "조직폭력",
           "마약", "drug", "밀수", "사기", "케이퍼", "caper", "heist"]
    return any(k in g for k in kws)


def is_mystery(genre: str) -> bool:
    g = _g(genre)
    kws = ["미스터리", "mystery", "추리", "탐정", "detective", "후더닛", "whodunit"]
    return any(k in g for k in kws)


def is_disaster(genre: str) -> bool:
    g = _g(genre)
    kws = ["재난", "disaster", "참사", "재해", "지진", "쓰나미",
           "화재", "전염병", "팬데믹", "pandemic"]
    return any(k in g for k in kws)


def is_period(genre: str) -> bool:
    g = _g(genre)
    kws = ["사극", "시대극", "period", "팩션", "faction",
           "조선", "고려", "삼국", "대하드라마"]
    return any(k in g for k in kws)


def is_coming_of_age(genre: str) -> bool:
    g = _g(genre)
    kws = ["청춘", "성장", "coming-of-age", "coming of age",
           "학원물", "학원", "학교", "하이틴", "high school", "highschool"]
    return any(k in g for k in kws)


def is_sf(genre: str) -> bool:
    g = _g(genre)
    return "sf" in g or "sci" in g or "에스에프" in g or "과학" in g


def is_fantasy(genre: str) -> bool:
    g = _g(genre)
    return "판타지" in g or "fantasy" in g


def is_drama(genre: str) -> bool:
    g = _g(genre)
    return "드라마" in g or "drama" in g or "멜로드라마" in g


def is_buddy(genre: str) -> bool:
    g = _g(genre)
    return "버디" in g or "buddy" in g


# ═══════════════════════════════════════════════════════════
# 2. VENUE POLICY TABLE — 장르별 권역 정책
#
#   max_share    : 지배 권역이 전체 씬에서 차지할 수 있는 최대 비율
#   max_run      : 같은 권역 연속 체류 허용 씬 수
#   min_venues   : 작품 전체에서 등장해야 할 최소 권역 수
#   world_balance: 두 주인공 세계 교대 강제 여부
#   minor_share  : 세계 교대 시 소수 세계가 확보해야 할 최소 비율
# ═══════════════════════════════════════════════════════════

VENUE_POLICY_TABLE = OrderedDict([
    ("한정공간", dict(max_share=0.85, max_run=99, min_venues=3,
                   world_balance=False, minor_share=0.0,
                   note="한정 공간 작품 — 폐쇄가 곧 장르 장치. 수동 지정 시에만 적용.")),
    ("호러/공포", dict(max_share=0.70, max_run=6, min_venues=4,
                   world_balance=False, minor_share=0.0,
                   note="공간의 폐쇄와 반복 자체가 공포의 엔진. 흩뿌리면 장르가 죽는다.")),
    ("재난", dict(max_share=0.60, max_run=5, min_venues=5,
                world_balance=False, minor_share=0.0,
                note="재난 현장 집중이 정상. 다만 외부 세계 컷어웨이는 필요.")),
    ("성장물", dict(max_share=0.45, max_run=4, min_venues=6,
                 world_balance=False, minor_share=0.0,
                 note="학교·집 거점이 강한 장르. 다만 거점 밖 세계가 있어야 성장이 보인다.")),
    ("사극/시대극", dict(max_share=0.45, max_run=4, min_venues=6,
                    world_balance=False, minor_share=0.0,
                    note="궁·관아 등 권력 공간 집중이 자연스럽다.")),
    ("코미디", dict(max_share=0.45, max_run=3, min_venues=7,
                 world_balance=False, minor_share=0.0,
                 note="같은 공간 재방문이 개그 누적 구조. 스크루볼 포함.")),
    ("드라마", dict(max_share=0.40, max_run=3, min_venues=7,
                 world_balance=False, minor_share=0.0,
                 note="")),
    ("로맨스/로코", dict(max_share=0.35, max_run=3, min_venues=8,
                    world_balance=True, minor_share=0.25,
                    note="두 세계의 교대 → 충돌 → 융합이 구조 그 자체.")),
    ("버디", dict(max_share=0.35, max_run=3, min_venues=8,
                world_balance=True, minor_share=0.25,
                note="두 주인공의 세계 대비가 갈등의 원천.")),
    ("미스터리", dict(max_share=0.35, max_run=3, min_venues=8,
                  world_balance=False, minor_share=0.0,
                  note="수사는 이동이다. 단서마다 새 공간이 붙는다.")),
    ("범죄/스릴러", dict(max_share=0.35, max_run=3, min_venues=8,
                    world_balance=False, minor_share=0.0,
                    note="추적·수사는 이동이 본질.")),
    ("SF/판타지", dict(max_share=0.35, max_run=3, min_venues=8,
                    world_balance=False, minor_share=0.0,
                    note="세계 확장이 장르의 약속. 공간이 좁으면 세계가 없다.")),
    ("액션", dict(max_share=0.30, max_run=2, min_venues=10,
                world_balance=False, minor_share=0.0,
                note="이동 자체가 장르. 한 건물 침투물은 '한정공간' 지정으로 분리.")),
    ("미지정", dict(max_share=0.40, max_run=3, min_venues=7,
                 world_balance=False, minor_share=0.0,
                 note="")),
])


def resolve_venue_policy(genre: str, confined: bool = False) -> dict:
    """장르 문자열 → 권역 정책 dict 반환. 먼저 걸리는 항목이 적용된다."""
    if confined:
        p = dict(VENUE_POLICY_TABLE["한정공간"]); p["label"] = "한정공간"; return p

    order = [
        ("호러/공포", is_horror),
        ("재난", is_disaster),
        ("성장물", is_coming_of_age),
        ("사극/시대극", is_period),
        # ★ 스크루볼은 권역 정책만 코미디를 따른다 (1막 셋업은 로코)
        ("코미디", lambda g: is_screwball(g)),
        ("로맨스/로코", lambda g: is_romcom(g) or is_romance(g)),
        ("버디", is_buddy),
        ("액션", is_action),
        ("미스터리", is_mystery),
        ("범죄/스릴러", is_thriller),
        ("SF/판타지", lambda g: is_sf(g) or is_fantasy(g)),
        ("코미디", is_comedy),
        ("드라마", is_drama),
    ]
    for label, fn in order:
        if fn(genre):
            p = dict(VENUE_POLICY_TABLE[label]); p["label"] = label; return p
    p = dict(VENUE_POLICY_TABLE["미지정"]); p["label"] = "미지정"; return p


# ═══════════════════════════════════════════════════════════
# 3. 씬 헤딩 파싱 + 권역 정규화
# ═══════════════════════════════════════════════════════════

_HEADING_RE = re.compile(
    r'^S#\s*(\d+)\s*[-–—]?\s*([A-Za-z]?)\s*\.?\s*'
    r'(INT\.?/EXT\.?|I\.?/E\.?|INT\.?|EXT\.?)\s*[.．]?\s*(.+)$'
)

# 시간대 정렬표 — 값이 작을수록 이른 시각
TOD_ORDER = {
    "새벽": 0, "동틀녘": 0, "여명": 0,
    "이른 아침": 1, "아침": 2, "오전": 3,
    "낮": 4, "정오": 4, "한낮": 4,
    "오후": 5, "늦은 오후": 6, "오후 늦게": 6, "해질녘": 6, "노을": 6,
    "저녁": 7, "초저녁": 7,
    "밤": 8, "늦은 밤": 9, "심야": 9, "새벽녘": 9,
}

# 날짜 경과 표기 — 이게 있으면 시간 역행이 아니다
_DAYSHIFT_RE = re.compile(
    r'(다음\s*날|이튿날|익일|다다음\s*날|이틀\s*(후|뒤)|사흘\s*(후|뒤)|'
    r'며칠\s*(후|뒤)|일주일\s*(후|뒤)|한\s*달\s*(후|뒤)|'
    r'\d+\s*(일|주|개월|년)\s*(후|뒤|전)|그날\s*밤|같은\s*날\s*밤)'
)

# 사실상 "(연속)"인 괄호 부기 — 씬 분리 우회 표기
_FAKE_SPLIT_RE = re.compile(
    r'\((\s*)(연속|계속|직후|잠시\s*후|조금\s*후|같은\s*시각|동시|이어서|'
    r'.*?직후|.*?경과|.*?중반|.*?후반|.*?도중|.*?진행\s*중|.*?의식|.*?장면)(\s*)\)'
)


def parse_scene_headings(text: str) -> list:
    """원고 텍스트에서 씬 헤딩을 순서대로 추출한다.

    반환: [{no, suffix, ie, place, tod, tod_raw, raw, line_index}, ...]
    """
    out = []
    if not text:
        return out
    for idx, raw_line in enumerate(text.split("\n")):
        line = raw_line.strip()
        if not line.startswith("S#"):
            continue
        m = _HEADING_RE.match(line)
        if not m:
            continue
        no = int(m.group(1))
        suffix = (m.group(2) or "").strip()
        ie = m.group(3).replace(".", "").upper()
        if ie in ("I/E", "INT/EXT"):
            ie = "INT/EXT"
        body = m.group(4).strip()

        place, tod_raw = body, ""
        for sep in ("—", "–", " - ", " — "):
            if sep in body:
                p, t = body.rsplit(sep, 1)
                place, tod_raw = p.strip(), t.strip()
                break
        out.append({
            "no": no,
            "suffix": suffix,
            "ie": ie,
            "place": place,
            "tod_raw": tod_raw,
            "tod": _normalize_tod(tod_raw),
            "raw": line,
            "line_index": idx,
        })
    return out


def _normalize_tod(tod_raw: str) -> str:
    """시간대 문자열에서 괄호 부기와 날짜 표기를 걷어내고 핵심 시간대만 남긴다."""
    t = re.sub(r'\(.*?\)', '', tod_raw or '').strip()
    t = _DAYSHIFT_RE.sub('', t).strip()
    t = t.strip('·,.-— ')
    # 표에 있는 표기를 길이 긴 것부터 매칭 ("오후 늦게"가 "오후"보다 먼저)
    for key in sorted(TOD_ORDER.keys(), key=len, reverse=True):
        if key in t:
            return key
    return t


# 권역 정규화에서 잘라낼 하위 공간 어휘
_SUBSPACE_WORDS = [
    "본식장", "메인 홀", "메인홀", "홀", "로비", "복도", "사무실", "소회의실",
    "회의실", "상담실", "대기실", "탈의실", "화장실", "주방", "부엌", "창고",
    "옥상", "계단", "지하", "주차장", "현관", "거실", "안방", "침실", "서재",
    "베란다", "테라스", "마당", "정원", "입구", "출입구", "외관", "건물 앞",
    "앞", "뒤", "뒷", "안", "내부", "외부", "창가", "소파", "테이블", "카운터",
    "무대", "무대 뒤", "백스테이지", "부스", "문틈", "야외 테이블", "코너",
    "병실", "수술실", "응급실", "복도끝", "엘리베이터", "옥탑", "다락",
    # 건물에 딸린 외부 공간 — 같은 권역으로 묶는다
    "뒷골목", "앞 골목", "골목길", "골목", "외벽", "인근", "부근", "근처",
]


def normalize_venue(place: str, venue_hints: list = None) -> str:
    """장소 문자열 → 권역(건물·구역) 문자열.

    'ㅇㅇ 소회의실', 'ㅇㅇ 복도', 'ㅇㅇ 로비'를 모두 'ㅇㅇ'으로 묶는다.
    venue_hints가 주어지면 그 목록을 최우선 적용한다 (수동 보정).
    """
    p = (place or "").strip()
    if not p:
        return "(미상)"

    # 1) 하위 공간 어휘 제거
    s = p
    for w in sorted(_SUBSPACE_WORDS, key=len, reverse=True):
        s = s.replace(w, " ")
    s = re.sub(r'\s+', ' ', s).strip(' ·,.-')

    # 2) 힌트 적용 — 힌트로 묶되, 이름은 읽기 좋게 유지
    #    '지수 법률사무소 상담실' → 힌트 '지수' 매칭 → 표기는 '지수 법률사무소'
    #    '선셋홀 소회의실'        → 힌트 '선셋홀' 매칭 → 표기는 '선셋홀'
    if venue_hints:
        for h in sorted([(x or "").strip() for x in venue_hints if x],
                        key=len, reverse=True):
            if h and h in p:
                if s.startswith(h) and len(s.split()) <= 2:
                    return s
                return h

    # 3) 남은 것이 없으면 원문 첫 어절
    if not s:
        toks = p.split()
        return toks[0] if toks else p

    # 4) 2어절 초과면 앞 2어절까지만 (권역명은 보통 1~2어절)
    toks = s.split()
    if len(toks) > 2:
        s = " ".join(toks[:2])
    return s


def auto_venue_hints(scenes: list, min_count: int = 2) -> list:
    """씬 목록에서 2회 이상 등장하는 권역 접두어를 자동 추출한다.
    STEP 1에 권역을 입력하지 않아도 기본 동작하도록 하는 폴백."""
    heads = []
    for s in scenes:
        toks = (s.get("place") or "").split()
        if toks:
            heads.append(toks[0])
    c = Counter(heads)
    return [k for k, v in c.most_common() if v >= min_count and len(k) >= 2]


# ═══════════════════════════════════════════════════════════
# 4. 검증기 — 위반 6종 (V1~V6)
# ═══════════════════════════════════════════════════════════

def verify_scene_sequence(full_text: str, genre: str = "",
                          confined: bool = False,
                          venue_hints: list = None) -> dict:
    """원고 전문을 파싱해 씬 시퀀스 위반을 검출한다.

    반환 dict:
      ok(bool), policy(dict), total(int), venues(list of (venue, count, share)),
      violations: {V1..V6: [메시지 리스트]}
    """
    policy = resolve_venue_policy(genre, confined=confined)
    scenes = parse_scene_headings(full_text or "")

    # 씬 번호 중복 제거 (재집필로 같은 번호가 두 번 나온 경우 뒤엣것 무시)
    seen, uniq, dup = set(), [], []
    for s in scenes:
        key = (s["no"], s["suffix"])
        if key in seen:
            dup.append(s)
            continue
        seen.add(key)
        uniq.append(s)

    v = {f"V{i}": [] for i in range(1, 7)}
    total = len(uniq)
    if total == 0:
        return dict(ok=True, policy=policy, total=0, venues=[], violations=v,
                    scenes=[], note="파싱된 씬 헤딩이 없습니다.")

    hints = list(venue_hints) if venue_hints else auto_venue_hints(uniq)
    for s in uniq:
        s["venue"] = normalize_venue(s["place"], hints)

    # ── V1. 권역 연속 체류
    run = [uniq[0]]
    runs = []
    for s in uniq[1:]:
        if s["venue"] == run[-1]["venue"]:
            run.append(s)
        else:
            runs.append(run); run = [s]
    runs.append(run)
    for r in runs:
        if len(r) > policy["max_run"]:
            v["V1"].append(
                f"S#{r[0]['no']}~S#{r[-1]['no']} · {r[0]['venue']} {len(r)}씬 연속 "
                f"(허용 {policy['max_run']}씬)"
            )

    # ── V2. 시간대 역행
    prev = None
    for s in uniq:
        cur = TOD_ORDER.get(s["tod"])
        dayshift = bool(_DAYSHIFT_RE.search(s["tod_raw"] or "")) or \
                   bool(_DAYSHIFT_RE.search(s["place"] or ""))
        if prev is not None and cur is not None and not dayshift and cur < prev[0]:
            v["V2"].append(
                f"S#{prev[1]}({prev[2]}) → S#{s['no']}({s['tod_raw']}) "
                f"— 날짜 경과 표기 없이 시간 역행"
            )
        if cur is not None:
            prev = (cur, s["no"], s["tod_raw"] or s["tod"])

    # ── V3. 시간대 단일화 (연속 5씬 이상 동일 시간대)
    trun = [uniq[0]]
    for s in uniq[1:]:
        if s["tod"] and s["tod"] == trun[-1]["tod"]:
            trun.append(s)
        else:
            if len(trun) >= 5 and trun[0]["tod"]:
                v["V3"].append(
                    f"S#{trun[0]['no']}~S#{trun[-1]['no']} · {len(trun)}씬 전부 "
                    f"'{trun[0]['tod']}' — 시간 경과가 보이지 않음"
                )
            trun = [s]
    if len(trun) >= 5 and trun[0]["tod"]:
        v["V3"].append(
            f"S#{trun[0]['no']}~S#{trun[-1]['no']} · {len(trun)}씬 전부 "
            f"'{trun[0]['tod']}' — 시간 경과가 보이지 않음"
        )

    # ── V4. 괄호 부기 (사실상 (연속) 표기)
    for s in uniq:
        if s["tod_raw"] and _FAKE_SPLIT_RE.search(s["tod_raw"]):
            v["V4"].append(f"S#{s['no']} {s['place']} — {s['tod_raw']}")

    # ── V5. 씬 번호 중복 / 결번
    if dup:
        nos = ", ".join(f"S#{d['no']}" for d in dup)
        v["V5"].append(f"중복 씬 번호 {len(dup)}건 — {nos}")
    nums = sorted(s["no"] for s in uniq)
    missing = [n for n in range(nums[0], nums[-1] + 1) if n not in set(nums)]
    if missing:
        v["V5"].append(
            f"결번 {len(missing)}건 — "
            + ", ".join(f"S#{n}" for n in missing[:12])
            + (" …" if len(missing) > 12 else "")
        )

    # ── V6. 권역 점유율 / 최소 권역 수
    cnt = Counter(s["venue"] for s in uniq)
    venues = [(k, c, c / total) for k, c in cnt.most_common()]
    top_v, top_c, top_share = venues[0]
    if top_share > policy["max_share"]:
        over = int(round((top_share - policy["max_share"]) * total))
        v["V6"].append(
            f"지배 권역 '{top_v}' {top_c}씬 / {total}씬 = {top_share*100:.1f}% "
            f"(장르 상한 {policy['max_share']*100:.0f}%) — 약 {over}씬을 타 권역으로 이전 필요"
        )
    if len(cnt) < policy["min_venues"]:
        v["V6"].append(
            f"권역 수 {len(cnt)}개 (장르 최소 {policy['min_venues']}개) "
            f"— {policy['min_venues'] - len(cnt)}개 부족"
        )

    ok = all(len(x) == 0 for x in v.values())
    return dict(ok=ok, policy=policy, total=total, venues=venues,
                violations=v, scenes=uniq, hints=hints)


_V_LABEL = {
    "V1": "권역 연속 체류 초과",
    "V2": "시간대 역행",
    "V3": "시간대 단일화",
    "V4": "괄호 부기 (씬 분리 우회)",
    "V5": "씬 번호 중복·결번",
    "V6": "권역 점유율·다양성",
}


def format_verify_report(report: dict) -> str:
    """검증 결과를 사람이 읽는 마크다운 리포트로 변환한다."""
    if not report or report.get("total", 0) == 0:
        return "파싱된 씬 헤딩이 없습니다. 원고를 먼저 생성하세요."

    pol = report["policy"]
    lines = []
    lines.append(f"**장르 정책**: {pol['label']} — "
                 f"지배권역 상한 {pol['max_share']*100:.0f}% / "
                 f"연속 {pol['max_run']}씬 / 최소 권역 {pol['min_venues']}개"
                 + (f" / 세계 교대 ON (소수 {pol['minor_share']*100:.0f}%↑)"
                    if pol["world_balance"] else ""))
    if pol.get("note"):
        lines.append(f"　_{pol['note']}_")
    lines.append("")
    lines.append(f"**총 {report['total']}씬 / 권역 {len(report['venues'])}개**")
    lines.append("")
    lines.append("| 권역 | 씬 수 | 비율 |")
    lines.append("|---|---:|---:|")
    for name, c, share in report["venues"][:12]:
        lines.append(f"| {name} | {c} | {share*100:.1f}% |")
    lines.append("")

    total_v = sum(len(x) for x in report["violations"].values())
    if total_v == 0:
        lines.append("### ✅ 위반 없음 — 씬 시퀀스 통과")
        return "\n".join(lines)

    lines.append(f"### ⚠️ 위반 {total_v}건")
    for code in ["V6", "V1", "V2", "V3", "V4", "V5"]:
        items = report["violations"][code]
        if not items:
            continue
        lines.append("")
        lines.append(f"**[{code}] {_V_LABEL[code]}** — {len(items)}건")
        for it in items:
            lines.append(f"- {it}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 5. 직전 씬 앵커 — 집필 직전 구조화 주입
# ═══════════════════════════════════════════════════════════

def build_prev_scene_anchor(previous_scene_text: str, genre: str = "",
                            confined: bool = False,
                            venue_hints: list = None,
                            full_text_so_far: str = "") -> str:
    """직전 비트의 마지막 씬 헤딩을 파싱해 시간·공간 기준점을 명시 주입한다.

    기존 방식은 직전 비트 원문 뒤 2,500자를 던지고 '연속성 유지'라고만 적었다.
    모델이 그 안에서 헤딩을 찾아 읽기를 기대하는 구조여서 시간 역행이 발생했다.
    이 함수는 파이썬이 직접 파싱해 결론만 박아 넣는다.
    """
    if not previous_scene_text:
        return ""

    policy = resolve_venue_policy(genre, confined=confined)
    scenes = parse_scene_headings(previous_scene_text)
    if not scenes:
        return ""

    hints = list(venue_hints) if venue_hints else auto_venue_hints(scenes, min_count=1)
    last = scenes[-1]
    last_venue = normalize_venue(last["place"], hints)

    # 전체 원고 기준 현재 연속 체류 길이 계산
    run_len = 1
    all_scenes = parse_scene_headings(full_text_so_far) if full_text_so_far else scenes
    if all_scenes:
        ah = list(venue_hints) if venue_hints else auto_venue_hints(all_scenes, min_count=1)
        vseq = [normalize_venue(s["place"], ah) for s in all_scenes]
        last_venue = vseq[-1]
        run_len = 1
        for x in reversed(vseq[:-1]):
            if x == last_venue:
                run_len += 1
            else:
                break

    tod = last["tod"] or "(시간대 미표기)"
    tod_idx = TOD_ORDER.get(last["tod"])
    if tod_idx is None:
        tod_line = f"★ 직전 씬 시간대가 표준 표기가 아니다. 새 씬 헤딩에는 표준 시간대를 쓰라."
    else:
        later = [k for k, x in sorted(TOD_ORDER.items(), key=lambda kv: kv[1])
                 if x > tod_idx]
        # 중복 제거하며 순서 유지
        seen, later_u = set(), []
        for k in later:
            if TOD_ORDER[k] not in seen:
                seen.add(TOD_ORDER[k]); later_u.append(k)
        allow = " / ".join(later_u[:5]) if later_u else "(다음 날 아침 이후)"
        tod_line = (
            f"★ 이 비트 첫 씬의 시간대는 '{tod}' 이후여야 한다. 허용: {allow}\n"
            f"★ '{tod}'보다 이른 시간대로 가려면 헤딩에 '다음 날'을 반드시 명기하라.\n"
            f"   ❌ S#N. INT. ○○ — 아침        (직전이 '밤'인데 표기 없음 = 시간 역행)\n"
            f"   ✅ S#N. INT. ○○ — 다음 날 아침"
        )

    over = run_len >= policy["max_run"]
    venue_line = (
        f"★ 직전 권역 '{last_venue}'에서 {run_len}씬 연속 체류 중 "
        f"(장르 허용 {policy['max_run']}씬).\n"
        + (f"★ 한계에 도달했다. 이 비트의 첫 씬은 반드시 다른 권역에서 시작하라.\n"
           if over else
           f"★ 이 비트에서 '{last_venue}'를 {policy['max_run'] - run_len}씬까지만 더 쓸 수 있다.\n")
    )

    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 직전 씬 앵커 — 시간·공간 연속성 기준점 (v3.9.0 SCENE SEQUENCE) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[직전 씬] {last['raw']}
  · 권역: {last_venue}
  · 시간대: {tod}

[공간 연속성]
{venue_line}
[시간 연속성]
{tod_line}

[씬 헤딩 표기 규칙 — 위반 시 씬 실패]
❌ 시간대 뒤 괄호 부기 금지 — (잠시 후) (직후) (연속) (세션 중반) (서약 의식)
   같은 권역 + 같은 시간대는 새 씬 번호를 받지 못한다. 하나의 씬 안에서
   CUT TO: 또는 지문의 시간 경과 문장으로 처리하라.
✅ 표준 표기 — S#N. INT./EXT. 장소 — 시간대
""".strip()


# ═══════════════════════════════════════════════════════════
# 6. 씬 플랜용 권역 규칙 블록
# ═══════════════════════════════════════════════════════════

def build_venue_rule_block(genre: str, confined: bool = False,
                           act: str = "", venue_hints: list = None) -> str:
    """build_scene_plan_prompt에 주입할 장르별 권역 설계 규칙."""
    p = resolve_venue_policy(genre, confined=confined)
    hint_line = ""
    if venue_hints:
        hint_line = "\n[이 작품의 권역 목록 — 작가 지정]\n  " + " / ".join(venue_hints) + "\n"

    wb = ""
    if p["world_balance"]:
        wb = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━
[두 주인공 세계 병렬 제시 — {p['label']} 강제]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★ 이 장르는 두 주인공이 각자의 세계를 갖는다. 한쪽 세계에 다른 쪽이 방문하는
  구조는 실패다. 상대역이 기획 자료에서 antagonist로 분류되어 있더라도,
  씬 플랜에서는 공동 주인공(co-protagonist)으로 취급하라.

[교대 쿼터]
- 소수 세계(주인공 B의 거점 권역)는 전체 씬의 {p['minor_share']*100:.0f}% 이상.
- 주인공 B가 자기 세계에서 상대 없이 행동하는 단독 씬을 각 막마다 배치하라.
  · 1막 최소 3씬 / 2막 최소 4씬 / 3막 최소 2씬
- A의 세계 → B의 세계 교차 배치. 같은 세계 4씬 연속 금지.

[병렬 제시의 목적]
두 세계가 각각 어떤 규칙으로 돌아가는지 관객이 먼저 알아야, 두 세계가
충돌할 때 무엇이 깨지는지 보인다. 세계를 보여주지 않으면 충돌이 사건이 아니라
말다툼으로 보인다.
"""

    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 권역(VENUE) 분산 — 장르 정책 강제 (v3.9.0 SCENE SEQUENCE) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 판정 단위는 '장소'가 아니라 '권역'이다. ★
  권역 = 건물·구역 단위. 하위 공간을 쪼개도 같은 권역이면 같은 것으로 센다.
  ❌ '선셋홀 사무실' '선셋홀 복도' '선셋홀 로비' '선셋홀 소회의실'을 서로
     다른 장소로 세어 분산 규칙을 통과했다고 판단하는 것 — 우회다.
  ✅ 위 4개는 전부 권역 '선셋홀' 1개다.
{hint_line}
[적용 장르 정책 — {p['label']}]
  · 지배 권역 상한: 전체 씬의 {p['max_share']*100:.0f}% 이하
  · 권역 연속 체류: 최대 {p['max_run']}씬
  · 최소 권역 수: {p['min_venues']}개 이상
{("  · " + p['note']) if p.get('note') else ""}

★ 이 수치는 장르에서 나온 것이다. 호러는 한 권역 70%가 문법이고,
  로맨틱 코미디는 35%가 상한이다. 같은 숫자가 장르에 따라 정반대다.

[비트 경계 교대 — 이 층이 비어 있었다]
★ 비트 내부만 교대시키면 안 된다. 비트가 끝나는 권역과 다음 비트가 시작하는
  권역이 같으면, 비트 경계를 넘어 권역이 뭉친다.
- 각 비트의 마지막 씬 권역과 다음 비트의 첫 씬 권역을 다르게 설계하라.
- 막 경계(1막→2막, 2막→3막)에서는 특히 엄격히 적용한다.

[시간대 연속성 — 씬 플랜 단계에서 확정]
- 모든 씬 헤딩에 시간대를 표기하라. 표준 표기만 사용:
  새벽 / 이른 아침 / 아침 / 오전 / 낮 / 오후 / 저녁 / 밤
- 앞 씬보다 이른 시간대로 갈 때는 반드시 '다음 날'을 명기하라.
- 한 비트의 씬이 5개 이상 전부 같은 시간대이면 시간이 멈춘 것으로 보인다.
  비트 안에서 최소 2개 시간대를 쓰라.
- 시간대 뒤 괄호 부기 금지: (연속) (직후) (잠시 후) (세션 중반) (30분 경과)
  같은 권역 + 같은 시간대는 새 씬 번호를 받을 수 없다.
{wb}
[플랜 제출 전 권역 자가 점검]
□ 지배 권역 씬 수 ___ / 전체 ___ = ___% (상한 {p['max_share']*100:.0f}%)
□ 권역 수 ___개 (최소 {p['min_venues']}개)
□ 권역 {p['max_run']}씬 초과 연속 구간: [있음/없음]
□ 비트 경계에서 권역이 이어지는 구간: [있음/없음]
□ 시간대 역행(다음 날 표기 없음): [있음/없음]
{"□ 소수 세계 씬 수 ___ / 전체 ___ = ___% (최소 " + f"{p['minor_share']*100:.0f}%)" if p["world_balance"] else ""}
→ 위반 1개 이상이면 플랜을 수정한 뒤 제출하라.
""".strip()


# ═══════════════════════════════════════════════════════════
# 7. 장르별 1막 셋업 규칙
#    Mr. MOON: "로맨틱 코미디면 주인공이 티키타카 하면서
#               캐릭터 셋업이 1막에 설치되어야 하지 않을까?"
# ═══════════════════════════════════════════════════════════

ACT1_ROMCOM = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 1막 셋업 강제 — 로맨틱 코미디 (v3.9.0) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 로코의 1막은 '주인공 소개'가 아니다. '두 사람이 왜 서로에게만 위험한가'를
  설치하는 구간이다. 1막이 끝날 때 관객은 두 사람이 붙으면 반드시 사고가
  난다는 것을 알고 있어야 한다. ★

[1. 공동 주인공 선언 — 최우선]
- 상대역이 기획 자료에서 role: antagonist로 분류되어 있어도, 집필에서는
  공동 주인공으로 다룬다. 로코의 상대역은 장애물이 아니라 또 하나의 주인공이다.
- 두 사람 각각 goal / need / flaw를 갖는다. 한쪽만 결핍이 있으면 로코가 아니라
  구애극이다.

[2. 미트큐트 이전 — 각자의 세계를 따로 설치한다]
★ 가장 자주 실패하는 지점이다. 상대역을 주인공의 세계에 '나타난 문제'로만
  도입하면, 그 인물은 끝까지 손님으로 남는다.
- 미트큐트 이전에 두 사람 각각 자기 거점 권역에서 상대 없이 행동하는 씬을
  최소 2씬씩 배치하라.
- 그 단독 씬에서 각자의 flaw가 '행동'으로 드러나야 한다. 설명 대사 금지.
  ✅ 무대 위에서는 완벽한데 무대 밖에서 파트너에게 "커피 타와" 한마디로
     대화를 끊어버리는 남자 — flaw가 행동으로 보인다.
  ❌ "저는 사람들과 가까워지는 게 어려워요" — 설명이다.
- 두 세계의 규칙이 서로 반대여야 한다. 한쪽이 감정을 파는 세계면 다른 쪽은
  감정을 잘라내는 세계다. 이 대비가 나중에 충돌의 재료가 된다.

[3. 미트큐트 — 배치 위치]
- Beat 2~4 구간에 배치한다. 너무 이르면 두 세계가 설치되지 않고,
  너무 늦으면 1막이 지루해진다.
- 미트큐트는 '만남'이 아니라 '충돌'이다. 두 사람의 목표가 그 자리에서
  정면으로 어긋나야 한다.
- 첫 만남에서 두 사람은 서로에 대해 틀린 결론을 내려야 한다. 그 오해가
  2막의 연료다.

[4. 티키타카 — 로코의 엔진]
★ 티키타카 = 두 사람이 번갈아 주고받는 대사의 연쇄. 로코 관객이 표를 사는
  이유가 이것이다. 사건이 아니라 대화가 재미의 본체다. ★

- 1막 안에 티키타카 씬을 최소 2씬 배치하라.
  · 티키타카 씬 = 두 사람이 6회 이상 연속으로 주고받는 씬.
    (A→B→A→B… 화자가 계속 교대되는 상태를 6회 이상 유지)
- 티키타카가 성립하는 조건 3가지:
  ① 말버릇이 서로 달라야 한다. 두 사람의 대사를 화자 이름 없이 읽어도
     누가 한 말인지 구분되어야 한다.
     예: 한쪽은 문장이 길고 자조적, 다른 쪽은 짧고 감정 단어를 쓰지 않는다.
  ② 서로의 말을 받아쳐야 한다. 각자 자기 할 말만 하면 티키타카가 아니라
     교대 독백이다. 상대의 마지막 단어를 물고 들어가라.
  ③ 대화에 걸린 판돈이 있어야 한다. 잡담은 티키타카가 아니다.
     둘 중 하나가 반드시 이겨야 하는 상황을 깔아라.
- 티키타카 안에서 정보가 전진해야 한다. 웃기기만 하고 상황이 그대로면
  씬을 삭제해도 시나리오가 성립한다 — 그건 실패한 티키타카다.

[5. 1막 종료 시점 설치 완료 체크 — 6항목]
□ A의 goal이 구체적 행동으로 선언되었는가
□ B의 goal이 구체적 행동으로 선언되었는가 (A의 세계 밖에서)
□ A의 flaw가 행동으로 드러났는가
□ B의 flaw가 행동으로 드러났는가
□ 두 사람이 서로를 필요로 할 수밖에 없는 거래 조건이 깔렸는가
□ 티키타카 씬이 2개 이상 있는가 (각 6회 교대 이상)
★ 6항목 중 하나라도 비어 있으면 2막에서 관계가 설득되지 않는다.

[1막 금지 패턴]
❌ 상대역이 주인공의 공간에만 등장 — 자기 세계가 없는 인물
❌ 첫 만남 전에 상대역의 결핍이 한 번도 안 나옴
❌ 두 사람이 같은 말투로 말함 — 티키타카가 성립하지 않음
❌ 첫 대면이 정중한 인사로 끝남 — 충돌이 없으면 미트큐트가 아니다
""".strip()

ACT1_BUDDY = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 1막 셋업 강제 — 버디 (v3.9.0) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1. 공동 주인공 — 두 사람 모두 결핍을 갖는다]
- 한쪽이 조력자로 축소되면 버디가 아니다. 둘 다 goal / need / flaw를 갖는다.
- 두 사람의 방법론이 정반대여야 한다. 같은 목표, 다른 수단.

[2. 강제 결합 이전 각자의 세계]
- 두 사람이 묶이기 전에 각자 자기 세계에서 일하는 씬을 최소 2씬씩.
- 각자의 방식이 그 세계에서는 잘 작동한다는 것을 먼저 보여라.
  그래야 상대와 묶였을 때 왜 마찰이 나는지 이해된다.

[3. 티키타카 — 마찰 대사]
- 1막에 두 사람이 6회 이상 연속으로 주고받는 씬 최소 2씬.
- 버디의 티키타카는 호감이 아니라 마찰이다. 서로를 무능하다고 판단하는
  대사가 오가야 한다.

[4. 1막 종료 체크]
□ 두 사람 각각의 goal이 선언되었는가
□ 두 사람의 방법론 대비가 행동으로 보였는가
□ 헤어질 수 없는 강제 결합 조건이 깔렸는가
□ 마찰 티키타카 2씬 이상
""".strip()

ACT1_ROMANCE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 1막 셋업 강제 — 로맨스/멜로 (v3.9.0) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1. 공동 주인공 선언]
- 상대역이 기획 자료에서 antagonist로 분류되어 있어도 공동 주인공으로 다룬다.
- 두 사람 각각 goal / need / flaw를 갖는다.

[2. 첫 만남 이전 각자의 세계]
- 두 사람 각각 자기 거점 권역에서 상대 없이 행동하는 씬 최소 2씬씩.
- 각자의 결핍이 행동으로 드러나야 한다. 설명 대사 금지.
- 두 세계의 규칙이 서로 반대일수록 만남의 낙차가 커진다.

[3. 첫 만남 — Beat 2~4]
- 만남의 순간에 두 사람의 목표가 어긋나 있어야 한다.
- 첫 만남에서 서로에 대해 틀린 결론을 내려야 한다.

[4. 1막 종료 체크]
□ 두 사람 각각의 goal / flaw가 행동으로 드러났는가
□ 상대역이 자기 세계에서 단독으로 행동하는 씬이 3씬 이상인가
□ 두 사람을 계속 만나게 만드는 구조적 이유가 깔렸는가
""".strip()

ACT1_GENERIC = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 1막 셋업 강제 (v3.9.0) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1막 종료 시점 설치 완료 체크]
□ 주인공의 goal이 구체적 행동으로 선언되었는가
□ 주인공의 flaw가 설명이 아니라 행동으로 드러났는가
□ 적대 세력의 존재와 능력이 관객에게 확인되었는가
□ 주인공이 되돌아갈 수 없게 만드는 문턱 사건이 발생했는가
★ 하나라도 비어 있으면 2막의 갈등이 설득되지 않는다.
""".strip()


def build_act1_setup_rule(genre: str) -> str:
    """장르별 1막 셋업 규칙 반환. 로코 우선 → 버디 → 로맨스 → 일반."""
    if is_romcom(genre) or is_screwball(genre):
        return ACT1_ROMCOM
    if is_buddy(genre):
        return ACT1_BUDDY
    if is_romance(genre):
        return ACT1_ROMANCE
    return ACT1_GENERIC


def needs_act1_setup(beat_number: int) -> bool:
    """1막(Beat 1~5) 여부."""
    try:
        return 1 <= int(beat_number) <= 5
    except (TypeError, ValueError):
        return False


# ═══════════════════════════════════════════════════════════
# 8. 비트 집필용 티키타카 강제 블록 (로코/버디 — 전 막)
# ═══════════════════════════════════════════════════════════

TIKITAKA_BEAT_RULE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━
★★★ 티키타카 대사 엔진 — 로코/버디 전 비트 적용 (v3.9.0) ★★★
━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 이 장르에서 관객이 표를 사는 이유는 사건이 아니라 두 사람의 대화다. ★

[비트당 최소 요구]
- 두 주인공이 동석하는 비트에는 6회 이상 연속 교대되는 대사 구간을
  최소 1개 배치하라. (A→B→A→B… 화자 교대가 끊기지 않는 상태)

[티키타카 3조건 — 하나라도 빠지면 성립하지 않는다]
① 말버릇 대비 — 화자 이름을 가리고 읽어도 누가 한 말인지 구분되어야 한다.
   두 사람의 문장 길이·어휘·감정 표현 방식이 달라야 한다.
② 받아치기 — 상대의 마지막 단어나 논리를 물고 들어가라.
   각자 자기 할 말만 하면 티키타카가 아니라 교대 독백이다.
③ 판돈 — 대화에 걸린 것이 있어야 한다. 둘 중 하나가 반드시 이겨야 하는
   상황을 먼저 깔고 대사를 시작하라.

[정보 전진 원칙]
티키타카가 끝났을 때 상황이 시작 전과 같으면 그 씬은 삭제 가능하다.
웃겼는지가 아니라 무엇이 바뀌었는지로 판정하라.
- 관계의 거리 / 정보의 공개 / 판돈의 크기 — 셋 중 하나는 반드시 움직여야 한다.

[금지]
❌ 두 사람이 같은 리듬으로 말하는 대사
❌ 한쪽이 질문만 하고 다른 쪽이 답만 하는 인터뷰형 대화
❌ 상대의 말을 받지 않고 각자 자기 주제를 밀고 나가는 대화
""".strip()


def build_tikitaka_block(genre: str) -> str:
    """로코·버디·스크루볼일 때만 티키타카 블록 반환."""
    if is_romcom(genre) or is_screwball(genre) or is_buddy(genre):
        return TIKITAKA_BEAT_RULE
    return ""


# ═══════════════════════════════════════════════════════════
# 9. 통합 빌더 — prompt.py에서 호출하는 단일 진입점
# ═══════════════════════════════════════════════════════════

def build_scene_sequence_plan_block(genre: str, act: str = "",
                                    confined: bool = False,
                                    venue_hints: list = None) -> str:
    """씬 플랜 프롬프트용 통합 블록 (권역 규칙 + 1막이면 셋업 규칙)."""
    parts = [build_venue_rule_block(genre, confined=confined,
                                    act=act, venue_hints=venue_hints)]
    if act and ("1막" in act or "act 1" in act.lower()):
        parts.append(build_act1_setup_rule(genre))
    return "\n\n".join(p for p in parts if p)


def build_scene_sequence_beat_block(genre: str, beat_number: int,
                                    previous_scene_text: str = "",
                                    confined: bool = False,
                                    venue_hints: list = None,
                                    full_text_so_far: str = "") -> str:
    """비트 집필 프롬프트용 통합 블록
    (직전 씬 앵커 + 1막 셋업 + 티키타카)."""
    parts = []
    anchor = build_prev_scene_anchor(
        previous_scene_text, genre=genre, confined=confined,
        venue_hints=venue_hints, full_text_so_far=full_text_so_far,
    )
    if anchor:
        parts.append(anchor)
    if needs_act1_setup(beat_number):
        parts.append(build_act1_setup_rule(genre))
    tk = build_tikitaka_block(genre)
    if tk:
        parts.append(tk)
    return "\n\n".join(p for p in parts if p)
