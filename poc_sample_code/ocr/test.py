import cv2

image = cv2.imread("./IMG_1134.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(f"image size {image.shape}")
# Apply thresholding
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
print(f"shape  post thresh hold {thresh.shape}")
cv2.imwrite("./updated.jpg",thresh)
cv2.imwrite("./grey.jpg",gray)

import easyocr

reader = easyocr.Reader(['en'])
text = reader.readtext("sample2.png", detail=0)
print(text)

# cv2.imshow("Processed Image", thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()