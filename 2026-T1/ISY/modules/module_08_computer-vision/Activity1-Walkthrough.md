Activity 1: Computer Vision Walkthrough

---

## [INTRO — 0:00]                                                                  
                                                                                
Hey, welcome. In this walkthrough we're going to tackle a classic computer vision
problem: looking at a photo and teaching a program to find the sky.               
                                                        
Not by magic — by understanding what a pixel actually is, and using that          
understanding to write a few lines of code that do something genuinely useful. By 
the end of this, you'll have a pipeline that takes any landscape photo, highlights
every sky pixel in green, and tells you exactly what percentage of the image is
sky. Let's go.                                                                   

---

## [STEP 1 — 0:20]
                
First thing — loading the image. We call cv2.imread, pass in the filename, and
what comes back is not some mysterious image object. It's just a NumPy array.     
Three dimensions: height, width, and three colour channels.
                                                                                
Every single pixel in the image is stored as three numbers — Blue, Green, Red —   
each between zero and two fifty-five. Zero means none of that colour, two        
fifty-five means full intensity. That's it. The entire photo is just a giant grid 
of numbers.                                               
                                                                                
One thing to watch out for: OpenCV reads images in BGR order — Blue, Green, Red — 
not the RGB order you might expect. That distinction matters later.
                                                                                
When we print the shape of our image, we get back the width, height, and confirm  
there are three channels. And we can peek at a single pixel — img[0, 0] — the    
top-left corner — and see its three raw values. This is the foundation. Images are
numbers.                                                 
                                                                                
---

## [STEP 2 — 1:15]
                                                                                
Now here's where it gets interesting. You might think: "sky is blue — so just find
pixels where the Blue channel is high." Sounds reasonable. Doesn't work.         
                                                        
Here's why. A bright white cloud gives you Blue=255, Green=255, Red=255.          
Everything is maxed out — there's no way to distinguish it from a white wall. And
a dark stormy sky might give you Blue=80, Green=60, Red=50. Low blue, no obvious  
rule.                                                     
                                                                                
The colour information and the brightness information are tangled together in BGR.
So we switch to HSV — Hue, Saturation, Value.
                                                                                
Hue captures the pure colour — which point on the rainbow. Saturation captures how
vivid versus grey it is. And Value captures brightness.                         
                                                                                
Now look at what happens when we convert and inspect the same pixel in both       
spaces. In BGR that pixel reads: Blue=148, Green=76, Red=0. Somewhat             
interpretable, but noisy. In HSV it reads: Hue=105, Saturation=255, Value=148. Hue
105 sits squarely in the blue-cyan zone. Saturation 255 means it's a vivid, pure
colour — not grey, not washed out. That's a sky pixel. HSV makes it obvious.     

---

## [STEP 3 — 2:20]
                                                                                
With HSV in hand, we define two rules — one for clear blue sky, one for white
clouds.                                                                           
                                                        
For clear blue sky: Hue between 90 and 130 — that's the blue-cyan band on the     
colour wheel — Saturation above 50, and Value above 50. Vivid, not too dark.
                                                                                
For white clouds or hazy sky: any Hue at all — because white doesn't have a real  
hue — but Saturation near zero (it's basically grey), and Value above 200 (it's  
bright).                                                                          
                                                        
We pass these lower and upper bounds into cv2.inRange. What comes back is a binary
mask — a 2D array the same size as the image, where every sky pixel is set to 255
(white), and everything else is zero (black).                                    
                                                        
We run that twice — once for blue, once for white — then combine them with a      
bitwise OR. A pixel is "sky" if it matches either rule.
                                                                                
Looking at the three masks side by side: the blue mask catches the clear sky, the 
white mask catches the bright clouds and haze, and the combined mask is the union
of both.                                                                          
                                                        
---

## [STEP 4 — 3:20]
                
Counting is almost embarrassingly simple at this point. cv2.countNonZero counts
every 255 in the mask — every sky pixel. We divide by total pixels and multiply by
100.
                                                                                
Our desert image has 363,750 pixels total. 169,465 of them are sky. That's 46.6%. 
                                                                                
Does that make sense? For a desert landscape — flat terrain, open horizon, large  
sky — yes, absolutely. Compare that to a dense city skyline or a forest photo,
where you'd expect maybe 10 or 15 percent. The number tells a story about the     
scene.                                                    
                                                                                
---

## [STEP 5 — 3:55]
                
Last step — making it visual. We make a copy of the original image — always work
on a copy, never destroy the original — and then we write one line:               

result[sky_mask == 255] = [0, 255, 0]                                             
                                                        
This is NumPy boolean indexing. It says: find every position in the image where   
the mask equals 255, and set those pixels to green. No loop. No coordinates. Just
one line that rewrites 169,000 pixels in one shot.                                
                                                        
We display three panels side by side: the original photo, the binary mask, and the
result with the sky painted green. The green patches match the sky perfectly.
Desert sand below, green sky above — ugly to look at, beautiful as a proof of     
concept.                                                  
                                                                                
---

## [OUTRO — 4:45]
                                                                                
And that's the pipeline. Five steps. Load → convert colourspace → threshold →
count → visualise.                                                                
                                                        
What you've actually built here is a primitive image segmentation system. The same
fundamental logic — define what you're looking for in a robust colourspace,
create a mask, measure and apply — shows up in medical imaging, autonomous        
vehicles, satellite analysis. The scale changes. The principle doesn't.
                                                                                
That's it for this one. Good luck with the rest of the module.