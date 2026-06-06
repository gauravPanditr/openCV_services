from fastapi import FastAPI


app = FastAPI(title="OpenCV Services")


@app.get("/")
def home():
    return {"status": "OpenCV Service Running"}