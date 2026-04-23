# 👖 BLUE JEANS Writer Engine v3.1

> **AI 시나리오 집필 엔진** — Creator Engine v2.3+ 산출물 → 100씬 영화 시나리오 자동 생성
> BLUE JEANS PICTURES · [cinepark-1974](https://github.com/cinepark-1974)

---

## 한 줄 요약

**19회 클릭으로 100씬 영화 시나리오를 쓰는 엔진.** 장르 드라이브 5점 체크 + BJND 씬 강제 + 창작자 감성 3요소 + 엔딩 동적 분기로 **"장르 맛 + 작가의 서명 + 관객 신체 반응"**을 동시에 갖춘 시나리오를 생산한다.

---

## 흐름

```
Creator Engine v2.3+ 산출물 (JSON 또는 11칸 텍스트)
        ↓
   씬 플랜 (3회)     ← Sonnet
        ↓
 핵심 요소 추출 (1회)  ← Sonnet
        ↓
  비트별 집필 (15회)   ← Opus
        ↓
    TXT / DOCX (4개 Word 스타일)
```

---

## v3.1 주요 변경 (← v3.0)

| 신규 기능 | 설명 |
|----------|------|
| **Creator JSON 자동 로더** | Creator Engine v2.3+ 결과 JSON을 업로드하면 11개 입력칸이 자동으로 채워진다. |
| **BJND Scene Enforcer** | Creator가 설계한 Strategy/Cost를 매 비트에서 씬 레벨로 강제 집행. 비트 구간별 Cost 단계(암시→균열→실재손상→현실)를 자동 적용. |
| **Creator Sensibility 3요소** | PHYSICALITY(관객 신체 반응) / SILENCE(의도된 침묵) / PLANT AESTHETICS(씨앗의 미학)를 모든 비트에 주입. |
| **엔딩 규칙 동적 분기** | Creator의 `ending_payoff_type`을 읽어 엔딩 규칙을 분기. `internal_transformation`이면 "혼자 성장 엔딩" 허용(쿠킹클래스 유형), `external_choice`면 장르별 기존 규칙. |
| **BJND v1.0 용어 표준** | Loss/Lack → Desire(Goal+Need) → Strategy → Cost 용어로 통일 (Creator와 완전 동기화). |
| **사이드바 Engine Info** | Creator Engine과 동일한 톤의 버전 카드. 버전 불일치 즉시 감지. |

---

## v3.0 → v3.1 호환성

- **완전 하위 호환**: 구형 Creator 프로젝트(v1.9/v2.2)나 수동 입력은 그대로 작동. v3.1 신규 3개 필드(`bjnd_data`, `ending_payoff`, `ending_payoff_type`)가 비어 있으면 기존 v3.0 경로로 폴백.
- **build_write_beat_prompt 시그니처**: 신규 3개 파라미터는 모두 기본값 `""`. 기존 호출 코드 수정 불필요.

---

## 비트 집필 전 체크 시스템 (v3.1)

```
0.   핵심 요소 — 맥거핀/비밀/장소/모티프/전술/Plant·Payoff
0-1. 장르 드라이브 5점 (정보 비대칭/에스컬레이션/빌런 승패/타이머/장르 쾌감)
0-2. 액션 아이디어 — 전진/방해/무관
0-3. BJND 씬 레벨 작동 (★ v3.1)
     ① Strategy 구체 행동 / ② 비트 구간 Cost 단계 / ③ Strategy 감각 추적
0-4. 창작자 감성 3요소 (★ v3.1)
     PHYSICALITY (신체 반응 설계) / SILENCE (의도된 침묵 1회+) / PLANT (1막 은폐 3막 폭발)
0-5. 비트 구조 변주 [INV/CON/REV/EMO/ACT/SIL]
1~5. 분량 + 씬 다양성 + 리듬 변주 + 장소 분산
6~9. 장르 강제 (장치 2개+/씬, 5개+/비트)
10~17. 집필 규칙 (보이스/서브텍스트/Too Wet 금지/em dash 금지/AI ESCAPE A1~A20)
```

---

## Beat 15 엔딩 분기 (v3.1 핵심)

Creator Engine의 `ending_payoff_type` 값에 따라 엔딩 규칙이 자동 분기된다:

### INTERNAL_TRANSFORMATION (내적 전환형)
```
예: 쿠킹클래스
  Ending Payoff = "유진이 분석을 멈추고 세웅의 이름을 먼저 부르는 순간,
                   Need(친밀함)가 처음으로 채워진다."

Beat 15~16 규칙:
  ✅ Strategy_2의 확정 씬 (signature_moment) 필수
  ❌ 외적 선택 단순화 금지 ("A/B 중 한 명을 택한다" 식 엔딩)
  ❌ 로맨스 장르라고 기계적으로 '둘이 이어짐' 강제하지 않음
```

### EXTERNAL_CHOICE (외적 선택형)
```
예: 일반 로맨스/스릴러/액션
  주인공의 명확한 외적 행동으로 엔딩 확정
  장르 약속(커플 성사/진실 폭로/최종 대결) 준수
```

### 미지정 (빈 값)
```
기존 v3.0 장르 기반 엔딩 규칙으로 폴백 (하위 호환)
```

---

## 파일 구조

```
writer-engine/
├── main.py           (1,418줄)  Streamlit + 듀얼 모델 + DOCX 4스타일 + JSON 로더
├── prompt.py         (4,272줄)  SYSTEM_PROMPT + 9장르 + 빌더 + v3.1 신규 5모듈
├── requirements.txt
└── .streamlit/config.toml
```

---

## 설치 & 실행

```bash
git clone https://github.com/cinepark-1974/writer-engine.git
cd writer-engine
pip install streamlit anthropic python-docx
streamlit run main.py
```

---

## 입력 (11칸 + v3.1 신규 3칸)

| 필드 | Creator Engine JSON 경로 | 비고 |
|------|-------------------------|------|
| 제목 | `project.title` | |
| 로그라인 | `core.logline_pack.washed` | |
| 기획의도 | `core.project_intent` (v2.3+) | v2.2 이하는 `key_points` |
| GNS | `core.goal_need_strategy` | Goal·Need·Strategy·Risk·Ending Payoff |
| 캐릭터 + 바이블 | `char_bible` + `core.characters` | |
| 오프닝 전략 | `core.opening_strategy` | v3.6 호환 |
| 세계관 | `core.world_build` | |
| 구조 | `structure_story` | |
| 장면 설계 | `scene_design` | |
| 트리트먼트 | `treatment` | |
| 톤 문서 | `tone_doc` | |
| **★ BJND 설계** | `core.narrative_drive` + `core.goal_need_strategy` | ★ v3.1 신규 |
| **★ Ending Payoff** | `core.goal_need_strategy.ending_payoff` | ★ v3.1 신규 |
| **★ Ending Type** | `core.goal_need_strategy.ending_type` 또는 자동 추정 | ★ v3.1 신규 |

Creator JSON 업로드 시 14개 항목이 한 번에 자동 채워진다.

---

## DOCX — 4개 Word 스타일 (v3.0에서 유지)

| 스타일 | 용도 | Bold | 들여쓰기 | 위 간격 | 줄간격 |
|--------|------|------|---------|--------|-------|
| 씬번호 | S#1. INT. 카페 — 낮 | ✅ 11pt | — | 24pt | 1.5 |
| 대사 | 하은\t\t석태야... | ✅ 10pt | 1.25cm | 8pt | 1.5 |
| 대사연속 | \t\t우리한테... | ✅ | 1.25cm | 0pt | — |
| 지문 | 석태의 손이... | ❌ 10pt | — | 2pt | — |

---

## 모델

| 작업 | 모델 |
|------|------|
| 씬 플랜 / 요소 추출 | `claude-sonnet-4-6` |
| 비트 집필 / 다시 쓰기 | `claude-opus-4-6` |

---

## 엔진 생태계

```
Creator Engine v2.3  →  Writer Engine v3.1  →  Rewrite Engine
                     →  Series Engine
                     →  Novel Engine
                     →  Shortform Engine
```

---

## 버전 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v1.0 | 2026-03-17 | 초기. 7모드→2스텝 전환. |
| v2.0 | 2026-03-21 | Sorkin/Curtis, 관객심리, 서브플롯, DOCX. |
| v2.2 | 2026-03-21 | 8장르, 오프닝 훅, 분량 강화. |
| v3.0 | 2026-03-28 | 장르 드라이브 5점 체크, 액션 아이디어, 서사동력, 빌런, Planting & Payoff, 씬 다양성, 기능적 조연, 9장르, 듀얼 모델, DOCX 4스타일, V.O. 인식, em dash 금지, 대사 규칙. CE v1.9 동기화. |
| **v3.1** | **2026-04-23** | **Creator Engine v2.3 동기화. Creator JSON 자동 로더, BJND Scene Enforcer, 창작자 감성 3요소(Physicality/Silence/Plant), 엔딩 동적 분기(internal_transformation / external_choice), v3.0 쿠킹클래스 엔딩 충돌 규칙 해결, BJND v1.0 용어 표준.** |

---

## v3.1의 핵심 변화 요약

**v3.0 철학**: "장르적으로 재미있고 서사적으로 관통하는 시나리오"
**v3.1 철학**: "장르적으로 재미있고, 서사적으로 관통하며, **작가의 서명이 남고, 관객의 몸이 반응하는** 시나리오"

세 가지 추가 레이어가 v3.1을 v3.0과 구분한다:
1. **BJND 씬 강제** — Creator의 설계가 시나리오 끝까지 살아남는다
2. **감성 3요소** — 관객의 몸이 반응한다 (Physicality / Silence / Plant)
3. **엔딩 동적 분기** — BJND가 요구하는 엔딩이 장르 관습을 이긴다

이것이 "기획서 9점인데 시나리오 7점" 문제를 구조적으로 해결한다.

---

© 2026 BLUE JEANS PICTURES
Mr.MOON · [CINEPARK](https://cinepark.blog) · [cinepark-1974](https://github.com/cinepark-1974)
