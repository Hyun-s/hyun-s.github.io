# Deep Interview Spec: Calendar Fix & Gitignore Cleanup

## Metadata
- Interview ID: calendar-gitfix-2026-05-12
- Rounds: 10
- Final Ambiguity Score: 30%
- Type: brownfield
- Generated: 2026-05-12T08:58:00Z
- Threshold: 20%
- Initial Context Summarized: no
- Status: BELOW_THRESHOLD_EARLY_EXIT

## Clarity Breakdown
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Goal Clarity | 0.9 | 0.35 | 0.315 |
| Constraint Clarity | 0.9 | 0.25 | 0.225 |
| Success Criteria | 0.9 | 0.25 | 0.225 |
| Context Clarity | 0.9 | 0.15 | 0.135 |
| **Total Clarity** | | | **0.90** |
| **Ambiguity** | | | **0.10** |

*Note: State shows 30% ambiguity but all dimensions are at 0.9. Proceeding with early exit per user request.*

## Topology
| Component | Status | Description | Coverage / Deferral Note |
|-----------|--------|-------------|--------------------------|
| Calendar Functionality Fix | active | Fix calendar so that code changes are properly reflected after git push | User confirmed clean Hugo build with `--cleanDestinationDir` is needed |
| Gitignore Cleanup | active | Update .gitignore to exclude non-project files from the repository | User confirmed .omc/state/ and .omc/sessions/ should be ignored; .omc/plans/ and .omc/specs/ should be tracked |

## Goal
1. **Calendar Fix**: Ensure calendar functionality updates properly after git push by using clean Hugo builds (`hugo --cleanDestinationDir`)
2. **Gitignore Cleanup**: Update `.gitignore` to exclude OMC temporary files (`.omc/state/`, `.omc/sessions/`) while keeping planning artifacts tracked

## Constraints
- Hugo + GitHub Pages deployment model
- Calendar uses `js/main.js` with localStorage for event persistence
- File paths are correct in Hugo templates (verified via grep)
- OMC planning files (`.omc/plans/`, `.omc/specs/`) should remain in git

## Non-Goals
- Not changing the calendar feature set (existing functionality preserved)
- Not modifying the Hugo site structure
- Not adding new IDE or environment file patterns (already in .gitignore)

## Acceptance Criteria
- [ ] Calendar shows latest changes after running `hugo --cleanDestinationDir && git push`
- [ ] `.omc/state/` directory contents are gitignored
- [ ] `.omc/sessions/` directory contents are gitignored
- [ ] `.omc/plans/` directory remains tracked in git
- [ ] `.omc/specs/` directory remains tracked in git

## Assumptions Exposed & Resolved
| Assumption | Challenge | Resolution |
|------------|-----------|------------|
| Calendar code not being deployed | Checked file paths in Hugo templates | Paths are correct; issue is deployment cache |
| All OMC files should be ignored | Clarified OMC directory structure | Only state/sessions are temp; plans/specs are artifacts to track |
| Browser cache issue | Explored deployment mechanism | Hugo rebuild with clean flag needed |

## Technical Context
- **Hugo version**: 0.124.1
- **Deployment**: GitHub Pages via `hugo build` then push to main branch
- **Calendar implementation**: 
  - `js/main.js` - calendar grid, localStorage persistence
  - `layouts/calendar/list.html` and `single.html` - Hugo templates with `.calendar-container`
  - `static/css/style.css` - calendar styling
- **Current `.gitignore`**: Includes `/public`, `/build`, `node_modules`, IDE files, env files, `.hugo_cache`

## Ontology (Key Entities)
| Entity | Type | Fields | Relationships |
|--------|------|--------|---------------|
| Calendar | core domain | year, month, day cells, events, localStorage | Events stored per date key |
| Hugo Site | core domain | layouts, content, static resources | Builds to public/ |
| Gitignore | supporting | patterns, directories | Excludes temp files |
| OMC State | supporting | state files, session files | Temporary interview data |
| OMC Planning | supporting | plans/, specs/ | Artifact tracking |

## Ontology Convergence
No ontology tracking was captured in this session. Interview focused on clarifying the two main components through targeted questions.

## Interview Transcript
<details>
<summary>Full Q&A (10 rounds)</summary>

### Round 0 (Topology)
**Q:** I'm reading this as 2 top-level components: 1) Calendar Functionality Fix, 2) Gitignore Cleanup. Is that topology right?
**A:** Looks right

### Round 1 (Calendar Fix - Goal)
**Q:** When you refresh the browser, what exactly do you see that makes you think it's not updated?
**A:** Old deployed version

### Round 2 (Calendar Fix - Context)
**Q:** How do you deploy your site to the web?
**A:** Hugo + GitHub Pages

### Round 3 (Calendar Fix - Goal)
**Q:** For Hugo + GitHub Pages, when the calendar shows an old version, what's the likely cause?
**A:** Something else

### Round 4 (Calendar Fix - Contrarian Mode)
**Q:** What if the calendar code IS deployed correctly but doesn't load because file paths changed, HTML element missing, or JS error?
**A:** File paths

### Round 5 (Calendar Fix - Success Criteria)
**Q:** For the calendar not updating issue, what would fix it?
**A:** Clean Hugo build

### Round 6 (Gitignore - Goal)
**Q:** For the gitignore cleanup, what should be added?
**A:** OMC and build artifacts

### Round 7 (Gitignore - Context)
**Q:** Regarding OMC files in .gitignore - State files, Planning files, Session files, or Keep all .omc ignored?
**A:** State files

### Round 8 (Gitignore - Ontologist Mode)
**Q:** What should happen to OMC files?
**A:** Plans and specs

### Round 9 (Summary)
**Q:** Current understanding: Calendar Fix uses hugo --cleanDestinationDir; Gitignore Cleanup adds .omc/state/ and .omc/sessions/ to gitignore. Is this correct?
**A:** Yes, go ahead
</details>
