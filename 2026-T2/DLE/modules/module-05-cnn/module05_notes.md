# Module 5 - Convolutional Neural Networks

> Key Highlights from the Module 5 resources: what a CNN is, why convolution works (sparse interactions, parameter sharing, equivariance), pooling, the landmark architectures (AlexNet/VGG/GoogleNet), and how to actually train one.

## Task List

> Tip: ✅ = Done, 🔥 = WIP, 🕐 = Not started

| # | Task | Status |
|---|------|--------|
| **1** | Read & summarise Goodfellow et al. (2016) - Convolutional Networks (Ch.9) | ✅ |
| **2** | Read & summarise Kelleher (2019) - Convolutional and Recurrent Neural Networks (Ch.5) | ✅ |
| 3 | Watch & summarise Fernandes (2018) - NN & CNN Essential Training | 🔥 needs manual LinkedIn access |
| **4** | Read & summarise Kumara (2020) - AlexNet, VGG16, GoogleNet | ✅ |
| **5** | Read & summarise Zhou (2019) - CNNs Part 2: Training a CNN | ✅ |
| 6 | Activity 1: Critical Analysis I - Initial Recommendation (CNN vs FNN) | 🕐 |
| 7 | Activity 2: Critical Analysis II - Final Recommendation | 🕐 |
| 8 | Activity 3: Train the Network (cats vs dogs strategy) | 🕐 |
| 9 | Activity 4: Collaboration (compute vs memory wiki debate) | 🕐 |

---

## Key Highlights

### 1. Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning - Chapter 9: Convolutional Networks.

**Citation:** Goodfellow, I., Bengio, Y. & Courville, A. (2016). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://www.deeplearningbook.org/ (Chapter 9)

**Purpose:** The canonical, theory-first account of CNNs. It defines convolution as a specialised linear operation, explains *why* it works (three structural ideas), and shows pooling, padding and the many practical variants of the basic convolution function. This is the spine of Module 5.

---

#### 1. What a CNN is, and the convolution operation (§9.1)
- **Definition:** A CNN is simply a neural network that uses **convolution in place of general matrix multiplication in at least one layer**. Everything else (loss, backprop, SGD) is unchanged.
- **Convolution** = slide a small **kernel** (a.k.a. filter) over the input, multiply-and-sum at each position. The output is a **feature map**: a record of *where* the feature the kernel detects appears.
- **Cross-correlation note:** most ML libraries implement convolution *without* flipping the kernel (technically cross-correlation) and still call it "convolution". The network learns the kernel either way.
- **Grid-structured data:** convolution is the right tool when data has a known grid topology - 1D (time series, text), 2D (images), 3D (volumetric / video).

#### 2. The three ideas that make convolution powerful (§9.2) ⭐
This is the most exam-worthy section. A convolutional layer beats a dense layer for grid data because of three properties:

| Idea | What it means | Why it helps |
|---|---|---|
| **Sparse interactions** (sparse connectivity / weights) | The kernel is **much smaller than the input**; each output touches only a small receptive field, not every input pixel. | Fewer parameters, less memory, fewer operations. m inputs to n outputs goes from `O(m×n)` to `O(k×n)` with kernel size `k ≪ m`. |
| **Parameter sharing** (tied weights) | The **same kernel weights are reused at every position** of the input. | One feature detector is learned once and applied everywhere → far fewer parameters than a fully-connected layer. |
| **Equivariant representations** | Convolution is **equivariant to translation**: shift the input, and the feature map shifts the same way (`f(g(x)) = g(f(x))`). | A feature detected in one location is detectable in any location - exactly what images need. |

- **Caveat:** convolution is **not** naturally equivariant to scale or rotation; those need other mechanisms (data augmentation, multi-filter pooling).

#### 3. Pooling (§9.3)
- **Pooling** replaces an output with a **summary statistic of its neighbours** - most commonly **max pooling** (the max in a rectangular region); average pooling and L2-norm pooling also exist.
- **Key benefit: approximate invariance to small translations.** If the input shifts a little, the pooled output barely changes - useful when you care *that* a feature is present, not exactly *where*.
- **Downsampling:** by spacing pooling regions `k` pixels apart you report fewer units → smaller representation, less compute for later layers.
- **Variable-size inputs:** pooling lets a network feed a **fixed-size** vector to the classifier regardless of input dimensions (e.g. pool into a fixed grid of regions).

#### 4. Infinitely strong priors, variants, and grounding (§9.4-§9.10)
- **Convolution + pooling as an "infinitely strong prior" (§9.4):** using a conv layer is *like* telling a fully-connected layer "your weights must be local, shared, and translation-invariant - with infinite confidence." Great when that prior is true (images); harmful when it is not.
- **Variants of the basic convolution (§9.5):**
  - **Strided convolution** - move the kernel by `s > 1` to downsample during convolution.
  - **Zero-padding** - controls output size: *valid* (no pad, shrinks), *same* (output = input size), *full* (grows).
  - **Locally connected layers (unshared convolution)** - local connectivity *without* weight sharing.
  - **Tiled convolution** - a compromise: cycle through a small set of kernels rather than one shared kernel.
  - **Channels** - real conv layers run many kernels in parallel, producing a stack of feature maps (depth).
- **Neuroscientific basis (§9.10):** CNNs are loosely modelled on the mammalian visual cortex (V1) - **simple cells** ≈ convolution / feature detectors, **complex cells** ≈ pooling units; Fukushima's **neocognitron** is the direct ancestor. Learned first-layer kernels resemble **Gabor filters** (edge / orientation detectors).

#### Key Takeaways for Deep Learning (DLE602)
1. **Memorise the three ideas (sparse interactions, parameter sharing, equivariance)** - they are the answer to Activity 1's "when recommend a CNN over an FNN?" A CNN wins whenever data has grid structure and features can appear anywhere (images, audio spectrograms, even text windows).
2. **The "fewer parameters" argument is your headline:** a dense layer on a 256×256 image is intractable; weight sharing makes the same task routine. This feeds Activity 4 (CNNs are *cheaper* than the equivalent dense net, but still heavy at depth).
3. Pooling = the invariance knob; convolution = the equivariance / efficiency engine. Kelleher (resource 2) gives the same picture in friendlier language.

---

### 2. Kelleher, J. D. (2019). Deep learning - Chapter 5: Convolutional and Recurrent Neural Networks.

**Citation:** Kelleher, J. D. (2019). Deep learning. Cambridge, MA: MIT Press. Retrieved from https://ebookcentral-proquest-com.torrens.idm.oclc.org/lib/think/reader.action?docID=5855529&ppg=173 (Chapter 5)

**Purpose:** The plain-English companion to Goodfellow Ch.9. It reframes CNNs through intuitive metaphors (the flashlight; the feature-detector neuron), then continues into RNNs / LSTMs and the encoder-decoder - showing where CNNs sit in the wider architecture landscape.

---

#### 1. Tailoring architecture to data = building in domain knowledge
- You can **tailor** a network three ways: restrict connections to subsets, **force neurons to share weights**, or add **backward connections** (recurrence). Each constrains the set of functions the network can learn, *guiding* it to a good solution.
- For data with **regular structure** - sequences (text) or grids (images) - there are proven specialised architectures: **CNNs for grids, RNNs for sequences.**

#### 2. CNNs explained intuitively
- **Design goal (LeCun, Fukushima):** early-layer neurons detect **local visual features** (edges, curve segments); deeper neurons combine them into parts (eyes, noses); final layers assemble whole objects (faces). A hierarchy of representation.
- **Translation invariance via weight sharing:** if two neurons share weights but watch different **receptive fields**, together they detect the feature *wherever* it occurs. (LeCun 1989: "the precise location of a feature is not relevant to the classification, we can afford to lose some position information.")
- **The flashlight metaphor:** sweeping a narrow flashlight systematically across a dark image = convolving one shared feature-detector across the whole image.
- **Stride length:** the hyperparameter controlling receptive-field overlap; larger stride = less overlap = smaller output.
- **Pipeline of a conv layer:** **Convolution (no nonlinearity) → ReLU nonlinearity → Pooling (max / avg) → (often) Dense layer.** A convolution alone is purely linear; the ReLU `max(0,z)` is applied *after*, to the feature map.
- **Multiple filters:** one kernel detects one feature; CNNs run **many filters in parallel**, each learning a different detector, then combine the feature maps (stacked, or fused by a dense layer).

#### 3. Worked landmark: AlexNet, and ResNet's skip connections
- **AlexNet (ILSVRC 2012 winner):** 5 conv layers + 3 dense layers; first conv layer = 96 kernels with ReLU + pooling. **60 million weights, 650,000 neurons** - and weight sharing is precisely what keeps that number from exploding further.
- **ResNet (ILSVRC 2015 winner):** added **skip connections** (feed one layer's output directly into a much deeper layer), which made it possible to train networks **152 layers deep**.

#### 4. The bridge to sequences: RNN → LSTM → encoder-decoder
- **RNN:** one hidden layer plus a **memory buffer** that feeds the previous step's activation back in - "as deep as the sequence is long." Suited to sequential data.
- **Vanishing gradients:** backprop through `k` time steps multiplies the gradient by the same weight `k` times; if `< 1` it vanishes exponentially - RNNs struggle on long sequences.
- **LSTM:** a **cell** plus three **gates** (forget / input / output, built from sigmoid + tanh layers) that regulate memory and fix vanishing gradients.
- **Word2vec embeddings** turn words into vectors where similar contexts → similar vectors (London ≈ Paris). **seq2seq / encoder-decoder** (two LSTMs) powers machine translation; swap the encoder LSTM for a **CNN** and you get **image captioning** - the same vector-representation idea across modalities.

#### Key Takeaways for Deep Learning (DLE602)
1. This reading gives you the **vocabulary to sound fluent** in Activity 1 / 2: receptive field, weight sharing, translation invariance, stride, filter, feature map - all defined with metaphors you can hand-draw.
2. The **CNN-encoder + RNN-decoder** combo is the conceptual link back to **Module 3 and Assessment 1**: the Zhao et al. (2018) GloVe-DCNN you cite for A1 is a *CNN applied to text*, and embeddings (word2vec / GloVe) are the input representation. Module 5 explains the architecture A1's reference paper actually uses.
3. ResNet skip connections + AlexNet scale = the case studies you need for resource 4 (architectures) and Activity 4 (compute / memory).

---

### 3. Fernandes, J. (2018). Neural Networks and Convolutional Neural Networks Essential Training [Video].

**Citation:** Fernandes, J. (2018). Neural networks and convolutional neural networks essential training [Video file]. Retrieved from https://www.linkedin.com/learning/neural-networks-and-convolutional-neural-networks-essential-training/convolutions?u=56744473

**Status:** 🔥 **WIP - needs manual LinkedIn Learning access (authenticated, no transcript available).** Watch **Chapter 4 (Convolutional Neural Networks)** and **Chapter 5 (CNNs in Keras)** - these pair directly with Zhou (resource 5) for the hands-on Keras implementation. Summarise after viewing.

---

### 4. Kumara, V. (2020). A Review of Popular Deep Learning Architectures: AlexNet, VGG16 and GoogleNet.

**Citation:** Kumara, V. (2020). A review of popular deep learning architectures: AlexNet, VGG16 and GoogleNet [Web log post]. Retrieved from https://blog.paperspace.com/popular-deep-learning-architectures-alexnet-vgg-googlenet/ (DigitalOcean / Paperspace; byline Vihar Kurama)

**Purpose:** A guided tour of the three CNN architectures (2012-2014) that defined modern computer vision. It shows how the field progressed - **deeper, then smarter** - and gives concrete design / training details for each.

---

#### 1. The three landmark architectures at a glance ⭐

| Architecture | Year | Depth | Top-5 error (ImageNet) | The one big idea |
|---|---|---|---|---|
| **AlexNet** (Krizhevsky et al.) | 2012 | 8 layers (5 conv + 3 FC) | 15.3% (next best 26.2%) | Proved deep CNNs + **GPUs** win; ReLU, dropout, augmentation |
| **VGG16** (Simonyan & Zisserman, Oxford) | 2014 | 16 weight layers (13 conv + 3 FC) | ~7.0% test error | **Depth + simplicity:** stacks of small **3×3** filters |
| **GoogleNet / Inception v1** (Google) | 2014 | 22 layers, 9 inception modules | **6.67%** (ILSVRC 2014 winner) | **Inception module** - go *wider*, not just deeper |

#### 2. AlexNet (2012) - the turning point
- Input **256×256×3 RGB**; **~60M parameters, 650k neurons**.
- 5 conv layers (first two with overlapping max-pooling) + 3 fully-connected; **ReLU** on all layers, **softmax** over 1000 classes.
- **Two regularizers against overfitting:** **dropout** (in the first two FC layers) + **data augmentation** (ties straight back to Module 4).
- Trained with **SGD** (batch 128, momentum 0.9, weight decay 0.0005, lr 0.001) for ~6 days on **two GTX 580 3GB GPUs**.

#### 3. VGG16 (2014) - depth through small filters
- Fixed **224×224** input; the key move is replacing large filters with **stacks of 3×3 filters, stride 1**, plus 2×2 max-pooling.
- Channels grow 64 → 128 → 256 → 512 (×2 after each pool); two 4096-wide FC layers then a 1000-way softmax; **dropout 0.5** on the FC layers.
- **Drawbacks:** slow to train (weeks on Titan Black GPUs) and **huge** - the trained model is **>500MB**. This is the canonical "memory cost of CNNs" example for Activity 4.

#### 4. GoogleNet / Inception (2014) - wider, not just deeper
- **Inception module:** run **1×1, 3×3, 5×5 convolutions + max-pool in parallel** at the same level and concatenate - the network becomes **wider**.
- **1×1 convolutions as a bottleneck:** placed before the 3×3 / 5×5 convs to **reduce channel dimensions** → far cheaper computation. This is the trick that makes Inception efficient.
- 22 layers, 9 inception modules, global average pooling at the end, auxiliary classifiers during training.

#### Key Takeaways for Deep Learning (DLE602)
1. **The narrative is the answer to Activity 2 (Final Recommendation):** vision progressed AlexNet (depth + GPU) → VGG (small-filter depth) → Inception (width + 1×1 bottlenecks). "Bigger" eventually gives way to "smarter / cheaper."
2. **Every regularizer from Module 4 shows up here in production:** ReLU, dropout, weight decay, data augmentation, lr-schedule early stopping. Module 5 is where Module 4's toolkit gets *used*.
3. **VGG's >500MB model + AlexNet's 6-day train** are your concrete evidence for Activity 4's compute / memory debate - real numbers beat hand-waving.

---

### 5. Zhou, V. (2019). CNNs, Part 2: Training a Convolutional Neural Network.

**Citation:** Zhou, V. (2019). CNNs, Part 2: training a convolutional neural network [Web log post]. Retrieved from https://victorzhou.com/blog/intro-to-cnns-part-2

**Purpose:** The hands-on counterpart to Goodfellow's theory: it trains a tiny CNN on **MNIST from scratch in pure NumPy**, deriving and implementing backprop through Softmax → MaxPool → Conv. The best resource for *actually understanding how a CNN learns*, and the model for Activity 3.

---

#### 1. The toy CNN and the two-phase loop
- Architecture: **Conv 3×3 (8 filters) → Max-Pool 2×2 → Softmax**, on 28×28 MNIST digits (`28×28 → 26×26×8 → 13×13×8 → 10`).
- Training = **forward phase** (input flows through, each layer **caches** what it'll need) → **backward phase** (gradients backprop, weights update).
- **Clean backprop contract:** every layer's `backprop()` *receives* `∂L/∂out` and *returns* `∂L/∂in`, so layers chain trivially: `grad = softmax.backprop(grad); grad = pool.backprop(grad); grad = conv.backprop(grad)`.

#### 2. Backprop through each layer

| Layer | Has weights? | Backward-pass behaviour |
|---|---|---|
| **Softmax** | Yes (W, b) | Cross-entropy loss `L = -ln(p_c)`; initial gradient is nonzero **only for the correct class**. Derive `∂L/∂w`, `∂L/∂b`, `∂L/∂input`; update W, b with SGD. |
| **Max-Pool** | **No** (nothing to train) | Routes each gradient back to **where the max came from**; all other positions get 0 (a non-max pixel had zero marginal effect on the loss). |
| **Conv** | Yes (filters) | `∂L/∂filter(x,y) = Σ ∂L/∂out · image(i+x, j+y)` - the gradient for a filter weight is the sum of input pixels it multiplied. Update filters with SGD. |

- **SGD update rule everywhere:** `weight -= learn_rate * gradient`. Same engine as a plain MLP - convolution just changes *which* weights exist.

#### 3. Results - the payoff of training
- From-scratch NumPy CNN (1k MNIST subset, 3 epochs): **2.3 loss / 10% accuracy → 0.6 loss / 78% accuracy** in ~3000 steps.
- Same architecture in **Keras** on the full 60k set: **~97.4% test accuracy** in 3 epochs (`Conv2D → MaxPooling2D → Flatten → Dense(softmax)`, SGD, categorical cross-entropy).
- "What now" pointers: **Batch Normalization** and **Data Augmentation** as the next levers to push accuracy higher.

#### Key Takeaways for Deep Learning (DLE602)
1. **This is your Activity 3 blueprint** (training a CNN to classify cats vs dogs): the forward / backward loop, SGD, learning rate, epochs, and "start small then scale to Keras" are exactly the strategy points to argue, with research backing.
2. **Backprop is unchanged from Module 2** - only the layer math differs. The Module 2 mantra ("backprop computes gradients; the optimiser updates") holds verbatim here.
3. The Keras snippet is the direct sibling of **Fernandes Chapter 5 (CNNs in Keras)** - watch that video against this code and you have the full theory-to-practice path.

---

### How Module 5 connects to the assessments
- **Assessment 1 (n-gram sentiment, due 28/06/2026):** A1 is deliberately *classical* (no CNN). But the **Zhao et al. (2018) GloVe-DCNN** paper you must cite **is** a CNN over text - Module 5 finally explains the architecture behind your reference paper (convolution over embedding windows, parameter sharing, pooling).
- **A2 / A3 (Review Pulse v2 direction):** CNNs (and the CNN-encoder + RNN-decoder pattern from Kelleher) are a credible architecture for sentiment / ABSA on review text and an obvious "what I'd build next" upgrade from the n-gram baseline.
- **Module 4 → Module 5 handoff:** every regularizer you studied last week (dropout, weight decay, data augmentation, early stopping) reappears *in production* inside AlexNet / VGG / GoogleNet. Module 5 is where the toolkit gets used.
</content>
