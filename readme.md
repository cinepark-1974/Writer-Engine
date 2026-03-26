# 👖 BLUE JEANS Writer Engine v3.0

> **AI 시나리오 집필 엔진** — Creator Engine 산출물 → 100씬 영화 시나리오 자동 생성  
> BLUE JEANS PICTURES · [cinepark-1974](https://github.com/cinepark-1974)

---

## 한 줄 요약

**19회 클릭으로 100씬 영화 시나리오를 쓰는 엔진.** 액션 아이디어 + 서사동력 + 장르 드라이브 5점 체크 + 빌런 승률 추적으로 "장르적으로 재미있는 시나리오"를 생산한다.

---

## 흐름

```
Creator Engine 산출물 (9칸)
        ↓
   씬 플랜 (3회)     ← Sonnet
        ↓
 핵심 요소 추출 (1회)  ← Sonnet
        ↓
  비트별 집필 (15회)   ← Opus
        ↓
    TXT / DOCX
```

---

## v3.0 주요 변경 (← v2.2)

| 신규 기능 | 설명 |
|----------|------|
| **장르 드라이브 5점 체크** | 매 비트마다 정보 비대칭/에스컬레이션/빌런 승패/타이머/장르 쾌감 추적 |
| **액션 아이디어** | 영화 전체를 하나의 행동으로 — 모든 비트가 이 행동을 향하는지 검증 |
| **서사동력 (BJND 연동)** | Goal/Need 간극 + 상실/결핍 방향 — Creator Engine 동기화 |
| **빌런 4대 질문 + 승률** | 빌런이 계속 이기는지 추적. Patriot Games 규칙. |
| **핵심 요소 추출** | 기획 자료에서 맥거핀/비밀/전술/장소/모티프/클라이맥스/톤 강제 추출 |
| **씬 다양성 4종** | [A]/[B]/[BR]/[CUT] + 장소 분산 + 리듬 변주 |
| **9장르 통일** | Creator Engine v1.5와 완전 동기화 |
| **듀얼 모델** | Opus (집필) + Sonnet (구조) — 품질 ↑ 비용 효율 ↑ |
| **villain_beat 참조** | Creator Engine treatment 연동 |

---

## 비트 집필 전 체크 시스템

AI가 매 비트 쓰기 전에 점검하는 것:

```
0.   핵심 요소 — 맥거핀/비밀/장소/모티프/전술
0-1. 장르 드라이브 5점
       ① 정보 비대칭  ② 에스컬레이션  ③ 빌런 승패
       ④ 타이머       ⑤ 장르 쾌감
       → 3개 "아니오"면 경고
0-2. 액션 아이디어 — "___하는 일" 전진/방해/무관
0-3. 서사동력 — Goal/Need 간극 유지?
1~5. 분량 기준 (600~800자/씬, 4,000~5,000자/비트)
5-1. 씬 다양성 [A]/[B]/[BR]/[CUT]
5-2. 리듬 변주
5-3. 장소 분산
6~9. 장르 강제 (장치 2개+/씬, 5개+/비트, Hook-Punch)
10~17. 집필 규칙 (보이스, 서브텍스트, Too Wet 금지...)
```

---

## 파일 구조

```
writer-engine/
├── main.py           (839줄)  Streamlit 앱 + 듀얼 모델 + DOCX
├── prompt.py         (1,075줄) SYSTEM_PROMPT + 9장르 + 빌더 함수 5개
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

## 설치 & 실행

```bash
# 1. 클론
git clone https://github.com/cinepark-1974/writer-engine.git
cd writer-engine

# 2. 의존성
pip install streamlit anthropic python-docx

# 3. API 키 설정 (Streamlit Secrets 또는 환경변수)
export ANTHROPIC_API_KEY="sk-..."

# 4. 실행
streamlit run main.py
```

---

## 입력 (9칸 — Creator Engine 산출물)

| 필드 | Creator Engine 출처 |
|------|-------------------|
| 프로젝트 제목 | 프로젝트 제목 |
| 로그라인 | Logline Pack |
| 기획의도 | KEY POINTS |
| GNS | Goal / Need / Strategy |
| 캐릭터 + 바이블 | Character + Bible + 빌런 4대 질문 |
| 세계관 | World Building |
| 구조 | Synopsis + 15-Beat + 빌런 승률 |
| 장면 설계 | Scene Design + Scene Map |
| 트리트먼트 | Treatment (villain_beat 포함) |
| 톤 문서 | Tone Document |

---

## 장르

| 장르 | 영문 |
|------|------|
| 범죄/스릴러 | Crime/Thriller/Noir |
| 드라마 | Drama |
| 액션 | Action |
| 로맨스 | Romance/Melodrama |
| 코미디 | Comedy |
| 호러/공포 | Horror |
| SF | Science Fiction |
| 판타지 | Fantasy |
| 미지정 | General |

---

## 모델

| 작업 | 모델 | 이유 |
|------|------|------|
| 씬 플랜 / 요소 추출 | `claude-sonnet-4-6` | 구조 작업 — 빠르고 충분 |
| 비트 집필 / 다시 쓰기 | `claude-opus-4-6` | 창작 — 품질 차이 큼 |

---

## 출력

- **TXT**: 씬 플랜 + 비트별 시나리오
- **DOCX**: 한국 표준 시나리오 서식
  - 폰트: 함초롬바탕
  - 페이지: A4 (210×297mm), 마진 20mm
  - 씬 헤딩 볼드, 캐릭터+탭+대사
  - 커버: 시나리오 제목 + 기획/제작 블루진픽처스

---

## BLUE JEANS PICTURES 엔진 생태계

```
Creator Engine v1.5  →  Writer Engine v3.0  →  Rewrite Engine v2.0
                     →  Series Engine v1.0
                     →  Novel Engine
                     →  Shortform Engine (계획 중)
```

---

## 버전 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v1.0 | 2026-03-17 | 초기. 7모드→2스텝 전환. |
| v2.0 | 2026-03-21 | Sorkin/Curtis, 관객심리, 서브플롯, DOCX. |
| v2.2 | 2026-03-21 | 8장르, 오프닝 훅, 분량 강화. |
| **v3.0** | **2026-03-26** | **장르 드라이브, 액션 아이디어, 서사동력, 빌런 시스템, 씬 다양성, 요소 추출, 9장르, 듀얼 모델.** |

---

## 라이선스

© 2026 BLUE JEANS PICTURES. All rights reserved.

---

## 제작

**BLUE JEANS PICTURES**  
프로듀서: Mr.MOON (문성주)  
블로그: [CINEPARK](https://cinepark.blog)
