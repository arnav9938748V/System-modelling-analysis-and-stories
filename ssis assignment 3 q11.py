import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import sys


def apply_universal_transform(img, matrix_2x2):
    """
    Takes an image and a 2x2 transformation matrix, calculates the new bounding box
    to prevent cropping, and applies the warp.
    """
    h, w = img.shape[:2]

    # Define the 4 corners of the original image: (x, y)
    corners = np.array([
        [0, 0],
        [w, 0],
        [0, h],
        [w, h]
    ])

    # Multiply the 2x2 matrix by the corners to find their new locations
    transformed_corners = np.dot(matrix_2x2, corners.T).T

    # Find the bounds of the new shape
    x_coords = transformed_corners[:, 0]
    y_coords = transformed_corners[:, 1]

    min_x, max_x = np.min(x_coords), np.max(x_coords)
    min_y, max_y = np.min(y_coords), np.max(y_coords)

    # Calculate new width and height
    new_w = int(np.ceil(max_x - min_x))
    new_h = int(np.ceil(max_y - min_y))

    # Calculate translation to prevent cropping (shifting negative coordinates to 0)
    t_x = -min_x if min_x < 0 else 0
    t_y = -min_y if min_y < 0 else 0

    # Create the final 2x3 affine matrix for OpenCV (injecting our calculated translations)
    affine_matrix = np.array([
        [matrix_2x2[0, 0], matrix_2x2[0, 1], t_x],
        [matrix_2x2[1, 0], matrix_2x2[1, 1], t_y]
    ], dtype=np.float32)

    # Apply the transformation
    result_img = cv2.warpAffine(img, affine_matrix, (new_w, new_h))

    return result_img


def main():
    # 1. Select the Image using a native file dialog
    print("--- Step 1: Select Image ---")

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        print("No file selected. Exiting...")
        sys.exit()

    # Load image (kept in BGR so cv2.imshow displays colors correctly)
    current_img = cv2.imread(file_path)

    if current_img is None:
        print("Error loading image.")
        sys.exit()

    # 2. Interactive Menu
    print("\n" + "=" * 30)
    print(" UNIVERSAL MATRIX TOOLBOX")
    print("=" * 30)
    print("1. Rotate")
    print("2. Resize (Scale)")
    print("3. Flip (Reflect)")
    print("4. Shear")
    print("5. Custom Matrix (2x2)")

    choice = input("Select an operation (1-5): ")

    if choice == '1':
        angle = float(input("Enter rotation angle in degrees (e.g., 45): "))
        theta = np.radians(angle)
        # 2x2 Rotation Matrix
        A = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        current_img = apply_universal_transform(current_img, A)
        print(f">>> Success: Image rotated by {angle} degrees.")

    elif choice == '2':
        scale = float(input("Enter resize scale (e.g., 0.5 for half, 2.0 for double): "))
        # 2x2 Scaling Matrix
        A = np.array([
            [scale, 0],
            [0, scale]
        ])
        current_img = apply_universal_transform(current_img, A)
        print(f">>> Success: Image scaled by {scale}x.")

    elif choice == '3':
        print("Directions: 0 = Vertical, 1 = Horizontal, -1 = Both")
        direction = int(input("Enter flip direction: "))
        # 2x2 Reflection Matrices
        if direction == 0:
            A = np.array([[1, 0], [0, -1]])  # Invert Y
        elif direction == 1:
            A = np.array([[-1, 0], [0, 1]])  # Invert X
        else:
            A = np.array([[-1, 0], [0, -1]])  # Invert Both

        current_img = apply_universal_transform(current_img, A)
        print(">>> Success: Image flipped.")

    elif choice == '4':
        shx = float(input("Enter X-axis shear factor (e.g., 0.5): "))
        shy = float(input("Enter Y-axis shear factor (e.g., 0.0): "))
        # 2x2 Shear Matrix
        A = np.array([
            [1, shx],
            [shy, 1]
        ])
        current_img = apply_universal_transform(current_img, A)
        print(">>> Success: Shear applied.")

    elif choice == '5':
        # Now only requires 4 numbers instead of 6, because the function handles translation natively!
        print("Enter 4 numbers for a 2x2 matrix separated by spaces.")
        print("Example for standard identity: 1 0 0 1")
        vals = input("Matrix values: ").split()
        if len(vals) == 4:
            A = np.array([
                [float(vals[0]), float(vals[1])],
                [float(vals[2]), float(vals[3])]
            ])
            current_img = apply_universal_transform(current_img, A)
            print(">>> Success: Custom 2x2 matrix applied.")
        else:
            print(">>> Error: You must enter exactly 4 numbers.")
            sys.exit()

    else:
        print(">>> Invalid choice. Exiting...")
        sys.exit()

    # 3. Show the final result
    print("\n>>> Showing final image. Press ANY KEY in the image window to close.")
    window_name = "Transformed Image (Press any key to close)"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, current_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()