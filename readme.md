# 👖 BLUE JEANS Writer Engine v3.0

> **AI 시나리오 집필 엔진** — Creator Engine 산출물 → 100씬 영화 시나리오 자동 생성  
> BLUE JEANS PICTURES · [cinepark-1974](https://github.com/cinepark-1974)

---

## 한 줄 요약

**19회 클릭으로 100씬 영화 시나리오를 쓰는 엔진.** 액션 아이디어 + 서사동력 + 장르 드라이브 5점 체크 + 빌런 승률 추적 + Planting & Payoff로 "장르적으로 재미있고 서사적으로 관통하는 시나리오"를 생산한다.

---

## 흐름

```
Creator Engine v1.9 산출물 (9칸)
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

## v3.0 주요 변경 (← v2.2)

| 신규 기능 | 설명 |
|----------|------|
| **장르 드라이브 5점 체크** | 매 비트: 정보 비대칭/에스컬레이션/빌런 승패/타이머/장르 쾌감 |
| **액션 아이디어** | 영화 전체 = 하나의 행동. 모든 비트가 이 행동을 향하는지 검증 |
| **서사동력 (BJND)** | Goal/Need 간극 + 상실/결핍 방향. Creator Engine 동기화 |
| **빌런 4대 질문 + 승률** | 빌런이 계속 이기는지 추적. Patriot Games 규칙 |
| **Planting & Payoff** | 1막 plant → 3막 payoff. 3쌍 추적. CE v1.9 연동 |
| **핵심 요소 추출 (11개)** | 맥거핀/비밀/전술/장소/모티프/클라이맥스/톤/장르드라이브 등 |
| **기능적 조연** | 1막 2명+, 2막 3명+. 세계를 살리는 인물들 |
| **씬 다양성 4종** | [A]/[B]/[BR]/[CUT] + 장소 분산 + 리듬 변주 |
| **9장르 × 12필드** | Creator Engine v1.9 Genre Rule Pack v2 동기화 |
| **듀얼 모델** | Opus (집필) + Sonnet (구조) |
| **DOCX 4개 Word 스타일** | 씬번호/대사/대사연속/지문 — 일괄 수정 가능 |
| **V.O./O.S. 인식** | 대사 파싱 개선 |
| **em dash · bold 금지** | AI 문체 신호 제거 |
| **대사 형식 규칙** | 같은 캐릭터 연속 대사 금지, 대사 교환 원칙 |

---

## 비트 집필 전 체크 시스템

```
0.   핵심 요소 — 맥거핀/비밀/장소/모티프/전술/Plant·Payoff
0-1. 장르 드라이브 5점
       ① 정보 비대칭  ② 에스컬레이션  ③ 빌런 승패
       ④ 타이머       ⑤ 장르 쾌감
       → 3개 "아니오"면 경고
0-2. 액션 아이디어 — "___하는 일" 전진/방해/무관
0-3. 서사동력 — Goal/Need 간극 유지? 상실/결핍 방향?
1~5. 분량 + 씬 다양성 + 리듬 변주 + 장소 분산
6~9. 장르 강제 (장치 2개+/씬, 5개+/비트, Hook-Punch)
10~17. 집필 규칙 (보이스, 서브텍스트, Too Wet 금지, em dash 금지...)
```

---

## 파일 구조

```
writer-engine/
├── main.py           (918줄)   Streamlit + 듀얼 모델 + DOCX 4스타일
├── prompt.py         (1,168줄) SYSTEM_PROMPT + 9장르 + 빌더 5개
├── requirements.txt
└── .streamlit/
    └── config.toml
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

## 입력 (9칸 — Creator Engine v1.9)

| 필드 | Creator Engine 출처 |
|------|-------------------|
| 로그라인 | Logline Pack |
| 기획의도 | KEY POINTS |
| GNS | Goal / Need / Strategy |
| 캐릭터 + 바이블 | Character + Bible + 빌런 4대 질문 |
| 세계관 | World Building |
| 구조 | Synopsis + 15-Beat + 빌런 승률 |
| 장면 설계 | Scene Design + plant_payoff_tag |
| 트리트먼트 | Treatment (villain_beat + plant_payoff) |
| 톤 문서 | Tone Document |

---

## DOCX — 4개 Word 스타일

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
Creator Engine v1.9  →  Writer Engine v3.0  →  Rewrite Engine v2.0
                     →  Series Engine v1.7
                     →  Novel Engine v2.5
                     →  Shortform Engine v2.1
```

---

## 버전 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v1.0 | 2026-03-17 | 초기. 7모드→2스텝 전환. |
| v2.0 | 2026-03-21 | Sorkin/Curtis, 관객심리, 서브플롯, DOCX. |
| v2.2 | 2026-03-21 | 8장르, 오프닝 훅, 분량 강화. |
| **v3.0** | **2026-03-28** | **장르 드라이브, 액션 아이디어, 서사동력, 빌런, Planting & Payoff, 씬 다양성, 기능적 조연, 요소 추출, 9장르, 듀얼 모델, DOCX 4스타일, V.O. 인식, em dash 금지, 대사 규칙. CE v1.9 동기화.** |

---

© 2026 BLUE JEANS PICTURES  
Mr.MOON · [CINEPARK](https://cinepark.blog) · [cinepark-1974](https://github.com/cinepark-1974)
