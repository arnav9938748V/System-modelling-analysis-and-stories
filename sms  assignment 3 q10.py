import cv2
import numpy as np
from PIL import Image


def apply_universal_transform(img_path, matrix_2x2, output_filename):
    # 1. Load the image and convert to RGB
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]

    #Define the 4 corners of the original image: (x, y)
    corners = np.array([
        [0, 0],
        [w, 0],
        [0, h],
        [w, h]
    ])

    transformed_corners = np.dot(matrix_2x2, corners.T).T

    #Find the bounds of the new shape
    x_coords = transformed_corners[:, 0]
    y_coords = transformed_corners[:, 1]

    min_x, max_x = np.min(x_coords), np.max(x_coords)
    min_y, max_y = np.min(y_coords), np.max(y_coords)

    #Calculate new width and height
    new_w = int(np.ceil(max_x - min_x))
    new_h = int(np.ceil(max_y - min_y))

    #Calculate translation to prevent cropping
    t_x = -min_x if min_x < 0 else 0
    t_y = -min_y if min_y < 0 else 0

    #Create the final 2x3 affine matrix for OpenCV
    affine_matrix = np.array([
        [matrix_2x2[0, 0], matrix_2x2[0, 1], t_x],
        [matrix_2x2[1, 0], matrix_2x2[1, 1], t_y]
    ], dtype=np.float32)

    #Apply the transformation
    result_img = cv2.warpAffine(img, affine_matrix, (new_w, new_h))

    #Save using PIL (which handles RGB correctly)
    Image.fromarray(result_img).save(output_filename)
    print(f"Saved: {output_filename}")

image_file = "hello.jpeg"

A1 = np.array([[2, 0],
               [0, 0.5]])
apply_universal_transform(image_file, A1, 'output_A1_scale.png')

A2 = np.array([[0, -1],
               [1, 0]])
apply_universal_transform(image_file, A2, 'output_A2_rotate.png')

A3 = np.array([[1, 1],
               [0, 1]])
apply_universal_transform(image_file, A3, 'output_A3_shear.png')

A4 = np.array([[-1, 0],
               [0, 1]])
apply_universal_transform(image_file, A4, 'output_A4_reflect.png')

A5 = np.array([[1, 0],
               [0, 0]])
apply_universal_transform(image_file, A5, 'output_A5_project.png')