"""
FINd Image Hashing API
======================
A RESTful API for comparing images using the FINd perceptual hashing algorithm.

Endpoint:
    POST /compare
        Accepts two images and returns their FINd hashes and Hamming distance.
        A distance of 0 indicates identical images; larger values indicate
        greater visual dissimilarity.

Usage:
    Run locally:
        python run.py

    Run with Docker Compose:
        docker-compose up --build

    Example request:
        curl -X POST "http://127.0.0.1:8945/compare" \
            -F "image1=@image1.jpg" \
            -F "image2=@image2.jpg"

Note:
    Only square images are supported. Non-square images will return
    a 400 error with a descriptive message.
"""
import io
import os
import sys

# Get the absolute path of the project root (where you are running uvicorn from)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add root and src to sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from PIL import Image
from fin.hasher import FINDHasher
from utils.logging_config import get_logger

logger = get_logger(__name__)
app = FastAPI()
hasher = FINDHasher()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.warning("Validation error: missing required fields")
    return JSONResponse(
        status_code=422,
        content={"detail": "Both image1 and image2 are required."}
    )

@app.post("/compare")
async def compare(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):
    logger.debug(f"Received request: image1={image1.filename}, image2={image2.filename}")

    try:
        img1 = Image.open(io.BytesIO(await image1.read()))
        img2 = Image.open(io.BytesIO(await image2.read()))
        logger.debug(f"Images loaded: image1={img1.size}, image2={img2.size}")
    except Exception:
        logger.exception("Failed to open image files")
        raise HTTPException(status_code=422, detail="Invalid image file.")

    try:
        hash1 = hasher.fromImage(img1)
        hash2 = hasher.fromImage(img2)
        distance = int(hash1 - hash2)
        logger.info(f"Hashing complete: distance={distance}")
    except ValueError as e:
        logger.warning(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "image1_hash": str(hash1),
        "image2_hash": str(hash2),
        "distance": distance
    }