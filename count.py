import imageio
from skimage.morphology import disk
from skimage.filters import rank
from skimage import img_as_ubyte
import numpy as np
import cv2

def locate_triradius_core(image_path):
    fingerprint_image = imageio.imread(image_path, pilmode="L")
    ridges = fingerprint_image - rank.median(fingerprint_image, disk(10))
    ridges_uint8 = img_as_ubyte(ridges)
    _, binary_image = cv2.threshold(ridges_uint8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    triradius_contour = max(contours, key=cv2.contourArea)
    triradius = tuple(triradius_contour[triradius_contour[:, :, 1].argmin()][0])
    contours = [c for c in contours if c is not triradius_contour]  # Exclude triradius_contour
    core_contour = max(contours, key=cv2.contourArea)
    core = tuple(core_contour[core_contour[:, :, 1].argmin()][0])

    return triradius, core

def count_ridges(image, roi_contour):
    if len(image.shape) == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
    ridge_image = cv2.filter2D(gray, cv2.CV_64F, kernel)

    mask = np.zeros_like(gray, dtype=np.uint8)
    cv2.drawContours(mask, [roi_contour], -1, (255), thickness=cv2.FILLED)

    region_of_interest = cv2.bitwise_and(ridge_image, ridge_image, mask=mask)
    _, binarized = cv2.threshold(region_of_interest, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binarized.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ridge_count = len(contours)

    return ridge_count

def count_ridges_between_triradius_core(image_path, triradius, core):
    fingerprint_image = imageio.imread(image_path, pilmode="L")

    x, y, w, h = cv2.boundingRect(np.array([triradius, core], dtype=np.int32))
    roi_contour = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.int32)
    ridge_count_result = count_ridges(fingerprint_image, roi_contour)

    return ridge_count_result

image_path = "test4.jpg"
triradius, core = locate_triradius_core(image_path)
ridge_count_result = count_ridges_between_triradius_core(image_path, triradius, core)

print(f"Triradius: {triradius}")
print(f"Core: {core}")
print(f"Number of ridges between triradius and core: {ridge_count_result}")