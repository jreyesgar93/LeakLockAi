from fastapi import APIRouter, HTTPException
from leak_lock_ai.services.prediction_service import load_latest_predictions
from typing import Dict

router = APIRouter()

@router.get("/latest-predictions")
def latest_predictions():
    """
    Fetches the latest leak probability predictions for each sensor.
    """
    try:
        predictions = load_latest_predictions()
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.post("/predict")
def predict_pipe_failure(features: Dict):
    try:
        return #get_model_prediction(features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))