# Notes for MFA502

## Module 1 - Introduction to Machine Learning (MFA)

### I. Introduction to Set Theory
    - Set → A collection of objects.
        - A carpenter’s tool box → set.
        - All presidents of USA → set.
        - Your ten best friends → set.
        - All the programming languages → Set.
    - We understand sets intuitively.
    - The objects in a set may be similar or different.
    - A set may contain finite number of objects → Finite Sets
    - A set might contain infinite number of objects → Infinite Sets
> A set is a collection of items which have a common trait

Collection of tall boys: Not a set
Collection of boys higher than 1.8m: Set

{ x | x=2k (k is an integer); and 1<=x<=100 } is the set of even numbers
![set of even numbers](./module_01_introduction-to-sets-functions-and-vectors/setOfEvenNumbers.png)

### Activity 1 - 15'
1) Identify three different sets
> set1 `even numbers less than 12` = { 2, 4, 6, 8, 10 }  
> set2 `common household pets` = { cat, dog, rabbit, guinea pig } 
> set3 `top 5 tech companies` = { apple, google, amazon, microsoft, meta } 

- how many elements does each have? 
> n(set1) = 5
> n(set2) = 4
> n(set3) = 5

- are they well-defined? 
> yes

- what are its elements?
> set1 = { 2, 4, 6, 8, 10 }
> set2 = { cat, dog, rabbit, guinea pig }
> set3 = { apple, google, amazon, microsoft, meta }

- would everyone agree with the elements?
> I believe so, since the membership is clear

2) Give two example of a null set
> Ø1 = {x | x is a natural number less than 0 } -> no such number meets this condition
> Ø2 = {x | x is a student who scored 11 out of a 10 exam } -> not possible

3) Give two example of a universal set
> context = numbers up to 20 -> U1 = {1, 2, …, 20}
> context = programming languages -> U2 = {Python, Javascript, Java, C++, C#, ...}

### II. Subsets
A = {1,2,3}
B = {x|0<=x<=50}
A⊆B // A is a subset of B

Conceptual Activity:
N⊆Z⊆Q⊆R

### III. Some Operations in Set Theory

Power set
If A has n members, then the power set of A has 2^n members
`pow(A) = {x | x⊆A}`

Example:
if A={a,b}
Then pow (A) has 2^2 = 4 members
That is: `pow({a,b}) = {{}, {a}, {b}, {a,b}}`

Intersection of sets:
![powerExample](./module_01_introduction-to-sets-functions-and-vectors/powerExample.png)
![setIntersection](./module_01_introduction-to-sets-functions-and-vectors/setIntersection.png)
![setIntersectionInAGlance](./module_01_introduction-to-sets-functions-and-vectors/setIntersectionInAGlance.png)

### IV. Undefined Concepts and Program Syntax
### V. Tutorial

## Takeways:
- 

## Questions for Dr. James Vakilian:
- n/a

## Follow up
- ...

---

## Module 2 - Vector Spaces, Subspaces, and Linear Transformation

### I. Introduction to linear algebra 
W.2 → Vectors & vector spaces
W.3 → Introduction to Matrix theory
W.4 → Transformations
W.5 → Eigenvalues & Eigenvectors 

### II. Data & Information
it can be interpreted as
- Scalars
- Vectors
- Matrices
- Tensors

### III. Coordinate Systems 
x and y coordinates
N-D coordation system:
P (x,y,z,t) -> Space-Time (Minkowski space) 

### IV. Vectors
A vector has direction and magnitude (length)

### V. Vector space
A space with infinite number of vectors
The better the axioms are defined and covered, the better the vector space will be and the less glitches will be present at given space

### VI. Subspace
If V is a vector space
If W is a subset of V
AND W is a vector space
Then W is a Subspace of V

## Module 3 - Matrices

### I. An Introduction to Linear Algebra
- A branch of Abstract Mathematics
- Deals with linear relationships between variables
- Hermann Grassmann (1844): published his "Theory of Extension"
- Linear Algebra → deeper understanding of machine learning.
- The most important concept in linear algebra → Matrix Theory

### II. Introduction to Matrices
Matrices provide:
- a systematic approach for arranging large arrays of values
- simplify analysis of large amounts of data
- simplify analysis of large arrays of equations and their solutions
- simplify computer algorithms for manipulating large arrays of data

Matrices and Hard Disk Memory
Using matrices → we can correlate a unique address to every data point in memory of a hard disk

Definitions
Horizontal rows -> m
Vertical columns -> n
m x n = size of matrix
element (i,j) = element in row i and column j

### III. Few Important Matrices
- Scalar
- Row and Columns
- Square
- Diagonal
- Identity
- Zero
- Upper Triangular
- Lower Triangular

### IV. Fundamental Operations on Matrices
- Transpose of a Matrix
    - A' = T(A)
    - m x n will become n x m
    - T(T(A)) = A

- Equality of Matrices
    - A = B if and only if:
    - A and B have the same size
    - Corresponding elements of both matrices are equal

- Addition and Subtraction
    - Add: A2x2+B2x2 = a1+b1, a2+b2, a3+b3, a4+b4
    - Sub: A2x2-B2x2 = a1-b1, a2-b2, a3-b3, a4-b4

- Multiplication
    - Two matrices can be multiplied if and only if:
    - the number of columns in the first matrix 
    - **is equal** 
    - to the number of rows in the second matrix
    - Amxn * Bnxk = Cmxk

- Division?
    - There is no division of matrices
    - However, matrix inversion can be viewed in some sense as a procedure similar to division

- Important properties
    - AB != BA
    - (AB)C = A(BC)
    - A(B+C) = AB + AC
    - (B+C)A = BA + CA

### V. Determinants

- The determinant of a matrix A is defined only for a *square matrix*
- It is a *scalar* value
- Various representations are shown as:
    - det(A), |A|, *delta*

#### Determinant of a 2x2 matrix
A = [ a11 a12
     a21 a22 ]
    
det(A) = a11a22 - a12a21

#### Determinant of a 3x3 matrix
A = [ **a11** **a12** **a13**
     a21 a22 a23
     a31 a32 a33 ]

det(A) = **a11**(a22a33 - a23a32) - **a12**(a21a33 - a23a31) + **a13**(a21a32 - a22a31)

If det(A) = 0, then A is singular

### VI. Inverse Matrix
- The inversed of a matrix A is denoted as A^-1
- A matrix is inversible → det(A) ≠ 0
- If A is inversible, then A^-1 is also inversible = AA^-1 = A^-1A = I

#### Inverse of a 2x2 matrix
A = [ a11 a12
     a21 a22 ]

> 1) Change the location of elements on the main diagonal
> 2) Multiply the other two elements in (-1)
> 3) Divide the matrix by det(A)

A^-1 = [ (a22/det(A)) (-a12/det(A))
         (-a21/det(A)) (a11/det(A)) ]

### Extra Reading
https://www.linkedin.com/pulse/linear-algebra-fuels-artificial-intelligence-kayode-odeyemi/

## Module 4 - Eigenvalues and Eigenvectors
Linear Transformations, Eigenvalues and Eigenvectors

### I. Image Processing
- Image processing → operations performed on images to improve quality or extract information.
- In real-world applications, images are represented as collections of pixels.

### II. Transformation

### III. Two types of Transformation

### IV. Linear Transformation

### V. Geometrical Interpretation of Matrices

### VI. Matrix Transformation

### VII. Different types of Matrix Transformation

### VIII. Tutorial