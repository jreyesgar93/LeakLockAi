from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from leak_lock_ai.services.sensors_service import get_latest_sensor_data, get_latest_data_for_all_sensors # Import service function

router = APIRouter()

# Request model for POST requests
class SensorRequest(BaseModel):
    sensor_id: str  # Sensor ID provided in the request

@router.post("/pipe-data")
def get_pipe_data(request: SensorRequest):
    """
    Fetch the latest 10 observations for a given sensor.
    """
    try:
        return get_latest_sensor_data(request.sensor_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-sensors-latest")
def get_all_sensors_data():
    """
    Fetch the latest available day's data for all sensors in the dataset.
    If data is old, includes a warning message.
    """
    try:
        return get_latest_data_for_all_sensors()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    