from fastapi import APIRouter, HTTPException
#from app.services.sensor_service import get_sensor_data
from typing import Dict

router = APIRouter()

@router.post("/pipe-data")
def get_pipe_data(sensor_id: str):
    try:
        #df = pd.read_csv(CSV_FILE_PATH)  # Load data
        #latest_data = df[df["sensor_id"] == sensor_id].to_dict(orient="records")
        latest_data = None
        if not latest_data:
            raise HTTPException(status_code=404, detail="Sensor ID not found")
        
        return {"sensor_id": sensor_id, "latest_data": latest_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    