import cv2
import numpy as np
from PIL import Image, ImageChops
import imagehash
import io

# -------------------------
# ELA FUNCTION
# -------------------------
def ela_score(pil_img):
    buffer = io.BytesIO()
    pil_img.save(buffer, 'JPEG', quality=90)
    buffer.seek(0)

    compressed = Image.open(buffer)

    diff = ImageChops.difference(pil_img, compressed)

    extrema = diff.getextrema()
    max_diff = max([e[1] for e in extrema])

    return max_diff


async def analyze_image(file):

    # -------------------------
    # 1. READ IMAGE
    # -------------------------
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # PIL image (for ELA)
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # -------------------------
    # 2. PREPROCESS
    # -------------------------
    img = cv2.resize(img, (512, 512))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -------------------------
    # 3. BRIGHTNESS CHECK
    # -------------------------
    brightness = float(img.mean())

    if brightness < 50:
        light_status = "VERY DARK"
    elif brightness > 200:
        light_status = "OVEREXPOSED"
    else:
        light_status = "NORMAL"

    # -------------------------
    # 4. BLUR DETECTION
    # -------------------------
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    quality = "GOOD" if blur_score > 50 else "BAD"

    # -------------------------
    # 5. EDGE DETECTION
    # -------------------------
    edges = cv2.Canny(gray, 100, 200)
    edge_score = float(edges.sum() / 100000)

    # -------------------------
    # 6. CONTOUR DETECTION
    # -------------------------
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_count = len(contours)

    # -------------------------
    # 7. FRAUD SCORE (RULE BASED)
    # -------------------------
    fraud_score = 0.0

    if blur_score < 40:
        fraud_score += 0.3

    if brightness < 40 or brightness > 220:
        fraud_score += 0.2

    if contour_count < 10:
        fraud_score += 0.3

    fraud_flag = fraud_score > 0.5

    # -------------------------
    # 8. EDITED IMAGE DETECTION (FINAL FIXED)
    # -------------------------
    ela = ela_score(pil_img)
    noise = cv2.Laplacian(gray, cv2.CV_64F).var()

    edited_score = 0.0

    # ELA anomaly
    if ela > 20:
        edited_score += 0.5
    elif ela > 12:
        edited_score += 0.3

    # blur + ELA mismatch
    if blur_score > 1000 and ela > 10:
        edited_score += 0.3

    # structure anomaly
    if contour_count > 500:
        edited_score += 0.3

    # edge anomaly
    if edge_score > 70:
        edited_score += 0.2

    # noise check
    if noise < 30:
        edited_score += 0.2

    edited_flag = edited_score >= 0.5

    # -------------------------
    # 9. DAMAGE LEVEL
    # -------------------------
    if edge_score > 50 or contour_count > 100:
        damage = "HIGH"
    elif edge_score > 20:
        damage = "MEDIUM"
    else:
        damage = "LOW"

    # -------------------------
    # RETURN RESULT
    # -------------------------
    return {
        "brightness": brightness,
        "light_status": light_status,
        "blur_score": blur_score,
        "image_quality": quality,
        "edge_score": edge_score,
        "contour_count": contour_count,
        "damage_level": damage,

        "fraud_score": round(fraud_score, 2),
        "fraud_suspected": fraud_flag,

        
        "ela_score": ela,
        "edited_score": round(edited_score, 2),
        "edited_image_suspected": edited_flag
    }