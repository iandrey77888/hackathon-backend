from fastapi import APIRouter, Depends
from api.dependencies import (
    get_current_active_user
)
from models.schemas.hack import OcrRequest, OcrResponse
from services.ocr_service import OcrService

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"],
    #responses={404: {"description": "Not found"}},
)

@router.get("/requestOcr")
async def request_ocr(
    request: OcrRequest = Depends(),
    current_user = Depends(get_current_active_user),
    ocr_service: OcrService = Depends()
):
    return ocr_service.sent_ocr_request(request)

@router.put("/ocrResults", response_model=OcrResponse)
async def get_ocr_results(
    request: OcrResponse = Depends()
):
    print(request)
    return 200