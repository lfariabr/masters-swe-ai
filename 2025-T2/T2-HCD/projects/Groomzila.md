From Groomzilla to Full-Stack Engineer: Building Wedstack
Tags: #nextjs #typescript #stripe #fullstack

Have you ever imagined being a Software Engineer, Project Manager, Designer, Customer Support agent, and Husband of the main stakeholder (**aka the Bride**) — all at once?  
**Yep, you read that right.**  

That was me for the past 4 weeks, during the conception, development, and deployment of **Wedstack** - a modern wedding invitation app I built from scratch.  

---

## What is Wedstack?  

**Wedstack** is a wedding invitation web application built with the following stack:  
- **Next.js + TypeScript** for the frontend  
- **Node.js + GraphQL** on the backend  
- **MongoDB** for persistence  
- **Stripe** for handling gifts and payments  

The app features:  
- Real-time presence confirmation  
- A guestbook for leaving messages  
- A gift store with seamless checkout (Apple Pay, PayID, Pix, credit cards)  
- A dynamic, playful UI with **shadcn/ui** components  
- Multi-language toggle between **Portuguese and English**  
- Deployment experiments on AWS and DigitalOcean  

---

## Inspirations  

Before diving into the keyboard, I explored some wedding-tech platforms that impressed me in the past with custom gifting and messaging features, such as [iCasei](https://www.icasei.com.br/) and [sayI.do](https://sayi.do/).  

But being the Software Engineer that I am (you can also call it stubbornness, haha), I refused to pay for an off-the-shelf solution.  Instead, I decided this was the perfect chance to:  
- Showcase my full-stack skills  
- Learn Stripe’s API in depth (first time going live with it)  
- Craft more custom React components  
- Impress the main stakeholder (the Bride 👰)!!!

---

## Features Bucket List  

- ✅ Leave a message to the couple (stored in MongoDB)  
- ✅ Stripe integration to receive gifts  
- ✅ Confirm presence via a friendly widget  
- ✅ Page with all wedding details  
- ✅ Menu preview with design-matched layout  
- ✅ Dynamic SVG backgrounds per section  
- ✅ Soft animations and transitions with **shadcn**  
- ✅ Multi-language support (en.json / pt.json)  
- ✅ Page navigation arrows (infinite carousel style)  
- ✅ AWS Beanstalk deployment trial (testing my [AWS Solutions Architect journey](https://dev.to/lfariaus/scaling-fastier-my-aws-solutions-architect-journey-with-forage-challenge-30j8))  

---

## What Went Well  

- MongoDB integration was smooth.  
- Dynamic backgrounds in Next.js were super fun.  
- The **multi-language switcher** turned out resilient and scalable.  
- Stripe integration was awesome: I created 4 products (gifts), wired Apple Pay, PayID, and Pix - guests just tap and pay.  

---

## Lessons Learned (***aka scars earned***)  

- **12+ hours invested on AWS Beanstalk** → load balancers, Nginx, configs. Ended up retreating to the comfort zone: a $12/month DigitalOcean Droplet.  
- **Layout churn**: multiple last-minute changes requested by the Bride (the “Main Stakeholder”... can't say no to that, right?). Next time: Figma first!  
- Didn’t have time to integrate CRM-style automation (auto-email/WhatsApp after confirmation). Would have been a nice “wow factor.”  

---

## Version History  

| Version | Feature Highlights |
|---------|-------------------|
| **1.x** | Project setup + MongoDB integration |
| **2.x** | Guests module + Dockerization |
| **3.x** | Language switcher PT/EN + AWS deployment trials |
| **4.x** | Stripe integration + DigitalOcean Go Live |

👉 [Full changelog here](https://github.com/lfariabr/wedstack/blob/master/_docs/notesWedstack.md).  

---

## Open Source & Demo  

- **Code**: [github.com/lfariabr/wedstack](https://github.com/lfariabr/wedstack)  
- **Live site**: [weddingln.com](https://weddingln.com)  

Drop us a message, confirm your presence, or (if you’re generous) buy us a gift via our transparent Stripe checkout.  
After multiple stakeholder meetings, design debates, and countless “scope creep” requests, the bride is happy with the final product. Which means… I’m not sleeping on the couch (for now).  

---

## Final Thoughts  

This project stretched me across roles: engineer, designer, PM, ops, support, and husband. But it was worth every late night.  

I learned Stripe end-to-end, polished my Next.js chops, wrestled with AWS, and delivered a product that my toughest client to date (my wife) is actually proud of.  

Sometimes the best side projects aren’t SaaS clones or hackathon demos. They’re personal, high-stakes apps with real users who care.  And in my case, the **user was the Bride**. Failure was not an option!!!