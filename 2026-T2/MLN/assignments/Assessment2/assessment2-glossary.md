# MLN601 Assessment 2 - Glossario de Apoio

Este arquivo serve para estudo e ensaio da apresentacao. O notebook e a submissao continuam em
ingles, mas aqui os termos sao explicados em portugues e ligados aos numeros reais do A2.

## Validacao e divisao dos dados

| Termo | Explicacao pratica |
|---|---|
| **Cross-validation (CV)** | Validacao cruzada. Dividimos somente os dados de treino em cinco partes. O modelo treina em quatro e valida na quinta, repetindo ate que todas tenham sido usadas para validacao. Usamos a media das cinco rodadas para selecionar o modelo. |
| **Fold** | Cada uma das cinco partes usadas na cross-validation. |
| **Training set** | Dados usados para aprender regras e ajustar hiperparametros. No A2: 4.256 amostras proxy. |
| **Held-out test set** | Dados separados e mantidos intocados durante selecao/tuning. No A2: 1.064 amostras usadas somente para confirmar a decisao final. |
| **Data leakage** | Quando informacao do teste ou da validacao entra no treino. Isso faz as metricas parecerem melhores do que realmente seriam em dados novos. |
| **Stratified split** | Divisao que preserva aproximadamente a mesma proporcao de low/high nos conjuntos de treino e teste. |
| **IQR / intervalo interquartil** | Distancia entre o primeiro e o terceiro quartil. A regra de 1.5-IQR marcou 1.473 linhas como estatisticamente incomuns, mas isso nao prova erro de medicao. |
| **Outlier** | Valor distante da regiao central dos dados. No A2, os valores marcados foram retidos porque continuam plausiveis e lotes raros podem ser justamente os mais importantes para screening. |

### CV em uma imagem mental

```text
Rodada 1: [VALIDA] [TREINA] [TREINA] [TREINA] [TREINA]
Rodada 2: [TREINA] [VALIDA] [TREINA] [TREINA] [TREINA]
Rodada 3: [TREINA] [TREINA] [VALIDA] [TREINA] [TREINA]
Rodada 4: [TREINA] [TREINA] [TREINA] [VALIDA] [TREINA]
Rodada 5: [TREINA] [TREINA] [TREINA] [TREINA] [VALIDA]
```

O test set nao aparece nessas rodadas. Ele continua fechado ate a avaliacao final.

## Metricas de classificacao

| Termo | Explicacao no caso dos lotes |
|---|---|
| **Positive class** | O evento que queremos detectar. No A2, low quality e classe 1/positiva porque gera revisao do lote. |
| **True Positive (TP)** | Lote proxy realmente low que foi corretamente enviado para revisao. Balanced Tree: 292. |
| **False Negative (FN)** | Lote proxy realmente low que o modelo liberaria pelo fluxo normal. E o erro operacional mais perigoso. Balanced Tree: 106. |
| **False Positive (FP)** | Lote proxy realmente high enviado desnecessariamente para revisao. Balanced Tree: 183. |
| **True Negative (TN)** | Lote proxy realmente high corretamente mantido no fluxo normal. Balanced Tree: 483. |
| **Sensitivity / recall** | Dos lotes realmente low, quantos foram detectados: `TP / (TP + FN)`. Resultado: 0.734 ou 73.4%. |
| **Specificity** | Dos lotes realmente high, quantos foram corretamente liberados: `TN / (TN + FP)`. Resultado: 0.725. |
| **Precision** | Dos lotes marcados como low, quantos eram realmente low. |
| **F1-score** | Media harmonica entre precision e sensitivity; cai quando uma das duas fica fraca. |
| **Balanced accuracy** | Media de sensitivity e specificity. Da o mesmo peso para as duas classes. |
| **G-mean** | Raiz geometrica de sensitivity x specificity. Penaliza fortemente um modelo que abandona uma classe. |
| **Confusion matrix** | Tabela que mostra TN, FP, FN e TP para um threshold especifico. |

## ROC, AUC e threshold

| Termo | Explicacao pratica |
|---|---|
| **Risk score** | Grau de suspeita produzido pelo modelo antes da decisao final. |
| **Threshold** | Linha de corte que transforma score em flag/review ou clear. Alterar o threshold muda sensitivity e specificity. |
| **ROC curve** | Mostra o trade-off entre sensitivity e false-positive rate para todos os thresholds. |
| **ROC-AUC / AUC** | Qualidade do ranking em todos os thresholds. AUC 0.824 no SVM significa que ele ordena um low acima de um high aleatorio em cerca de 82.4% dos pares; nao significa 82.4% de accuracy. |

Por isso o SVM pode ter o maior AUC e mesmo assim nao ser aprovado: no threshold atual sua
sensitivity e apenas 0.590, abaixo do gate operacional de 0.70.

## Modelos e tuning

| Termo | Explicacao pratica |
|---|---|
| **Decision Tree** | Modelo formado por regras `if/else`. Cada no divide os dados por uma feature e um valor. Foi o algoritmo exigido pelo brief. |
| **Hyperparameter** | Configuracao definida antes do treino, como `max_depth` e `min_samples_leaf`. |
| **GridSearchCV** | Testa varias combinacoes de hiperparametros usando cross-validation e escolhe a melhor segundo a metrica definida. |
| **Gini impurity** | Mede o quanto uma folha esta misturada entre classes. Zero significa folha pura. |
| **max_depth** | Limita quantos niveis a arvore pode criar. Evita memorizar ruido. Valor escolhido: 5. |
| **min_samples_leaf** | Minimo de amostras permitido em uma folha. Evita regras baseadas em poucos casos. Valor escolhido: 20. |
| **Class weighting** | Aumenta o custo de errar a classe minoritaria. Foi o mecanismo usado pela Balanced Tree para detectar mais lotes low. |
| **SMOTE** | Cria amostras sinteticas da classe minoritaria somente dentro dos folds de treino. Ajudou a sensitivity, mas falhou o gate de specificity. |
| **SVM** | Support Vector Machine. Procura uma fronteira que separe as classes com maior margem. |
| **RBF kernel** | Permite que o SVM represente uma fronteira nao linear. Foi o melhor ranking, mas nao o modelo operacional aprovado. |
| **C no SVM** | Controla a penalidade por erros de treino. O melhor resultado usou `C=1`, um compromisso intermediario entre margem e erros. |
| **Gamma no RBF** | Controla o alcance de cada ponto na fronteira RBF. `gamma='scale'` ajusta esse alcance a variancia das features. |

## Interpretacao e operacao

| Termo | Explicacao pratica |
|---|---|
| **Correlation** | Associacao linear entre duas variaveis. `alcohol = -0.4145` contra low quality significa que mais alcohol esta associado a menor chance da classe low. Nao prova causalidade. |
| **Feature importance** | Quanto uma feature contribuiu para as divisoes da arvore. Alcohol teve aproximadamente 0.62. Nao e a mesma coisa que correlation. |
| **Explainable AI / XAI** | Tecnicas que tornam o comportamento geral do modelo ou uma previsao individual mais compreensiveis. |
| **Global explanation** | Explica o modelo sobre muitas amostras. No SHAP global, alcohol teve a maior contribuicao absoluta media: 0.192. |
| **Local explanation** | Explica uma previsao especifica. No exemplo do A2, alcohol contribuiu +0.222 e volatile acidity +0.070 para a classe low. |
| **SHAP** | Decompoe a diferenca entre a previsao base e a previsao de uma amostra em contribuicoes aditivas de cada feature. Valores positivos aqui empurram para `low = 1`. |
| **SHAP additivity check** | Confirma que `baseline + soma das contribuicoes = probabilidade do modelo`. O erro maximo observado foi `1.41e-14`, essencialmente zero numerico. |
| **Feature engineering** | Criacao de atributos derivados. Bound SO2 e free-SO2 ratio foram testados, mas rejeitados porque a melhoria nao foi material. |
| **Class imbalance** | Classes com tamanhos diferentes. Depois da deduplicacao: 62.6% high e 37.4% low. |
| **Proxy lot sample** | Interpretacao operacional de uma linha UCI como amostra representativa de lote. O dataset nao possui um `lot_id` real. |
| **Human-supervised pilot** | O modelo direciona revisao, mas uma pessoa continua responsavel por liberar, reter ou retrabalhar o lote. |
| **Model monitoring** | Acompanhamento de sensitivity, specificity, hold rate, escapes, lead time e diferencas entre vinho red/white apos o piloto. |

## Frase curta para a apresentacao

> "CV e a validacao cruzada feita somente dentro do treino. Eu divido o treino em cinco folds,
> valido o modelo cinco vezes e uso a media para escolher a configuracao antes de abrir o test set."
