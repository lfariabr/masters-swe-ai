
# ☢️ Therac-25 – Killer Software Bug Case Study

**Title**: *Killer Bug. Therac-25: Quick-and-Dirty*  
**Author**: Aleksey Statsenko  
**Published by**: PVS-Studio  
**Incident Period**: 1985–1987  
**Consequence**: At least 6 overdoses, including 2 known deaths

---

## 📖 Overview

The **Therac-25** was a computer-controlled **radiation therapy machine** developed by **Atomic Energy of Canada Limited (AECL)**. It was designed to treat cancer patients with either electron or X-ray radiation.

Unlike earlier models (Therac-6 and Therac-20), the Therac-25 removed **hardware interlocks** and relied entirely on **software** to ensure patient safety. This decision led to **catastrophic failures** when multiple latent bugs combined with race conditions during operator input.

---

## 💀 What Went Wrong

### 1. Race Conditions
- Typing commands too fast (e.g. changing beam type from "x" to "e") could **desynchronize** system state and physical hardware — leading to incorrect beam settings.

### 2. Shared Variable Bugs
- One variable was used both to **read inputs** and **track the turntable's position**.
- Under fast input conditions, this led to the **wrong mode** being activated.

### 3. Missing Safety Checks
- Removing hardware interlocks left safety enforcement to poorly tested code.
- Division by zero errors and unbounded beam power increases occurred.

### 4. Operator Interface Issues
- Error messages were cryptic and unhelpful.
- Treatment would stop entirely on small input errors, forcing reentry.

---

## ⚖️ Investigation & Findings

- Investigators like **Nancy Leveson** and **Clark Turner** were brought in to study the accidents.
- They found the code reused from Therac-6 and Therac-20 had been **heavily repurposed without proper validation**.
- Minimal **unit testing** had been done; testing was limited to integrated systems under narrow scenarios.

---

## 🔧 Fixes Introduced (After the Damage)

- Independent **hardware-based emergency shutdown** (dead-man switch)
- **Potentiometer** to monitor turntable position
- Display of **dose rates and meaningful error messages**
- Refactoring of race-prone variables and improved time synchronization

---

## 📚 Lessons for SDM and Engineering

- **Safety-Critical Software Must Be Rigorously Tested**
- Reuse of code in new systems can be **dangerous** without full revalidation
- **Multithreaded programming without synchronization** = disaster waiting to happen
- **Removing hardware safety nets** without replacing them with bulletproof software is irresponsible
- Unit tests ≠ integration tests ≠ real-world conditions — **all are required**

---

## 🤹 Curiosities

- The operator once caused an overdose **by pressing keys too quickly**.
- A variable was incremented (`x = x + 1`) to set a Boolean — making the system fail randomly **1 in 256 times**.
- The **FDA completely overhauled software safety protocols** in medical devices after this incident.
- Most of the faulty code came from **a single programmer**.

---

## 💬 Quote-Worthy

> “Program code started using machines to kill people as early as in 1985.”

> “I wouldn't want to be treated by a drill whose speed is controlled by a variable with just one extra zero.”
