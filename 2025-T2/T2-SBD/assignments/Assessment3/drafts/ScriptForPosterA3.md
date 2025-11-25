# CuraNexus: Secure-by-Design Web Application — Presentation Script

---

## Opening (30 seconds)

Good afternoon everyone, my name is Luis Faria, and today I'll present a 
**security design guide for web-based data retrieval applications**, demonstrated 
through ***CuraNexus Analytics*** — our reference implementation that integrates 
hospital and retail data streams while maintaining confidentiality, integrity, 
and availability.

This isn't just one solution—it's a replicable framework aligned with ISO 27001, 
NIST 800-63B, and OWASP ASVS that any organization can adapt for secure database-driven 
web applications.

---

## Quadrant 1 – Request Phase (Input Security) [~1 minute]
> This phase is where most vulnerabilities originate — especially injection attacks and authentication failures.
Here, we implemented:
- multi-factor authentication following NIST 800-63B
- parameterized SQL queries to prevent SQL injection
- server-side validation, using regex rules and canonicalization, ensuring data such as emails or IDs meet strict format limits.

Additionally, wildcard escaping prevents unsafe use of the SQL "LIKE" operator, 
while CSRF tokens and SameSite=strict cookies protect state-changing operations.

**To prevent automated bot attacks**, we implemented reCAPTCHA v3, rate limiting 
at 10 requests per IP per minute, and IP reputation checking against threat feeds—
distinguishing legitimate users from credential-stuffing bots.

This way, we ensure data entering the system is clean, validated, authenticated, 
and protected from both human and automated threats before it touches the database.

---

## Quadrant 2 – Retrieve Phase (Database Security) [~1 minute]
> The Retrieve Phase focuses on how we fetch and transmit data.
Data in transit is protected by TLS 1.3 with forward secrecy, while data at rest uses AES-256-GCM encryption, managed through AWS Key Management Service.

Each database account follows the Principle of Least Privilege, meaning that doctors, analysts, and administrators have separate credentials with only the permissions they truly need.

We also added SHA-256 integrity checks for every retrieved record and configured role-based read limits to avoid large data exposures.

No raw SQL is allowed — everything goes through ORM-based stored procedures, fully parameterized.

---

## Quadrant 3 – Review Phase (Access Control) [~1 minute]

The Review Phase enforces role-based access control (RBAC), defining three user groups:
Standard users like doctors or retail analysts can only read their domain data,
Accounting and management can write financial records,
and Administrators manage the infrastructure but can’t alter their own permissions.

Authentication tokens are JWTs signed with RSA-2048, sessions expire after 20 minutes of inactivity, and the system follows a Join–Move–Leave lifecycle for user management.

This ensures separation of duties, accountability, and traceability — core to both ISO 27001 §9.2 and NIST 800-64 Rev.2.

---

## Quadrant 4 – Key Security Metrics (Risk & Monitoring) [~1.5 minutes]

To quantify risk, we used the DREAD model applied at two levels:

**First, general web application threats** per OWASP Top 10:
- SQL Injection scores 8.2/10 — mitigated through parameterized queries
- Broken Authentication scores 7.5/10 — mitigated through MFA
- Sensitive Data Exposure scores 8.0/10 — mitigated through encryption

**Second, CuraNexus-specific risks**: Our highest-priority scenario was insider 
data exfiltration, scoring 7.0 out of 10, driven by high damage potential and 
moderate detectability.

The mitigation strategy includes:
– Immutable audit logs,
– Real-time SIEM alerts,
– 12-month retention, and
– AWS S3 encrypted backups for resilience.

We also link this back to the company’s Information Security Management System (ISMS) and Business Continuity Plan (BCP): incidents trigger alerts, backups restore data within four hours, and lessons learned feed back into the Plan–Do–Check–Act cycle.

This closes the loop — from secure input to encrypted storage and monitored access — demonstrating continuous improvement, a key SbD principle emphasized by Mead & Woody (2017).

---

## Closing (30 seconds)

To conclude, this design guide provides a **replicable Secure-by-Design framework**—
from validated inputs and encrypted storage to risk-based monitoring and governance 
alignment.

CuraNexus proves these principles work in practice, but the **methodology itself** 
scales to any web-based data retrieval context—healthcare, finance, or retail.

The key takeaway: security isn't bolted on after development—it's **designed in 
from day one**.