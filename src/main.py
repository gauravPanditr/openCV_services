from fastapi import FastAPI, UploadFile

from src.config.db import check_db
from src.service.image_service import analyze_image
from src.model.response import ImageAnalysisResponse

app = FastAPI()

@app.on_event("startup")
def startup():

    check_db()

    print("MongoDB Connected")

@app.post(
    "/analyze",
    response_model=ImageAnalysisResponse
)
async def analyze(
    file: UploadFile,
    claim_id: str
):

    return await analyze_image(
        file,
        claim_id
    )