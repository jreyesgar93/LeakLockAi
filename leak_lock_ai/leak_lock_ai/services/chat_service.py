import openai
import os
from leak_lock_ai.config import CHATGPT_API_KEY

# Fixed system context
SYSTEM_CONTEXT = (
    "LeakLock AI specializes in predictive maintenance for water pipelines. "
    "It uses real-time sensor data and machine learning models to predict failures."
)

def get_chatgpt_response(user_prompt: str) -> str:
    """Send a prompt to ChatGPT with a fixed system context and return response."""
    try:
        openai.api_key = CHATGPT_API_KEY  # Secure API Key access
        
        print(f"CHATGPT_API_KEY (last 4 chars): {CHATGPT_API_KEY[-4:]}")

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
    
    except Exception as e:
        return f"Error: {str(e)}"
