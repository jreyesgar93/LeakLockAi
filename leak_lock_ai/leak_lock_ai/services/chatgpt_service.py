import openai
import os
from fastapi import HTTPException
from datetime import datetime
from leak_lock_ai.config import CHATGPT_API_KEY
import pandas as pd
import json
from leak_lock_ai.services import sensors_service, prediction_service

DATA_FILE_PATH = "data/water_leak_detection.csv"

# Define the directory for saving reports
REPORTS_DIR = "leak_lock_ai/reports"

# Ensure the reports directory exists
os.makedirs(REPORTS_DIR, exist_ok=True)

# Fixed system context
SYSTEM_CONTEXT = (
    "LeakLock AI specializes in predictive maintenance for water pipelines. "
    "It uses real-time sensor data and machine learning models to predict failures."
    "It provides maintenance supervisors with daily reports on pipeline health, including key insights, metrics, and recommendations."
)

def pipeline_report():
    """
    Generates a detailed prompt for ChatGPT to analyze the latest available day's pipeline data
    and generate a daily maintenance report for the supervisor.
    """
    # Load the latest day's pipeline data
    latest_sensor_data = sensors_service.get_latest_data_for_all_sensors()
    latest_predictions = prediction_service.load_latest_predictions()

    # Extract the last available date
    last_available_date = latest_sensor_data.get("last_available_date", "Unknown Date")

    # Convert sensor data and predictions to JSON format
    pipeline_data_json = json.dumps(latest_sensor_data.get("data", {}), indent=2, default=str)
    predictions_json = json.dumps(latest_predictions, indent=2, default=str)

    # Construct a clear and structured prompt for ChatGPT
    user_prompt = f"""
    **Role:** You are an expert in pipeline maintenance. Your job is to analyze the latest pipeline sensor data 
    and machine learning predictions to generate a **daily maintenance report** for the **Maintenance Supervisor**.

    **Objective:** The report should:
    - Summarize the state of all monitored pipes.
    - Highlight any anomalies, leaks, burst risks, or irregularities.
    - Provide **clear, actionable recommendations** for preventive maintenance or urgent repairs.

    ---
    
    **Latest Data Available Date:** {last_available_date}
    
    Below is the pipeline sensor data for the latest recorded day. **Use this data to generate the report**:

    ```
    {pipeline_data_json}
    ```

    **Additionally, here are the latest leak probability predictions for each sensor.**
    These predictions indicate the likelihood of a pipeline failure based on recent sensor readings.

    ```
    {predictions_json}
    ```

    ---
    
    **🔹 Report Structure & Template:**  
    Format the report exactly as follows. Use **bold headings** and ensure it is structured professionally.

    ```
    # Daily Pipeline Maintenance Report

    **Date:** {last_available_date}
    **Prepared for:** Maintenance Supervisor  
    **Prepared by:** LeakLock AI  

    ## 1. Overview
    Provide a brief summary of the overall pipeline conditions. Mention the number of sensors monitored, the reliability of machine learning predictions, and whether the system is stable or if anomalies were detected.

    ## 2. Key Metrics
    Summarize important data points, such as:
    - **Average Pressure:** [Insert Value] bar
    - **Average Flow Rate:** [Insert Value] L/s
    - **Temperature Range:** [Insert Min-Max] °C
    - **Total Sensors Reporting Issues:** [Insert Count]
    - **Total Sensors with High Leak Probability:** [Insert Count]

    ## 3. Anomalies & Issues
    Identify specific sensors where anomalies occurred and **correlate them with leak probability predictions**.  
    Format it as a **bullet-point list**:
    - **Sensor [ID]:** Describe the issue (e.g., pressure spike, leak detected) and mention if the model predicted a high probability of failure.
    - **Sensor [ID]:** Another issue.

    ## 4. Recommended Actions
    Provide **clear, actionable maintenance recommendations**.  
    **Examples:**
    - **If a leak is detected:** "Dispatch maintenance team to inspect Sensor S456 for a possible pipeline leak."
    - **If pressure is too high:** "Reduce pressure in affected areas to prevent pipe bursts."
    - **If temperature is abnormal:** "Investigate heating/cooling factors affecting water temperature."
    - **If model predicts high leak probability:** "Urgently inspect the following sensors flagged by the ML model."

    ## 5. Conclusion
    Provide a final summary and **call to action** for the maintenance team.
    ```

    ---
    
    **Instructions for Completion:**
    - **Follow the template exactly** and format the report properly.
    - **Use clear, professional language.**
    - **Only report on the latest available day's data**.
    - **Ensure recommendations are actionable** and relevant to the issues detected.
    - **Correlate real sensor anomalies with machine learning predictions** to enhance insights.

    **Output the final report in a well-structured format.**
    """

    print("Generated Prompt:\n", user_prompt)
    return user_prompt


def maintenance():
    return "List upcoming maintenance tasks and alerts for the pipeline system."

def activity_report():
    return "Summarize the latest pipeline activities, including detected anomalies and operational status."

# Dictionary mapping features to functions
FEATURE_PROMPTS = {
    "pipeline_report": pipeline_report,
    "maintenance": maintenance,
    "activity_report": activity_report
}

def get_chatgpt_response(feature: str) -> str:
    """
    Selects the predefined prompt function based on the provided feature and sends it to ChatGPT.
    Raises an error if the feature is not available.
    """
    try:
        openai.api_key = CHATGPT_API_KEY  # Secure API Key access
        
        print(f"CHATGPT_API_KEY (last 4 chars): {CHATGPT_API_KEY[-4:]}")
        
        # Validate feature input
        if feature not in FEATURE_PROMPTS:
            raise HTTPException(status_code=400, detail=f"Invalid feature: '{feature}'. Available features: {list(FEATURE_PROMPTS.keys())}")

        # Call the function associated with the feature to get the prompt text
        user_prompt = FEATURE_PROMPTS[feature]()
        print(user_prompt)
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_CONTEXT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        return response["choices"][0]["message"]["content"]
    
    except HTTPException as http_err:
        raise http_err  # Ensure FastAPI handles expected errors properly
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")



def save_report_to_markdown(feature: str, report_content: str):
    """
    Saves the ChatGPT-generated report to a markdown file.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{REPORTS_DIR}/{feature}_report_{timestamp}.md"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"# {feature.replace('_', ' ').title()} Report\n\n")
            file.write(report_content)

        print(f" Report saved: {filename}")
    except Exception as e:
        print(f" Error saving report: {str(e)}")

def get_chatgpt_response(feature: str) -> str:
    """
    Selects the predefined prompt function based on the provided feature and sends it to ChatGPT.
    Saves the response as a Markdown file.
    """
    try:
        openai.api_key = CHATGPT_API_KEY  # Secure API Key access
        
        print(f"CHATGPT_API_KEY (last 4 chars): {CHATGPT_API_KEY[-4:]}")
        
        # Validate feature input
        if feature not in FEATURE_PROMPTS:
            raise HTTPException(status_code=400, detail=f"Invalid feature: '{feature}'. Available features: {list(FEATURE_PROMPTS.keys())}")

        # Call the function associated with the feature to get the prompt text
        user_prompt = FEATURE_PROMPTS[feature]()
        print("Generated Prompt:\n", user_prompt)

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_CONTEXT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        chatgpt_response = response["choices"][0]["message"]["content"]

        # Save response to markdown file
        save_report_to_markdown(feature, chatgpt_response)

        return chatgpt_response
    
    except HTTPException as http_err:
        raise http_err  # Ensure FastAPI handles expected errors properly
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
