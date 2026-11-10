# Module 9 · Activity 1 - Organisation X: reviewing quality controls across a systems integration (draft)

**Status:** 🔥 draft for Luis to review, then post to the discussion forum and comment on two posts. No word limit in the brief; kept near 300 words.

---

Organisation X is in financial services, so a quality failure is not just rework: it can be a wrong balance in a client's statement. The review has to show that the pilots were checked against requirements that were measurable in the first place.

**1. How I would review the quality controls**

- **Start from the requirements, not the tests.** For each pilot, check that every quality requirement has Penzenstadler's (2018) four parts: a description, a metric, how it is measured, and the reason. "The integration should be reliable" fails. "Zero unreconciled transactions over a month's replay, because a mismatch reaches a client" passes.
- **Sample the evidence.** Pick a few verified pilots and trace one requirement through to a test result and a sign-off by a named owner.
- **Price the failures.** Log the rework, the defects found late and the incidents. Mahmood et al. (2014) show the cost of poor quality stays hidden until someone records it.

**2. Key processes to analyse**

- Requirements and change control.
- Data mapping and reconciliation between systems.
- Testing and regression after fixes. A fix can introduce a new fault (Zhang & Pham, 2001).
- Release gates, access control and audit logging, given the regulator.
- Hand-offs between the external QA specialists and the internal engineer.

**3. Updating the quality policy**

Probably yes, if the review finds objectives that cannot be measured. Basu (2012) puts it plainly: if you cannot define it, you cannot measure, control or improve it. I would run the update as a PDCA cycle:
1. Draft measurable objectives per function.
2. Pilot them on the next integration.
3. Check the results.
4. Have management sign the revised policy.

Zhang (2001) adds that internal, objective measures, such as defect rates, are the precondition for the external, subjective ones, such as client satisfaction.

In my placement, the smallest version of this is a written rules note, then a row-by-row comparison before anything reaches staff.

**Question for you:** with external QA specialists involved, who should own the quality policy, them or the internal engineer?

---

### References
- Basu, R. (2012). Introduction: Why managing quality is essential in project management. In *Managing quality in projects* (pp. 1-12). Taylor & Francis.
- Mahmood, S., Ahmed, S. M., Panthi, K., & Kureshi, N. I. (2014). Determining the cost of poor quality and its impact on productivity and profitability. *Built Environment Project and Asset Management, 4*(3), 296-311. https://doi.org/10.1108/BEPAM-09-2013-0034
- Penzenstadler, B. (2018, April 16). *Quality requirements - RE learning glass lecture 14* [Video].
- Zhang, Q. (2001). Quality dimensions, perspectives and practices: A mapping analysis. *International Journal of Quality & Reliability Management, 18*(7), 708-721.
- Zhang, X., & Pham, H. (2001). A software reliability model with testing coverage and imperfect debugging. In H. Pham (Ed.), *Recent advances in reliability and quality engineering* (pp. 17-31). World Scientific.
