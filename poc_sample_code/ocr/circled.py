import cv2
import pytesseract
import numpy as np

# Configure path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update if needed


def detect_circles(image):
    
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve contrast and noise removal
    #blurred = cv2.medianBlur(gray, 5)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)

    # Connect broken ovals
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    _ = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return original, gray, contours


def segment_word(word):
    """Segments a word into potential valid words, handling prefixes and unexpected characters."""

    # Preprocessing: Remove non-alphanumeric characters except spaces
    word = re.sub(r"[^\w\s]", "", word)
    if d.check(word):
        return [word]  # Already a valid word

    n = len(word)
    # Attempt segmentation with potential prefix removal
    for prefix_len in range(1, min(4, n)):  # Try prefixes up to 3 characters long
        prefix = word[:prefix_len]
        remaining_word = word[prefix_len:]
        if not prefix.isalpha(): # Check if prefix is non-alphabetic
          segmented_remaining = segment_word(remaining_word) # Recursive call for the rest
          if len(segmented_remaining) > 1 or d.check(segmented_remaining[0]): # Check validity of segmentation
            return segmented_remaining # If segmentation is valid, accept result

    # Regular segmentation
    for i in range(1, n):
        prefix = word[:i]
        suffix = word[i:]
        if d.check(prefix) and d.check(suffix):
            return [prefix, suffix]

    #If no valid words can be segmented
    if not d.check(word):
      # Find the longest valid prefix
      longest_prefix = ""
      for i in range(1, len(word)):
          prefix = word[:i]
          if d.check(prefix):
              longest_prefix = prefix
          else:
              break
      if longest_prefix:
          #If longest prefix found, return it and recursively call on the rest
          return [longest_prefix] + segment_word(word[len(longest_prefix):])
      else:
          # If no prefix is found, return the original word
          return [word]

    return [word]  # No valid segmentation found


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

        # Check for open circles using circularity
        perimeter = cv2.arcLength(cnt, True)
        circularity = 4 * np.pi * area / (perimeter ** 2)

        if 0.5 < aspect_ratio < 2.0 or len(cnt) >= 5 and circularity < 0.85:
            # Crop slightly larger region around contour
            pad = 10
            x1, y1 = max(x - pad, 0), max(y - pad, 0)
            x2, y2 = min(x + w + pad, image.shape[1]), min(y + h + pad, image.shape[0])
            roi = gray[y1:y2, x1:x2]

            # Enhance OCR accuracy (experiment with these)
            roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            roi = cv2.GaussianBlur(roi, (3, 3), 0)
            _, roi_thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Apply adaptive thresholding
            roi_thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            # Use Tesseract with specific config (adjust if needed)
            text = pytesseract.image_to_string(roi_thresh, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
            if 1 <= len(text) <= 50 and text.strip():
                open_circled_texts.append((text, (x, y, w, h)))
                print(text, segment_word(text))
                if debug:
                    cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(original, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    if debug:
        cv2.imshow(original)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return [text for text, _ in open_circled_texts]