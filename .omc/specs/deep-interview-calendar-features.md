# Deep Interview Spec: Calendar Features Implementation

## Metadata
- Interview ID: di-20260512-002
- Rounds: 4
- Final Ambiguity Score: 35%
- Type: brownfield
- Generated: 2026-05-12T00:00:00Z
- Threshold: 20%
- Initial Context Summarized: no
- Status: PASSED (early exit with user approval)

## Clarity Breakdown
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Goal Clarity | 0.90 | 0.35 | 0.3150 |
| Constraint Clarity | 0.85 | 0.25 | 0.2125 |
| Success Criteria | 0.85 | 0.25 | 0.2125 |
| Context Clarity | 0.90 | 0.15 | 0.1350 |
| **Total Clarity** | | | **0.8750** |
| **Ambiguity** | | | **12.5%** |

## Topology

| Component | Status | Description | Coverage / Deferral Note |
|-----------|--------|-------------|--------------------------|
| calendar-time-support | active | 이벤트에 단일 시간(시작) 또는 시작-종료 시간 쌍 추가 가능 | 드롭다운 UI, 시작/종료 시간 선택, 24시간 형식 |
| calendar-month-nav | active | 이전/다음 버튼으로 다른 월도 볼 수 있도록 | 월 이동 시 이벤트도 표시, 상단 월 정보 업데이트 |
| calendar-click-to-add | active | 날짜 클릭 시 모달을 열어 바로 이벤트 추가 가능 | 플로팅 폼, 기존 form과 필드 공유, 바로 반영 |

## Goal
1. **시간 지원**: 이벤트에 시작 시간과 종료 시간을 드롭다운으로 선택하여 추가. 시작 시간만 선택하거나 시작-종료 쌍을 모두 선택 가능. 시간은 24시간 형식(HH:MM) 사용.
2. **월 이동**: 이전/다음 버튼을 통해 현재 월 외의 다른 월도 볼 수 있도록. 월을 바꿀 때 해당 월의 이벤트도 모두 표시하고, 상단 월 정보도 업데이트.
3. **날짜 클릭 추가**: 달력에서 날짜를 클릭하면 모달이 열리고, 바로 이벤트를 추가할 수 있도록. 모달은 기존 하단 form과 입력 필드를 공유하며, 저장 시 달력에 즉시 반영.

## Constraints
- Hugo 정적 사이트 환경 유지
- localStorage를 사용한 일정 저장 (서버 불필요)
- 기존 CSS 스타일 시스템과 통합
- 시작 시간이 종료 시간보다 뒤일 수 없음 (유효성 검증)
- 모달 내에서 다른 날짜 클릭 시 즉시 날짜가 변경됨

## Non-Goals
- 서버 기반 일정 동기화
- 사용자 계정 및 인증
- 반복 일정 (recurrence) 기능
- 일정 수정/삭제 기능 (V1 제외)
- 이벤트 카테고리 또는 태그 기능
- 알림 및 푸시 기능

## Acceptance Criteria
- [ ] 시간 드롭다운이 정상적으로 표시되고, 시작 시간과 종료 시간을 개별/함께 선택 가능
- [ ] 이전/다음 버튼 클릭 시 달력 그리드와 상단 월 정보가 업데이트됨
- [ ] 월을 바꿀 때, 해당 월의 이벤트가 날짜에 표시됨
- [ ] 날짜를 클릭하면 모달이 열리고, 날짜에 이미 있는 이벤트도 표시됨
- [ ] 모달에서 이벤트를 저장하면 달력에 즉시 반영됨
- [ ] 시간 입력은 선택 사항 (비워둘 수 있음)
- [ ] 종료 시간은 시작 시간보다 뒤여야 함 (유효성 검증)

## Assumptions Exposed & Resolved

| Assumption | Challenge | Resolution |
|------------|-----------|------------|
| 시간 UI方式가 명확하지 않음 | 시간 선택 UI를 어떻게 할지 물음 | 드롭다운 선택으로 결정 (간단하고 직관적) |
| 이전/다음 버튼만으로 충분할지 | 월 드롭다운도 필요한지 물음 | 이전/다음 버튼만으로 충분하다고 결정 |
| 모달 방식이 명확하지 않음 | alert 대체 vs 플로팅 폼 vs 사이드바 | 플로팅 폼으로 결정 (기존 form과 공유) |
| 시간 형식이 명확하지 않음 | 12시간 vs 24시간 형식 | 24시간 형식(HH:MM)으로 결정 |
| 월 이동 시 이벤트 표시 | 다른 월의 이벤트도 표시할지 | 예, 해당 월의 이벤트 모두 표시 |
| 모달 내 날짜 변경 | 모달 열려있어도 날짜 변경 가능 | 예, 즉시 날짜 변경 가능 |

## Technical Context

### Project Structure
- **Framework**: Hugo 정적 사이트 생성기
- **Language**: JavaScript (ES6+)
- **Storage**: localStorage
- **Styling**: CSS Grid (7-column layout)

### Existing Files
- `/js/main.js` - Calendar JavaScript (수정 필요)
- `/css/style.css` - Calendar CSS (lines 270-350, 추가 스타일 필요)
- `/layouts/calendar/list.html` - Hugo template (수정 불필요)
- `/content/calendar/_index.md` - Content (수정 불필요)

### Current Implementation Summary
- Calendar displays current month by default
- Events stored in localStorage as `events_YYYY-MM-DD`
- Basic event form at bottom of page
- Alert-based UI for viewing events
- No month navigation
- No time support in events
- No click-to-add modal

### Required Changes
1. Add time dropdown to event form (start time, end time options)
2. Add previous/next month navigation buttons to calendar header
3. Implement month switching logic in `initializeCalendar()`
4. Create modal for click-to-add event functionality
5. Update event structure to include optional time fields

## Ontology (Key Entities)

| Entity | Type | Fields | Relationships |
|--------|------|--------|---------------|
| Calendar | core domain | year, month, days, events | Contains calendar-day elements |
| Event | core domain | title, description, date, timestamp, startTime, endTime | Belongs to a date |
| Month | supporting | year, monthNumber, daysInMonth | Contains events |
| User | external | id (implicit) | Creates events |
| localStorage | external | key-value storage | Persists events |

## Interview Transcript
<details>
<summary>Full Q&A (4 rounds)</summary>

### Round 1
**Q:** 시간 입력 UI를 어떻게 제공하시겠습니까? 드롭다운, 숫자 입력, 타임피커 중 어떤 방식인가요?

**A:** Dropdown 선택

**Q:** 월 이동 버튼만으로 충분한가요, 월 드롭다운도 필요한가요?

**A:** 이전/다음 버튼만

**Q:** 모달 방식은 어떤 것이 좋으세요? alert 대체, 플로팅 폼, 사이드바 중?

**A:** 플로팅 폼

### Round 2
**Q:** 월 이동 성공 기준은 무엇인가요? 달력만 바뀌나요, 이벤트도 표시되나요?

**A:** 이벤트 표시 포함

**Q:** 모달과 기존 form은 어떻게 공유할까요? 필드를 공유할 건가요?

**A:** 공유 필드 (같은 입력 필드 공유)

### Round 3
**Q:** 시간 입력은 필수인가요? 선택인가요? 12시간 vs 24시간 형식?

**A:** Start + End 선택, 24시간 형식

**Q:** 모달 성공 기준은 무엇인가요? 기존 이벤트도 보이나요?

**A:** 바로 반영

### Round 4
**Q:** 종료 시간이 시작 시간보다 뒤여야 하나요? 유효성 검증할까요?

**A:** 종료 >= 시작 (검증)

**Q:** 모달 열려있을 때 다른 날짜 클릭하면 바로 바뀌나요?

**A:** 날짜 즉시 변경

</details>
