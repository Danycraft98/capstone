import cv2
import pytesseract
import numpy as np

# Configure path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if needed


def detect_circles(image):
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur and Threshold (adjust thresholds if needed)
    #blurred = cv2.medianBlur(gray, 5)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0) #5,5
    _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return original, gray, contours


def is_handdrawn_circle(gray_image, x, y, w, h):
    """
    Verifies if the given region (x, y, w, h) contains a hand-drawn circle or oval.
    :param gray_image: Grayscale image (cv2.COLOR_BGR2GRAY).
    :param x, y, w, h: Coordinates of the region to check.
    :return: True if a circle/oval is detected, else False.
    """

    # Crop the region of interest
    roi = gray_image[y:y + h, x:x + w]

    # Preprocessing
    blurred = cv2.GaussianBlur(roi, (3, 3), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the region
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 50:  # too small to be meaningful
            continue

        # Fit ellipse only if contour has sufficient points
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            (cx, cy), (MA, ma), angle = ellipse
            aspect_ratio = max(MA, ma) / min(MA, ma)
        else:
            aspect_ratio = None

        # Circularity check
        perimeter = cv2.arcLength(cnt, True)
        circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter != 0 else 0

        # Extent = contour area / bounding box area
        x_cnt, y_cnt, w_cnt, h_cnt = cv2.boundingRect(cnt)
        rect_area = w_cnt * h_cnt
        extent = float(area) / rect_area if rect_area != 0 else 0

        # Criteria for hand-drawn circle or oval:
        # - moderate extent (not too sparse),
        # - acceptable circularity (not square/line),
        # - relaxed aspect ratio for ovals
        if extent > 0.3 and circularity > 0.4:
            if aspect_ratio is None or (1.0 <= aspect_ratio <= 9.0):
                return True

    return False


def extract_circled_texts(image_path, debug=False):
    image = cv2.imread(image_path)
    original, gray, contours = detect_circles(image)

    open_circled_texts = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200 or area > 8000:
            continue  # Adjusted for small + large circles

        # Approximate shape
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)

        if 1.0 <= aspect_ratio < 10.0:
            roi = gray[y:y + h, x:x + w]

            # Enhance OCR accuracy (experiment with these)
            roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            roi = cv2.GaussianBlur(roi, (3, 3), 0)
            #_, roi_thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Apply adaptive thresholding
            roi_thresh2 = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


            # Use Tesseract with specific config (adjust if needed) + --oem 1
            config = "--psm 6 --oem 1 -c tessedit_char_whitelist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '"
            text = pytesseract.image_to_string(roi_thresh2, config=config).strip()
            if 2 <= len(text) <= 50 and text and is_handdrawn_circle(gray, x, y, w, h):
                open_circled_texts.append((text, (x, y, w, h)))
                if debug:
                    cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(original, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    if debug:
        cv2.imshow(original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return [text for text, _ in open_circled_texts]