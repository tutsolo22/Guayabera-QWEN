# 🚀 SPRINT 1 KICKOFF - Guayabera ERP v2

**Date:** May 21, 2026  
**Sprint Duration:** May 21 - May 28 (7 days)  
**Team:** 6 AI Agents + Producer  
**Status:** ✅ READY TO LAUNCH

---

## 📢 EXECUTIVE SUMMARY

We are launching **Sprint 1** to establish Guayabera ERP v2 with a solid backend foundation.

### What We're Building This Week
✅ Production-ready database with Alembic migrations  
✅ Inventario module complete (Productos, Categorias, Almacenes, Movimientos)  
✅ Full API routers for inventory management  
✅ 20 unit tests with >80% coverage  
✅ GitHub Actions CI/CD pipeline  

### Why This Sprint Matters
- v1 (original) has logic but doesn't compile
- v2 (refactored) compiles but is incomplete
- **Sprint 1 goal:** Prove v2 architecture is solid + add first business module

### Success = Green CI/CD + 20 tests passing + zero blockers

---

## 📋 PRE-SPRINT CHECKLIST

### For All Agents
- [ ] Read `PROJECT_BRIEF.md` (sections 1-8)
- [ ] Read `AGENT_TEAM.md` (your role + responsibilities)
- [ ] Read `SPRINT_1_PLAN.md` (this sprint's tasks)
- [ ] Understand multi-tenant architecture (empresa_id filtering)
- [ ] Understand brand guidelines from `MARCA_IDENTITY.md`

### For Backend (Sage)
- [ ] PostgreSQL 15+ running on localhost:5432
- [ ] Python 3.11+ installed
- [ ] v2/backend cloned, venv activated
- [ ] `pip install -r requirements.txt` works
- [ ] Can import FastAPI without errors

### For QA (Ivy)
- [ ] pytest installed: `pip install pytest pytest-cov pytest-asyncio`
- [ ] Can run: `pytest --version`
- [ ] Understand fixture pattern (conftest.py)
- [ ] Understand faker for test data

### For Frontend (Nova)
- [ ] Node 18+ installed: `node --version`
- [ ] npm 9+ installed: `npm --version`
- [ ] v2/frontend cloned, `npm install` works
- [ ] Can run: `npm start` (may have warnings, that's OK)

### For All Git Operations
- [ ] GitHub repo cloned to local machine
- [ ] Can run: `git status`, `git branch`
- [ ] Can create branches: `git checkout -b feature/sprint-1-test`
- [ ] SSH or HTTPS auth configured

---

## 🎯 SPRINT 1 CRITICAL PATH

```
Monday 9 AM:     Sprint Planning + Team Sync
  ↓
T1.1 (Sage):     Alembic setup → May 22 EOD
  ↓
T1.2-T1.3 (Sage): Models + Schemas → May 23 EOD
  ↓
T1.4-T1.5 (Sage): CRUD + Routers → May 25 EOD
  ↓
[Parallel]
T1.6-T1.7 (Ivy): Tests → May 26 EOD
T2.2 (Nova):     Storybook → May 27 EOD
  ↓
T2.1 (Sage+Ivy): CI/CD → May 27 EOD
  ↓
Friday EOD:      Sprint Review + Retro
  ↓
Result:          🟢 Production-ready Inventory module + tests
```

---

## 📅 DAILY SCHEDULE

### 9:00 AM UTC - Daily Standup (15 min)
**Attendees:** Remy, Sage, Ivy, Nova  
**Where:** Video call or Slack  
**What to report:**
```
✅ YESTERDAY:
- Task completed + status
- Blockers fixed

📅 TODAY:
- Planned work
- Expected blockers

❓ HELP NEEDED:
- If anything stuck
```

### 2:00 PM UTC - Async PR Reviews
- Sage: Approve backend PRs (tests passed)
- Ivy: Approve test PRs (coverage OK)
- Nova: Approve frontend PRs (accessibility checked)

### 5:00 PM UTC - Merge & Deploy
- Remy: Reviews all approved PRs
- Remy: Merges to develop/main
- CI/CD: Automatically tests merged code

---

## 🎓 QUICK ONBOARDING

### Multi-Tenant Architecture in 2 Minutes
```python
# ✅ CORRECT: All queries filter by empresa_id
def get_productos(db: Session, empresa_id: UUID) -> List[Producto]:
    return db.query(Producto).filter(
        Producto.empresa_id == empresa_id  # ← This is critical!
    ).all()

# ❌ WRONG: Gets products from ALL companies (security breach!)
def get_productos(db: Session) -> List[Producto]:
    return db.query(Producto).all()  # ← BUG!

# How to extract empresa_id in routers:
@router.get("/api/v1/products")
async def list_products(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  # JWT
):
    empresa_id = current_user.empresa_id  # From JWT token
    return get_productos_by_empresa(db, empresa_id)
```

### Testing Pattern
```python
# tests/test_inventory.py
def test_create_producto(db, empresa, sample_categoria):
    """Create a product and verify all fields"""
    producto_data = ProductoCreate(
        nombre="Guayabera Yucateca",
        sku="GY-001",
        precio_base=50.00,
        categoria_id=sample_categoria.id
    )
    producto = create_producto(
        db, 
        obj_in=producto_data, 
        empresa_id=empresa.id
    )
    assert producto.nombre == "Guayabera Yucateca"
    assert producto.empresa_id == empresa.id  # Multi-tenant check
```

### Git Workflow
```bash
# 1. Start new task
git checkout -b feature/sprint-1-alembic-setup

# 2. Make changes, commit with [SPRINT-1] prefix
git commit -m "[SPRINT-1] Setup: Configure Alembic for PostgreSQL"

# 3. Push to GitHub
git push origin feature/sprint-1-alembic-setup

# 4. Create Pull Request on GitHub
# PR template:
# - What: [Brief description]
# - Why: [Business reason]
# - Tests: [Coverage % or test count]
# - Review: [Who should approve]

# 5. Wait for 2 approvals + CI green

# 6. (Remy merges via GitHub UI)
# - Regular merge (not squash/rebase)
```

---

## 🚨 CRITICAL RULES

### Code Quality
- ✅ All code must have type hints (Python: `-> UUID`, `List[Producto]`)
- ✅ All functions must have docstrings
- ✅ All queries must filter by `empresa_id` (multi-tenant)
- ✅ No hardcoded values (use `.env` for config)

### Testing
- ✅ Every endpoint must have at least 1 test
- ✅ Tests must be independent (no shared state)
- ✅ Tests must run in <10 seconds total
- ✅ Coverage target: >80% for inventory module

### Git
- ✅ Commit message format: `[SPRINT-1] Action: Description`
- ✅ No merging own PRs (wait for review)
- ✅ No force push to main/develop
- ✅ Branch names: `feature/sprint-1-*`, `fix/issue-*`

### Communication
- ✅ Blockers reported immediately to Remy
- ✅ Daily standup is non-negotiable
- ✅ Code reviews within 4 hours
- ✅ Ask questions before guessing

---

## 📊 SPRINT SUCCESS DASHBOARD

**Track Progress Here:**

| Task | Owner | Status | % Done | Deadline |
|------|-------|--------|--------|----------|
| T1.1 Alembic | Sage | ⏳ Ready | 0% | May 22 |
| T1.2 Models | Sage | 🔄 - | 0% | May 23 |
| T1.3 Schemas | Sage | ⏳ - | 0% | May 23 |
| T1.4 CRUD | Sage | ⏳ - | 0% | May 24 |
| T1.5 Routers | Sage | ⏳ - | 0% | May 25 |
| T1.6 pytest | Ivy | ⏳ Ready | 0% | May 22 |
| T1.7 Tests | Ivy | ⏳ - | 0% | May 26 |
| T2.1 CI/CD | Ivy+Sage | ⏳ - | 0% | May 27 |
| T2.2 Storybook | Nova | ⏳ - | 0% | May 27 |

**Status Legend:** ⏳ Ready | 🔄 In Progress | ✅ Done | ❌ Blocked

---

## 📞 HELP & ESCALATION

**Problem with your task?**
1. First: Check `PROJECT_BRIEF.md` + `SPRINT_1_PLAN.md`
2. Second: Ask in daily standup (9 AM UTC)
3. Third: Message your domain owner:
   - Backend issues → Sage
   - Test issues → Ivy
   - Frontend issues → Nova
   - Product questions → Kira
   - Scope/merge issues → Remy

**Blocked and can't move forward?**
- Notify Remy immediately
- Remy escalates to brainstorm if needed
- Decision made within 1 hour

**Need to change scope?**
- Ask Remy first: "Is X in scope for this sprint?"
- Remy decides: Ship vs defer vs cut
- Never add tasks without Remy approval

---

## 🎉 CELEBRATION MOMENTS

We'll celebrate:
- ✅ T1.1 complete: Alembic working
- ✅ T1.5 complete: First API endpoints live
- ✅ T1.7 complete: 20 tests passing
- ✅ T2.1 complete: CI/CD green
- 🏁 Sprint 1 done: Inventory module shipped!

---

## 📚 REFERENCE DOCUMENTS

All team members should bookmark:
1. **PROJECT_BRIEF.md** ← Source of truth
2. **AGENT_TEAM.md** ← Your role + team structure
3. **SPRINT_1_PLAN.md** ← This sprint's tasks
4. **MARCA_IDENTITY.md** ← Brand guidelines
5. **RESUMEN_TECNICO.md** ← Tech stack overview
6. **guayabera-erp-v2/README.md** ← How to run locally

---

## ✨ FINAL WORDS FROM REMY

> "Welcome to Sprint 1, team. This week we prove v2 is the right choice. We'll be methodical, test everything, and ship clean code. No scope creep—if it's not in the plan, we defer it. Everyone knows their tasks, everyone has support. Let's make this happen."

---

## 🎬 LET'S GO!

**Monday Morning (May 22 at 9 AM UTC):**

1. ✅ Daily standup
2. ✅ Sage starts T1.1 (Alembic)
3. ✅ Ivy starts T1.6 (pytest setup)
4. ✅ Progress updated in Slack

**By Friday EOD (May 28):**

```
✅ T1.1-T1.7 Complete
✅ 20 tests passing
✅ Inventory module ready
✅ CI/CD green
✅ PR merged to main
🚀 Sprint 1 Success
```

---

**Questions before we launch?**  
**Ready to deploy agents?**  
**Let's build Guayabera! 🧵✨**

---

**Last Updated:** May 21, 2026 02:28 UTC  
**Authored by:** Remy (Producer)  
**Next Checkpoint:** Daily Standup May 22 @ 9 AM UTC
