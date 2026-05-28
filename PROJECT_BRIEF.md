# PROJECT_BRIEF.md - Guayabera ERP Suite v2

**Owner:** tutsolo22  
**Repository:** Guayabera-QWEN  
**Current Branch:** main  
**Last Updated:** May 21, 2026  
**Status:** 🟡 In Active Development (Sprint 1)

---

## 1. PROJECT OVERVIEW

**Guayabera ERP Suite v2** es un sistema integral de planificación de recursos empresariales (ERP) especializado para la industria textil y manufacturera, con arquitectura multi-tenant y autenticación de superusuario global.

### Vision
Proporcionar a empresas textiles mexicanas una solución ERP completa, moderna y escalable que combine la robustez de soluciones líderes (CONTPAQi, Odoo) con la flexibilidad de plataformas web modernas.

### Brand Identity
- **Nombre:** Guayabera ERP Suite
- **Paleta:** Azul Profundo (#1B365D), Verde Empresarial (#2E8B57), Gris Noble (#F5F7FA)
- **Ver:** MARCA_IDENTITY.md

---

## 2. TECH STACK

### Backend
- **Framework:** FastAPI 0.104.1+ (Python 3.11)
- **ORM:** SQLAlchemy 2.0.23 + PostgreSQL 15
- **Auth:** JWT (Python-Jose)
- **Cache:** Redis
- **Tasks:** Celery
- **Testing:** pytest

### Frontend
- **Framework:** React 18+ (TypeScript)
- **UI:** Ant Design v5
- **State:** Redux Toolkit
- **Testing:** Vitest + Cypress

### Infrastructure
- **Containers:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Proxy:** NGINX
- **Security:** Let's Encrypt SSL

---

## 3. ARCHITECTURE

### Multi-Tenant Design
```
┌─────────────────────────────────┐
│    SUPERUSER (Global Admin)     │
│    - No pertenece a empresa     │
│    - Acceso todo el sistema     │
└──────────────┬──────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
   ┌────────┐      ┌────────┐
   │Tenant 1│      │Tenant 2│
   │(Empresa│      │(Empresa│
   │   A)   │      │   B)   │
   └────────┘      └────────┘
   ├─ Usuarios
   ├─ Productos
   ├─ Datos aislados
   └─ Recursos compartidos
```

### Data Isolation
- `empresa_id` en todos los modelos
- Queries automáticamente filtradas por tenant
- Seguridad de base de datos

---

## 4. MODULES (TARGET)

### ✅ Phase 1 (Sprints 1-2)
- **Autenticación:** Usuarios, Roles, Permisos
- **Base de Datos:** Migraciones, Seeders
- **Infrastructure:** CI/CD, Health Checks

### ⏳ Phase 2 (Sprints 3-5)
- **Inventario:** Productos, Almacenes, Movimientos
- **Ventas:** Clientes, Pedidos, Facturas
- **Finanzas:** Cuentas, Transacciones, Reportes

### ⏳ Phase 3 (Sprints 6-7)
- **Recursos Humanos:** Empleados, Nómina, Asistencia
- **Compras:** Proveedores, Órdenes, Recepción
- **Producción:** MRP, Órdenes de Producción

### ⏳ Phase 4 (Sprints 8+)
- **Integraciones:** Bancos, Email, OCR
- **IA/Analytics:** Predicción, OCR, Análisis
- **Reportes Avanzados:** BI, Dashboards, KPIs

---

## 5. CURRENT STATE

### v2 Status (Active)
- ✅ Backend: FastAPI estructura base
- ✅ Frontend: React + Ant Design v5 compilando
- ✅ Auth: JWT implementado (login/register)
- ✅ Docker: docker-compose.yml configurado
- ❌ Migraciones: Incompletas
- ❌ Tests: No existen
- ❌ CI/CD: No configurado

### Critical Issues
1. Migraciones Alembic no inicializadas
2. Sin tests unitarios (0% cobertura)
3. Modelos incompletos (solo auth)
4. Sin routers para módulos de negocio

---

## 6. SUCCESS METRICS

### Sprint Level
- ✅ All tests pass (green CI/CD)
- ✅ Zero regressions
- ✅ Code coverage +5% per sprint (target: 60% by release)

### Feature Level
- ✅ Acceptance criteria met
- ✅ QA sign-off
- ✅ No critical bugs

### Code Quality
- ✅ TypeScript strict mode
- ✅ Linting: 0 errors
- ✅ Documentation: Updated
- ✅ PR reviews: Approvals before merge

---

## 7. SPRINT PLANNING

### Sprint 1: Backend Foundation (Week 1, May 21-28)
**Goal:** v2 database + tests ready to go

**Prioritized Backlog:**
1. Alembic setup + migrations
2. Models: Inventario, Productos, Categorías
3. CRUD services para Productos
4. API routers para /api/v1/products
5. pytest setup + 20 basic tests
6. GitHub Actions CI/CD

**Agent Prompts Ready:** ✅
- Sage (Backend): Focus on database migrations + services
- Ivy (QA): Setup pytest framework + first tests
- Nova (Frontend): Storybook setup + base components

**Success Criteria:**
- `pytest tests/` passes 100%
- `alembic upgrade head` works
- GET/POST /api/v1/products responds
- CI green on GitHub

---

### Sprint 2: Testing Infrastructure (Week 2, May 28-June 4)
**Goal:** Comprehensive test framework + 25% code coverage

**Prioritized Backlog:**
1. Expand test suite (auth, models, services)
2. Frontend: Vitest + Cypress setup
3. Test data factories (Faker)
4. Coverage reports
5. Local test environment

**Success Criteria:**
- 25% code coverage
- Frontend tests compile
- All tests run in <60sec

---

### Sprint 3: Module Porting (Week 3-4, June 4-18)
**Goal:** Finanzas + RH modules functional

**Prioritized Backlog:**
1. Port Finance models from v1
2. Port HR models from v1
3. CRUD operations
4. Adapt to multi-tenant
5. Tests (50% coverage target)

**Success Criteria:**
- Finance CRUD works
- HR CRUD works
- No regressions
- 50% total coverage

---

### Sprint 4: Frontend Launch (Week 4-5, June 18-July 2)
**Goal:** Full UI for auth + product management

**Prioritized Backlog:**
1. Login/Register pages
2. Dashboard layout (brand colors)
3. Product CRUD pages
4. Form validation
5. E2E tests

**Success Criteria:**
- All pages render
- Forms submit correctly
- E2E tests pass

---

## 8. TEAM STRUCTURE

### **Remy** (Producer/You)
- Sprint planning + coordination
- PR reviews + merging
- Risk management
- Backlog prioritization

### **Sage** (Backend Lead)
- FastAPI architecture
- Database migrations
- Services + CRUD
- API contracts

### **Ivy** (QA Lead)
- Test strategy + frameworks
- Coverage reporting
- Bug triage
- Release validation

### **Nova** (Frontend Lead)
- React components
- UI/UX implementation
- E2E tests
- Accessibility

### **Kira** (Product)
- Feature specifications
- User stories
- Acceptance criteria
- Stakeholder coordination

### **Milo** (Design/Art)
- Visual design
- Brand implementation
- Component design
- Accessibility guidelines

---

## 9. GIT WORKFLOW

### Branch Strategy
```
main (stable, production-ready)
  ↑
  └─ develop (integration)
      ↑
      ├─ feature/sprint-1-*
      ├─ feature/auth-*
      └─ feature/products-*
```

### PR Requirements
- ✅ CI/CD green
- ✅ 2 approvals (code review)
- ✅ QA sign-off (for backend changes)
- ✅ 0 merge conflicts

### Commit Format
```
[SPRINT-1] Feature: Add product CRUD endpoints

- Created Product model with SQLAlchemy
- Implemented CRUD operations
- Added input validation with Pydantic
- 100% test coverage for service

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## 10. DOCUMENTATION

### Required Docs
- ✅ PROJECT_BRIEF.md (this file)
- ✅ MARCA_IDENTITY.md (brand guidelines)
- ✅ RESUMEN_TECNICO.md (tech overview)
- ⏳ API.md (OpenAPI spec)
- ⏳ CONTRIBUTING.md (dev guidelines)
- ⏳ docs/sprint-N/plan.md (per sprint)
- ⏳ docs/sprint-N/progress.md (daily updates)
- ⏳ docs/sprint-N/done.md (deliverables)

---

## 11. RISKS & MITIGATIONS

| Risk | Probability | Mitigation |
|------|-------------|-----------|
| Multi-tenant isolation failures | Medium | Automated tests per tenant |
| Database migrations conflicts | Low | Backup + dry-run before production |
| Auth token expiry issues | Low | Refresh token implementation |
| TypeScript strict mode blockers | Medium | Gradual migration per module |
| Frontend/Backend sync issues | Medium | Contract-first API design |

---

## 12. RELEASE PLAN

### v2.0.0 (Target: Aug 2026)
- ✅ Full authentication system
- ✅ Inventario + Productos
- ✅ Ventas básico
- ✅ Finanzas core
- ✅ RH basics
- ✅ 60% test coverage
- ✅ API documentation

### v2.1.0 (Q3 2026)
- Integraciones bancarias
- Reportes avanzados
- Mobile app
- IA/Predictive analytics

---

## 13. CONTACT & ESCALATION

- **Producer (Remy):** Sprint coordination + merging
- **Backend Issues:** Sage
- **Frontend Issues:** Nova
- **QA Issues:** Ivy
- **Product Decisions:** Kira
- **Escalations:** tutsolo22@github

---

**Last Updated:** May 21, 2026 02:28 UTC  
**Next Review:** After Sprint 1 Retrospective
