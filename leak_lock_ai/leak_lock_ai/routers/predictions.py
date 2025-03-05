from fastapi import APIRouter, HTTPException
#from app.services.prediction_service import get_model_prediction, get_latest_predictions
from typing import Dict

router = APIRouter()

@router.get("/latest-predictions")
def latest_predictions():
    try:
        return #get_latest_predictions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
def predict_pipe_failure(features: Dict):
    try:
        return #get_model_prediction(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))