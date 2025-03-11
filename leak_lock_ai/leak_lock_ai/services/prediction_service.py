import pandas as pd
import os
from fastapi import HTTPException

# Define the path to the predictions CSV
DATA_FILE_PATH = "leak_lock_ai/data/predictions.csv"

def load_predictions_file():
    """
    Loads the predictions CSV file into a Pandas DataFrame.
    """
    if not os.path.exists(DATA_FILE_PATH):
        raise HTTPException(status_code=500, detail="Predictions file not found.")

    try:
        df = pd.read_csv(DATA_FILE_PATH)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading CSV file")
    



def validate_predictions_data(df):
    """
    Validates that the required columns exist in the DataFrame.
    """
    required_columns = {"Timestamp", "Sensor_ID", "Leak_Probability"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise HTTPException(status_code=500, detail=f"Missing columns in dataset: {missing_columns}")

    return df

 ### THIS FUNCTION IS WRONG. IMPLEMENTED JUST FOR DEMO PURPOSES
def preprocess_predictions(df):
    """
    Converts Timestamp to datetime and selects the observation with the highest 
    Leak_Probability per unique Sensor_ID.
    """
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Select the record with the highest Leak_Probability per Sensor_ID
    highest_prob_data = df.loc[df.groupby("Sensor_ID")["Leak_Probability"].idxmax()]

    return highest_prob_data.reset_index(drop=True)


def interpret_leak_risk(probability):
    """
    Interprets the leak risk based on the probability threshold.
    """
    if probability < 0.05:
        return "No problem"
    elif 0.05 <= probability < 0.2:
        return "Warning"
    else:
        return "Review Immediately"

def generate_predictions_json(latest_data):
    """
    Applies risk interpretation and converts the latest predictions to JSON format.
    """
    latest_data["Interpretation"] = latest_data["Leak_Probability"].apply(interpret_leak_risk)
    output_data = latest_data[["Sensor_ID", "Leak_Probability", "Interpretation"]]
    
    return output_data.to_dict(orient="records")

def load_latest_predictions():
    """
    Loads, processes, and returns the latest predictions with risk interpretation.
    """
    try:
        print("Loading predictions file...")
        df = load_predictions_file()
        
        print("Validating dataset structure...")
        df = validate_predictions_data(df)
        
        print("Processing latest predictions...")
        latest_data = preprocess_predictions(df)
        
        print("Generating JSON response...")
        predictions_json = generate_predictions_json(latest_data)
        
        print("Predictions successfully generated!")
        return predictions_json
        #return {}

    except Exception as e:
        print(f"Error in load_latest_predictions(): {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing predictions: {str(e)}")

