# Module 12 — Learning Activities: Drafts

Draft answers for the discussion forum. 

---

## Activity 1: Analyse the Facebook Data Privacy Scandal

Facebook's actual response followed the same pattern almost every time: deny it's a "breach" ("no systems were infiltrated"), delay a real statement by days, then issue a templated apology from Zuckerberg ("this was a big mistake... I'm sorry"). That pattern repeated across at least a dozen separate incidents between 2007 and 2020 - Beacon, the 2013 shadow-profile bug, Cambridge Analytica, the 2018 access-token breach, the 2019 plaintext-password storage. The Cambridge Analytica case specifically wasn't a hack - Kogan's app legitimately used Facebook's own API, and the platform's real failure was a **governance** one: no oversight of what third-party developers did with data after collection, permissive default sharing (friends' data pulled in without those friends' consent), and terms of service too broad for users to meaningfully understand what they'd agreed to.

I would not have responded the same way. Two things I'd have done differently:

1. **Audit-then-disclose, not deny-then-amend.** Facebook's habit was to minimise publicly first ("not a breach") and only walk it back once journalists forced the issue - that's the opposite of Ohlhorst's data-classification instinct: know what you're liable for *before* you're asked, not after.
2. **Process-based access controls on the developer API**, applied years earlier. The single root cause across nearly every incident in the timeline is the same: an app or partner had access to *far more* data than its stated purpose required (friends-of-friends data, address books, even data from users who'd opted out). Ohlhorst's "control access by process, not job function" principle applies just as well to third-party developers as to internal staff - Facebook only started meaningfully restricting API scope in 2018, a full four years after the Kogan app first collected the data.

The GDPR connection makes the failure sharper: the EU's Article 6 lawful-basis requirement and Article 25 "data protection by design and default" principle are essentially a codified version of what Facebook should have been doing voluntarily. That the regulation only forced the fix after the scandal, rather than the fix pre-empting the need for regulation, is the real lesson.

---

## Activity 2: Review All Things Big Data and Analytics (closing discussion)

Talking points for the vocal discussion:

- **Most important topic**: data quality and governance underpins everything else in the subject - clustering, association rules, graph analytics are all only as good as the data feeding them, and Module 12 makes explicit what was implicit all along: if you don't classify and control access to data properly, none of the analytics matter because you either can't trust the output or you're not legally allowed to have run the analysis in the first place.
- **Most interesting**: graph analytics (Module 11) - reframing link prediction as an ordinary supervised classification problem (drop edges → positive labels, unconnected pairs → negative labels) was the one "click" moment in the subject where a completely different-looking technique turned out to be the same toolkit already in use elsewhere.
- **Weakest area, and how to fix it**: privacy/security is the weakest-covered area relative to how much it actually gates real-world Big Data work - one module at the very end, versus a full assessment's worth of technical modules (clustering, association rules, graph analytics). In practice, governance questions come *first*, not last (what are you allowed to collect, keep, and analyse), so treating it as a closing "ethics" module rather than a foundational constraint understates how much it shapes every technical decision earlier in a real pipeline.
