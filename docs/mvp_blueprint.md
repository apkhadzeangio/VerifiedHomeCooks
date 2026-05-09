# Verified Home Cooks — Exact MVP Scope (One-District Launch, Tbilisi)

## Product Boundary for This MVP
This MVP is intentionally limited to **one district in Tbilisi** (e.g., Vake as pilot district) so operations, moderation, and delivery coordination stay manageable.

Primary launch objective:
- Let customers discover **verified** home cooks and their dishes.
- Let customers place and track simple orders.
- Let cooks manage dishes.
- Let admins verify cooks and moderate content.

---

## 1) Must-have for launch
These are required to go live.

### A. Accounts & access
- Customer registration/login/logout (email + password)
- Cook registration/login/logout
- Admin login
- Role-based access control (customer/cook/admin pages separated)

### B. Cook verification and trust
- Cook application form (basic identity/contact + short profile)
- Admin approval/rejection of cook applications
- Visible cook verification badge/status on public cook page
- Only **approved cooks** can publish visible dishes

### C. Marketplace browsing (customer)
- Public homepage with value proposition and CTAs
- Browse list of verified cooks in the pilot district
- Cook profile page with approved dishes
- Dish card/details with:
  - photo
  - title
  - price (GEL)
  - ingredients
  - allergens
  - availability for today

### D. Cook dish management
- Cook dashboard (basic)
- Add/edit/unpublish dishes
- Mark dish available/unavailable for today
- Dish moderation workflow:
  - cook submits dish
  - admin approves/rejects
  - only approved dishes are visible to customers

### E. Ordering (core transaction)
- Customer selects dish quantity and places order
- Order contains customer info, cook, items, totals, note, delivery/pickup choice
- Order status flow (simple):
  - `placed`
  - `accepted`
  - `preparing`
  - `ready`
  - `completed`
  - `canceled`
- Customer can view order status page
- Cook can update status on own orders
- Basic safeguards:
  - customer sees only own orders
  - cook sees only own incoming orders

### F. Admin content control
- Admin queue for pending cook applications
- Admin queue for pending dishes
- Ability to approve/reject and add short moderation note
- Ability to hide/unpublish problematic dish

### G. Operational basics
- Responsive Bootstrap UI (mobile-first enough for real use)
- Server-side validation for forms and order totals
- Basic audit trail for key status changes
- Error handling pages (404/500 minimal templates)

---

## 2) Should-have after launch (next 4–8 weeks)
Important, but not blocking day-1 launch.

- Customer reviews/ratings after completed orders
- Complaint submission and admin complaint queue
- Cook metrics widgets (today's orders, completed count)
- Admin quick filters/search (by cook, status, date)
- Soft district boundary enhancements (address hints, delivery notes)
- Basic notification emails (order placed/accepted/ready)
- Better dish photo guidelines and moderation rules in admin UI

---

## 3) Later version
Build once pilot demand and operations are stable.

- Online payments (card gateway integration)
- Promo codes and referral system
- Real-time chat between cook and customer
- Multi-district expansion across Tbilisi
- Georgian/English full i18n support (content + validation messages)
- Reorder/favorites and personalized recommendations
- Advanced analytics (retention, cohort, cook SLA)
- Courier/logistics integrations
- Native mobile apps

---

## 4) Do not build now
Explicit anti-scope to protect MVP speed.

- Complex microservices architecture
- Real-time websocket-heavy features from day 1
- Automated fraud scoring system
- Dynamic surge pricing
- Enterprise BI warehouse stack
- Full marketplace escrow/payment-wallet system
- AI recommendation engine before reliable baseline data exists

---

## Pilot Constraints (One District in Tbilisi)
To keep MVP functional and realistic:

- Operate in **one district only** at launch (config constant in settings later).
- Show only cooks flagged as operating in that district.
- Keep delivery model simple: `pickup` or `local delivery` set by cook.
- Keep support flow manual-admin first; no heavy automation.

---

## MVP Acceptance Criteria (Launch Readiness)
MVP is launch-ready only if all are true:

1. Customer can browse verified cooks and approved dishes in pilot district.
2. Customer can place an order and see status updates.
3. Cook can add/edit dishes and manage availability.
4. Admin can approve cooks, approve dishes, and hide content when needed.
5. Role and data permissions prevent cross-account data exposure.
6. Core journey works on mobile and desktop browsers without breaking.

---

## Recommended Tech Direction (kept simple)
- Django monolith
- Server-rendered templates
- Bootstrap UI
- PostgreSQL
- Django admin + lightweight custom admin pages for moderation queues

This keeps development and maintenance cost low while supporting a real production pilot.
