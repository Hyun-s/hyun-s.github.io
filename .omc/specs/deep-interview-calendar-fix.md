# Deep Interview Spec: 달력 버그 수정 및 일정 추가 기능

## Metadata
- Interview ID: di-20260512-001
- Rounds: 1
- Final Ambiguity Score: 13.5%
- Type: brownfield
- Generated: 2026-05-11T16:42:00Z
- Threshold: 20%
- Initial Context Summarized: no
- Status: PASSED

## Clarity Breakdown
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Goal Clarity | 0.85 | 0.35 | 0.2975 |
| Constraint Clarity | 0.90 | 0.25 | 0.2250 |
| Success Criteria | 0.80 | 0.25 | 0.2000 |
| Context Clarity | 0.95 | 0.15 | 0.1425 |
| **Total Clarity** | | | **0.865** |
| **Ambiguity** | | | **13.5%** |

## Topology

| Component | Status | Description | Coverage / Deferral Note |
|-----------|--------|-------------|--------------------------|
| calendar-bug-fix | active | calendarContainer 스코프 버그, refreshCalendar 페이지 리로드 루프 등 기존 버그 수정 | 달력이 \"calnder\" 텍스트만 보이고 렌더링되지 않는 문제 수정 |
| calendar-event-add | active | 달력에 일정을 추가할 수 있는 기본 기능 추가 | 폼 기반 일정 추가 기능 구현 예정 |

## Goal
1. **달력 버그 수정**: 달력이 \"calnder\" 텍스트만 보이고 실제 UI가 렌더링되지 않는 문제 해결
2. **일정 추가 기능**: 사용자가 달력에서 날짜를 선택하고 일정을 추가할 수 있는 기본 기능 구현

## Constraints
- Hugo 정적 사이트 환경 유지
- localStorage를 사용한 일정 저장 (서버 불필요)
- 기존 CSS 스타일 시스템과 통합

## Non-Goals
- 서버 기반 일정 동기화
- 사용자 계정 및 인증
- 반복 일정 (recurrence) 기능
- 일정 수정/삭제 기능 (V1 제외)

## Acceptance Criteria
- [ ] 달력이 정상적으로 렌더링되어 매월 날짜 표시
- [ ] 달력에서 날짜 클릭 시 해당 날짜에 대한 정보 표시
- [ ] 일정 추가 폼이 정상적으로 표시되고 작동
- [ ] 저장된 일정이 페이지 재로드 후에도 유지

## Assumptions Exposed & Resolved

| Assumption | Challenge | Resolution |
|------------|-----------|------------|
| "calnder" 텍스트는 HTML template 오타일 것이라고 가정 | explore agent 결과 calnder 텍스트는 없었음 | 사용자가 브라우저에서 보는 실제 결과이며, JavaScript 에러로 인해 렌더링되지 않은 것으로 판단 |
| 달력은 완전히 작동하지 않음 | CSS 파일에 calendar 관련 스타일이 정의됨을 확인 | 달력 컨테이너는 존재하나 JS 에러로 인해 내용이 렌더링되지 않은 것으로 판단 |
| localStorage로 충분함 | 데이터 영속성 문제 제기 | V1은 localStorage로 충분하며, 서버 사이드는 향후 확장으로 미룸 |

## Technical Context

### Project Structure
- **Framework**: Hugo 정적 사이트 생성기
- **Language**: JavaScript (ES6+)
- **Storage**: localStorage

### Existing Files
- `/js/main.js` - Calendar JavaScript (버그 발견됨)
- `/css/style.css` - Calendar CSS (lines 270-350)
- `/layouts/calendar/list.html` - Hugo template
- `/content/calendar/_index.md` - Content

### Bug Analysis

**Bug 1: Variable Scope Issue (main.js line 6 vs 105)**
```javascript
// Line 6 - calendarContainer defined inside DOMContentLoaded callback
const calendarContainer = document.querySelector('.calendar-container');

// Line 105 - Used in addEventForm() but out of scope!
calendarContainer.appendChild(form);
```
**Fix**: `calendarContainer`를 전역 변수로 이동 또는 `addEventForm()`에 파라미터로 전달

**Bug 2: Page Reload Loop (main.js line 176)**
```javascript
function refreshCalendar() {
    location.reload();  // This causes infinite reload loop
}
```
**Fix**: `location.reload()`를 제거하고 달력 재렌더링 함수로 대체

**Bug 3: Event Handler Timing (main.js line 186-206)**
```javascript
function initializeEventHandling() {
    const eventInput = document.getElementById('event-input');  // null at this point!
    // ...
}
```
**Fix**: 폼 요소 생성 후에 이벤트 리스너 등록

## Ontology (Key Entities)

| Entity | Type | Fields | Relationships |
|--------|------|--------|---------------|
| Calendar | core domain | year, month, days | Contains calendar-day elements |
| Event | core domain | title, description, date, timestamp | Belongs to a date |
| User | external | id (implicit) | Creates events |
| localStorage | external | key-value storage | Persists events |

## Ontology Convergence
Not applicable - single round interview

## Interview Transcript
<details>
<summary>Full Q&A (1 round)</summary>

### Round 1
**Q:** "달력이 안 보인다"고 하셨는데, 구체적으로 어떤 상황인가요? 1. 빈 화면이 보이나요? 2. "calnder"라는 텍스트만 보이고 달력 UI가 보이지 않나요? 3. 콘솔에 에러 메시지가 보이나요?

**A:** "calnder"라는 텍스트만 보이고 달력 UI가 보이지 않음. 깃에 배포까지 해달라고 요청함.

**Q:** "calnder"라는 텍스트는 어디서 오는가요? 1. HTML template에 오타로 포함되어 있나요? 2. JavaScript 코드 내에서 텍스트가 잘못 표시되나요? 3. 아니면 다른 원인인가요?

**A:** 모름.

**Ambiguity:** 13.5% (Goal: 0.85, Constraints: 0.90, Criteria: 0.80, Context: 0.95)

</details>
