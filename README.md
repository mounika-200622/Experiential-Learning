# 🎓 Lab 1: Requirements Engineering & UML Use-Case Modelling

![Status](https://img.shields.io/badge/status-completed-brightgreen)
![Course](https://img.shields.io/badge/course-Software%20Engineering-blue)

**Problem Statement:** #06 — Alumni Mentorship & Mock Interview Platform
**Domain:** Campus & Academic Operations

---

## 📌 Problem Context

Connecting students with alumni working in specialized domains requires an intelligent matching mechanism, availability calendar booking, and structured post-interview scorecard recording.

**👥 Stakeholders / Actors**
| Actor | Role |
|---|---|
| 🧑‍🎓 Student Mentee | Seeks mentorship, books sessions |
| 👨‍💼 Alumni Mentor | Provides mentorship, manages availability |
| 🔔 Notification System | Sends automated reminders |

---

## 🎯 Objective

From the given scenario, elicit key functions and constraints, write clear and verifiable **Functional (FR)** and **Non-Functional (NFR)** requirements, and translate them into a **UML use-case diagram** and a **use-case flow specification**.

---

## 📂 Deliverables

| File | Description |
|---|---|
| 📄 `Requirements_Table.pdf` | 5 FRs + 2 NFRs with ID, Type, Description, Priority, Acceptance Criteria, Rationale |
| 🖼️ `UML_UseCase_Diagram.pdf` | Actors, use cases, one `«include»` and one `«extend»` relationship |
| 📃 `UseCase_Flow.pdf` | One-page flow for UC-02 (Book Mentorship Session) |

---

## 📋 Requirements Summary

| Req ID | Type | Priority | Description |
|---|---|---|---|
| FR-001 | Functional | 🔴 High | Recommend alumni mentors based on domain matching + one-click booking |
| FR-002 | Functional | 🔴 High | Allow mentors to set/update weekly availability |
| FR-003 | Functional | 🟡 Medium | Allow students to view mentor profiles before booking |
| FR-004 | Functional | 🔴 High | Allow mentors to submit post-interview scorecards |
| FR-005 | Functional | 🟡 Medium | Send automated reminders (24h & 1h before session) |
| NFR-001 | Non-Functional | 🔴 High | Data privacy compliance + 24h soft-deletion |
| NFR-002 | Non-Functional | 🟡 Medium | Support 500 concurrent users, <3s response time |

📎 *Full details with Acceptance Criteria & Rationale → see `Requirements_Table.pdf`*

---

## 🧩 Use-Case Model

**Actors:** Student Mentee · Alumni Mentor · Notification System

**Use Cases:**
- `UC-01` Search / Match Mentor
- `UC-02` Book Mentorship Session
- `UC-03` Manage Availability
- `UC-04` View Mentor Profile
- `UC-05` Submit Post-Interview Scorecard
- `UC-06` Send Session Reminder

**Relationships:**
> 🔗 `UC-02` **«include»** `UC-06` — every booking automatically triggers a reminder
> 🔗 `UC-04` **«extend»** `UC-01` — viewing a profile is an optional step during mentor search

---

## 🔄 Use-Case Flow — UC-02: Book Mentorship Session

**Primary Actor:** Student Mentee
**Secondary Actor:** Alumni Mentor

**✅ Preconditions**
- Student is logged in
- At least one matching mentor has published availability

**🏁 Postconditions**
- Confirmed session exists on both calendars with a meeting link
- Booked slot marked unavailable

**➡️ Main Success Scenario**
1. Student searches by domain
2. Selects a mentor
3. Picks a time slot
4. System confirms booking, updates calendars, sends confirmation

**⚠️ Alternate Flow**
If the selected slot is booked by someone else in the interim, the system notifies the student and displays the mentor's remaining available slots.

📎 *Full step-by-step flow → see `UseCase_Flow.pdf`*

---

## 🛠️ Tools Used
- Diagramming: UML use-case notation (draw.io style)
- Documentation: Word / PDF

---

## 👩‍💻 Author
**Mounika** · [@mounika-200622](https://github.com/mounika-200622)
