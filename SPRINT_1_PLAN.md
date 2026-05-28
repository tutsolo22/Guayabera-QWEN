# Sprint 1: Backend Foundation (May 21-28)

**Status:** ✅ READY FOR KICKOFF

## Quick Overview

**Goal:** v2 Backend foundation with Inventario module + 20 tests  
**Team:** Sage (Backend), Ivy (QA), Nova (Frontend), Remy (Producer)  
**Duration:** 7 days  
**Success:** `pytest tests/ -v` → 20/20 PASS + `alembic upgrade head` OK

---

## Critical Path (T1.1 → T1.2 → T1.3 → T1.4 → T1.5)

1. **T1.1 Alembic Setup** (2h, May 22) - Sage
2. **T1.2 Models** (3h, May 23) - Sage  
3. **T1.3 Schemas** (2h, May 23) - Sage
4. **T1.4 CRUD** (4h, May 24) - Sage
5. **T1.5 Routers** (3h, May 25) - Sage

Parallel:
6. **T1.6 pytest** (2h, May 22) - Ivy
7. **T1.7 Tests** (4h, May 26) - Ivy
8. **T2.1 CI/CD** (2h, May 27) - Ivy+Sage
9. **T2.2 Storybook** (2h, May 27) - Nova

---

## Task Details (Abbreviated)

### T1.1: Alembic Migrations
- Initialize Alembic in v2/backend
- Configure PostgreSQL connection
- Test: `alembic upgrade head` ✅

### T1.2: Inventario Models
- Categoria, Producto, Almacen, MovimientoInventario
- Multi-tenant with empresa_id
- Foreign keys + relationships

### T1.3: Pydantic Schemas
- CategoriaCreate/Read/Update
- ProductoCreate/Read/Update
- AlmacenCreate/Read/Update
- MovimientoInventarioCreate/Read

### T1.4: CRUD Operations
- get/create/update/delete for each model
- Multi-tenant filtering
- Error handling

### T1.5: API Routers
- GET/POST /api/v1/products
- GET/POST /api/v1/categorias
- GET/POST /api/v1/almacenes
- GET/POST /api/v1/movimientos

### T1.6: pytest Framework
- Install test deps
- conftest.py fixtures
- Coverage config

### T1.7: 20 Unit Tests
- Models tests (4)
- CRUD tests (8)
- API endpoint tests (8)
- Coverage: >80%

### T2.1: GitHub Actions
- `.github/workflows/ci.yml`
- Auto-test on push

### T2.2: Storybook
- Component documentation
- Brand colors

---

## Daily Standups (9 AM UTC, 15 min max)

**Template:**
```
✅ YESTERDAY:
- [Task + status]

📅 TODAY:
- [Planned work]

❓ BLOCKERS:
- [If any]
```

Log to: `docs/sprint-1/progress.md`

---

## Success Criteria ✅

- [ ] 20/20 tests passing
- [ ] >80% inventory coverage
- [ ] `alembic upgrade head` works
- [ ] All endpoints respond 200
- [ ] CI/CD green
- [ ] Zero blockers

---

## Escalation

- **Backend Issues:** Sage
- **Test Issues:** Ivy
- **Scope Questions:** Remy
- **Product Decisions:** Kira

---

**Ready to kickoff? Start with T1.1 (Alembic)**
