import cv2
import numpy as np

# ===== GRAYSCALE CONVERTER =====
def grayscaling(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

# ===== GAUSSIAN BLUR =====
def gaussian(image, sigma=1.4, kz=0):
    return cv2.GaussianBlur(image, (kz, kz), sigmaX=sigma)

# ===== CANNY EDGE DETECTION PIPELINE =====
def canny(image, low=50, high=150):
    edges = cv2.Canny(image, low, high)
    return edges

# ===== MORPHOLOGICAL CLOSING =====
def closing(image, kernel_size=5):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# ===== CONTOUR DETECTION & LABELING =====
def makecontours(image):
    color_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours[1:], start=1):  # skip background
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0 or area < 100:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        M = cv2.moments(contour)
        if M['m00'] == 0:
            continue
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

        if circularity > 0.85:
            label = 'NORMAL'
            color = (0, 255, 0)
        elif circularity > 0.5:
            label = 'CACAT'
            color = (0, 0, 255)
        else:
            label = 'KACANG'
            color = (255, 255, 255)

        cv2.drawContours(color_img, [contour], -1, color, 2)
        cv2.putText(color_img, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return color_img

# ===== QUALITY ANALYSIS =====
def analyze_quality(image, image2):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    output_img = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)

    total_count = 0
    normal_count = 0
    defect_count = 0

    for i, contour in enumerate(contours):
        if i == 0:
            continue

        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0 or area < 100:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        M = cv2.moments(contour)
        if M['m00'] == 0:
            continue
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

        total_count += 1

        if circularity > 0.85:
            label = "NORMAL"
            normal_count += 1
            color = (0, 255, 0)
        elif circularity > 0.5:
            label = "CACAT"
            defect_count += 1
            color = (0, 0, 255)
        else:
            label = "KACANG"
            color = (255, 255, 255)

        cv2.drawContours(output_img, [contour], 0, color, 2)
        cv2.putText(output_img, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Hitung persentase
    if total_count == 0:
        normal_pct = defect_pct = kelayakan = 0.0
    else:
        normal_pct = 100 * normal_count / total_count
        defect_pct = 100 * defect_count / total_count
        kelayakan = normal_pct

    # Tentukan warna untuk kelayakan
    if kelayakan < 50:
        kelayakan_color = (0, 0, 255)  # merah
    elif kelayakan < 80:
        kelayakan_color = (0, 255, 255)  # kuning
    else:
        kelayakan_color = (0, 255, 0)  # hijau

    # Tambahkan teks analisis
    cv2.putText(output_img, f"Total      : {total_count}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(output_img, f"Normal     : {normal_count} ({normal_pct:.1f}%)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(output_img, f"Cacat      : {defect_count} ({defect_pct:.1f}%)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(output_img, f"Kelayakan  : {kelayakan:.1f}%", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, kelayakan_color, 2)

    return output_img
