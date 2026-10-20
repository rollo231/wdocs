---
name: wdocs-design
description: Use when writing or reviewing a Korean engineering Design Doc (설계 문서, 개발 계획서) that decides how to build something — context, architecture, data model, API, alternatives, cross-cutting concerns, milestones — or when told a document reads "ai 스러운" or is hard to read.
---

# wdocs-design: Design Doc

Design Doc은 「어떻게」를 정한다. 무엇을 왜 만드는지는 PRD(`wdocs-prd`)에 있고, 이 문서는 그것을 링크하고 반복하지 않는다. 쓰기 전에 `../../shared/style.md`를 읽는다.

참고(refactoringenglish.com): "How to Write an Effective Software Design Document"(되돌리기 비싼 결정에 지면을 쓰고, 몇 시간이면 고칠 세부에는 쓰지 않는다), "Little Moments" 설계 문서(결정마다 이유), "Useful feedback on design docs"(리뷰어가 찾아보거나 짐작하지 않게 쓴다). Design Docs at Google(맥락은 요구사항 문서가 아니다, 검토한 대안, 교차 관심사).

## 쓰기 전

- PRD가 있는지 확인한다. 있으면 맥락 절에 링크만 건다. 없고 작은 변경이면 맥락 절에 요구를 다섯 줄 이내로 적는다. 크면 `wdocs-prd`를 먼저 쓴다.
- 코드 기준 커밋을 정한다. 문서의 사실은 그 커밋에서 확인한 것만 쓴다.

## 구조

큰 제목은 번호를 붙인다(`## 1. 문서 정보`). 작은 제목(###)은 번호 없이. 내용이 없는 절은 지우고 번호를 다시 매긴다.

| 절 | 내용 |
|---|---|
| 문서 정보 | 작성자, 상태(Draft, In review, Approved), 작성일, 리뷰어, 리뷰 기한, 승인자와 승인일, PRD 링크, 관련 문서, 코드 기준 커밋 |
| 목차 | 큰 제목 번호 목록 아래 작은 제목을 들여 쓴다. 항목마다 제목 링크(`1. [문서 정보](#1-문서-정보)`). 제목을 고치면 다시 만든다 |
| 맥락 | 한 단락. 어느 시스템 안에서 무엇을 바꾸는지와 PRD 링크. 요구를 다시 쓰지 않는다 |
| 기술 목표 / 하지 않는 것 | 각각 큰 제목. 설계가 지켜야 할 결과(지연, 규모, 호환)와 일부러 하지 않는 것 |
| 제약 | 설계를 묶는 조건(인프라, 외부 시스템, 예산)(있을 때만) |
| 설계 | 구성 그림과 구성 표(구성 요소, 하는 일, 부르는 곳), 데이터 모델 표, 규칙 표, API, 새로 만드는 것과 고치는 것 |
| 기존 동작 변경 | 지금, 바뀐 뒤, 영향(있을 때만) |
| 알림 | 이벤트, 수신자, 채널(있을 때만) |
| SLO / 모니터링 / 로깅 | 숫자 목표, 장애를 알아채는 법, 남기는 것(있을 때만) |
| 개인정보 / 데이터 보존 / 보안 | 민감한 데이터와 볼 수 있는 사람, 보관 기간. 위협마다 "Scenario:" / "Mitigation:" |
| 구현 일정 | Milestone마다 작은 제목, 작업 표(작업 번호, 내용, 선행 작업), "What's implemented:" / "What's not implemented:". Milestone은 확인할 수 있는 결과물이 나오게 나눈다 |
| Open issues | 기술로 정할 것만. 형식은 `wdocs-prd`와 같다 |
| Closed issues | 결정된 이슈. "Decision:"이 맨 위 |
| 검토한 대안 | 유력했던 대안만. "(selected)", "Pros:", "Cons:" |
| 부록 | API 명세 등 긴 참조 |

- 되돌리기 비싼 결정(데이터 모델, API 계약, 외부 연동, 권한 규칙)은 자세히, 금방 고칠 세부는 짧게 쓰거나 부록으로.
- 코드는 기능 이름으로 쓰고, 구현자가 찾아야 하는 곳만 함수 이름을 붙인다. 파일 경로와 행 번호는 작업 추적 도구의 작업 설명에 적는다.
- 작업 번호는 작업 추적 도구의 형식을 따른다(예: `API-1`, `WEB-1`). 선행 작업은 같은 Milestone이나 앞 Milestone에 있어야 한다.
- 영어로 두는 것은 Open issues, Closed issues 제목과 라벨(Milestone, Decision, Affects, Background, Options, Proposal, Next step, Scenario, Mitigation, What's implemented, What's not implemented, selected, Pros, Cons)뿐이다.

## 마무리 점검

1. `python3 ../../shared/check_style.py --kind design <문서>`가 합계 0.
2. 문서에 적은 함수 이름과 동작이 기준 커밋의 코드와 맞는지 다시 연다.
3. 작업 표의 선행 작업 순서를 본다.
4. `review.md`의 에이전트 리뷰(PRD 대조, 문서 안 일관성, 읽는 사람)를 새 에이전트로 동시에 돌리고 지적을 확인해 반영한다.
5. 넘길 때 문서 공유 도구에 올리는 법을 함께 준다. 마크다운 목차 링크는 도구에서 동작하지 않을 수 있으니 도구의 목차 기능으로 바꾸라고 적고, 그림 파일 목록을 "파일 / 들어갈 절" 표로 준다.
6. 사람 리뷰와 설계 회고는 `review.md`를 따른다.
