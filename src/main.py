from fastapi import FastAPI, File, UploadFile

from src.analyzer import analyze_image
app = FastAPI(title="OpenCV Services")


@app.get("/")
def home():
    return {"status": "OpenCV Service Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = await analyze_image(file)
    return result