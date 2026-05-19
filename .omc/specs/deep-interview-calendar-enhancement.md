# Deep Interview Spec: Calendar Enhancement

## Metadata
- Interview ID: deep-interview-calendar-2026-05-19
- Rounds: 7
- Final Ambiguity Score: 6%
- Type: brownfield
- Generated: 2026-05-19
- Threshold: 20%
- Initial Context Summarized: no
- Status: PASSED

## Topology

| Component | Status | Description | Coverage / Deferral Note |
|-----------|--------|-------------|--------------------------|
| Click-to-add interaction | Active | Replace bottom form with click-on-date dialog showing existing events + inline add form | Full CRUD (create, read, update, delete) with inline expand for details |
| Month navigation | Active | Add previous/next buttons to navigate between months | Previous/Next buttons confirmed; state persists on page reload |

## Goal

Enhance the existing Hugo calendar implementation with:
1. **Click-to-add interaction**: Replace the separate add-event form at the bottom with an interactive dialog that opens when clicking any date. The dialog shows existing events for that date AND provides an inline form to add new events.
2. **Month navigation**: Add previous/next month navigation buttons so users can view and add events to any month, not just the current month (May).

## Constraints

- **Dialog design**: Combined dialog showing existing events list + inline add form
- **Event details**: Clicking an event title expands it inline to show full details with Edit/Delete buttons
- **Styling**: Modernize slightly — add subtle shadows, rounded corners, and smooth transitions while maintaining the existing design language
- **Deployment**: Must work with current GitHub Pages auto-deploy workflow (push to main → https://hyun-s.github.io)
- **Storage**: Continue using localStorage with `events_YYYY-MM-DD` key format
- **Browser compatibility**: Must work in modern browsers (Chrome, Firefox, Safari, Edge)

## Non-Goals

- No backend/database integration
- No multi-day event support
- No recurring events
- No event categories or colors
- No mobile-specific touch gestures

## Acceptance Criteria

- [ ] Clicking any calendar day opens a dialog showing that date's events and an add-event form
- [ ] Dialog displays the selected date in the header (e.g., "May 15, 2024")
- [ ] Existing events are listed in the dialog with clickable titles
- [ ] Clicking an event title expands it inline to show description + Edit/Delete buttons
- [ ] Edit mode pre-fills the form with existing event data
- [ ] Delete button removes the event and updates the calendar
- [ ] Empty dates show "No events for this date" message + add form
- [ ] Empty title validation prevents saving incomplete events
- [ ] Previous/Next buttons navigate to adjacent months
- [ ] Calendar remembers the viewed month on page reload
- [ ] New events can be added in any month (not just current month)
- [ ] Modernized UI with subtle shadows, rounded corners, smooth transitions
- [ ] All changes work with existing GitHub Pages deployment (no build step required)

## Assumptions Exposed & Resolved

| Assumption | Challenge | Resolution |
|------------|-----------|------------|
| Dialog vs. separate flow | Contrarian mode questioned if combined dialog was necessary | User confirmed single combined dialog with inline form |
| Complexity level | Simplifier mode questioned if features could be reduced | User confirmed all CRUD operations needed |
| Event details view | Multiple UI patterns possible | User confirmed inline expand pattern |
| Styling approach | Three options presented | User confirmed "modernize slightly" approach |

## Technical Context

**Current implementation** (brownfield):
- Template: `layouts/calendar/list.html` — renders `.calendar-container` div
- JavaScript: `assets/js/main.js` — `initializeCalendar()`, `showEventsForDate()`, `saveEvent()` functions
- CSS: `assets/css/style.css` — calendar styles (lines 270-392)
- Storage: localStorage with `events_YYYY-MM-DD` keys
- Event structure: `{ title, description, date, timestamp }`

**Changes required**:
1. Modify `showEventsForDate()` to include inline add/edit form
2. Add expand/collapse logic for event details
3. Add Edit/Delete functionality
4. Add month navigation buttons to `initializeCalendar()`
5. Add state persistence for viewed month
6. Update CSS with modernized styling

## Ontology (Key Entities)

| Entity | Type | Fields | Relationships |
|--------|------|--------|---------------|
| Event | Core domain | title, description, date, timestamp | Belongs to a specific date |
| Date | Core domain | year, month, day, events[] | Contains multiple events |
| Calendar | Supporting | currentMonth, currentYear, days[] | Displays dates and their events |
| Dialog | Supporting | date, events[], form | Shows events and add/edit form for a date |

## Ontology Convergence

| Round | Entity Count | New | Changed | Stable | Stability Ratio |
|-------|-------------|-----|---------|--------|----------------|
| 1 | 2 | 2 | - | - | - |
| 2 | 3 | 1 | 0 | 2 | 67% |
| 3 | 4 | 1 | 0 | 3 | 75% |
| 4 | 4 | 0 | 0 | 4 | 100% |
| 5 | 4 | 0 | 0 | 4 | 100% |
| 6 | 4 | 0 | 0 | 4 | 100% |
| 7 | 4 | 0 | 0 | 4 | 100% |

Ontology has converged — the same 4 entities appeared in 4 consecutive rounds with no changes.

## Interview Transcript

<details>
<summary>Full Q&A (7 rounds)</summary>

### Round 1
**Q**: When you click on a date, you want to add an event. For the new click-to-add flow, do you want a single dialog with existing events + add form, two separate flows, or something else?
**A**: "i want first option" (single dialog with existing events + add form)
**Ambiguity**: 49% (Goal: 0.9, Constraints: 0.5, Criteria: 0.4)

### Round 2
**Q**: For the combined dialog, do you want a time field for each event, or just date + title?
**A**: "date and title. moreover, if i click event (title), i want to see details"
**Ambiguity**: 37% (Goal: 0.95, Constraints: 0.7, Criteria: 0.5)

### Round 3
**Q**: When you click an event to see details, should it expand inline, open a secondary dialog, or use a context menu? Should users be able to delete and edit events?
**A**: "oh i need delete and edit" (confirmed inline expand with edit/delete)
**Ambiguity**: 23% (Goal: 0.95, Constraints: 0.8, Criteria: 0.7)

### Round 4 (Contrarian Mode)
**Q**: What if you only needed to jump to specific months rather than navigate sequentially? Do you want prev/next buttons, month/year dropdowns, or both?
**A**: "1. previous and next buttons"
**Ambiguity**: 16% (Goal: 0.95, Constraints: 0.85, Criteria: 0.7, Context: 0.6)

### Round 5
**Q**: When clicking an event for details/edit/delete, should it expand inline, open a secondary dialog, or use a context menu?
**A**: "1." (inline expand)
**Ambiguity**: 11% (Goal: 0.95, Constraints: 0.85, Criteria: 0.85, Context: 0.75)

### Round 6 (Simplifier Mode)
**Q**: For styling, should I match existing styles, modernize slightly, or keep it simple?
**A**: "2." (modernize slightly)
**Ambiguity**: 6% (Goal: 0.95, Constraints: 0.9, Criteria: 0.9, Context: 0.85)

### Round 7
**Q**: How should edge cases be handled (empty state, date selection flow, validation)?
**A**: "모두 다 고려해줘. 추가로, 현재의 배포방식을 고려해서" (handle all edge cases, consider current deployment)
**Ambiguity**: 6% (Goal: 0.95, Constraints: 0.95, Criteria: 0.95, Context: 0.85)

</details>
