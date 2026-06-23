# Reading list - DLE602 Assessment 2 (Review Pulse v2 / ABSA)

Papers for the proposal (A2) and the build (A3). All 11 are collected locally. PDFs in this folder are kept **local only** (see `.gitignore`) - downloaded for personal study; the index below is the only tracked file.

## Downloaded here (open access)

| File | Paper | Role in our project | Priority |
|---|---|---|---|
| `Zhao2018_Deep-CNN-Twitter-sentiment.pdf` | Zhao, Gui & Zhang (2018), *IEEE Access* | The A1 seed paper; the sentence-level CNN whose single-label limitation we improve on | Skim (you know it from A1) |
| `Pontiki2014_SemEval2014-Task4_ABSA.pdf` | Pontiki et al. (2014), SemEval-2014 Task 4 | Defines our benchmark, annotation scheme and evaluation protocol | **Must read** |
| `Wang2016_ATAE-LSTM_attention.pdf` | Wang et al. (2016), ATAE-LSTM | **Our Model 1** (attention-LSTM) + the attention we visualise | **Must read** |
| `Sun2019_BERT-for-ABSA_auxiliary-sentence.pdf` | Sun, Huang & Qiu (2019) | **Our Model 2** (DistilBERT, aspect as auxiliary sentence) | **Must read** |
| `Tang2016_TD-LSTM_target-dependent.pdf` | Tang et al. (2016), TD-LSTM | Motivates aspect-conditioned sequence models | Read |
| `Devlin2019_BERT.pdf` | Devlin et al. (2019), BERT | Transformer background (you used BERT in Review Pulse v1) | Skim |
| `He2017_ABAE_unsupervised-aspect-extraction.pdf` | He et al. (2017), ABAE | Neural aspect *discovery* - the optional Topic Modelling stage | Read if doing the stretch |
| `Jayakody2024_ABSA-techniques-comparative-study.pdf` | Jayakody et al. (2024), arXiv | Comparative study of deep-NN ABSA on **our** SemEval-2014 sets (reports LSA+DeBERTa ~90%); realistic upper bound | Read |
| `Simmering2023_LLMs-for-ABSA.pdf` | Simmering & Huoviala (2023), arXiv | The LLM/generative frontier we position against (GPT zero/few-shot vs fine-tuning) | Skim |
| `Hua2024_ABSA-systematic-review.pdf` | Hua, Denny, Wicker & Taskova (2024), *AI Review* | Recency anchor; 2024 taxonomy of ABSA subtasks/methods (727-study SLR) | Read |
| `Setiadi2024_LDA-topic-modeling-ABSA.pdf` | Setiadi, Marutho & Setiyanto (2024), *J. Future AI & Tech* | Topic Modelling + ABSA combo (LDA on Amazon reviews) - the Topic Modelling angle | Read if doing the stretch |

## Not here

All papers from the reading list are now collected locally - nothing outstanding to fetch.

## Suggested first pass (in order)

1. **Pontiki 2014** - understand the task and the data.
2. **Wang 2016 (ATAE-LSTM)** - our first model.
3. **Sun 2019 (BERT-for-ABSA)** - our second model.
4. **InstructABSA 2024** - see where the field is now on our exact benchmark.

> APA (all confirmed from the PDFs; confirm volume/issue/pages for the journal items):
> - Hua, Y. C., Denny, P., Wicker, J., & Taskova, K. (2024). A systematic review of aspect-based sentiment analysis: Domains, methods, and trends. *Artificial Intelligence Review, 57*, Article 296. https://doi.org/10.1007/s10462-024-10906-z
> - Setiadi, D. R. I. M., Marutho, D., & Setiyanto, N. A. (2024). Comprehensive exploration of machine and deep learning classification methods for aspect-based sentiment analysis with Latent Dirichlet Allocation topic modeling. *Journal of Future Artificial Intelligence and Technologies*. https://doi.org/10.62411/faith.2024-3
> - Jayakody, D., Isuranda, K., Malkith, A. V. A., de Silva, N., Ponnamperuma, S. R., Sandamali, G. G. N., & Sudheera, K. L. K. (2024). Aspect-based sentiment analysis techniques: A comparative study. *arXiv* preprint arXiv:2407.02834. https://arxiv.org/abs/2407.02834
> - Simmering, P. F., & Huoviala, P. (2023). Large language models for aspect-based sentiment analysis. *arXiv* preprint arXiv:2310.18025. https://arxiv.org/abs/2310.18025
