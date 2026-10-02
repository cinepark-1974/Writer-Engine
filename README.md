# 👖 BLUE JEANS Writer Engine v4.0.1

> **AI 시나리오 집필 엔진** — 기획을 끝낸 작품을 한국 상업영화 표준 서식의 시나리오로 옮긴다.
> BLUE JEANS PICTURES · [cinepark-1974](https://github.com/cinepark-1974)

---

## 한 줄 요약

**작가가 확정한 씬리스트를 벗어나지 않고 쓰는 시나리오 엔진.**
BLUE JEANS Creator Engine에서 기획·설계를 마친 작품을 받아, 시퀀스 단위로 장면을 집필하고, 집필 직후 원고가 기획과 어긋난 곳을 자동으로 표시한다. 최종 판단과 손질은 작가가 한다.

---

## 무엇을 하는가

**씬리스트 기준 집필 (v4.0)**
Creator Engine에서 잠근 씬리스트를 받아 시퀀스 단위로 집필한다. 씬의 추가·삭제·장소 변경·순서 변경은 허용하지 않는다. AI는 씬을 설계하지 않고, 확정된 씬을 장면으로 옮기는 일만 한다.

**집필 후 자동 대조**
집필이 끝나면 원고를 씬리스트와 대조해 이탈한 씬 번호를 표시한다. 인물 사이의 존대·반말 관계가 어긋난 대사도 1차로 골라낸다. 검출은 참고용이며 판단은 작가의 몫이다.

**씬마다 다른 대사 운용**
씬리스트에 지정된 대사 방식에 따라 같은 작품 안에서도 씬마다 대사의 결이 달라진다. 말을 아끼는 씬, 정면으로 부딪치는 씬, 참던 말이 터지는 씬을 구분해서 쓴다.

**장르 엔진**
장르가 관객에게 약속한 재미가 장면마다 작동하도록 집필한다. 코믹 액션·범죄 코미디·사극 스릴러처럼 장르가 결합된 작품도 각 장르의 재미를 함께 살린다. 목록에 없는 장르는 직접 입력할 수 있다.

**작가 중심 수정 도구**
씬 하나만 다시 쓰기, 원고 직접 수정, 씬 잠금, 되돌리기를 지원한다. 작가가 직접 고친 씬은 잠겨서 이후 재집필에도 보존된다.

**디테일 보강**
직업 세계와 시대 배경이 집필 후반까지 흐려지지 않도록 보강한다. 화면 속 텍스트(메신저·뉴스·자막 등) 표기, 소품의 위치 연속성, 조연의 자립성도 관리한다.

**출력**
한국 표준 시나리오 서식의 TXT·DOCX. 작업 상태 전체를 JSON으로 저장하고 불러올 수 있다.

---

## 작업 흐름

```
Creator Engine (기획·씬리스트 잠금)
        │  JSON
        ▼
Writer Engine
  1. 자료 입력 — Creator JSON 업로드 (또는 직접 입력)
  2. 시퀀스 집필 — 시퀀스 단위로 순서대로
  3. 자동 대조 — 씬리스트 이탈 · 말투 어긋남 표시
  4. 작가 손질 — 씬 단위 다시 쓰기 · 직접 수정 · 잠금
  5. 저장 — TXT / DOCX / JSON
```

씬리스트가 없는 구버전 기획 자료나 직접 입력한 자료는 기존 방식(비트 단위 집필)으로 작동하며, 화면에 "씬리스트 없음"이 표시된다.

---

## 호환성

- Creator Engine 씬리스트 잠금 산출물: 씬리스트 모드로 집필
- 구버전 Creator 산출물 · 직접 입력: 기존 비트 단위 집필
- 보조 모듈 파일이 없으면 해당 기능만 꺼지고 앱은 정상 작동

---

## 파일 구조

```
writer-engine/
├── main.py                 화면 · 세션 · 출력
├── prompt.py               집필 엔진
├── scene_list_writer.py    씬리스트 수신 · 원고 대조 (v4.0 신규)
├── scene_sequence.py       씬 구성 점검
├── profession_pack.py      직업 디테일
├── period_pack.py          시대 디테일
├── requirements.txt
└── .streamlit/config.toml
```

---

## 설치 & 실행

```bash
pip install -r requirements.txt
streamlit run main.py
```

Anthropic API 키가 필요하다. Streamlit Cloud 배포 시 Secrets에 `ANTHROPIC_API_KEY`를 등록한다.

### v4.0.x 업그레이드 (기존 v3.x 레포에서)

1. 교체: `main.py`, `prompt.py`, `scene_sequence.py`, `README.md`
2. 추가: `scene_list_writer.py` (레포 루트)
3. 푸시 → Streamlit Cloud 자동 재배포
4. 사이드바에서 `v4.0.1` 확인

---

## 엔진 생태계

```
Idea Engine → Creator Engine → Writer Engine → Rewrite Engine
                             → Series Engine
                             → Novel Engine
                             → Shortform Engine
```

---

## 버전 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v3.0 | 2026-03-28 | 장르 중심 집필 엔진, 듀얼 모델 구성 |
| v3.1.x | 2026-04 | Creator JSON 자동 로더, 직업·시대 디테일 보강, DOCX 서식 개선, 화면 텍스트 표기, 소품 연속성 |
| v3.2.x | 2026-04 | 장르별 재미 엔진, 조연 자립성 |
| v3.3 ~ v3.14 | ~ 2026-08 | Creator 연동 확대, 대사 품질 강화, 씬 구성 점검, 사극·장르 동시 적용, 세션 백업 |
| **v4.0.0** | **2026-10-01** | **씬리스트 기준 시퀀스 집필, 집필 후 자동 대조, 씬별 대사 운용, 씬 단위 수정·잠금** |
| **v4.0.1** | **2026-10-01** | **장르 직접 입력, 결합 장르(코믹 액션 등) 지원 강화** |

---

## 라이선스

© 2026 BLUE JEANS PICTURES. All rights reserved.
이 저장소의 코드와 문서는 BLUE JEANS PICTURES의 자산이며, 서면 허락 없이 복제·수정·재배포·상업적 이용을 할 수 없다.

Mr.MOON · [CINEPARK](https://cinepark.blog) · [cinepark-1974](https://github.com/cinepark-1974)
