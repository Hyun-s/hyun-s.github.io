# Calendar Features Implementation Plan

## Plan Summary

**Plan saved to:** `.omc/plans/calendar-features-implementation.md`

**Scope:**
- 5 tasks across 2 files (main.js, style.css)
- Estimated complexity: MEDIUM

**Key Deliverables:**
1. Time dropdown UI (start/end time selection) in 24-hour format (HH:MM)
2. Previous/Next month navigation buttons with event filtering
3. Click-to-add modal with floating form sharing existing form fields

**Consensus mode:** RALPLAN-DR (Short mode - no high-risk signals detected)

---

## Requirements Summary

| Requirement ID | Description | Priority |
|----------------|-------------|----------|
| R1 | Time dropdown UI with start time and end time options | MUST |
| R2 | 24-hour time format (HH:MM) | MUST |
| R3 | Start time must be before or equal to end time (validation) | MUST |
| R4 | Previous/Next month navigation buttons | MUST |
| R5 | Month switching updates calendar grid and displays events | MUST |
| R6 | Click-to-add modal opens on date click | MUST |
| R7 | Modal shares form fields with existing bottom form | MUST |
| R8 | Events persist in localStorage (existing key format) | MUST |
| R9 | Time fields are optional (can be empty) | SHOULD |
| R10 | Modal allows date selection while open | SHOULD |

---

## Acceptance Criteria (Testable)

| AC ID | Test Description | Pass Criteria |
|-------|------------------|---------------|
| AC1 | Time dropdown displays correctly | Two dropdowns visible in form (start/end time) |
| AC2 | Time format is 24-hour | Options show 00:00 through 23:30, HH:MM format |
| AC3 | Start time validation works | Cannot select end time before start time |
| AC4 | Previous button changes month | Month decreases by 1, events update |
| AC5 | Next button changes month | Month increases by 1, events update |
| AC6 | Events show on correct dates | Stored events appear as colored dots on calendar |
| AC7 | Date click opens modal | Modal overlay appears with form |
| AC8 | Modal has cloned form structure | Form elements cloned in modal (not shared DOM) |
| AC9 | Modal stores event on save | localStorage updated with new event |
| AC10 | Modal date changes on date click | Clicking another date in modal updates selected date |
| AC11 | Keyboard navigation for month buttons | Arrow Left/Right changes month, Enter activates |
| AC12 | Modal close mechanisms | X button, click outside, Escape key all work |
| AC13 | Start time <= end time validation with UI feedback | Error message shown when end < start |
| AC14 | Time display in day cells | Events with time show HH:MM in day cells |
| AC15 | Modal z-index above other content | Modal appears above header and hero sections |

---

## Implementation Steps with File References

### Step 1: Update `static/js/main.js` - Make Form Persistent and Add Time Dropdown UI

**File:** `/home/hyuns/hyun-s.github.io/static/js/main.js`

**Critical Fix First: Fix refreshCalendar() to not destroy form**

**Current Issue:** `refreshCalendar()` at line 189-197 calls `location.reload()` which destroys the entire page and recreates everything via `initCalendar()`. This loses any form state.

**Fix:** Replace `location.reload()` with DOM-based refresh.

**Changes:**
1. **Fix `refreshCalendar()` function** (line 189-197):
   ```javascript
   function refreshCalendar() {
       if (calendarContainer) {
           calendarContainer.innerHTML = '';
           initCalendar();
       }
   }
   ```

2. Add `TIME_OPTIONS` constant (array of "HH:MM" strings, 00:00-23:30 in 30-min intervals)

3. **Make form persistent** - Move form creation outside `initCalendar()`:
   - Add module-level `eventFormElement` variable
   - Create form once in `initCalendar()` if not exists
   - Reuse existing form on subsequent calls

4. Modify `addEventForm()` to include time dropdown fields:
   ```javascript
   <select id="event-start-time">
   <select id="event-end-time">
   ```

5. Update `saveEvent()` to capture and store time fields:
   - Read `startTime` and `endTime` values
   - Add to event object as optional fields

**Acceptance:** Time dropdowns appear in both bottom form and modal, form persists across month navigation

---

### Step 2: Update `static/js/main.js` - Month Navigation

**File:** `/home/hyuns/hyun-s.github.io/static/js/main.js`

**Changes:**
1. Add module-level state: `currentYear`, `currentMonth` (initialized to today's values)
2. Modify `initCalendar()` to add navigation buttons in calendar header:
   ```html
   <div class="calendar-nav">
     <button id="prev-month">&lt;</button>
     <span id="month-display">YYYY년 M월</span>
     <button id="next-month">&gt;</button>
   </div>
   ```
3. Implement `navigateMonth(direction)` function:
   - Update `currentMonth` (handle year rollover: -1 for prev, +1 for next)
   - Rebuild calendar grid with `currentYear` and `currentMonth`
   - Update month display text
   - Re-render events for the new month
4. **Add keyboard navigation:** Arrow Left/Right to change months, Enter/Space to activate
5. Update `isToday()` to use `currentYear`/`currentMonth`

**Acceptance:** Previous/Next buttons visible, month display updates, events filter correctly, keyboard accessible

---

### Step 3: Update `static/js/main.js` - Click-to-Add Modal

**File:** `/home/hyuns/hyun-s.github.io/static/js/main.js`

**Changes:**
1. Create `openDateModal(date)` function:
   - Create modal overlay element with proper z-index (1000+)
   - Clone form structure (not reference - safer for modal context)
   - Set modal date from clicked date
   - Show events for that date in modal
2. Modify `showEventsForDate()` to return events array instead of alert
3. Create `modalFormSubmit()` handler:
   - Validate start time <= end time with UI feedback (error message)
   - Save event with all fields (including time)
   - Update localStorage
   - Close modal
   - Refresh calendar display
4. Add `changeModalDate(newDate)` for clicking other dates in modal:
   - Preserve time inputs when changing dates
   - Update event list for new date
5. **Add modal close mechanisms:**
   - X button in modal header
   - Click outside modal (overlay click)
   - Escape key

**Acceptance:** Modal opens on date click, form cloned in modal, saves correctly, closes properly

---

### Step 4: Update `static/css/style.css` - Modal and Navigation Styles

**File:** `/home/hyuns/hyun-s.github.io/static/css/style.css`

**Changes:**
1. Add modal overlay styles with high z-index:
   ```css
   .cal-modal-overlay {
     position: fixed;
     top: 0; left: 0; right: 0; bottom: 0;
     background: rgba(0,0,0,0.5);
     z-index: 1000;
     display: flex;
     align-items: center;
     justify-content: center;
   }
   .cal-modal-content {
     background: white;
     padding: 1.5rem;
     border-radius: 0.75rem;
     position: relative;
     max-width: 400px;
     width: 90%;
   }
   .cal-modal-close {
     position: absolute;
     top: 0.5rem; right: 0.5rem;
     background: none; border: none;
     font-size: 1.5rem; cursor: pointer;
   }
   ```
2. Add navigation button styles:
   ```css
   .cal-nav-button {
     background: var(--primary-color);
     color: white;
     border: none;
     padding: 0.5rem;
     cursor: pointer;
     font-size: 1.2rem;
     border-radius: 0.25rem;
   }
   .cal-nav-button:hover { background: var(--primary-dark); }
   .cal-month-display {
     margin: 0 1rem;
     font-weight: 600;
   }
   ```
3. Add time dropdown styles (align with form):
   ```css
   .cal-time-select {
     width: 100px;
     padding: 0.5rem;
     border: 1px solid var(--border-color);
     border-radius: 0.5rem;
   }
   ```
4. **Add CSS scoping prefix:** Use `.cal-` prefix for all calendar-related classes to prevent conflicts

**Acceptance:** Modal displays correctly, navigation buttons styled, dropdowns aligned, z-index above all content

---

### Step 5: Update `static/css/style.css` - Visual Enhancements

**File:** `/home/hyuns/hyun-s.github.io/static/css/style.css`

**Changes:**
1. Add hover effect for navigation buttons (already included in Step 4)
2. Add time display in day cells with events (if time present):
   ```css
   .cal-event-time {
     font-size: 0.8rem;
     color: var(--text-secondary);
   }
   ```
3. Add zebra striping for modal event list:
   ```css
   .cal-event-list li:nth-child(odd) { background: #f9fafb; }
   ```
4. Ensure responsive behavior for modal on mobile:
   ```css
   @media (max-width: 480px) {
     .cal-modal-content { width: 95%; }
   }
   ```
5. Add keyboard focus styling:
   ```css
   .cal-nav-button:focus-visible { outline: 2px solid var(--primary-color); }
   ```

**Acceptance:** Calendar looks polished, events show time when present, accessible keyboard navigation

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Modal Z-index conflicts with existing styles | HIGH | MEDIUM | Use z-index: 1000+, test on all pages with different layers |
| Time validation logic errors | MEDIUM | LOW | Unit test: validateTime(startTime, endTime) with specific test cases |
| Month navigation breaks existing events | MEDIUM | HIGH | Test with multiple events across months; verify events persist in localStorage |
| localStorage key format changes | LOW | HIGH | Use existing format: `events_YYYY-MM-DD`; document format |
| Form state lost on refresh | HIGH | HIGH | **FIXED:** `refreshCalendar()` now rebuilds DOM only, no page reload |
| Form destroyed on month navigation | HIGH | HIGH | **FIXED:** Form created once, moved outside `initCalendar()` |
| Modal date click loses time inputs | MEDIUM | MEDIUM | **FIXED:** `changeModalDate()` preserves form state |
| No keyboard navigation | MEDIUM | MEDIUM | **FIXED:** Added Arrow Left/Right for month, Enter/Space for buttons |
| Responsive modal on mobile | MEDIUM | MEDIUM | Test on viewport widths 320px-768px; ensure touch targets 44px+ |
| Time dropdown overwrites on month nav | HIGH | MEDIUM | **FIXED:** Form is persistent, time dropdowns preserved |
| Validation error feedback missing | MEDIUM | LOW | **FIXED:** Add inline error message for start > end time |

---

## RALPLAN-DR Summary

### Principles (3-5)

| Principle | Description |
|-----------|-------------|
| Consistency | Modal shares form fields with existing bottom form |
| Persistence | localStorage key format unchanged (`events_YYYY-MM-DD`) |
| Incremental | Modify existing functions, don't rewrite |
| Validation | Start time must be <= end time |
| User Experience | Time optional, modal closes on save |

### Decision Drivers (Top 3)

| Driver | Weight | Impact |
|--------|--------|--------|
| Backward compatibility | High | Existing events must remain accessible |
| LocalStorage persistence | High | No server sync, browser-only storage |
| Minimal code changes | Medium | Avoid full rewrite, use existing patterns |

### Viable Options (>=2)

**Option A: Separate Form in Modal (Chosen)**
- Create duplicate form elements inside modal
- **Pros:** Simple implementation, clear separation
- **Cons:** Slightly more code, potential sync issues

**Option B: Shared Form Reference**
- Move form to modal, reference from bottom area
- **Pros:** Single source of truth
- **Cons:** Complex layout changes, breaking existing UI

**Option C: Hybrid (Invalidated)**
- Use input fields for time instead of dropdowns
- **Pros:** More flexible input
- **Cons:** No validation without extra code, spec requires dropdown

**Revised Option A (Chosen):** Clone form structure in modal, not share DOM elements
- **Pros:** Simple implementation, clear separation, no state collision
- **Cons:** Slightly more code duplication

---

## ADR (Architecture Decision Record)

### Decision
Implement time dropdown UI with start/end time selection, previous/next month navigation buttons, and click-to-add modal with form cloning (not DOM sharing) for proper state isolation.

### Drivers
1. **Backward Compatibility:** Existing localStorage events must remain accessible after changes
2. **Minimal Scope:** Modify existing functions rather than full rewrite
3. **User Experience:** Time fields should be optional; validation prevents invalid ranges

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| DOM-level form sharing (Option A original) | **Revised:** Form is appended inside container, destroyed on month nav; cloning is safer for modal context |
| Input fields for time | Spec requires dropdown (clarified in Round 1 of interview) |
| Full calendar rewrite | Brownfield constraint (spec Section 3.1) |
| Server-side storage | Non-goal (spec Section 4) |

### Why Chosen
Revised Option A (clone form structure in modal) was chosen because:
- Matches spec requirement for "모달에서 이벤트 추가" (add event in modal)
- Form persistence via module-level variable avoids destruction on month nav
- Cloning form structure is safer for modal context (no DOM state collision)
- Validation is simple: dropdown options ensure valid start/end pairs
- Implementation is incremental: reuse `addEventForm()` structure
- Keyboard navigation added for accessibility
- CSS scoping with `.cal-` prefix prevents style conflicts
- Fixed critical `refreshCalendar()` issue - no longer destroys form

### Consequences

| Consequence | Positive/Negative | Mitigation |
|-------------|-------------------|------------|
| Modal z-index conflicts | Negative | Use z-index: 1000+, test on all pages |
| Form cloning (not sharing) | Neutral | Slightly more code, but cleaner state isolation |
| Time validation logic | Negative | Add `validateTime()` helper function with UI feedback |
| Month navigation complexity | Negative | Test with events across month boundaries |
| localStorage unchanged | Positive | Existing events remain accessible |
| Fixed refreshCalendar() | Positive | Form state no longer lost on month navigation |

### Follow-ups
1. Test with existing events in localStorage
2. Verify month navigation with events at month boundaries
3. Mobile responsive test for modal overlay
4. Consider adding event editing functionality in V2
5. Consider adding event deletion functionality in V2
6. Add time display in day cells as optional visual enhancement

---

## Files to Modify

| File | Lines to Add | Lines to Modify |
|------|--------------|-----------------|
| `/home/hyuns/hyun-s.github.io/static/js/main.js` | ~80 | 5-10 |
| `/home/hyuns/hyun-s.github.io/static/css/style.css` | ~50 | 0-5 |

---

## Task Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Add Time Dropdown UI                                 │
│    - TIME_OPTIONS constant                              │
│    - Update addEventForm() with select elements         │
│    - Update saveEvent() to capture times                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 2. Add Month Navigation                                 │
│    - Add navigation buttons to header                   │
│    - Implement navigateMonth() function                 │
│    - Update currentYear/currentMonth state              │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 3. Implement Click-to-Add Modal                         │
│    - Create openDateModal() function                    │
│    - Update showEventsForDate() to return array         │
│    - Implement modalFormSubmit()                        │
│    - Add changeModalDate() for date selection           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 4. Add Modal & Navigation Styles                        │
│    - Modal overlay styles                               │
│    - Navigation button styles                           │
│    - Time dropdown alignment                            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 5. Visual Enhancements                                  │
│    - Responsive modal testing                           │
│    - Time display in day cells                          │
│    - Polish and cleanup                                 │
└─────────────────────────────────────────────────────────┘
```

---

## Success Criteria

- [ ] Time dropdowns appear in both bottom form and modal (00:00-23:30, 30-min intervals)
- [ ] Previous/Next buttons change month and display correct events
- [ ] Clicking a date opens modal with events for that date
- [ ] Modal form stores event with optional time fields
- [ ] localStorage format unchanged (backward compatible)
- [ ] Start time validation prevents end time before start time
- [ ] Modal closes after successful save and calendar updates
- [ ] Mobile responsive: modal overlay works on touch devices

---

## How to Proceed

This plan is ready for executor handoff.

**Does this plan capture your intent?**
- "proceed" - Begin implementation via /oh-my-claudecode:start-work
- "adjust [X]" - Return to interview to modify
- "restart" - Discard and start fresh
