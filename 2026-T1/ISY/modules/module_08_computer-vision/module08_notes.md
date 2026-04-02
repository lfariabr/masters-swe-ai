# Module 08 — Computer Vision
## ISY503 Intelligent Systems

## TL;DR

- **Computer vision** lets machines interpret images and video — images are pixel matrices (grayscale: 0–255; colour: three R/G/B channels)
- **OpenCV** is the go-to Python library for CV tasks; it ships pre-trained models for face detection and supports frame-level video processing
- **Face detection** progresses from classical (Haar cascades + AdaBoost) to deep learning (MTCNN) — MTCNN also returns facial keypoints
- **Object tracking** extends detection to video via frame differencing, colorspace thresholding, CAMShift, optical flow (Lucas-Kanade), or background subtraction
- **Transfer learning** reuses knowledge from a trained model on a new task — cuts data and compute needs dramatically

---

## Task List

| # | Resource / Activity | Type | Status |
|---|---------------------|------|--------|
| **1** | **Watch & summarise Crash Course (2017) — How computer vision works** | **Video** | **✅** |
| 2 | Watch & summarise Fernandes (2019) — Intro to Deep Learning with OpenCV | Video | 🔥 WIP — needs manual access |
| **3** | **Read & summarise Brownlee (2019) — Face detection with deep learning** | **Article** | **✅** |
| **4** | **Read & summarise Howse et al. (2016) — Chapter 8: Object Tracking** | **Book chapter** | **✅** |
| 5 | Activity 1: Image Processing Practices (sky pixel detection) | Jupyter | 🕐 |
| **6** | **Read & summarise Moltzau (2019) — What is transfer learning?** | **Article** | **✅** |
| 7 | Activity 2: Write 100-word transfer learning summary (Discussion Forum) | Written | 🕐 |

---

## Key Highlights

---

### 1. Crash Course. (2017). How Computer Vision Works. [Video]

**Citation:** Crash Course. (2017, 15 November). How computer vision works [Video file]. Retrieved from https://www.youtube.com/watch?v=-4E2-0sxVUM

**Purpose:** Broad overview of computer vision — from simple pixel-level color tracking through edge-detecting kernels (convolutions) up to deep CNNs and real-world applications like face recognition, emotion detection, and gesture tracking.

---

#### 1. Why Computer Vision?

- Vision is the **highest-bandwidth sense** — provides a firehose of information about the world
- Computers capture photos with incredible fidelity, but *capturing ≠ seeing* (Fei-Fei Li: "to take pictures is not the same as to see")
- Goal: extract **high-level understanding** from digital images and videos

#### 2. Image Representation

- Images stored as grids of pixels; each pixel = **RGB value** (combination of red, green, blue intensities)
- Colors are **additive**: combining intensities of R, G, B produces any color

#### 3. Simple Color Tracking

- Find a target color (e.g., a bright pink ball) → scan every pixel → keep the closest RGB match
- Runnable on every video frame → tracks object over time
- **Limitation:** sensitive to lighting changes, shadows, and color collisions (e.g., same-color jersey)
- Rarely used unless environment is tightly controlled

#### 4. Edge Detection — Kernels and Convolutions

- Features larger than one pixel (edges) require looking at **patches** of pixels
- **Kernel / filter**: a small grid of values applied to a pixel patch via pixel-wise multiplication and sum → result stored in the center pixel
- This operation = **convolution**
- A vertical-edge kernel detects large color differences left-to-right; a horizontal-edge kernel detects top-to-bottom differences
- **Prewitt Operators**: classic horizontal and vertical edge-enhancing kernels

| Kernel type | What it finds |
|---|---|
| Vertical edge (Prewitt) | Strong left-right color differences |
| Horizontal edge (Prewitt) | Strong top-bottom color differences |
| Sharpening | Enhances local contrast |
| Blurring | Smooths pixel values |
| Line detector | Bright strip with dark surroundings |
| Island detector | Bright region surrounded by contrasting pixels |

#### 5. Viola-Jones Face Detection

- Applies multiple kernels sensitive to **face-like features** (nose bridge brightness, dark eye circles, etc.)
- Slides a search window across the image, combines many weak detectors
- Each kernel = weak face detector; **combined** → accurate (unlikely that face-like features cluster randomly without a face)
- Early and influential algorithm; precursor to modern deep learning approaches

#### 6. Convolutional Neural Networks (CNNs)

- Artificial neurons: multiply inputs by weights → sum → output; when input is 2D pixel data, this **is exactly a convolution**
- Key insight: **networks learn their own kernels** from data rather than using hand-crafted ones
- Layers build hierarchical complexity:
  1. Layer 1: detects **edges**
  2. Layer 2: combines edges → **corners / simple shapes**
  3. Layer 3: combines shapes → **facial parts** (mouths, eyebrows)
  4. Final layer: integrates all → "it's a face"
- Deep (many layers) = **deep learning**; required for recognising complex objects/scenes

#### 7. Applications Beyond Face Detection

| Application | Technique involved |
|---|---|
| Facial landmark detection | Specialized CV on isolated face region |
| Emotion recognition | Landmark geometry → eye/brow/mouth positions |
| Biometric face recognition | Facial geometry as unique identifier |
| Handwritten text recognition | CNNs applied to character patches |
| Medical imaging (tumour detection) | CNNs on CT/MRI scans |
| Traffic monitoring | Object detection on video streams |
| Gesture / body tracking | Landmark models on hands and full bodies |
| AR filters (e.g., Snapchat) | Real-time face + landmark tracking |

#### 8. Abstraction Stack in Computer Vision

```
Novel applications (smart TV, tutoring systems, gesture UIs)
        ↑
Interpretation algorithms (emotion, gesture meaning)
        ↑
CV algorithms (face detection, landmark tracking)
        ↑
Camera hardware (sensor fidelity, resolution)
```

Each layer is an active research area; breakthroughs at any level improve the whole stack.

#### Key Takeaways for ISY503
1. Convolutions are the shared foundation of classical kernels (Prewitt, Viola-Jones) and CNNs — understanding one unlocks the other
2. Viola-Jones is the classical predecessor directly mentioned in the module intro alongside Haar-cascades and AdaBoost (Resources 2 & 3 build on this)
3. The CNN layering model (edges → shapes → objects) explains *why* deep networks outperform shallow ones — critical for assessments covering DL architecture trade-offs

---

### 2. Fernandes, J. (2019). Introduction to Deep Learning with OpenCV. [Video]

**Citation:** Fernandes, J. (2019, 17 June). Introduction to Deep Learning with OpenCV [Video file]. Retrieved from https://www.linkedin.com/learning/introduction-to-deep-learning-with-opencv/

**Purpose:** Hands-on walkthrough of the OpenCV library — setup, image manipulation, blob representation with the DNN module, and image/video classification.

> *Status: 🔥 WIP — needs manual access (LinkedIn Learning requires authentication).*

---

### 3. Brownlee, J. (2019). How to Perform Face Detection with Deep Learning.

**Citation:** Brownlee, J. (2019, 3 June). How to perform face detection using deep learning. Retrieved from https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/

**Purpose:** Step-by-step tutorial comparing classical (Haar cascade via OpenCV) and deep learning (MTCNN) approaches to face detection in Python. Practical code for both techniques.

---

#### 1. What is Face Detection?

- **Face detection** = locate and localize one or more faces in an image (output: bounding boxes)
- **Locating** = finding x,y coordinates; **localizing** = defining the extent (bounding box)
- Trivial for humans; hard for computers due to variability in orientation, lighting, age, accessories, hair, and makeup
- Face detection is a *prerequisite* for face recognition systems

#### 2. Classical Approach — Cascade Classifiers (OpenCV)

- Introduced by **Viola & Jones (2001)** in "Rapid Object Detection using a Boosted Cascade of Simple Features"
- **AdaBoost** selects weak features — each weak classifier depends on a single feature
- Multiple classifiers arranged in a **cascade** (hierarchy of increasing complexity)
  - Coarse classifiers filter out negatives quickly → complex classifiers focus on promising regions
- Commercially deployed in smartphones and digital cameras
- OpenCV ships a pre-trained model: `haarcascade_frontalface_default.xml`

**OpenCV usage:**
```python
from cv2 import CascadeClassifier, imread
classifier = CascadeClassifier('haarcascade_frontalface_default.xml')
bboxes = classifier.detectMultiScale(pixels)  # returns list of (x, y, w, h)
```

#### 3. Deep Learning Approach — MTCNN

- **MTCNN** = Multi-Task Cascaded Convolutional Neural Network
- State-of-the-art on benchmark face detection datasets
- Detects faces **and** facial keypoints (eyes, nose, mouth corners)
- Python library: `mtcnn`

**MTCNN usage:**
```python
from mtcnn.mtcnn import MTCNN
detector = MTCNN()
faces = detector.detect_faces(pixels)
# Each result: {'box': [x,y,w,h], 'keypoints': {...}, 'confidence': float}
```

#### 4. Comparison: Classical vs Deep Learning Face Detection

| Feature | Cascade Classifier (OpenCV) | MTCNN |
|---|---|---|
| Type | Classical feature-based | Deep learning |
| Core algorithm | AdaBoost + Haar features | Multi-task CNN cascade |
| Speed | Fast | Slower |
| Accuracy | Good (frontal faces) | State-of-the-art |
| Facial keypoints | No | Yes (eyes, nose, mouth) |
| Pre-trained models | Ships with OpenCV | MTCNN library |
| Best for | Real-time, resource-constrained | High accuracy needs |

#### Key Takeaways for ISY503
1. Connects directly to **Activity 1** (pixel-level processing) and the broader CV workflow: preprocess → detect → classify
2. The cascade classifier concept echoes **ensemble methods** (AdaBoost) from Module 3's ML models coverage
3. MTCNN shows how **multi-task learning** extends a single model to produce multiple outputs simultaneously (bbox + keypoints)

---

### 4. Howse, J., Joshi, P. & Beyeler, M. (2016). OpenCV: Computer Vision Projects with Python — Chapter 8: Object Tracking.

**Citation:** Howse, J., Joshi, P. & Beyeler, M. (2016). Opencv: Computer vision projects with python. Birmingham, England: Packt. Chapter 8: Object Tracking.

**Purpose:** Practical introduction to tracking objects across video frames using five progressively sophisticated techniques — from simple frame differencing to adaptive background subtraction.

---

#### 1. Frame Differencing

- Simplest motion detection: compute `absdiff` between consecutive frames, `bitwise_AND` two diffs
- Shows **which pixels are moving**, not what they are
- **Limitation:** purely reactive — no object identity, fails for slow-moving objects

```python
diff1 = cv2.absdiff(next_frame, cur_frame)
diff2 = cv2.absdiff(cur_frame, prev_frame)
motion = cv2.bitwise_and(diff1, diff2)
```

#### 2. Colorspace-Based Tracking

- Convert frame to **HSV colorspace** (more perceptually meaningful than RGB)
- Apply `cv2.inRange(hsv, lower, upper)` to threshold a specific color
- **Limitation:** must know the target object's color in advance; fails for multi-colored objects

#### 3. CAMShift — Interactive Object Tracker

- **Meanshift**: compute centroid of color histogram backprojection in a region; move bounding box toward centroid
- **CAMShift** (Continuously Adaptive Meanshift): extends Meanshift by **adapting bounding box size and orientation**
  - Handles object moving closer/further from camera
  - Returns an ellipse (handles rotation)
- User selects region of interest → histogram computed → tracking via `cv2.CamShift()`

#### 4. Feature-Based Tracking — Optical Flow (Lucas-Kanade)

- Track individual **feature points** (keypoints) across frames
- **Lucas-Kanade method**: for each feature point, find best-matching 3×3 patch in previous frame → displacement = motion vector
- Uses `cv2.calcOpticalFlowPyrLK()` — pyramid-based for scale robustness
- Motion vectors visualized as lines on output frame

```python
feature_points_1, _, _ = cv2.calcOpticalFlowPyrLK(
    prev_img, current_img, feature_points_0, None, **tracking_params
)
```

#### 5. Background Subtraction (MOG)

- Build an **adaptive background model** (not just frame diff)
- `cv2.BackgroundSubtractorMOG()` — Mixture of Gaussians
- `learningRate` controls how fast the model adapts; static objects eventually absorbed into background
- **Advantage over frame diff:** handles gradual lighting changes, detects any moving foreground object

#### 6. Tracking Techniques Comparison

| Technique | Mechanism | Strength | Limitation |
|---|---|---|---|
| Frame differencing | `absdiff` between frames | Simple, zero setup | No identity, noisy |
| Colorspace tracking | HSV thresholding | Tracks specific colors | Needs known color |
| CAMShift | Histogram backprojection + adaptive mean | Handles size & orientation | Needs user init |
| Optical flow (Lucas-Kanade) | Feature point patch matching | Tracks individual features | Computationally heavier |
| Background subtraction (MOG) | Adaptive background model | Works in static scenes | Fails with moving cameras |

#### Key Takeaways for ISY503
1. Object tracking is fundamentally about **temporal consistency** — connecting detections across frames, not just detecting per frame
2. CAMShift and optical flow are still widely used baselines in real-time applications due to their low compute footprint
3. Background subtraction underpins many **video surveillance** systems — directly mentioned in the resource overview's application list

---

### Activity 2 — Moltzau, A. (2019). What is Transfer Learning?

**Citation:** Moltzau, A. (2019, 5 September). What is transfer learning? [Blog post]. Retrieved from https://medium.com/@alexmoltzau/what-is-transfer-learning-6ebb03be77ee

**Purpose:** Accessible intro to the concept of transfer learning — how pre-trained models can be adapted to new tasks with less data and compute.

---

#### 1. What is Transfer Learning?

- **Transfer learning** = store knowledge from solving one problem and apply it to a *different but related* problem
  - Example: car recognition knowledge → truck recognition
- Roots in psychological literature on transfer of learning
- Particularly powerful in **deep learning**: take a trained neural network, replace/fine-tune the output layer

#### 2. How It Works (CNN Example)

1. Start with a large pre-trained CNN (e.g., trained on ImageNet)
2. **Delete the loss output layer** (the final prediction layer)
3. **Replace** with a new loss output layer tuned for the new task (e.g., horse identification)
4. Fine-tune on the **smaller target dataset** — train the full network, last few layers only, or just the new layer

#### 3. When to Use Transfer Learning

| Scenario | Suitable? |
|---|---|
| Small dataset for new domain | ✅ Yes — leverages large pre-trained weights |
| Large dataset available for new task | May not need it |
| New task is unrelated to pre-trained task | ⚠️ Risky — knowledge may not transfer |
| Resource-constrained training | ✅ Yes — faster convergence, less compute |

#### 4. Practical Tools

- **NVIDIA Transfer Learning Toolkit** — GPU-accelerated pre-trained models (video analytics, medical imaging)
- **TensorFlow/Keras** — built-in tutorial for transfer learning
- IBM perspective: transfer learning reduces model training compute → better resource stewardship

#### Key Takeaways for ISY503
1. Transfer learning is the bridge between academic DL experiments and real-world deployment — it explains why models like MTCNN (Resource 3) are practical without training from scratch
2. Connects to Module 4/5 deep learning content: once you understand CNN architectures, transfer learning is the natural next step for practical applications
3. Activity 2 asks for a 100-word summary — lead with the core definition, one concrete example, and one practical tool
