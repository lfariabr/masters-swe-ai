Engineering Principles Applied to Daily Life: Concierge Edition
tags: #automation, #streamlit, #softwareengineering, #programming

> “What's easy to go through is hard to talk about, and what's hard to go through is easy to talk about.”
> *- Ariano Suassuna* (Translated from PT to EN)

One of the most unexpected things about my journey toward Australian Permanent Residency is how much I've been learning **outside** of Software Engineering and interestingly enough, how much of that learning is still *engineering at heart*.

## Context: From Fullstack Dev to Front Desk Ops

While grinding toward the PR dream, one of the roles I’ve taken on is a **concierge**. Not glamorous, but definitely meaningful.

I sit behind a desk, wearing a tie and a smile, handling dozens of tasks:  
- Booking lifts and loading docks;
- Organizing and delivering parcels (sometimes to doors!);
- Managing keys for contractors;
- Logging what goes out, what comes in;
- Running admin across multiple platforms.

It’s an intense mix of **customer service, logistics, and situational awareness**, and it runs on *systems*.

Now here's the twist: between service calls and package handovers, I’ve been **coding like a beast** in anonymous browser tabs. 
Like that dog that keeps drinking water even when full, that’s how hungry I am for progress, you know?

## The Problem: A Monster Spreadsheet

At one building, I inherited a **confusing spreadsheet**. Take a look at it below:

![Building Spreadsheet](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lqxhf4v9tkstmjkwwrif.png)

It was the system to track parcel delivery instructions, but it was chaotic.
It took time as it required *reading between lines*. New staff had no clue what to do unless they memorized the whole thing or invested a considered time of the day to map the instructions to the apartments.

> Residents asking: “Why hasn’t my parcel been delivered?”  
> Staff asking: “Am I even supposed to deliver this?”

The sort of problem that could be solved with engineering.

## The Solution: Streamlit + Logic

So I built a tool.

A simple, open-source **Streamlit web app** that:
- Receives an apartment number
- Fetches the relevant delivery instructions
- Tells the Concierge on duty exactly what to do

Here’s the logic breakdown (Python snippet):

```python
if "deliver to door" in notes_clean:
    st.success(f"🚪 Deliver to door. Use {lift} for apartment {apt}")

elif "deliver if requested" in notes_clean:
    st.info(f"📦 Deliver if requested. Use {lift} for apartment {apt}")

elif "store package and send notification" in notes_clean:
    st.info(f"✅ Store and notify. Use {lift} for apartment {apt}")

elif notes:
    st.info(f"ℹ️ Note: {notes}. Use {lift} for apartment {apt}")
```

From confusion to clarity — in a single input field. **That’s engineering.**

## Outcome & Vision

The app is already deployed at one site and in daily use by concierges.  
Staff love it. Residents get faster service. Managers don’t need to train people on convoluted spreadsheets anymore.

This was a **small win**, but when reflecting on it, it really showed me something bigger:  
**Every problem is a system problem. Every system can be improved.**

## Try it Out

- 🖥 [Live Demo (Streamlit)](https://excelbm-swharf.streamlit.app/)  
- 💻 [Open Source Code (GitHub)](https://github.com/lfariabr/concierge)

Thanks for reading this article. And remember: you don’t need a tech title to act like an Engineer.  
Build things. Solve problems. Share with the world.

🇦🇺🦘🔥