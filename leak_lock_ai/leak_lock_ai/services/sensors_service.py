import pandas as pd
import os
from fastapi import HTTPException

# Define the path to the dataset
DATA_FILE_PATH = "leak_lock_ai/data/water_leak_detection.csv"

def load_dataset():
    """Load the dataset and ensure necessary columns exist."""
    if not os.path.exists(DATA_FILE_PATH):
        raise HTTPException(status_code=500, detail="Data file not found.")

    try:
        df = pd.read_csv(DATA_FILE_PATH)

        # Ensure required columns exist
        required_columns = {"Timestamp", "Sensor_ID", "Pressure (bar)", "Flow Rate (L/s)", "Temperature (°C)", "Leak Status", "Burst Status"}
        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise HTTPException(status_code=500, detail=f"Missing columns in dataset: {missing_columns}")

        # Convert timestamp column to datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading dataset: {str(e)}")

def get_last_available_date(df):
    """Return the most recent available date in the dataset."""
    return df["Timestamp"].dt.date.max()

def filter_data_by_date(df, date):
    """Return only rows matching the specified date."""
    return df[df["Timestamp"].dt.date == date]

def check_data_freshness(df, last_available_date):
    """Check if the dataset is outdated."""
    days_old = (df["Timestamp"].max().date() - last_available_date).days
    return f"Warning: Data may not be updated. Last available date in dataset: {last_available_date}" if days_old > 1 else None

def get_latest_sensor_data(sensor_id: str):
    """
    Fetch all observations for a given sensor from the most recent available day in the dataset.
    """
    df = load_dataset()

    # Filter for specific sensor
    filtered_df = df[df["Sensor_ID"] == sensor_id]

    if filtered_df.empty:
        raise HTTPException(status_code=404, detail=f"Sensor ID '{sensor_id}' not found in dataset.")

    last_available_date = get_last_available_date(filtered_df)
    latest_data = filter_data_by_date(filtered_df, last_available_date)

    if latest_data.empty:
        raise HTTPException(status_code=404, detail=f"No data available for Sensor ID '{sensor_id}' on the last recorded day.")

    # Select required columns
    latest_data = latest_data.loc[:, ["Timestamp", "Sensor_ID", "Pressure (bar)", "Flow Rate (L/s)", "Temperature (°C)", "Leak Status", "Burst Status"]]

    # Check if data is outdated
    data_warning = check_data_freshness(df, last_available_date)

    return {
        "last_available_date": str(last_available_date),
        "data": latest_data.to_dict(orient="records"),
        "warning": data_warning
    }


def get_latest_data_for_all_sensors():
    """
    Fetch the latest available day's data for all sensors in the dataset.
    """
    df = load_dataset()

    last_available_date = get_last_available_date(df)
    latest_data = filter_data_by_date(df, last_available_date)

    if latest_data.empty:
        raise HTTPException(status_code=404, detail=f"No data available for the last recorded day ({last_available_date}).")

    # Select required columns and ensure Sensor_ID is included
    latest_data = latest_data.loc[:, ["Timestamp", "Sensor_ID", "Pressure (bar)", "Flow Rate (L/s)", "Temperature (°C)", "Leak Status", "Burst Status"]]

    # Group data by Sensor_ID
    grouped_data = latest_data.groupby("Sensor_ID").apply(lambda x: x.to_dict(orient="records")).to_dict()

    # Check if data is outdated
    data_warning = check_data_freshness(df, last_available_date)

    return {
        "last_available_date": str(last_available_date),
        "data": grouped_data,
        "warning": data_warning
    }
