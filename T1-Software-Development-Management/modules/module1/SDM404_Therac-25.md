# ☢️ Summary of "Killer Bug: The Therac-25 Accidents"

## 📚 Overview

This article recounts one of the most tragic examples of software failure in history: the **Therac-25 radiation therapy machine**, which caused the **deaths or serious injuries of at least six patients** between 1985 and 1987 due to a series of fatal software bugs. The case remains a **cautionary tale** in software engineering, human factors, and safety-critical systems.

---

## 🏥 What Was Therac-25?

- A **radiation therapy machine** used for treating cancer.
- Manufactured by AECL (Atomic Energy of Canada Limited).
- It was a successor to the Therac-6 and Therac-20, but unlike them, **Therac-25 relied heavily on software rather than hardware for safety interlocks**.

---

## ❌ The Fatal Bug

- The **machine would sometimes deliver massive overdoses of radiation**—up to 100 times the intended dose.
- The problem occurred due to a **race condition** in the software when operators rapidly modified treatment settings.
- **A single-byte flag variable** controlled whether the beam was correctly set up.
- The system believed it was in a safe state and enabled the beam prematurely, despite hardware not being ready.

---

## ⚠️ Why Did It Happen?

### 1. **Over-Reliance on Software**
- Hardware interlocks were removed in favor of software checks.
- Developers and management believed software was "inherently safe."

### 2. **Inadequate Testing**
- The race condition only occurred under **very specific timing conditions** and was missed in testing.

### 3. **Poor Error Reporting**
- The machine displayed vague error codes (e.g. "MALFUNCTION 54").
- Operators had no way to understand or react appropriately.

### 4. **Dismissal of Operator Reports**
- AECL dismissed complaints from hospitals, attributing incidents to user error.
- Real investigation started only after multiple injuries.

---

## 💣 Consequences

- At least **six known incidents** of massive overdoses.
- **Multiple deaths** and severe patient injuries (e.g., burns, amputations).
- Ultimately led to lawsuits and a full recall of the Therac-25.

---

## 🧠 Lessons Learned

### ✅ 1. Safety-Critical Software Requires Rigorous Practices
- Software bugs can be just as deadly as hardware malfunctions.

### ✅ 2. Defensive Programming & Redundancy
- Critical systems should use **both hardware and software safeguards**.

### ✅ 3. Code Reviews and Formal Verification
- Important for uncovering subtle bugs like race conditions.

### ✅ 4. Human Factors Matter
- Usability, logging, and meaningful error messages are crucial.

### ✅ 5. Ethics in Engineering
- Dismissing user feedback and hiding failures are ethically and professionally unacceptable.

---

## 📌 Reference

**PVS-Studio Article:**  
[https://pvs-studio.com/en/blog/posts/0438/](https://pvs-studio.com/en/blog/posts/0438/)

**Original Incident Source:**  
Nancy Leveson and Clark Turner, *"An Investigation of the Therac-25 Accidents"*