# ─────────────────────────────────────────────────────────────
# BLUE JEANS Story Engine — Scene List Writer Pack v1.2.0
# scene_list_writer.py — 씬리스트 기준 집필 레이어 (로더 + 파이썬 검증)
# © 2026 BLUE JEANS PICTURES
#
# v1.2.0 (2026-10-25) — Writer Engine v4.3.0
# - check_scene_length() / sequence_length_target() / length_fix_instruction(): 씬별 최소 분량(600자, 인물 없는 씬 400자).
# - dead_beat_fix_instruction(short=True): 분량 미달 씬은 빈 지문을 지우지 않고 행동으로 바꾸게 한다.
# - precheck_scene_list(): Creator 잠금본 사전 점검 — 퇴장 인물 재등장 · 중복 의심 · 끼움 씬 · 요약 속 공간 이동.
#
# v1.1.0 (2026-10-24) — Writer Engine v4.2.0
# - 하위 씬(S#4-1) 지원: 공간이 바뀌면 씬을 나눈다. 원 번호는 Creator 씬리스트 그대로.
#   parse_scenes()에 sub 필드. get/replace_scene_text는 S#N 블록(하위 씬 포함) 단위.
#   verify_against_scene_list: 하위 씬 위치(원 번호 바로 뒤)·같은 공간 쪼개기 점검.
# - check_space_crossing(): 한 씬 안에서 인물이 다른 공간으로 넘어간 뒤 장면이 이어지는 곳.
# - check_dead_beats(): A40 빈 반응 지문(입 여닫기·멈춘다·보기만·무반응) 집계.
# - renumber_sequence_texts(): 다운로드용 최종 번호(S#1~N).
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
MODULE_VERSION = "v1.2.0"
MODULE_BUILD_DATE = "2026-10-25"


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
    r"^\s*S#\s*(\d+)(?:-(\d+))?\s*[.．]?\s*"
    r"(?:(INT\s*/\s*EXT|EXT\s*/\s*INT|INT|EXT|I/E)\s*[.．]?\s*)?"
    r"(.*?)\s*(?:[—–]|\s-\s)\s*(.+?)\s*$",
    re.IGNORECASE,
)
_HEAD_LOOSE_RE = re.compile(r"^\s*S#\s*(\d+)(?:-(\d+))?\b(.*)$")
_NOTES_RE = re.compile(r"<WRITER_NOTES_BEGIN>.*?(?:<WRITER_NOTES_END>|$)", re.S)


_CHECK_TAG_RE = re.compile(r"<((?:GENRE|HELPER)_[A-Z_]*)>[\s\S]*?</\1>", re.S)


def strip_notes(text: str) -> str:
    """내부 메모 제거 — WRITER_NOTES + 장르/조력자 자가검증 태그(_HORROR 등 접미사 포함)."""
    t = _NOTES_RE.sub("", text or "")
    t = _CHECK_TAG_RE.sub("", t)
    return t


def parse_scenes(text: str) -> list:
    """원고 → [{no, sub, int_ext, location, time, heading, body, start, end}]
    start/end는 원문 내 줄 인덱스 (씬 교체용).
    ★ v4.2.0 — 하위 씬(S#4-1)은 no=4, sub=1. 원 번호 씬은 sub=0."""
    body_text = strip_notes(text)
    lines = body_text.split("\n")
    heads = []
    for i, ln in enumerate(lines):
        m = _HEAD_RE.match(ln)
        if m:
            heads.append((i, int(m.group(1)), int(m.group(2) or 0),
                          (m.group(3) or "").upper().replace(" ", ""),
                          m.group(4).strip(), m.group(5).strip(), ln.strip()))
            continue
        m2 = _HEAD_LOOSE_RE.match(ln)
        if m2:
            heads.append((i, int(m2.group(1)), int(m2.group(2) or 0), "",
                          m2.group(3).strip(" .—-"), "", ln.strip()))
    out = []
    for k, (i, no, sub, ie, loc, tm, head) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out.append({"no": no, "sub": sub, "int_ext": ie, "location": loc, "time": tm,
                    "heading": head, "body": "\n".join(lines[i + 1:j]).strip("\n"),
                    "start": i, "end": j})
    return out


def _scene_block_range(text: str, no: int):
    """S#no 블록 = 원 번호 씬 + 바로 뒤에 붙은 하위 씬(S#no-1, S#no-2 …). (start, end) 또는 None."""
    sc = parse_scenes(text)
    for k, s in enumerate(sc):
        if s["no"] == int(no):
            end = s["end"]
            for t in sc[k + 1:]:
                if t["no"] == int(no) and t["sub"] > 0:
                    end = t["end"]
                else:
                    break
            return s["start"], end
    return None


def get_scene_text(text: str, no: int) -> str:
    """S#no 한 블록(하위 씬 포함)의 원고."""
    lines = strip_notes(text).split("\n")
    r = _scene_block_range(text, no)
    if not r:
        return ""
    return "\n".join(lines[r[0]:r[1]]).strip("\n")


def replace_scene_text(text: str, no: int, new_scene: str) -> str:
    """원고에서 S#no 한 블록(하위 씬 포함)만 교체. 내부 메모는 버린다(본문만 남김)."""
    lines = strip_notes(text).split("\n")
    r = _scene_block_range(text, no)
    if not r:
        return text
    new_lines = strip_notes(new_scene).strip("\n").split("\n")
    tail = lines[r[1]:]
    mid = new_lines + (["", ""] if tail else [])   # 씬 사이 빈 줄 2개 유지
    return "\n".join(lines[:r[0]] + mid + tail).rstrip() + "\n"


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
    subs = 0
    prev = None
    for a in actual:
        no = a["no"]
        # ★ v4.2.0 — 하위 씬: 공간이 바뀌어 나눈 씬. 원 번호 씬 바로 뒤에만, 다른 공간이어야 한다.
        if a.get("sub", 0) > 0:
            subs += 1
            if no not in exp_by_no:
                issues.append({"no": no, "type": "추가", "detail": f"씬리스트에 없는 번호의 하위 씬 — {a['heading']}"})
            elif not prev or prev["no"] != no:
                issues.append({"no": no, "type": "하위 씬 위치",
                               "detail": f"S#{no}-{a['sub']}가 S#{no} 바로 뒤에 있지 않음 — {a['heading']}"})
            elif _place_ok(prev["location"], a["location"]) and prev["int_ext"] == a["int_ext"]:
                issues.append({"no": no, "type": "같은 공간 쪼개기",
                               "detail": f"S#{no}-{a['sub']}가 앞 씬과 같은 공간 '{a['location']}' — 공간이 바뀔 때만 나눈다"})
            prev = a
            continue
        prev = a
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
    return {"seq": seq_no, "expected": len(exp_order), "written": len(actual) - subs,
            "subs": subs, "issues": issues, "ok": not issues}


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
    sub_t = f" · 공간 분할 하위 씬 {rep['subs']}개" if rep.get("subs") else ""
    if rep.get("ok"):
        return f"시퀀스 {rep['seq']}: 씬리스트 {rep['expected']}씬 전부 일치{sub_t}."
    lines = [f"시퀀스 {rep['seq']}: 씬리스트 {rep['expected']}씬 / 원고 {rep['written']}씬{sub_t} — 이탈 {len(rep['issues'])}건"]
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


# ═══════════════════════════════════════════════════════════
# 9. ★ v4.2.0 — 공간 횡단 점검 · 빈 반응 지문 점검 · 최종 번호
#    세는 주체(파이썬)와 쓰는 주체(AI)를 분리한다. 표시만 하고 자동 수정하지 않는다.
# ═══════════════════════════════════════════════════════════

_SENT_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+")
_SUBJ_RE = re.compile(r"^([가-힣A-Za-z][가-힣A-Za-z\s]{0,8}?)(?:이|가|은|는)\s")
_ENTER_RE = re.compile(r"(?:안으로\s*)?(?:들어간다|들어선다)\.?$")
_EXIT_RE = re.compile(r"(?:^|[\s,])(?:밖으로\s*)?(?:나간다|빠져나간다)\.?$")


def _action_sentences(body: str):
    """씬 본문 → [(줄 번호, 문장)] — 대사 줄은 제외."""
    out = []
    for li, raw in enumerate((body or "").split("\n")):
        ln = raw.strip()
        if not ln or _DIALOGUE_RE.match(raw.rstrip()) or ln.startswith(("[", "INSERT", "<", "CUT TO", "(")):
            continue
        for s in _SENT_SPLIT_RE.split(ln):
            s = s.strip()
            if s:
                out.append((li, s))
    return out


def _subject_of(sent: str) -> str:
    m = _SUBJ_RE.match(sent)
    return normalize_name(m.group(1).strip()) if m else ""


def check_space_crossing(text: str, names: list = None) -> list:
    """한 씬 안에서 인물이 다른 공간으로 넘어간 뒤에도 그 인물의 장면이 이어지는 곳.
    (예: EXT 골목 씬에서 '중이 문을 열고 들어간다.' 다음에 중의 대사가 계속됨)
    판정은 '넘어간 인물의 대사가 같은 씬에서 이어지는가'만 본다 (지문 언급은 회상·관계절 오탐이 많다).
    → 공간이 바뀌었으니 하위 씬(S#N-1)으로 나눠야 한다는 표시.
    names를 주면 그 인물만 주어로 본다 (실·연기 같은 사물 주어 오탐 차단)."""
    flags = []
    for sc in parse_scenes(text):
        ie = sc["int_ext"]
        lines = sc["body"].split("\n")
        sents = _action_sentences(sc["body"])
        for idx, (li, sent) in enumerate(sents):
            crossing = (ie == "EXT" and _ENTER_RE.search(sent)) or (ie == "INT" and _EXIT_RE.search(sent))
            if not crossing:
                continue
            subj = _subject_of(sent)
            if not subj or (names and subj not in names):
                continue
            cont = False
            for raw in lines[li + 1:]:
                m = _DIALOGUE_RE.match(raw.rstrip())
                if m and normalize_name(_PAREN_RE.sub("", m.group(1))) == subj:
                    cont = True
                    break
            if cont:
                label = f"S#{sc['no']}" + (f"-{sc['sub']}" if sc.get("sub") else "")
                flags.append({"no": sc["no"], "label": label, "subject": subj, "line": sent,
                              "heading": sc["heading"]})
    return flags


# ── 빈 반응 지문 (A40) ──
_DB_MOUTH_RE = re.compile(r"입을\s*(?:연다|열었다|열다|열고|열려|다문다|다물|닫는다|닫았다|닫고)|입술(?:이|만)\s*(?:움직|달싹|떨)")
_DB_STOP_RE = re.compile(r"멈춘다\.?$")
_DB_LOOK_RE = re.compile(r"^[^,，]{0,30}(?:본다|바라본다|쳐다본다|돌아본다|내려다본다|올려다본다|들여다본다)\.?$")
_DB_NONACT_RE = re.compile(r"(?:대답하지 않는다|대답이 없다|아무 말도 하지 않는다|아무 말이 없다|말이 없다|움직이지 않는다)\.?$")

DEAD_BEAT_QUOTA = {"mouth": 0, "nonact": 1, "stop": 1, "look": 3}   # 시퀀스(또는 비트) 1회 집필당 허용
DEAD_BEAT_LABELS = {"mouth": "입 여닫기·입술만 움직임", "nonact": "무반응 선언", "stop": "멈춘다 단독", "look": "보기만 하는 문장"}


_BODY_SUBJ_RE = re.compile(r"^(?:[가-힣A-Za-z ]{1,8}의\s*)?(?:손|손가락|발|걸음|숨|입술|몸|눈|시선|어깨)(?:이|가|은|는)\s")


def _is_person_stop(sent: str, names: list) -> bool:
    """멈춘다의 주어가 사람(또는 사람의 몸)인가. 사물·현상의 멈춤은 호러 사건이라 제외(A40 예외)."""
    if _BODY_SUBJ_RE.match(sent) or not _SUBJ_RE.match(sent):
        return True                      # 몸의 멈춤, 또는 주어 없는 '멈춘다.'
    subj = _subject_of(sent)
    if not names:
        return True
    return any(subj.startswith(n) for n in names if n)


def check_dead_beats(text: str, names: list = None) -> dict:
    """A40 — 아무것도 바꾸지 않는 반응 지문을 센다.
    입 여닫기는 0회 허용, 나머지는 허용치를 넘는 것부터 표시. 연속된 '본다' 문장은 허용치와 무관하게 표시.
    names(인물 이름)를 주면 사물·현상의 '멈춘다'(바늘이 멈춘다)는 세지 않는다."""
    found = {k: [] for k in DEAD_BEAT_QUOTA}
    prev_look = None
    for sc in parse_scenes(text):
        label = f"S#{sc['no']}" + (f"-{sc['sub']}" if sc.get("sub") else "")
        for li, sent in _action_sentences(sc["body"]):
            kind = None
            if _DB_MOUTH_RE.search(sent):
                kind = "mouth"
            elif _DB_NONACT_RE.search(sent):
                kind = "nonact"
            elif _DB_STOP_RE.search(sent) and len(sent) <= 32 and _is_person_stop(sent, names):
                kind = "stop"
            elif _DB_LOOK_RE.match(sent):
                kind = "look"
            if kind:
                item = {"no": sc["no"], "label": label, "line": sent, "consecutive": False}
                if kind == "look" and prev_look and prev_look["label"] == label and prev_look["li"] == li:
                    item["consecutive"] = True
                found[kind].append(item)
                prev_look = {"label": label, "li": li} if kind == "look" else None
            else:
                prev_look = None
    flags = []
    for k, items in found.items():
        q = DEAD_BEAT_QUOTA[k]
        for i, it in enumerate(items):
            if i >= q or it["consecutive"]:
                flags.append(dict(it, kind=k, label_kind=DEAD_BEAT_LABELS[k]))
    flags.sort(key=lambda x: (x["no"], x["label"]))
    return {"counts": {k: len(v) for k, v in found.items()}, "flags": flags}


def format_dead_beat_report(rep: dict) -> str:
    c = rep["counts"]
    head = " · ".join(f"{DEAD_BEAT_LABELS[k]} {c[k]}" + (f"(허용 {DEAD_BEAT_QUOTA[k]})") for k in DEAD_BEAT_QUOTA)
    lines = [f"빈 반응 지문(A40): {head} — 표시 {len(rep['flags'])}건"]
    for f in rep["flags"][:60]:
        lines.append(f"  {f['label']} [{f['label_kind']}{' · 연속' if f['consecutive'] else ''}] {f['line']}")
    return "\n".join(lines)


def dead_beat_fix_instruction(flags: list, short: bool = False) -> str:
    """씬 다시 쓰기용 지시문 — 표시된 문장만 고치게 한다.
    ★ v4.3.0 short=True(이 씬이 최소 분량 미달)면 '지운다'를 쓰지 않고 행동으로 바꾸게 한다."""
    if not flags:
        return ""
    body = "\n".join(f"- {f['line']}" for f in flags)
    if short:
        how = ("이 씬은 최소 분량에 못 미친다. 지우지 말고, 각 문장을 상황을 바꾸는 행동으로 바꿔라 —\n"
               "소품의 위치·상태, 인물의 위치, 상대가 아는 정보 중 하나가 바뀌어야 한다.\n")
        keep = "나머지 대사·씬 구성은 바꾸지 마라.\n"
    else:
        how = ("각 문장을 둘 중 하나로 처리하라.\n"
               "① 지운다 — 앞뒤 행동·대사만으로 장면이 성립하면 지운다.\n"
               "② 상황을 바꾸는 행동으로 바꾼다 — 소품의 위치·상태, 인물의 위치, 상대가 아는 정보 중 하나가 바뀌어야 한다.\n")
        keep = "나머지 문장·대사·씬 구성은 한 글자도 바꾸지 마라.\n"
    return ("[A40 빈 반응 지문 정리 — 이 지시만 수행한다]\n"
            "아래 문장은 아무것도 바꾸지 않는 반응 지문이다. " + how + keep + body)


_RENUM_RE = re.compile(r"^(\s*)S#\s*\d+(?:-\d+)?(\s*[.．]?)", re.M)


def renumber_sequence_texts(done: dict, order: list) -> tuple:
    """★ v4.2.0 — 다운로드용 최종 번호. 하위 씬을 포함해 S#1부터 끝까지 다시 매긴다.
    반환: (새 dict, 전체 씬 수). 원본은 바꾸지 않는다."""
    counter = [0]

    def _sub(m):
        counter[0] += 1
        return f"{m.group(1)}S#{counter[0]}{m.group(2) or '.'}"
    out = {}
    for n in order:
        if n in done and done[n]:
            out[n] = _RENUM_RE.sub(_sub, done[n])
    return out, counter[0]


# ═══════════════════════════════════════════════════════════
# 10. ★ v4.3.0 — 분량 점검 (씬별 최소 분량)
#    「THE CRIMSON ROBE」 실측: 82씬 중 58씬이 600자 미만, 씬당 평균 502자.
#    원인 중 하나 — '행동' 방식 씬은 짧아도 된다는 문구(46/82씬이 행동 방식).
# ═══════════════════════════════════════════════════════════

SCENE_MIN_CHARS = 600          # 이름 있는 인물이 나오는 씬 (대사 방식 무관 — '행동' 씬도 같다)
SCENE_MIN_CHARS_NOCHAR = 400   # 이름 있는 인물이 없는 공간·현상 씬
SCENE_TARGET_CHARS = 700


def _body_len(body: str) -> int:
    """공백 포함 글자 수 — 줄바꿈·연속 공백은 한 칸으로 센다."""
    return len(re.sub(r"\s+", " ", body or "").strip())


def scene_min_chars(scene: dict) -> int:
    chars = [c for c in (scene.get("characters") or []) if str(c).strip()]
    return SCENE_MIN_CHARS if chars else SCENE_MIN_CHARS_NOCHAR


def sequence_length_target(h: dict, seq_no: int) -> dict:
    sc = get_seq_scenes(h, seq_no)
    return {"scenes": len(sc), "min_total": sum(scene_min_chars(s) for s in sc),
            "target_total": len(sc) * SCENE_TARGET_CHARS}


def check_scene_length(text: str, h: dict, seq_no: int) -> dict:
    """씬리스트 씬(하위 씬 포함 블록)마다 본문 글자 수를 세어 최소 분량 미달을 뽑는다."""
    parsed = parse_scenes(text)
    got = {}
    for s in parsed:
        got[s["no"]] = got.get(s["no"], 0) + _body_len(s["body"])
    short = []
    for e in get_seq_scenes(h, seq_no):
        n = int(e["no"])
        if n not in got:
            continue
        m = scene_min_chars(e)
        if got[n] < m:
            short.append({"no": n, "got": got[n], "min": m, "summary": e.get("summary", ""),
                          "mode": e.get("dialogue_mode", "")})
    tgt = sequence_length_target(h, seq_no)
    return {"seq": seq_no, "total": sum(got.values()), "short": short,
            "min_total": tgt["min_total"], "target_total": tgt["target_total"], "scenes": tgt["scenes"]}


def format_length_report(rep: dict) -> str:
    head = (f"분량: {rep['total']:,}자 / 목표 {rep['target_total']:,}자 (최소 {rep['min_total']:,}자) · "
            f"최소 분량 미달 {len(rep['short'])}씬")
    lines = [head]
    for s in rep["short"]:
        lines.append(f"  S#{s['no']} {s['got']}자 / 최소 {s['min']}자 — {s['summary'][:50]}")
    return "\n".join(lines)


def length_fix_instruction(item: dict) -> str:
    """씬 다시 쓰기용 — 분량 보강 지시. 빈 지문이 아니라 사건의 단계로 늘린다."""
    return (f"[분량 보강 — S#{item['no']} 현재 {item['got']}자 → 최소 {item['min']}자, 목표 {SCENE_TARGET_CHARS}자 안팎]\n"
            f"이 씬의 '내용': {item['summary']}\n"
            "늘리는 방법 — 이 사건을 단계로 나눠 화면에 보여라: 인물이 원하는 것을 시도한다 → 무엇이 막는다 →\n"
            "다른 방법을 쓴다 → 결과로 무언가가 바뀐다. 각 단계는 소품·위치·정보 중 하나를 바꾸는 행동과 대사로 쓴다.\n"
            "금지 — 빈 반응 지문(A40: 입 여닫기·멈춘다·보기만 하는 문장), 감정 설명, 풍경 나열로 늘리지 않는다.\n"
            "금지 — 씬리스트에 없는 사건·인물·장소를 더하지 않는다. 대사 방식이 '행동'이면 대사를 늘리지 말고 행동 단계를 늘린다.")


# ═══════════════════════════════════════════════════════════
# 11. ★ v4.3.0 — 씬리스트 사전 점검 (Creator 잠금본 안전망)
#    Writer는 씬리스트를 바꾸지 않는다. 집필 전에 작가에게 보여줄 뿐이다.
#    판정은 요약 문장 기반 1차 검출 — 최종 판단은 작가.
# ═══════════════════════════════════════════════════════════

_DEATH_RE = re.compile(r"죽고|죽는다|죽었|죽어\s|죽인다|숨진다|숨을 거둔|숨이 끊|사망|미라처럼|재처럼\s*부스러|재가 된다")
_DEAD_OK_RE = re.compile(r"회상|시신|혼|영정|환영|형체|사진|무덤|장례|기억|꿈")
_CROSS_SUM_RE = re.compile(r"들어간다|들어가|들어선다|나와|나온다|나간다|이동하던|이동한다|돌아오다|돌아온다|빠져나")
_FLASH_RE = re.compile(r"회상")
_YEAR_RE = re.compile(r"\d{4}년|\d+년\s*전")
_SUM_STOP = {"응우옛", "하고", "하며", "하자", "하는", "한다", "있다", "없다", "그리고", "다시", "순간", "앞에서", "위에", "속에서"}


def _sum_tokens(s: str, names: list) -> set:
    w = re.findall(r"[가-힣0-9]{2,}", s or "")
    w = [re.sub(r"(을|를|이|가|은|는|에서|에게|으로|로|와|과|의|도|만|에)$", "", x) for x in w]
    stop = _SUM_STOP | {n for n in names if n}
    return {x for x in w if len(x) >= 2 and x not in stop}


def _trigrams(s: str) -> set:
    t = re.sub(r"\s+", "", s or "")
    return {t[i:i + 3] for i in range(len(t) - 2)}


def _main_names(h: dict) -> list:
    names = set()
    for key in ("character_voice", "character_core"):
        for c in h.get(key) or []:
            n = normalize_name((c or {}).get("name", ""))
            if n:
                names.add(n)
    for s in h.get("scenes") or []:
        for c in s.get("characters") or []:
            n = normalize_name(c)
            if n:
                names.add(n)
    return sorted(names, key=len, reverse=True)


def precheck_scene_list(h: dict) -> dict:
    """잠긴 씬리스트를 집필 전에 점검한다.
    dead_reappear — 사망 표지 이후 회상·시신 표지 없이 다시 등장하는 인물
    duplicates    — 같은 사건으로 보이는 씬 쌍 (요약 유사도, 회상은 같은 연도·'N년 전')
    fillers       — 이름 있는 인물이 없고 앞뒤가 같은 공간인 끼움 씬
    crossings     — 요약 한 줄 안에서 공간을 넘나드는 씬"""
    scenes = [s for s in (h.get("scenes") or []) if isinstance(s, dict)]
    names = _main_names(h)
    out = {"dead_reappear": [], "duplicates": [], "fillers": [], "crossings": []}

    # 1) 퇴장 인물 재등장
    #   사망한 인물 판정: ① 'X의 시신' ② 사망 표지 뒤 관형형('쪼그라든 X') ③ 사망 표지 바로 앞 25자 안의 가장 가까운 이름
    #   재등장 예외: 그 씬이 회상이거나, 'X의 시신·혼·영정·사진·환영·형체'처럼 죽은 상태로 나올 때
    dead_at = {}
    for s in scenes:
        summ = s.get("summary", "") or ""
        no = int(s.get("no", 0))
        present = [normalize_name(c) for c in (s.get("characters") or [])]
        for nm, at in dead_at.items():
            if nm in present and no > at and not _FLASH_RE.search(summ) and \
                    not re.search(re.escape(nm) + r"의\s*(?:시신|혼|영정|사진|환영|형체|무덤|유품)", summ):
                out["dead_reappear"].append({"name": nm, "dead_at": at, "no": no, "summary": summ})
        if _FLASH_RE.search(summ):
            continue
        found = set()
        for nm in names:
            if re.search(re.escape(nm) + r"의\s*시신", summ):
                found.add(nm)
        for m in _DEATH_RE.finditer(summ):
            after = summ[m.end():m.end() + 20]
            am = re.match(r"\s*\S*[든된]\s+(.+)", after)
            hit = ""
            if am:
                hit = next((nm for nm in names if am.group(1).startswith(nm)), "")
            if not hit:
                window = summ[max(0, m.start() - 25):m.start()]
                pos = -1
                for nm in names:
                    p = window.rfind(nm)
                    if p > pos:
                        hit, pos = nm, p
            if hit:
                found.add(hit)
        for nm in found:
            dead_at.setdefault(nm, no)

    # 2) 중복 의심
    for i, a in enumerate(scenes):
        for b in scenes[i + 2:]:      # 바로 붙은 씬은 연속 장면일 수 있어 제외
            sa, sb = a.get("summary", ""), b.get("summary", "")
            fa, fb = bool(_FLASH_RE.search(sa)), bool(_FLASH_RE.search(sb))
            reason = ""
            if fa and fb:
                ya, yb = set(_YEAR_RE.findall(sa)), set(_YEAR_RE.findall(sb))
                if ya & yb:
                    reason = f"같은 과거 회상 ({', '.join(sorted(ya & yb))})"
            if not reason:
                ta, tb = _sum_tokens(sa, names), _sum_tokens(sb, names)
                j = len(ta & tb) / max(1, len(ta | tb))
                g = len(_trigrams(sa) & _trigrams(sb)) / max(1, len(_trigrams(sa) | _trigrams(sb)))
                if g >= 0.15 or j >= 0.30:
                    reason = f"요약 겹침 ({', '.join(sorted(ta & tb)[:5])})"
            if reason:
                out["duplicates"].append({"a": int(a["no"]), "b": int(b["no"]), "reason": reason,
                                          "sa": sa, "sb": sb})

    # 3) 끼움 씬 (이름 있는 인물 없음 + 앞뒤 씬이 같은 공간)
    def _key(s):
        return ((s.get("int_ext") or "").upper(), _norm_place(s.get("location", "")))
    for k in range(1, len(scenes) - 1):
        s = scenes[k]
        named = [c for c in (s.get("characters") or []) if normalize_name(c) in names]
        if named:
            continue
        if _key(scenes[k - 1]) == _key(scenes[k + 1]):
            out["fillers"].append({"no": int(s["no"]), "location": s.get("location", ""),
                                   "between": f"{scenes[k - 1].get('location', '')}", "summary": s.get("summary", "")})

    # 4) 요약 안의 공간 횡단
    for s in scenes:
        summ = s.get("summary", "") or ""
        m = _CROSS_SUM_RE.search(summ)
        if m and not _FLASH_RE.search(summ):
            out["crossings"].append({"no": int(s["no"]), "word": m.group(0), "heading": format_heading(s),
                                     "summary": summ})
    return out


def precheck_counts(rep: dict) -> int:
    return sum(len(rep.get(k) or []) for k in ("dead_reappear", "duplicates", "fillers", "crossings"))


def format_precheck_report(rep: dict) -> str:
    L = []
    if rep["dead_reappear"]:
        by = {}
        for x in rep["dead_reappear"]:
            by.setdefault((x["name"], x["dead_at"]), []).append(x["no"])
        L.append("■ 퇴장 인물 재등장 (사망 표지 이후 등장)")
        L += [f"  {nm} — S#{at}에서 사망 표지 → S#{', S#'.join(map(str, nos))}에 다시 등장" for (nm, at), nos in by.items()]
    if rep["duplicates"]:
        L.append("■ 중복 의심 (같은 사건·같은 회상)")
        L += [f"  S#{x['a']} ↔ S#{x['b']} — {x['reason']}" for x in rep["duplicates"]]
    if rep["fillers"]:
        L.append("■ 끼움 씬 (이름 있는 인물 없음 · 앞뒤가 같은 공간)")
        L += [f"  S#{x['no']} {x['location']} — {x['summary'][:45]}" for x in rep["fillers"]]
    if rep["crossings"]:
        L.append("■ 요약 한 줄 안에서 공간 이동 (집필 시 하위 씬으로 나뉠 수 있음)")
        L += [f"  S#{x['no']} '{x['word']}' — {x['heading']}" for x in rep["crossings"]]
    return "\n".join(L) if L else "이상 없음"
