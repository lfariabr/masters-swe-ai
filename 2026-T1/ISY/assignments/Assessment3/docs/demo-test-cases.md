# Demo Test Cases - ISY503 Assessment 3

Use these cases to validate the Streamlit app before recording or presenting. Record final observed outputs after the trained model is available.

| Case | Input | Expected Behaviour | Observed Output | Notes |
|---|---|---|---|---|
| Clear positive | This product worked perfectly, arrived quickly, and I would happily buy it again. | Positive review | TBD | Outside-training style sentence |
| Clear negative | The item broke after one day and the quality was extremely disappointing. | Negative review | TBD | Outside-training style sentence |
| Books positive | The story was engaging, well written, and hard to put down. | Positive review | TBD | Domain-aligned |
| DVD negative | The movie was boring, badly paced, and not worth watching again. | Negative review | TBD | Domain-aligned |
| Electronics positive | The sound quality is excellent and the battery lasts longer than expected. | Positive review | TBD | Domain-aligned |
| Kitchen negative | The handle feels cheap and the pan warped after a few uses. | Negative review | TBD | Domain-aligned |
| Ambiguous short | It is okay. | Low confidence or unstable output | TBD | Explain binary limitation |
| Mixed sentiment | The camera is great, but the software crashes constantly. | May be mixed/unstable | TBD | Use for limitations |
| Sarcasm | Great, another product that stops working right after the return window closes. | May be misclassified | TBD | Use for error analysis |
| Domain shift | The hotel staff were friendly but the check-in process was slow. | May be unstable | TBD | Outside product-review domain |

## Acceptance Notes

- The app must accept raw text through a text area.
- The app must require an explicit classify action.
- The prediction must display as `Positive review` or `Negative review`.
- Confidence can be shown, but the required assessment output is the sentiment label.
