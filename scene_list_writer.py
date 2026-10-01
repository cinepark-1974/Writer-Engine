# ─────────────────────────────────────────────────────────────
# BLUE JEANS Story Engine — Scene List Writer Pack v1.0.0
# scene_list_writer.py — 씬리스트 기준 집필 레이어 (로더 + 파이썬 검증)
# © 2026 BLUE JEANS PICTURES
#
# v1.0.0 (2026-10-01):
# - Mr. MOON 요청: "비트 단위 자유 집필에서 씬리스트 기준 집필로 전환한다.
#   CREATOR가 확정한 것을 벗어나지 못하게 한다."
# - Creator Engine v2.8.2 writer_handoff_v28 수신 (실제 샘플 「부활」로 검증).
#   여섯 항목: scene_list_locked / sequences / speech_matrix /
#             character_voice / character_core / state_axes
#   참조표: dialogue_modes / speech_registers / time_slots
#   보조: structure_story.storyline (시퀀스별 요약·갈등·훅)
#
# [설계 원칙]
# 1) 세는 주체와 어기는 주체를 분리한다 (scene_sequence.py와 같은 원칙).
#    씬리스트 이탈(W3)·말투 어긋남(W4)은 AI가 아니라 파이썬이 판정한다.
# 2) 말투 판별은 종결어미만 보는 1차 검출이다. 최종 판단은 작가.
#    - 혼용 관계는 판정에서 제외한다.
#    - 하대는 반말 어미로 판정한다.
#    - 셋 이상 등장 씬에서 상대가 불분명하면 판정 불가로 둔다.
#    - 하오체·사투리 등 이분법에 들지 않는 어미는 위반이 아니라 판정 불가.
# 3) prompt.py를 import 하지 않는다 (순환 참조 방지).
# ─────────────────────────────────────────────────────────────

import re
import copy

MODULE_NAME = "BLUE JEANS Story Engine — Scene List Writer Pack"
MODULE_VERSION = "v1.0.0"
MODULE_BUILD_DATE = "2026-10-01"


# ═══════════════════════════════════════════════════════════
# 1. 로더 (W1)
# ═══════════════════════════════════════════════════════════

def _project_of(creator_json: dict) -> dict:
    """Creator 저장 파일은 {"_meta":..., "project": {...}} 구조.
    project 래퍼가 없는 경우도 허용한다."""
    if not isinstance(creator_json, dict):
        return {}
    proj = creator_json.get("project")
    return proj if isinstance(proj, dict) else creator_json


def load_scene_list_handoff(creator_json: dict) -> dict:
    """Creator JSON에서 씬리스트 집필용 데이터를 읽는다.

    반환:
      {"available": bool, "reason": str, ...데이터}
    available=False면 기존 15비트 방식으로 집필한다.
    """
    proj = _project_of(creator_json)
    meta = creator_json.get("_meta", {}) if isinstance(creator_json, dict) else {}
    out = {
        "available": False,
        "reason": "",
        "creator_version": meta.get("engine_version", ""),
        "creator_stage": meta.get("stage", ""),
    }

    handoff = proj.get("writer_handoff_v28")
    if not isinstance(handoff, dict):
        out["reason"] = "Creator JSON에 writer_handoff_v28 없음 (씬리스트 잠금 전 단계 또는 구버전)"
        return out

    locked = handoff.get("scene_list_locked") or {}
    scenes = locked.get("scenes") if isinstance(locked, dict) else None
    if not scenes:
        # 보조 경로 — project.scene_list.locked
        sl = proj.get("scene_list") or {}
        scenes = sl.get("locked") if isinstance(sl, dict) else None
    if not scenes:
        out["reason"] = "잠금된 씬리스트가 비어 있음"
        return out

    sequences = handoff.get("sequences") or []
    if not sequences:
        # 시퀀스 정보가 없으면 씬의 seq 값으로 재구성
        seq_nos = sorted({int(s.get("seq", 0)) for s in scenes if s.get("seq")})
        sequences = [{"seq": n, "act": 0, "label": "", "goal": "", "beats": [],
                      "scene_budget": 0, "pages": ""} for n in seq_nos]

    # 보조 — 시퀀스별 storyline (요약·갈등·감정·훅)
    storyline = {}
    ss = proj.get("structure_story") or {}
    for item in (ss.get("storyline") or []):
        try:
            storyline[int(item.get("seq"))] = item
        except (TypeError, ValueError):
            pass

    out.update({
        "available": True,
        "structure_type": handoff.get("structure_type") or proj.get("structure_type", ""),
        "variant": locked.get("variant", "") if isinstance(locked, dict) else "",
        "locked_at": locked.get("locked_at", "") if isinstance(locked, dict) else "",
        "scenes": copy.deepcopy(scenes),
        "sequences": copy.deepcopy(sequences),
        "storyline": storyline,
        "speech_matrix": copy.deepcopy(handoff.get("speech_matrix") or []),
        "character_voice": copy.deepcopy(handoff.get("character_voice") or []),
        "character_core": copy.deepcopy(handoff.get("character_core") or []),
        "state_axes": copy.deepcopy(handoff.get("state_axes") or {}),
        "dialogue_modes": copy.deepcopy(handoff.get("dialogue_modes") or {}),
        "speech_registers": copy.deepcopy(handoff.get("speech_registers") or {}),
    })
    return out


def handoff_summary(h: dict) -> str:
    """UI 표시용 한 줄 요약."""
    if not h or not h.get("available"):
        return "씬리스트 없음"
    return (f"{len(h['scenes'])}씬 / {len(h['sequences'])}시퀀스 · "
            f"구조 {h.get('structure_type') or '-'} · {h.get('variant') or '-'}"
            f" · 잠금 {h.get('locked_at') or '-'}")


# ═══════════════════════════════════════════════════════════
# 2. 이름 정규화 / 별칭
# ═══════════════════════════════════════════════════════════

def normalize_name(name: str) -> str:
    """'엄만복 (58세)' → '엄만복', '서광명 목사 (52세, 교단 2인자)' → '서광명 목사'."""
    s = re.sub(r"\(.*?\)", "", str(name or ""))
    return re.sub(r"\s+", " ", s).strip()


def _squash(s: str) -> str:
    return re.sub(r"[\s'\"‘’“”·.,]", "", str(s or ""))


def _all_canonical_names(h: dict) -> list:
    names = []
    for m in h.get("speech_matrix", []):
        for k in ("from", "to"):
            n = normalize_name(m.get(k, ""))
            if n and n not in names:
                names.append(n)
    for c in h.get("character_voice", []) + h.get("character_core", []):
        n = normalize_name(c.get("name", ""))
        if n and n not in names:
            names.append(n)
    for s in h.get("scenes", []):
        for c in s.get("characters", []):
            n = normalize_name(c)
            if n and n not in names:
                names.append(n)
    return names


_GENERIC_ADDRESS = {"당신", "너", "자네", "형", "언니", "누나", "오빠", "엄마", "아빠",
                    "아버지", "어머니", "아부지", "선생님", "사장님", "목사님", "우리아들"}


def build_alias_map(h: dict) -> dict:
    """정규 이름 → 별칭 집합.
    별칭: 전체 이름 / 성+이름 / 이름(성 제외) / 성+직함 / 말투표의 호칭(address).
    씬 대사의 화자 표기('만복', '서목사' 등)를 정규 이름으로 되돌리는 데 쓴다.
    """
    amap = {}
    for full in _all_canonical_names(h):
        tokens = full.split(" ")
        base = tokens[0]
        aliases = {full, base, _squash(full)}
        if len(base) == 3:              # 한국식 3음절 이름 — 성 1음절 가정
            aliases.add(base[1:])
        for title in tokens[1:]:
            aliases.add(base[0] + title)   # 서 + 목사 → 서목사
            aliases.add(base + title)
        amap[full] = aliases
    # 말투표의 호칭 → 받는 사람(to)의 별칭
    for m in h.get("speech_matrix", []):
        to = normalize_name(m.get("to", ""))
        addr = str(m.get("address", "") or "")
        for part in re.split(r"또는|→|,|/", addr):
            p = _squash(part)
            # 일반 대명사·긴 설명문은 별칭에서 제외 (화자 표기로 쓰이지 않음)
            if p in _GENERIC_ADDRESS or len(p) > 6:
                continue
            if p and to in amap:
                amap[to].add(p)
                # 호격 조사 제거 ('두철아' → '두철')
                if len(p) >= 2 and p[-1] in "아야":
                    amap[to].add(p[:-1])
    return amap


def resolve_name(label: str, candidates: list, amap: dict) -> str:
    """화자 표기를 후보 정규 이름 중 하나로 해석. 실패하면 ''."""
    lab = _squash(normalize_name(label))
    if not lab:
        return ""
    hits = [c for c in candidates if lab in {_squash(a) for a in amap.get(c, {c})}]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        # 포함 관계 보조 판정 (예: '광명' ⊂ '서광명목사')
        hits = [c for c in candidates if len(lab) >= 2 and lab in _squash(c)]
        if len(hits) == 1:
            return hits[0]
    return ""


# ═══════════════════════════════════════════════════════════
# 3. 시퀀스 / 씬 조회
# ═══════════════════════════════════════════════════════════

def seq_numbers(h: dict) -> list:
    return [int(q.get("seq")) for q in h.get("sequences", [])]


def get_sequence(h: dict, seq_no: int) -> dict:
    for q in h.get("sequences", []):
        if int(q.get("seq")) == int(seq_no):
            return q
    return {}


def get_seq_scenes(h: dict, seq_no: int) -> list:
    return [s for s in h.get("scenes", []) if int(s.get("seq", 0)) == int(seq_no)]


def act_of_seq(h: dict, seq_no: int) -> int:
    q = get_sequence(h, seq_no)
    try:
        a = int(q.get("act") or 0)
    except (TypeError, ValueError):
        a = 0
    return a


def format_heading(scene: dict) -> str:
    """씬리스트 항목 → 한국 표준 씬 헤딩."""
    ie = (scene.get("int_ext") or "").strip().upper()
    ie = f"{ie}. " if ie else ""
    return f"S#{scene.get('no')}. {ie}{scene.get('location', '')} — {scene.get('time', '')}"


def format_scene_line(scene: dict) -> str:
    chars = ", ".join(normalize_name(c) for c in scene.get("characters", [])) or "-"
    return (f"{format_heading(scene)}\n"
            f"   · 등장: {chars}\n"
            f"   · 대사 방식: {scene.get('dialogue_mode') or '서브텍스트'}\n"
            f"   · 내용: {scene.get('summary', '')}")


# ═══════════════════════════════════════════════════════════
# 4. 프롬프트 재료 블록
# ═══════════════════════════════════════════════════════════

_REG_ORDER = ("하대", "반말", "존대", "혼용")


def _register_from_text(text: str) -> str:
    """'하대 — 이름 호칭…' / '반말 유지하되…' / '존대를 유지하지만…' → 첫 등장 말투."""
    t = str(text or "")
    best, pos = "", 10 ** 9
    for r in _REG_ORDER:
        i = t.find(r)
        if 0 <= i < pos:
            best, pos = r, i
    return best


def effective_register(entry: dict, beat: int) -> tuple:
    """(말투, 호칭/메모, 전환 적용 여부). 씬 비트가 전환 비트 이상이면 전환 후 말투."""
    reg = entry.get("register", "")
    sb = entry.get("shift_beat") or 0
    try:
        sb = int(sb)
    except (TypeError, ValueError):
        sb = 0
    if sb and beat and int(beat) >= sb and entry.get("shift_to"):
        shifted = _register_from_text(entry.get("shift_to", "")) or reg
        return shifted, entry.get("shift_to", ""), True
    return reg, entry.get("address", ""), False


def scene_pairs(h: dict, scene: dict) -> list:
    """이 씬 등장인물끼리의 말투표 항목만 추린다 (W4)."""
    present = [normalize_name(c) for c in scene.get("characters", [])]
    out = []
    for m in h.get("speech_matrix", []):
        f, t = normalize_name(m.get("from", "")), normalize_name(m.get("to", ""))
        if f in present and t in present and f != t:
            out.append(m)
    return out


def build_speech_table_for_scene(h: dict, scene: dict) -> str:
    beat = scene.get("beat") or 0
    lines = []
    for m in scene_pairs(h, scene):
        reg, note, shifted = effective_register(m, beat)
        f, t = normalize_name(m["from"]), normalize_name(m["to"])
        if shifted:
            lines.append(f"     - {f} → {t}: {reg} (전환 후: {note} / 계기: {m.get('shift_cause', '')})")
        else:
            lines.append(f"     - {f} → {t}: {reg} · 호칭 '{note}'")
    return "\n".join(lines) if lines else "     - (말투표 해당 쌍 없음)"


def build_voice_block(h: dict, names: list) -> str:
    """시퀀스 등장인물의 기본 말투·사투리 설정."""
    lines = []
    for c in h.get("character_voice", []):
        n = normalize_name(c.get("name", ""))
        if n not in names:
            continue
        od = c.get("origin_dialect") or {}
        dial = ""
        if od.get("dialect"):
            dial = (f" / 사투리: {od.get('dialect')}(강도 {od.get('strength', '-')}) — "
                    f"{od.get('trigger', '')}")
        lines.append(f"  · {n}: {c.get('base_register', '')}{dial}")
    return "\n".join(lines)


def build_core_block(h: dict, names: list) -> str:
    lines = []
    for c in h.get("character_core", []):
        n = normalize_name(c.get("name", ""))
        if n not in names:
            continue
        lines.append(f"  · {n}\n"
                     f"     결함: {c.get('flaw', '')}\n"
                     f"     모순: {c.get('contradiction', '')}\n"
                     f"     상처: {c.get('wound_event', '')}")
    return "\n".join(lines)


def build_state_block(h: dict, beats: list) -> str:
    sa = h.get("state_axes") or {}
    axes = sa.get("axes") or []
    if not axes:
        return ""
    ax_names = [f"{a.get('positive', '')}↔{a.get('negative', '')}" for a in axes]
    lines = ["  축: " + " / ".join(ax_names)]
    for t in sa.get("targets") or []:
        if t.get("beat") in beats:
            lines.append(f"  · 비트 {t.get('beat')}: 주인공 {t.get('protagonist')} / "
                         f"적대자 {t.get('antagonist')} — {t.get('cause', '')}")
    return "\n".join(lines)


def seq_character_names(h: dict, seq_no: int) -> list:
    names = []
    for s in get_seq_scenes(h, seq_no):
        for c in s.get("characters", []):
            n = normalize_name(c)
            if n not in names:
                names.append(n)
    return names


# ═══════════════════════════════════════════════════════════
# 5. 원고 파싱
# ═══════════════════════════════════════════════════════════

_HEAD_RE = re.compile(
    r"^\s*S#\s*(\d+)\s*[.．]?\s*"
    r"(?:(INT\s*/\s*EXT|EXT\s*/\s*INT|INT|EXT|I/E)\s*[.．]?\s*)?"
    r"(.*?)\s*(?:[—–]|\s-\s)\s*(.+?)\s*$",
    re.IGNORECASE,
)
_HEAD_LOOSE_RE = re.compile(r"^\s*S#\s*(\d+)\b(.*)$")
_NOTES_RE = re.compile(r"<WRITER_NOTES_BEGIN>.*?(?:<WRITER_NOTES_END>|$)", re.S)


_CHECK_TAG_RE = re.compile(r"<((?:GENRE|HELPER)_[A-Z_]*)>[\s\S]*?</\1>", re.S)


def strip_notes(text: str) -> str:
    """내부 메모 제거 — WRITER_NOTES + 장르/조력자 자가검증 태그(_HORROR 등 접미사 포함)."""
    t = _NOTES_RE.sub("", text or "")
    t = _CHECK_TAG_RE.sub("", t)
    return t


def parse_scenes(text: str) -> list:
    """원고 → [{no, int_ext, location, time, heading, body, start, end}]
    start/end는 원문 내 줄 인덱스 (씬 교체용)."""
    body_text = strip_notes(text)
    lines = body_text.split("\n")
    heads = []
    for i, ln in enumerate(lines):
        m = _HEAD_RE.match(ln)
        if m:
            heads.append((i, int(m.group(1)), (m.group(2) or "").upper().replace(" ", ""),
                          m.group(3).strip(), m.group(4).strip(), ln.strip()))
            continue
        m2 = _HEAD_LOOSE_RE.match(ln)
        if m2:
            heads.append((i, int(m2.group(1)), "", m2.group(2).strip(" .—-"), "", ln.strip()))
    out = []
    for k, (i, no, ie, loc, tm, head) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out.append({"no": no, "int_ext": ie, "location": loc, "time": tm,
                    "heading": head, "body": "\n".join(lines[i + 1:j]).strip("\n"),
                    "start": i, "end": j})
    return out


def get_scene_text(text: str, no: int) -> str:
    lines = strip_notes(text).split("\n")
    for s in parse_scenes(text):
        if s["no"] == int(no):
            return "\n".join(lines[s["start"]:s["end"]]).strip("\n")
    return ""


def replace_scene_text(text: str, no: int, new_scene: str) -> str:
    """원고에서 S#no 한 씬만 교체. 내부 메모는 버린다(본문만 남김)."""
    lines = strip_notes(text).split("\n")
    for s in parse_scenes(text):
        if s["no"] == int(no):
            new_lines = strip_notes(new_scene).strip("\n").split("\n")
            tail = lines[s["end"]:]
            mid = new_lines + (["", ""] if tail else [])   # 씬 사이 빈 줄 2개 유지
            return "\n".join(lines[:s["start"]] + mid + tail).rstrip() + "\n"
    return text


def last_scene_text(text: str) -> str:
    sc = parse_scenes(text)
    if not sc:
        return ""
    return get_scene_text(text, sc[-1]["no"])


# ═══════════════════════════════════════════════════════════
# 6. W3 — 씬리스트 대조
# ═══════════════════════════════════════════════════════════

def _norm_place(s: str) -> str:
    return re.sub(r"[\s.,·()\-—–/]", "", str(s or "")).lower()


def _place_ok(expected: str, actual: str) -> bool:
    e, a = _norm_place(expected), _norm_place(actual)
    return bool(e) and bool(a) and (e == a or e in a or a in e)


def verify_against_scene_list(text: str, h: dict, seq_no: int) -> dict:
    """원고를 씬리스트와 대조. 이탈 씬 번호와 사유를 반환."""
    expected = get_seq_scenes(h, seq_no)
    exp_by_no = {int(s["no"]): s for s in expected}
    exp_order = [int(s["no"]) for s in expected]
    actual = parse_scenes(text)
    issues = []

    seen = []
    for a in actual:
        no = a["no"]
        if no not in exp_by_no:
            issues.append({"no": no, "type": "추가", "detail": f"씬리스트에 없는 씬 — {a['heading']}"})
            continue
        if no in seen:
            issues.append({"no": no, "type": "중복", "detail": f"같은 번호가 두 번 등장 — {a['heading']}"})
            continue
        seen.append(no)
        e = exp_by_no[no]
        if not _place_ok(e.get("location", ""), a["location"]):
            issues.append({"no": no, "type": "장소 변경",
                           "detail": f"씬리스트 '{e.get('location')}' ↔ 원고 '{a['location'] or '(없음)'}'"})
        if e.get("time") and not _place_ok(e.get("time", ""), a["time"]):
            issues.append({"no": no, "type": "시간 변경",
                           "detail": f"씬리스트 '{e.get('time')}' ↔ 원고 '{a['time'] or '(없음)'}'"})
        eie = (e.get("int_ext") or "").upper()
        if eie and a["int_ext"] and eie != a["int_ext"]:
            issues.append({"no": no, "type": "INT/EXT 변경",
                           "detail": f"씬리스트 {eie} ↔ 원고 {a['int_ext']}"})

    for no in exp_order:
        if no not in seen:
            issues.append({"no": no, "type": "누락", "detail": f"씬리스트 씬 미집필 — {format_heading(exp_by_no[no])}"})

    order_actual = [n for n in seen if n in exp_by_no]
    order_expected = [n for n in exp_order if n in order_actual]
    if order_actual != order_expected:
        first_bad = next((a for a, e in zip(order_actual, order_expected) if a != e),
                         order_actual[0] if order_actual else 0)
        issues.append({"no": first_bad, "type": "순서 변경",
                       "detail": f"원고 순서 {order_actual} ↔ 씬리스트 {order_expected}"})

    issues.sort(key=lambda x: x["no"])
    return {"seq": seq_no, "expected": len(exp_order), "written": len(actual),
            "issues": issues, "ok": not issues}


# ═══════════════════════════════════════════════════════════
# 7. W4 — 말투 1차 검출
# ═══════════════════════════════════════════════════════════

_DIALOGUE_RE = re.compile(r"^([^\t\n]{1,20}?)\t+(\S.*)$")
_PAREN_RE = re.compile(r"\([^)]*\)")

# 순서가 중요 — 존대 → 판정 불가(하오체 등) → 반말
_JONDAE_END = ("니다", "니까", "세요", "셔요", "시죠", "지요", "십시오", "십쇼",
               "니더", "이소", "예", "요", "죠")
_NEUTRAL_END = ("시다", "시오", "구려", "구먼", "는가", "던가", "게나", "하오", "소", "오", "네")
_BANMAL_END = ("다고", "라고", "냐고", "자고", "잖아", "거든", "는데", "데이", "구나", "다니", "어", "아", "야", "지",
               "냐", "니", "자", "래", "게", "다", "라", "까", "해", "돼", "줘", "봐",
               "와", "워", "걸", "군", "노", "재", "나", "응", "겨", "랴", "마")


def _sentences(line: str) -> list:
    s = _PAREN_RE.sub(" ", line)
    s = re.sub(r"[\"'“”‘’]", "", s)
    parts = re.split(r"[.?!…~]+|\s—\s|—$", s)
    return [p.strip(" ,—-–") for p in parts if p.strip(" ,—-–")]


def classify_sentence(sent: str) -> str:
    w = re.sub(r"[^가-힣]+$", "", sent.strip())
    if not w or not re.search(r"[가-힣]$", w):
        return "불명"
    for e in _JONDAE_END:
        if w.endswith(e):
            return "존대"
    for e in _NEUTRAL_END:
        if w.endswith(e):
            return "불명"
    for e in _BANMAL_END:
        if w.endswith(e):
            return "반말"
    return "불명"


def classify_line(line: str) -> set:
    return {c for c in (classify_sentence(x) for x in _sentences(line)) if c != "불명"}


def _expected_class(reg: str) -> str:
    if reg in ("반말", "하대"):
        return "반말"
    if reg == "존대":
        return "존대"
    return ""   # 혼용·미지정 → 판정 제외


def check_speech_registers(text: str, h: dict, seq_no: int) -> dict:
    """대사 종결어미로 말투표와 어긋난 대사를 뽑는다 (1차 검출)."""
    amap = build_alias_map(h)
    exp_by_no = {int(s["no"]): s for s in get_seq_scenes(h, seq_no)}
    matrix = {}
    for m in h.get("speech_matrix", []):
        matrix[(normalize_name(m.get("from", "")), normalize_name(m.get("to", "")))] = m

    stats = {"checked": 0, "excluded_mixed": 0, "undecidable": 0, "unknown_speaker": 0}
    flags = []
    for sc in parse_scenes(text):
        exp = exp_by_no.get(sc["no"])
        if not exp:
            continue
        present = [normalize_name(c) for c in exp.get("characters", [])]
        beat = exp.get("beat") or 0
        for raw in sc["body"].split("\n"):
            m = _DIALOGUE_RE.match(raw.rstrip())
            if not m:
                continue
            label, line = m.group(1).strip(), m.group(2).strip()
            label = _PAREN_RE.sub("", label).strip()
            speaker = resolve_name(label, present, amap)
            if not speaker:
                stats["unknown_speaker"] += 1
                continue
            others = [p for p in present if p != speaker and (speaker, p) in matrix]
            if not others:
                stats["undecidable"] += 1
                continue
            regs = {}
            for o in others:
                r, _, _ = effective_register(matrix[(speaker, o)], beat)
                regs[o] = r
            classes = {_expected_class(r) for r in regs.values()}
            if len(others) > 1 and len(classes) > 1:
                stats["undecidable"] += 1      # 상대 불분명 + 말투가 상대마다 다름
                continue
            exp_cls = classes.pop()
            if not exp_cls:
                stats["excluded_mixed"] += 1
                continue
            got = classify_line(line)
            if not got:
                stats["undecidable"] += 1
                continue
            stats["checked"] += 1
            wrong = "반말" if exp_cls == "존대" else "존대"
            if wrong in got:
                target = others[0] if len(others) == 1 else "/".join(others)
                flags.append({
                    "no": sc["no"], "speaker": speaker, "to": target,
                    "expected": "/".join(sorted(set(regs.values()))),
                    "detected": "/".join(sorted(got)), "line": line,
                })
    return {"seq": seq_no, "flags": flags, "stats": stats}


# ═══════════════════════════════════════════════════════════
# 8. 보고서
# ═══════════════════════════════════════════════════════════

def format_scene_list_report(rep: dict) -> str:
    if rep.get("ok"):
        return f"시퀀스 {rep['seq']}: 씬리스트 {rep['expected']}씬 전부 일치."
    lines = [f"시퀀스 {rep['seq']}: 씬리스트 {rep['expected']}씬 / 원고 {rep['written']}씬 — 이탈 {len(rep['issues'])}건"]
    for i in rep["issues"]:
        lines.append(f"  S#{i['no']} [{i['type']}] {i['detail']}")
    return "\n".join(lines)


def format_speech_report(rep: dict) -> str:
    st = rep["stats"]
    head = (f"시퀀스 {rep['seq']}: 판정 {st['checked']}줄 · 어긋남 {len(rep['flags'])}줄 · "
            f"판정 불가 {st['undecidable']}줄 · 혼용 제외 {st['excluded_mixed']}줄 · "
            f"말투표 밖 화자 {st['unknown_speaker']}줄")
    lines = [head]
    for f in rep["flags"]:
        lines.append(f"  S#{f['no']} {f['speaker']} → {f['to']} (표: {f['expected']} / 대사: {f['detected']})  {f['line']}")
    return "\n".join(lines)
