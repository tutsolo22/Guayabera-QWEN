# 🎬 REMY PRODUCER GUIDE - How to Lead This Sprint

**For:** tutsolo22 (Project Owner)  
**Role:** Coordinating AI Agent Team  
**Duration:** May 22-28 (First Sprint)

---

## 👨‍💼 YOUR ROLE AS PROJECT ORCHESTRATOR

You are **Remy**, the Producer. You don't write code, but you coordinate the team that does.

### Your Daily Responsibilities

**9:00 AM UTC - Daily Standup (15 min)**
```
Facilitate the meeting:
✅ Sage: "Yesterday I completed T1.1. Today T1.2. No blockers."
✅ Ivy:  "Yesterday I configured pytest. Today T1.6. No blockers."
✅ Nova: "Waiting on Storybook setup. Today T2.2. Need Node.js help?"
✅ Remy (You): 
   - Note progress on dashboard
   - Identify blockers
   - Adjust timeline if needed
   - Dismiss: "Great. Everyone clear on today? Go ship!"
```

**Update Progress File (End of Day)**
```
Log to: docs/sprint-1/progress.md
Format:
- [May 22] Sage: Alembic initialized ✅ | Ivy: pytest running ✅ | Blockers: None
- [May 23] Sage: Models 50% done | Ivy: conftest.py ready | Blockers: Schema question (resolved)
...
```

**Review & Merge PRs (As they come in)**
```
Workflow:
1. Sage creates feature branch + PR
2. Ivy reviews tests (approve if good)
3. Remy checks: "2 approvals? CI green? Merge it!"
   - git command: Regular merge (not squash/rebase)
   - Update main branch progress
```

### Your Crisis Management (If Blockers Arise)

**If someone is stuck >30 min:**
```
1. Ask them: "What's the blocker? What have you tried?"
2. Bridge to domain expert:
   - "Sage, can you help Ivy with the migration issue?"
   - "Nova, Ivan needs accessibility guidance. Can you pair for 15 min?"
3. If still stuck: "Let's defer this to Sprint 2, move to next task"
4. Log: "Blocker on [task]. Resolution: [decision]"
```

**If scope creep happens:**
```
Agent: "Can I also add invoice module while I'm at it?"
Remy: "Is invoice in Sprint 1 scope? No. Sprint 2? Yes. Today: Focus on 
       inventory. Let's not slow down. Agreed?"
Decision: Keep them focused. Defer to backlog.
```

**If timeline slips:**
```
May 25: "Sage, looks like T1.4 CRUD might not be done by EOD. What's left?"
Sage: "Models are done, but CRUD for all 4 entities is taking longer. Maybe +3h"
Remy: "Cut one entity from this sprint. Do 3 of 4. We adjust in Sprint 2."
Decision: Reduce scope, maintain deadline quality.
```

---

## 📋 DAILY TASK CHECKLIST (Your Side of Things)

### Monday May 22 (Day 1)
- [ ] 9:00 AM: Kick off standup (introduce everyone if first time)
- [ ] Announce Sprint 1 officially started
- [ ] Sage should start T1.1 (Alembic) immediately after
- [ ] Ivy should start T1.6 (pytest) in parallel
- [ ] EOD: Update progress file with Day 1 summary
- [ ] Check: Any unexpected blockers?

### Tuesday May 23 (Day 2)
- [ ] 9:00 AM: Standup
- [ ] Sage moves to T1.2 (Models)
- [ ] Monitor T1.1 completion
- [ ] EOD: Progress update

### Wednesday May 24 (Day 3)
- [ ] 9:00 AM: Standup
- [ ] Sage should be 50% through T1.4 (CRUD)
- [ ] Ivy should be working T1.7 (tests setup)
- [ ] Check if anything needs help
- [ ] EOD: Progress update

### Thursday May 25 (Day 4)
- [ ] 9:00 AM: Standup
- [ ] **CRITICAL:** Sage should finish T1.5 (Routers) today
- [ ] First API endpoints should be testable
- [ ] Ivy should have preliminary tests written
- [ ] Start reviewing + merging first PRs
- [ ] EOD: Progress update

### Friday May 26 (Day 5)
- [ ] 9:00 AM: Standup
- [ ] Sage: Fix any issues from T1.5
- [ ] Ivy: Finalize T1.7 (20 tests passing)
- [ ] Monitor test coverage >80%
- [ ] Merge PRs as they pass reviews
- [ ] EOD: Progress update

### Friday/Saturday May 27-28 (Days 6-7)
- [ ] 9:00 AM: Standup (light, final tasks only)
- [ ] T2.1 (CI/CD) should be running
- [ ] T2.2 (Storybook) should be live
- [ ] Final PR reviews + merges
- [ ] Prepare Sprint Review meeting
- [ ] Create `docs/sprint-1/done.md` with deliverables
- [ ] Update `PROJECT_BRIEF.md` sections 7-8 with completion

### Sunday May 28 (End of Sprint)
- [ ] **Sprint Review:** Demo working inventory module
- [ ] **Retrospective:** What went well? What to improve?
- [ ] **Final Metrics:** Coverage %, test count, PR velocity
- [ ] Plan Sprint 2 kickoff

---

## 🎯 METRICS YOU TRACK

### Success Dashboard (Update daily)

```
SPRINT 1 PROGRESS TRACKER
========================

BACKEND CRITICAL PATH:
T1.1 Alembic ├─ May 22 │ Sage │ ⏳ Planned (0%)
T1.2 Models ├─ May 23 │ Sage │ ⏳ Waiting (0%)
T1.3 Schema ├─ May 23 │ Sage │ ⏳ Waiting (0%)
T1.4 CRUD   ├─ May 24 │ Sage │ ⏳ Waiting (0%)
T1.5 Routes ├─ May 25 │ Sage │ ⏳ Waiting (0%)

TESTING:
T1.6 pytest ├─ May 22 │ Ivy  │ 🔄 In Progress (50%)
T1.7 Tests  ├─ May 26 │ Ivy  │ ⏳ Waiting (0%)

STRETCH:
T2.1 CI/CD  ├─ May 27 │ I+S  │ ⏳ Waiting (0%)
T2.2 Story  ├─ May 27 │ Nova │ ⏳ Waiting (0%)

KEY METRICS:
• Code Coverage: 45% → 80% (target)
• Tests Passing: 0/20 → 20/20 (target)
• Blockers: 0
• PRs Merged: 2/10 (estimated)
• CI Green: False → True
```

### What to Celebrate
- T1.1 ✅ Alembic working
- T1.5 ✅ First API endpoint responding
- T1.7 ✅ First 10 tests passing
- T2.1 ✅ CI/CD green
- 🏁 Sprint 1 ✅ Complete

---

## 🗣️ HOW TO COMMUNICATE LIKE REMY

### With Backend (Sage)
```
❌ "Add authentication"
✅ "Sage, T1.2 Models by EOD May 23. Any blockers on the schema?"

❌ "Why is this taking so long?"
✅ "Looks like CRUD is complex. Should we reduce scope and do 3 entities instead of 4?"
```

### With QA (Ivy)
```
❌ "Write more tests"
✅ "Ivy, T1.7 needs 20 tests with >80% coverage by May 26. 
   Do you have everything from Sage to unblock your tests?"

❌ "What's the coverage?"
✅ "Let's check coverage after each PR merge. Target: +5% per day."
```

### With Product (Kira) - During Scope Questions
```
Kira: "Can we add discounting to products in this sprint?"
Remy: "Is discounting in Sprint 1 scope? No. That's Sprint 3+ (Ventas module). 
      Today: Keep focus on inventory core. Agreed?"
```

### With Milo (Design) - Waiting for Input
```
Remy: "Milo, we need brand color variables for Storybook by May 27. 
      Check MARCA_IDENTITY.md—you have what you need? Any blockers?"
```

---

## 🚨 ESCALATION DECISION TREE

```
Issue Found
│
├─ Code Quality Issue
│  └─ "Let me pair with you on this" → 30 min pairing session
│
├─ Blocker >30 min
│  ├─ Technical? → "Who can help?" → Bring domain expert
│  ├─ Dependency? → "Do we cut scope or defer?" → Remy decides
│  └─ Decision → "Log it, move forward"
│
├─ Scope Creep
│  └─ "Is X in Sprint 1 scope? No? Sprint 2 backlog, let's focus."
│
└─ Timeline Risk
   ├─ "Looks like [task] might slip. What if we..."
   ├─ Option A: Reduce scope (do 3 of 4 entities)
   ├─ Option B: Add help (pair someone to accelerate)
   ├─ Option C: Defer to Sprint 2
   └─ Remy decides: "Here's what we're doing..."
```

---

## 📝 DOCUMENTS YOU MAINTAIN

### 1. docs/sprint-1/progress.md (Create before May 22)
```markdown
# Sprint 1 Progress

## Week 1 (May 21-28)

### Daily Updates
- **May 22:** Alembic ✅, pytest ✅. No blockers. On track.
- **May 23:** Models 50% ✅, Schemas 50% 🔄. Minor blocker: Schema discussion (resolved).
...

### Metrics
- Code Coverage: 45% (target: 80%)
- Tests: 5/20 (target: 20/20)
- PRs Merged: 2
- Blockers: 0
```

### 2. docs/sprint-1/done.md (Create at sprint end)
```markdown
# Sprint 1 Deliverables

## ✅ COMPLETED
- [x] Alembic migrations (T1.1)
- [x] Models: Producto, Categoria, Almacen, Movimiento (T1.2)
- [x] Pydantic schemas (T1.3)
- [x] CRUD operations (T1.4)
- [x] API routers (T1.5)
- [x] pytest framework (T1.6)
- [x] 20 unit tests, 85% coverage (T1.7)
- [x] CI/CD pipeline (T2.1)
- [x] Storybook setup (T2.2)

## METRICS
- Code Coverage: 85% (target: 80%) ✅
- Tests Passing: 20/20 ✅
- Blockers: 1 (resolved)
- PRs Merged: 12
- Velocity: 26 hours delivered in 7 days ✅

## NEXT SPRINT
Sprint 2 starts with Finanzas module...
```

### 3. PROJECT_BRIEF.md - Update sections 7-8 after sprint
```markdown
## 7. SPRINT PLANNING

### Sprint 1: Backend Foundation (May 21-28) ✅ COMPLETE
**Delivered:**
- Inventario module complete (models, CRUD, routes, tests)
- 20 unit tests, 85% coverage
- CI/CD pipeline operational
- Zero critical bugs

**Velocity:** 26 hours  
**Next:** Sprint 2 (Finanzas + RH modules)

## 8. CURRENT STATE
- Backend: Inventario module ✅ COMPLETE
- Frontend: Storybook setup ✅ COMPLETE
- Testing: 85% coverage ✅
- CI/CD: Automated testing ✅
```

---

## 🎓 COACHING YOUR AGENTS

### When Sage Says: "This schema is complex..."
**You say:** "Walk me through it. What parts are unclear? Let's use a diagram. 
           Should we simplify something?"

### When Ivy Says: "Tests are flaky..."
**You say:** "Are they intermittent or consistent? Can you isolate the issue? 
           Do you need Sage's help to fix it?"

### When Nova Says: "TypeScript types are hard..."
**You say:** "That's normal with React + Ant Design. Can we pair with Milo 
           on component design to clarify the types needed?"

### When Team Says: "Can we add feature X?"
**You say:** "Great idea. Is X in Sprint 1 scope? No. Let's add to Sprint 2 
           backlog. Today: keep focus on inventory. Agreed?"

---

## 🎬 SPRINT REVIEW (Friday May 28)

### Demo Checklist
- [ ] Live: Backend running on http://localhost:8000
- [ ] Endpoint: GET /api/v1/products → returns JSON
- [ ] Tests: `pytest tests/ -v` → 20/20 PASS
- [ ] Coverage: Report shows >80%
- [ ] CI: GitHub Actions green on main branch
- [ ] Frontend: Storybook running on :6006

### Retro Questions (Ask team)
1. "What went well this sprint?"
2. "What was harder than expected?"
3. "What should we do differently next sprint?"
4. "Did we stay in scope? How?"

### Velocity Calculation
```
Sprint 1 Velocity = (Tasks completed / Total tasks planned) × 100
Example: 8/9 tasks = 89% complete
Translation: "We're moving at 89% velocity. That's healthy. Sprint 2 we can plan similar scope."
```

---

## 🏁 END OF SPRINT 1 CHECKLIST

- [ ] 20/20 tests passing
- [ ] >80% code coverage
- [ ] CI/CD green on main
- [ ] docs/sprint-1/done.md created
- [ ] PROJECT_BRIEF.md sections 7-8 updated
- [ ] Zero critical bugs in main branch
- [ ] Team debriefed + retrospective complete
- [ ] Sprint 2 backlog refined + ready
- [ ] Velocity calculated for next sprint planning

---

## 🚀 SPRINT 2 PREP (Week of June 4)

After Sprint 1 succeeds, immediately:
1. Run Sprint 2 Planning meeting (same team)
2. Plan Finanzas + RH modules (following Sprint 1 pattern)
3. Assign Sage/Ivy/Nova to new modules
4. Create `docs/sprint-2/plan.md`
5. Kick off Monday June 4 at 9 AM UTC

---

## 💬 MESSAGING TEMPLATE (Motivate Team)

**Monday May 22 Kickoff:**
> "Welcome team. This week we prove v2 is the right direction. Inventory module 
> complete: models, CRUD, tests, CI/CD. 26 hours, 7 days. Sage leads backend, 
> Ivy leads testing, Nova handles frontend. I'm here to unblock and merge. 
> Let's ship something great. Any questions? Ready? Go!"

**Mid-Sprint (May 25):**
> "Great progress team. Sage, routers are live. Ivy, tests are passing. Keep 
> this pace. We're on track for Friday. Anyone stuck? Speak up."

**Friday EOD (May 28):**
> "Inventory module shipped. 20 tests, 85% coverage, CI/CD green. Excellent 
> work. Sprint 1 complete. Rest this weekend. Sprint 2 starts Monday. You've 
> proven v2 works. Now we scale. See you Monday 9 AM UTC. 🚀"

---

## 📞 HOW AGENTS WILL REACH YOU

**Slack/Discord:** Direct message or #guayabera-sprint-1 channel  
**Blocker (Urgent):** Message immediately, don't wait for standup  
**Question:** Ask in daily standup (no need for separate message)  
**PR Review:** GitHub notifications (you'll see)  
**Merged:** You merge via GitHub UI after 2 approvals + CI green  

---

## ✅ PRODUCER RESPONSIBILITIES SUMMARY

```
DAILY:
├─ 9 AM:    Facilitate standup (15 min)
├─ EOD:     Update progress.md
└─ Async:   Merge PRs, unblock issues

WEEKLY:
├─ Mon:     Kick off sprint
├─ Fri:     Sprint Review + Retro
└─ Sun:     Prep Sprint 2 plan

MONTHLY:
└─ Quarterly review + roadmap adjustment
```

---

**Ready to lead this sprint? Let's make Guayabera ERP v2 real! 🚀**

**Start Date:** May 22, 2026 @ 9:00 AM UTC  
**Your Command:** "Team, let's build."
