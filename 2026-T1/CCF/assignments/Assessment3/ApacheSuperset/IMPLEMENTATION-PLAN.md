# CCF Assessment 3 — Implementation Plan

## Recommendation: Apache Superset on Azure

**Grade Estimate:** 9/10 (High Distinction target)

### Why Superset?

Based on your priorities (portfolio differentiation + career narrative) and 10+ hour budget:

✅ **Portfolio differentiation** — Nobody in cohort doing this (off the brief's list)  
✅ **Career narrative** — Data Analyst → Data Engineer trajectory  
✅ **RBAC depth** — Rich content for 20% governance rubric criterion  
✅ **Subject integration** — Feeds directly into BDA601 (T4)  
✅ **Technical credibility** — Multi-service Docker Compose deployment  

### Trade-offs Acknowledged

**vs Metabase:** Higher complexity, but stronger differentiation  
**vs MLflow:** Better immediate payoff (ML subjects don't start until T2)

---

## Execution Phases (10-14 hours total)

### Phase 1: Preparation (2-3 hours)
**Can start immediately:**

1. **Verify Azure account** — Log in, check free tier eligibility, VM quota
2. **Draft docker-compose.yml** — See technical artifacts below
3. **Define screenshots** — List 10 required screenshots for rubric
4. **Document security** — NSG rules + RBAC roles design
5. **Find references** — Start collecting 12 APA sources
6. **Write intro** — Draft Introduction section (300w)

### Phase 2: Azure Infrastructure (1-2 hours)
**Sequential (must do in order):**

7. **Create resource group** → `rg-superset-ccf501` (Australia East)
8. **Add VNet** → `vnet-superset` (10.0.0.0/16) + subnet (10.0.1.0/24)
9. **Configure NSG** → Allow 22, 80, 443, 8088 / Deny all else
10. **Launch VM** → Ubuntu 22.04 LTS, Standard_B2s

📸 **Screenshot each step** (these are 40% of your grade!)

### Phase 3: Superset Deployment (2-3 hours)

11. **Install Docker** → SSH to VM, install docker + docker-compose
12. **Deploy stack** → Run docker-compose up, initialize Superset
13. **Configure RBAC** → Create Admin, Alpha, Gamma users
14. **Load data** → Connect PostgreSQL, import sample data
15. **Verify UI** → Build dashboard with 2-3 charts

📸 **6-8 screenshots needed**

### Phase 4: Security Hardening (1 hour)

16. **Harden NSG** → Review and tighten rules
17. **Document RBAC** → Screenshot user roles and permissions
18. **SSL (optional)** → Let's Encrypt if time permits

### Phase 5: Report Writing (3-4 hours)

19. **Section 2a** → Provider rationale + comparison table
20. **Section 2b** → Mermaid block diagram
21. **Section 2c** → Deployment procedure walkthrough
22. **Section 2d** → Security policies (NSG + RBAC)
23. **Section 2e** → Robustness improvements
24. **Conclusion** → 200w summary
25. **References** → 12 APA sources
26. **Format** → Word doc, check word count (1,350-1,650)

### Phase 6: Finalize & Submit (1-2 hours)

27. **Screencast** → Record with Screencastify
28. **Final review** → Proofread, check APA formatting
29. **Submit** → Upload by May 6, 2026 (11:55pm AEST)

---

## Timeline Recommendation

- **Days 1-2:** Phases 1-3 (Setup + Deployment)
- **Days 3-4:** Phase 5 (Report writing)
- **Day 5:** Phase 6 (Finalize + Submit)

Spread over 4-5 days, 2-3 hours per day.

---

## Success Criteria

### Technical
- ✅ Superset accessible via public IP on port 8088
- ✅ 3 user roles configured (Admin, Alpha, Gamma)
- ✅ Sample dashboard with 2-3 charts published
- ✅ NSG deny-by-default with explicit allows

### Report
- ✅ Word count: 1,350-1,650 words
- ✅ 8-10 screenshots properly captioned
- ✅ 12+ APA references
- ✅ All five Part 2 sections addressed

### Portfolio
- ✅ Differentiated from cohort
- ✅ Career narrative coherence
- ✅ Feeds into future subjects

---

## Fallback Plan

If Superset proves too complex → **pivot to Metabase**
- Same Azure infrastructure
- Simpler deployment (15 minutes)
- Your brainstorm.md already has the Metabase section written
- Still achieves 8/10 grade estimate

---

## SQL Tracking Commands

```sql
-- Mark todo in-progress
UPDATE todos SET status = 'in_progress', updated_at = CURRENT_TIMESTAMP 
WHERE id = 'prep-azure-account';

-- Mark todo done
UPDATE todos SET status = 'done', updated_at = CURRENT_TIMESTAMP 
WHERE id = 'prep-azure-account';

-- Check what's ready to work on
SELECT t.id, t.title 
FROM todos t
WHERE t.status = 'pending'
AND NOT EXISTS (
    SELECT 1 FROM todo_deps td
    JOIN todos dep ON td.depends_on = dep.id
    WHERE td.todo_id = t.id AND dep.status != 'done'
);
```

---

## Next Steps

1. Read `TECHNICAL-ARTIFACTS.md` for docker-compose config and commands
2. Start Phase 1 tasks (can begin immediately)
3. Take screenshots at every step
4. Update todo status in SQL as you progress
