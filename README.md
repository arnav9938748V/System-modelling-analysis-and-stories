Image Transformation Toolbox
Overview
This project contains two Python programs demonstrating image transformations using linear algebra and PIL/NumPy.

Assignment 03 q10 and q11.py - An interactive image transformation toolbox.

Assignment 03.py - Demonstrates predefined transformation matrices and their linear algebra properties.

1. Interactive Image Transformation Toolbox
File
Assignment 03 q11.py (Uses PIL)

Requirements
Bash
pip install pillow
How to Run
Bash
python "Assignment 03 q11.py"
Enter your image file path when prompted.

Available Operations
Rotate: Enter angle in degrees.

Resize: Enter a scale factor (e.g., 0.5 for half, 2.0 for double).

Flip: h (horizontal) or v (vertical).

Shear: Enter X and Y shear factors.

Custom Matrix: Enter six coefficients (a, b, c, d, e, f) for custom scaling, shearing, and shifting.

Reset/Exit: Restore the original image or close the program.

2. Linear Algebra Image Transformation Program
File
Assignment 03.py (Uses NumPy, Matplotlib, PIL)

Requirements
Bash
pip install numpy matplotlib pillow
Input Image
Place an image named your_image.jpg in the same folder as the script.

Core Features
Transformation Matrices: Applies 5 standard matrices (Scaling, 90° Rotation, Horizontal Shear, Y-axis Reflection, X-axis Projection).

Basis Vectors: Calculates T(e1) and T(e2) to show how standard directions change.

Rank and Information Loss: Checks matrix rank; if rank(A) < 2 (like in projection), it reports information loss.

Method: Calculates the inverse matrix to map output pixels safely back to the original image boundaries.

Output
Displays the original and transformed images, and prints the mathematical properties (basis vectors, rank, info loss) to the console.

Concepts Used
Geometric/Affine transformations, transformation matrices, basis vectors, matrix rank, information loss, NumPy arrays, and PIL/Matplotlib processing.

Notes & Project Purpose
The interactive program supports standard formats like JPG or PNG.

For visualization purposes, the singular projection matrix uses a small y-scale to draw the image while still mathematically reporting its true rank and loss.

Purpose: To bridge the gap between theoretical linear algebra and practical computer graphics/image processing.
