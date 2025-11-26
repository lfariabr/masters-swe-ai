# Slide 1 - INTELLIGENT RATE LIMITING SYSTEM
**Subtitle**: Restoring Human Agency in Autonomous AI Systems  
**Speaker**: Luis

Good afternoon. I'm Luis Faria, and with my colleagues Julio and Tamara, we're presenting the Intelligent Rate Limiting System, a human-centred solution to one of the biggest challenges in autonomous AI: uncontrolled resource consumption and loss of human oversight. 

Over the next 12 minutes, we'll show you how we can restore transparency, fairness, and trust to agentic AI systems.

**[PRESENTER NOTE: Make eye contact, gesture to teammates when introducing them. Set collaborative tone from the start. ~30 seconds.]**

# Slide 2 - THE RISE OF AGENTIC AI
**Subtitle**: A New Risk Frontier  
**Speaker**: Luis

Agentic AI systems like AutoGPT and Devin represent a fundamental shift:
- These aren't assistants waiting for commands
- They're autonomous agents making decisions and taking actions independently

As we documented in Assessment 2, this creates serious problems:
- One developer's misconfigured agent generated a **$50,000 AWS bill overnight**
- Current rate-limiting gives you a '429 error' with no explanation—no context, no fairness, and critically, no human control

This is the gap we're addressing.

**[PRESENTER NOTE: Emphasize "$50,000" - let it sink in. Pause after "no human control" for dramatic effect. ~50 seconds.]**


# Slide 3 - WHAT GOES WRONG TODAY?
**Speaker**: Tamara

The problems in current Agentic AI systems span four critical dimensions:

1. **Environmental**: Continuous agent workloads generate 800 kg CO₂ monthly with no carbon-aware routing
2. **Performance**: Cascading failures—uptime drops from 99.7% to 85% when agents misbehave
3. **Human Impact**: Over 47,000 Stack Overflow questions show developers are confused and frustrated
4. **Fairness & Ethics**: Opaque throttling creates perceived unfairness, widens the digital divide, and risks 'ethics washing'—where companies deploy harmful systems but point to governance dashboards as superficial proof of responsibility”

**[PRESENTER NOTE: Transition from Luis with confidence. Build through the four dimensions—#3 (human impact) should have most emphasis. ~60 seconds.]**


# Slide 4 - HUMAN-CENTRED DESIGN FAILURES
**Speaker**: Tamara

These technical failures translate directly into human-centred design failures:

- Users don't know **WHY** they're being throttled
- They can't predict **WHEN** it will happen
- They have **no way to appeal** or override decisions
- System behavior feels **arbitrary**

This violates 8 of Amershi's 18 guidelines for human-AI interaction.

**Most critically**: it erodes trust. And without trust, even the most capable AI system becomes unusable.

**[PRESENTER NOTE: Emphasize the bold words—WHY, WHEN, no way to appeal, arbitrary. The trust line is your hook into the solution. Remove learning outcome reference—it feels forced for external audience. ~45 seconds.]**

# Slide 5 - THE IRL PROPOSAL
**Subtitle**: Governance Middleware for Agentic AI  
**Speaker**: Luis

Our solution, the IRL, is a governance middleware that sits between agentic AI workloads and backend APIs.

Unlike traditional rate limiters that just block requests, IRL provides:
- **Dynamic throttling** based on real-time conditions
- **Weighted-fair queuing** for equity
- **Carbon-aware scheduling** for sustainability
- **Explainable feedback** and human-in-the-loop override

It transforms rate limiting from an automated constraint into a **collaborative resource dialogue** between humans and AI.

**[PRESENTER NOTE: This is the pivot from problem to solution. Show architecture diagram if available. Emphasize "collaborative dialogue"—that's the HCD core. ~55 seconds.]**

# Slide 6 - ADAPTIVE QUOTAS WITH CONTEXTUAL FEEDBACK
**Subtitle**: Core Component #1  
**Speaker**: Luis

Instead of a cryptic '429 Too Many Requests,' you get actionable intelligence:

**Example**: _"Request 547 blocked—you've used 847 of your 850 kWh daily limit. This will reset in 25 minutes, or you can request an override."_

This follows Miller's **contrastive explanation framework**:
- Not just 'what happened'
- But 'why this happened' and 'what would make it succeed'

And critically, **humans retain override capability** when automation gets it wrong.

**[PRESENTER NOTE: Read the example message slowly—it demonstrates the UX improvement. Emphasize "override capability"—this is about restoring human agency. ~50 seconds.]**

# Slide 7 - CARBON-AWARE THROTTLING, Core Component #2
**Speaker**: Julio

Component two addresses environmental justice. The system integrates real-time carbon intensity data from regional electricity grids—using the Green Software Foundation's Carbon Aware SDK. 

When renewable energy availability drops, say at night when solar is offline, the system automatically deprioritizes non-urgent agent tasks. 

Wiesner's research shows this temporal workload shifting reduces carbon emissions by 15 to 30 percent. Alevizos recently demonstrated that algorithmic choices matter too—Particle Swarm Optimization emits less than half the carbon of exhaustive search. 

Our system makes these trade-offs visible and actionable.

**[PRESENTER NOTE: Emphasize "visible and actionable" - this is the HCD angle. Pause after "environmental justice" to let it land. ~60 seconds total.]**

# Slide 8 - OPERATIONALIZING FAIRNESS, Core Component #3
**Speaker**: Tamara

Component three tackles the fairness paradox using Value-Sensitive Design. We asked: 'Fairness for whom?' 

A flat rate limit is equal, but not equitable—it would disproportionately hurt independent researchers and startups compared to well-funded enterprises. 

Our weighted fair queuing gives priority tiers to:
- Research, education, and non-profits (priority)
- Startups (moderate allocation)
- Enterprises (standard rates but higher absolute quotas)

Critically, this is culturally adaptable. Hofstede's research shows individualist cultures prefer personalized allocation, while collectivist cultures favor community-centered sharing. Our system lets organizations configure fairness models to match cultural expectations.

**[PRESENTER NOTE: Emphasize the question "Fairness for whom?" - this was our breakthrough moment. The bullet points should appear on click. ~60 seconds.]**

# Slide 9 - DESIGNING FOR VISIBILITY, PREDICTABILITY & CONTROL, Core Component #4
**Speaker**: Julio

Component four is where human-centered design becomes tangible. The dashboard shows:
- Real-time quota consumption with countdown timers
- Carbon and financial impact side-by-side
- Prominent override button when you need to escalate

The information hierarchy follows Amershi's guideline two: 'make clear what the system can do.' 

At 90% quota → bright warning  
At 95% → action required

This prioritizes imminent quota exhaustion and actionable feedback over overwhelming users with statistical detail they can't use.

**[PRESENTER NOTE: If you have the dashboard screenshot, point to the override button. This is where theory becomes practice. ~50 seconds.]**

# Slide 10 - PREDICTING EFFECTIVENESS
**Subtitle**: HCI and XAI Research Foundation  
**Speaker**: Tamara

**Important caveat**: These are theoretical predictions, not validated results. We haven't conducted user testing yet.

However, the evidence is strong:
- Our system implements **8 of Amershi's 18 Human-AI interaction guidelines**
- Binns showed procedural transparency improves perceived fairness (even with unfavorable outcomes)
- Miller's meta-analysis found contrastive explanations boost trust

**But—and this is critical**—actual comprehension rates, fairness scores, and trust metrics require controlled usability studies with diverse participant populations. 

That's our primary future work.

**[PRESENTER NOTE: Lead with the caveat—academic honesty builds credibility. Emphasize "8 of 18" and "diverse populations." ~60 seconds.]**

# Slide 11 - TECHNICAL PERFORMANCE RESULTS
**Speaker**: Luis

**Benchmark Results** (Simulated load testing):
- **50,000 concurrent agents** → 42 ms latency (target: <50 ms) ✅
- **Throughput**: 12,500 req/second (goal: 10,000) ✅
- **Abuse detection**: 94% precision, 89% recall ✅
- **DDoS resilience**: 99.7% uptime with 100,000 malicious agents ✅

The Redis token bucket scales horizontally with consistent performance.

**Important caveat**: These are synthetic workloads—real production traffic may reveal edge cases we haven't modeled.

**[PRESENTER NOTE: Lead with "The system performs well under stress testing." Acknowledge the caveat with confidence—honesty builds credibility. ~50 seconds.]**

# Slide 12 - ECONOMIC IMPACT PROJECTIONS
**Speaker**: Julio

**Cost Reduction**: 60–75% for runaway spend
- 40% from infinite loop prevention
- 15% from redundant call elimination
- 10% from query optimization
- Hard caps prevent $15k–$25k overnight billing disasters

**Real-World Context**: One production deployment avoided 3 billing catastrophes in first month—each would have exceeded $20,000.

**[PRESENTER NOTE: Lead with "Let's talk about money saved." The 60-75% number is the hook. ~40 seconds.]**

# Slide 13 - ENVIRONMENTAL & SOCIAL IMPACT
**Speaker**: Julio

**Carbon Footprint Reduction**: 25–35% emissions cut
- ~800 kg CO₂/month (medium deployment)
- 9,600 tonnes/year at 1,000-org scale
- **Equivalent to taking 2,000 cars off the road**

**Social Impact**:
- **Accountability restoration**: Immutable audit logs clarify responsibility
- **Trust building**: Transparency prevents automation bias
- **Digital equity**: Weighted quotas reduce barriers for researchers and startups

**[PRESENTER NOTE: The "2,000 cars" comparison makes it tangible. Emphasize that social impact isn't secondary—it's core to the design. ~50 seconds.]**


# Slide 14 - LIMITATIONS
**Speaker**: Julio

We believe honest acknowledgment of limitations is part of responsible design.

**Technical**:
- 40-60 ms latency unacceptable for high-frequency trading or robotics
- Carbon data accuracy varies regionally
- Distributed synchronization creates eventual consistency challenges

**Ethical**:
- Schema might not handle novel dilemmas
- False positives create friction
- Ethics washing risk remains

**Evaluation**:
- Synthetic workloads don't capture production complexity
- Developer-focused pilots don't validate accessibility for non-technical users

**Bottom line**: Empirical validation with diverse populations essential before production deployment.

**[PRESENTER NOTE: Frame as "responsible design" not weakness. Deliver with confidence—acknowledging limitations shows maturity. ~50 seconds.]**

# Slide 15 - FUTURE WORK
**Speaker**: Luis

Our research roadmap is ambitious but grounded:

**Short-term** (6-12 months):
- Controlled usability studies with diverse populations (devs, business users, non-technical stakeholders)
- Multi-site cultural validation

**Medium-term** (1-2 years):
- Adaptive governance using reinforcement learning (carefully designed reward functions)
- Plug-ins for major frameworks (LangChain, Semantic Kernel)
- Federated governance with blockchain audit logs

**Long-term** (2-5 years):
- Does transparency actually build trust over years?
- Does carbon-aware throttling meaningfully reduce emissions at scale?

**[PRESENTER NOTE: Frame as "roadmap not wishlist." The long-term questions show intellectual humility. ~55 seconds.]**

# Slide 16 - CONCLUSION
**Speaker**: Luis (with Julio & Tamara on stage)

IRL represents a fundamental reframing: rate limiting isn't just a technical constraint—it's a collaborative dialogue between humans and AI systems.

We've shown that human-centered values and technical sophistication aren't competing goals. They're mutually reinforcing. 

By embedding transparency, fairness, and control into the architecture, we restore the human agency that first-generation agentic systems systematically violated.

The design choices we make today will determine whether autonomous AI amplifies human capability—or undermines it. 

Our work demonstrates that innovation and responsibility can coexist. 

**Thank you. We're happy to take questions.**

**[PRESENTER NOTE: All three presenters should be visible during conclusion. Luis delivers, but gesture to acknowledge team. Pause before "Thank you" for impact. Total: ~45 seconds.]**

