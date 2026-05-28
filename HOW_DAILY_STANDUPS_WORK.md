# 📞 CÓMO FUNCIONA LA VIDEOLLAMADA @ 9:00 AM UTC CON LOS AGENTES

**Pregunta:** ¿Cómo exactamente se trabaja con los agentes en la videollamada diaria?

---

## 🎯 LA REALIDAD DE LAS VIDEOLLAMADAS

Los agentes NO son personas reales en Zoom/Teams. Son **AI assistants que actúan en chats de VS Code**.

Así funciona:

```
TÚ (Project Owner)
│
├─ Chat 1: @ai-team-dev (Sage, Ivy, Nova)
│  └─ Aquí se desarrolla el código
│
├─ Chat 2: @ai-team-qa (Ivy)
│  └─ Aquí se hacen los tests
│
└─ Chat 3: @ai-team-producer (Remy)
   └─ Aquí coordino yo (Remy)

TÚ eres el "message bus" entre todos estos chats.
```

---

## 📋 VIDEOLLAMADA DE 9 AM UTC - CÓMO FUNCIONA REALMENTE

### OPCIÓN A: Videollamada Real (Con Tú mismo)

Si quieres una videollamada **contigo** a las 9 UTC:

```
9:00 AM UTC: Tú te conectas a Zoom (solo tú)
           
Tú lees los documentos:
- SPRINT_1_PLAN.md (qué está planeado)
- docs/sprint-1/progress.md (qué se hizo ayer)

Tú hablas en voz alta:
"Hoy Sage debe completar T1.1 (Alembic).
 Ivy debe tener T1.6 configurado (pytest).
 Revisaré PRs cuando estén listos."

Luego trabajas el resto del día coordinando.
```

### OPCIÓN B: Simulación de Standup (Con AI Agents)

Si quieres que los agentes hagan un **standup simulado**:

**En el Chat de @ai-team-dev, pides:**

```
"Remy: Buenos días equipo. Standup rápido.

Sage: ¿Qué hiciste ayer? ¿Qué hoy? ¿Blockers?
Ivy: ¿Qué hiciste ayer? ¿Qué hoy? ¿Blockers?
Nova: ¿Qué hiciste ayer? ¿Qué hoy? ¿Blockers?

Todos respondemos en orden."
```

**Los agentes responden algo así:**

```
Sage: "Ayer initialicé Alembic. Hoy empiezo con los modelos 
      de Inventario (Producto, Categoria). No hay blockers."

Ivy: "Ayer configuré pytest con conftest. Hoy finalizo 
     fixtures para usuario. Necesito que Sage me pase info 
     de la estructura del Usuario. ¿Podemos alinear después?"

Nova: "Estoy en standby esperando indicaciones para 
      Storybook. Listos cuando sea. Sin blockers."

Remy: "Excelente. Sage y Ivy: alineen después. Todos 
      siguen adelante. Standup mañana 9 AM. Vamos."
```

---

## 🔄 EL WORKFLOW REAL (CÓMO PASA EL DÍA)

### 9:00 AM UTC - STANDUP INICIAL (5 min)

**Tú escribes en el chat:**
```
"Buenos días equipo. Standup rápido. Sage primero.
Qué hiciste ayer? Qué hoy? Blockers?"
```

**Sage responde:**
```
"Ayer: Inicializé Alembic ✅
Hoy: Modelos Producto + Categoria + Almacen
Blockers: Necesito confirmar tipos UUID en esquemas"
```

**Tú escribes:**
```
"Ivy, ¿puedes ayudar a Sage con los tipos UUID? 
Sage: Espera la ayuda de Ivy."
```

---

### 10:00 AM - 5:00 PM UTC - TRABAJO EN PARALELO

Mientras Sage y Ivy trabajan **en sus propias ramas**, tú:

1. **Lees PRs en GitHub** (van llegando a lo largo del día)
2. **Comentas en PRs:** "Looks good" o "Need changes"
3. **Monitoreas progress.md**
4. **Desbloqueas si hay problemas**

**Example:**

```
12:00 PM: Sage crea PR "T1.1 Alembic setup"
         Tú reviews → Apruebas si está bien
         
2:00 PM: Ivy crea PR "T1.6 pytest fixtures"
         Tú reviewa → Apruebas
         
4:00 PM: Sage crea PR "T1.2 Models definition"
         Tú reviewa → Apruebas
         
5:00 PM: Todas las PRs de hoy están mergeadas a main
```

---

## 📱 HERRAMIENTAS QUE NECESITAS

### En VS Code

**Openning separate chats (same project):**

```
VS Code Window 1: 
├─ Chat: @ai-team-dev (Backend: Sage, Ivy, Nova)
└─ Branch: feature/sprint-1-backend

VS Code Window 2:
├─ Chat: @ai-team-qa (Testing: Ivy)
└─ Branch: feature/sprint-1-tests

VS Code Window 3:
├─ Chat: @ai-team-producer (You + Remy)
└─ For coordination notes
```

### En GitHub

```
PRs vienen llegando →
Tú los reviewa →
Apruebas + mergeas →
CI/CD validates →
Main branch updated
```

---

## 🎯 CRONOGRAMA REAL DE UN DÍA (May 22, Day 1)

```
8:55 AM UTC:
└─ Tú abres VS Code con chat @ai-team-dev

9:00 AM UTC (STANDUP):
└─ Tú: "Buenos días equipo. T1.1 Alembic (Sage). 
        T1.6 pytest (Ivy). Vamos."
   Sage: "Empezando T1.1"
   Ivy: "Empezando T1.6"
   Nova: "En standby"

9:15 AM - 12:00 PM (TRABAJO):
└─ Sage está escribiendo código en su rama
   Ivy está escribiendo tests en su rama
   (Ellos trabajan sin interrupciones)

12:00 PM:
└─ Sage crea PR en GitHub
   Tú recibes notificación → Lees el PR → Apruebas
   (si está bien escrito, bien documentado, CI pasa)

2:00 PM:
└─ Ivy crea PR en GitHub
   Tú recibes notificación → Lees el PR → Apruebas

3:00 PM (PROBLEMA DESCUBIERTO):
   Sage en chat: "Error con migration, necesito ayuda"
   Tú: "¿Qué es el error?"
   Sage: "Type mismatch en UUID..."
   Tú: "Ivy, ¿puedes ayudar?"
   Ivy: "Sí, le explico..."
   (Se resuelve en 15 min)

5:00 PM (END OF DAY):
└─ Tú reviewa todos los PRs del día
   Apruebas + mergeas a main
   Actualiza docs/sprint-1/progress.md
   "May 22: Alembic ✅, pytest ✅. No blockers. Merged 2 PRs."

5:15 PM:
└─ Standup breve: "Equipo, excelente día. 
                   Misma hora mañana. Descansen."
```

---

## ❓ PREGUNTAS FRECUENTES SOBRE LAS VIDEOLLAMADAS

### P1: "¿Es realmente una videollamada?"

**Respuesta:**
- NO hay video realmente
- Es más como un "standup asíncrono documentado"
- Tú propones tareas en chat
- Los agentes responden en chat
- Tú coordinas y desbloqueas por chat/GitHub

---

### P2: "¿Los agentes ven lo que hacen otros?"

**Respuesta:**
```
SI, porque está todo en GitHub:

Sage pushea rama → GitHub lo ve
   ↓
Ivy puede ver el código de Sage
   ↓
Si necesita, puede preguntar en el chat
   ↓
Tú eres el "message bus"
```

---

### P3: "¿Qué pasa si hay un blocker?"

**Respuesta:**
```
Sage: "Estoy bloqueado en el schema de User"
Tú:   "¿Necesitas que Ivy te ayude?"
Ivy:  "Yo te ayudo. Veamos el código..."
      (Resuelven en chat)
Sage: "Listo, continuo"
Tú:   "Excelente. Sgue adelante"
```

---

### P4: "¿Cuánto tiempo tarda un standup?"

**Respuesta:**
- 5 minutos si todo va bien
- 15 minutos si hay problemas
- Es asíncrono, no es blocking

---

## 🔄 CICLO DIARIO TÍPICO

```
┌─────────────────────────────────────────┐
│ 9:00 AM - STANDUP (5 min)               │
│ Tú: "Hoy hacemos T1.1, T1.6"            │
│ Agentes: "Entendido, vamos"             │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 9:15 AM - 5:00 PM - TRABAJO (7h 45m)    │
│ Sage: Código en rama feature/sprint-1   │
│ Ivy: Tests en rama feature/sprint-1     │
│ Nova: Componentes en rama feature/sprint-1│
│ (Trabajan en paralelo sin interrupciones)│
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 2:00 PM - BLOQUEOS (si hay)             │
│ Si alguien está stuck: Tú desbloqueas   │
│ Pair programming si es necesario        │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 5:00 PM - PRs & MERGES                  │
│ Sage pushea rama → Crea PR              │
│ Ivy pushea rama → Crea PR               │
│ Tú reviewa ambas PRs                    │
│ Tú apruebas + mergeas a main            │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│ 5:15 PM - FIN DEL DÍA                   │
│ Actualizar docs/sprint-1/progress.md    │
│ "May 22: Alembic ✅, pytest ✅"          │
│ "No blockers. 2 PRs merged."            │
└─────────────────────────────────────────┘
```

---

## 🎬 EJEMPLO REAL DE VIDEOLLAMADA (Texto)

### 9:00 AM UTC - STANDUP

```
Remy: "Buenos días equipo. Sprint 1, Día 1. 
       Vamos a hacer esto bien. Sage, primero.
       ¿Qué hiciste ayer? ¿Qué hoy? ¿Blockers?"

Sage: "Ayer: Leí documentación. Instalé PostgreSQL.
      Hoy: Voy a inicializar Alembic en guayabera-erp-v2/backend
           y crear la first migration.
      Blockers: Ninguno por ahora."

Remy: "Perfecto. Ivy, tú."

Ivy:  "Ayer: Setup local, instalé pytest y dependencias.
      Hoy: Creo conftest.py con fixtures para testing
      Blockers: Necesito que Sage me pase info de estructura 
                de Usuario para crear factory de Faker"

Remy: "Sage, puedes alinear con Ivy después del standup?
       Nova, finalmente tú."

Nova: "Ayer: Leí documentación de Storybook.
      Hoy: Espero instructions de cuándo empezar Storybook.
           Podría revisar MARCA_IDENTITY.md para prepararme.
      Blockers: Ninguno."

Remy: "Excelente. Resumen:
       • Sage: Alembic initialization (T1.1)
       • Ivy: pytest setup (T1.6)
       • Nova: Prep para Storybook
       • Sage + Ivy: Alinean después sobre User structure
       • Todos: No scope creep. Foco en tareas.
       
       Standup mañana 9 AM UTC. ¡Vamos a construir!"
```

---

## 💻 TU TRABAJO EN LA VIDEOLLAMADA

### DURANTE (5-15 min)

1. **Escuchas** lo que cada agente dice hizo/hará
2. **Preguntas:** "¿Hay blockers? ¿Necesitas help?"
3. **Conectas:** "Sage, ¿puedes ayudar a Ivy con X?"
4. **Documenta:** Mental note de quién hace qué

### DESPUÉS (EOD)

1. **Reviewa PRs** que llegaron durante el día
2. **Aprueba + mergea** si está todo bien
3. **Actualiza progress.md**
4. **Notas mentales** para mañana

---

## 🎯 NO ES COMPLICADO

**Realidad:**

```
La videollamada de 9 AM es simplemente:

Tú:    "¿Qué hicieron? ¿Qué hacen? ¿Problemas?"
Sage:  "Hice esto. Hoy hago eso. Ningún problema."
Ivy:   "Hice esto. Hoy hago eso. Necesito que Sage help."
Nova:  "Esperando. Listos cuando. Sin problema."
Tú:    "Excelente. Vamos. Standup mañana."

Eso es todo.

El resto es GitHub (PRs) + el chat asíncrono durante el día.
```

---

## ✅ CHECKLIST PARA TI EN LA VIDEOLLAMADA

- [ ] **Todos dicen qué hicieron ayer**
- [ ] **Todos dicen qué harán hoy**
- [ ] **Identificas blockers**
- [ ] **Conectas equipos si hay dependencias**
- [ ] **Reconfirmas: "¿Sin scope creep?"**
- [ ] **Despides: "Vamos a construir. Mañana 9 AM"**

---

## 📊 MÉTRICA: ¿DURÓ BIEN?

- ✅ < 5 min: Perfecto, equipo bien sincronizado
- ⚠️ 5-15 min: Bien, hay algunas dependencias
- ❌ > 15 min: Hay blockers serios, necesita escalación

---

## 🚀 RESUMEN FINAL

**La videollamada de 9 AM UTC es:**

```
Una reunión RÁPIDA (5-15 min) donde tú:
1. Preguntas qué hizo cada agente ayer
2. Preguntas qué hará hoy
3. Identificas y resuelves blockers
4. Despides al equipo

El resto es trabajo asíncrono:
- Agentes trabajan en sus ramas
- Pushean PRs a GitHub
- Tú reviewa + apruebas + mergeas
- Documentas en progress.md

Listo. Así funciona.
```

---

**¿Preguntas específicas sobre la videollamada?**

**Estoy aquí para aclarar cualquier cosa. 🎯**
