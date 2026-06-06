import cv2
import numpy as np
from PIL import Image
from src.service.kafka_producer import publish_analysis
from src.config.db import photos
from src.service.hash_service import generate_hash
from src.service.duplicate_service import check_duplicate
from src.service.analyzer import analyze

async def analyze_image(file, claim_id):

    content = await file.read()

    np_arr = np.frombuffer(content, np.uint8)

    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    pil_img = Image.fromarray(
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    )

    phash = generate_hash(pil_img)

    duplicate, duplicate_of = check_duplicate(
        phash,
        claim_id
    )

    photos.insert_one({
        "claim_id": claim_id,
        "phash": phash
    })

    analysis = analyze(img, pil_img)

    reasons = []

    if duplicate:
        reasons.append(
            f"Duplicate image of {duplicate_of}"
        )

    if analysis["edited"]:
        reasons.append(
            "Edited image suspected"
        )

    return {
        "claim_id": claim_id,
        "ela_score": analysis["ela_score"],
        "edited_suspected": analysis["edited"],
        "is_duplicate": duplicate,
        "duplicate_of": duplicate_of,
        "fraud_flag": duplicate or analysis["edited"],
        "fraud_score": analysis["fraud_score"],
        "damage_level": analysis["damage"],
        "fraud_reasons": reasons
    }
    publish_analysis(result)

    return result



  
 
 
