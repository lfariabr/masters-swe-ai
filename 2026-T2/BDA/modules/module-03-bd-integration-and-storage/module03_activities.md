# Module 3 — Activity Responses

> Drafts for the Module 3 learning activities. Activity 1 is a written discussion-forum post; Activity 2 is a self-taken knowledge check.

---

## Activity 1 — Discussion Forum: Cost models of AWS S3 vs ADLS Gen2

**Brief:** explore the cost models of AWS S3 and ADLS Gen2, say which is more cost-effective for big-data storage (your opinion + why), and note other factors to consider (~150 words). Then reply to at least one peer.

### Main post (~150 words)

Both Amazon S3 and Azure Data Lake Storage (ADLS) Gen2 are pay-as-you-go, with three cost levers: **storage** (per GB/month), **transactions/requests** (per 10,000 operations), and **data egress** (transfer out). Both cut storage cost via **access tiers** — S3's Standard / Infrequent-Access / Glacier and ADLS's Hot / Cool / Cold / Archive — where colder tiers are cheaper to store but charge retrieval fees and add latency.

In my opinion, for a general data lake where access patterns are **unpredictable**, S3 is marginally more cost-effective because **S3 Intelligent-Tiering** auto-moves objects between tiers with no retrieval penalty, removing the guesswork. ADLS Gen2 wins when you already run the **Azure analytics stack** (Synapse, Databricks): co-locating storage and compute avoids egress, which is often the hidden cost.

Other factors: **transaction pricing**, **retrieval fees/latency** on cold tiers, **reserved-capacity discounts**, **data gravity** (co-location with compute), and **governance/security** features.

### Peer reply (~50 words — adapt to whoever posted)

I agree S3 Intelligent-Tiering is a sensible default for an unpredictable lake. I'd add that the verdict hinges on **egress**: if your analytics compute lives in Azure, ADLS often wins overall, because cross-cloud transfer-out can dwarf the per-GB storage gap. Did your comparison account for egress and transaction costs?

> 🔎 **Verify before posting:** exact $/GB and per-10k-transaction rates change often and vary by region. Confirm current numbers on the live pricing pages rather than quoting figures from memory:
> - AWS S3 pricing — https://aws.amazon.com/s3/pricing/
> - Azure Blob / ADLS Gen2 pricing — https://azure.microsoft.com/pricing/details/storage/data-lake/
> The **cost-model structure** above (tiers · transactions · egress · pay-as-you-go) is stable; only the headline rates drift.

---

## Activity 2 — Interactive Knowledge Check

No written deliverable — this is the in-LMS quiz (retake as often as you like): https://mylearn.torrens.edu.au/courses/26571/files/10605037/preview?

**Concepts to have cold before you attempt it** (from [module03_notes.md](module03_notes.md)):
- **Integration pipeline:** schema alignment → record linkage → data fusion (and which ambiguity each solves).
- **Why NoSQL over relational** for big data (schema-less, horizontal scale, availability).
- **4 NoSQL data models:** key-value · column-oriented · document · graph — plus a sample engine for each.
- **CAP theorem:** partition-resilience is mandatory → the real choice is **CP (consistency) vs AP (availability)**; know one CP and one AP engine.
- **Lake storage:** S3 vs ADLS Gen2, and "performance → less compute → lower cost".

> Mark this ✅ once you've passed the check.
