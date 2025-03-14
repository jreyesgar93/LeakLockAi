# LeakLockAi
## Predictive Pipeline Monitoring System

LeakLock AI is a real-time monitoring and predictive maintenance system designed for water pipelines. By leveraging sensor data, machine learning models, and cloud infrastructure, the system can predict potential failures and provide actionable insights to maintenance teams.

This repository contains FastAPI-based backend services, machine learning inference pipelines, and real-time data processing workflows.

## **Features (WIP)**
- **Real-Time Sensor Data Processing**: Ingests and processes water pipeline data (pressure, flow rate, temperature, etc.).
- **Machine Learning Predictions**: Uses AWS SageMaker models to predict leak probabilities.
- **Low-Latency Database**: Stores transformed data in **DynamoDB** for real-time access.
- **Serving & API Layer**: Provides RESTful APIs via **FastAPI** for UI dashboards and external integrations.
- **Automated Reports**: Uses **LLMs (ChatGPT)** to generate daily **pipeline health reports**.
- **Scalable & Containerized**: Runs on **AWS ECS** and is containerized using **Docker**.

## **Getting Started**

### **1 Prerequisites**
Ensure you have the following installed:
- **Python 3.8+ (may need to update package versions for)**
- **pip (Python Package Manager)**
- **Docker (For containerized deployment)**
- **Virtual Environment (Recommended)**

### **2 Installation**
Clone the repository and install dependencies:

```bash
git clone https://github.com/jreyesgar93/LeakLockAi.git

```
Create a virtual environment:
```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install required dependencies:
```
pip install -r requirements.txt
```
### **3 Setting Up Environment Variables**

1. Create an /env directory in the root of the project.
```
mkdir env
```
2. Inside /env, create the following environment files:

- `development.env`
- `production.env`
- `testing.env`
3. Populate these .env files with the necessary environment variables.
`CHATGPT_API_KEY=your_openai_api_key`

### **4 Running with Docker**

1. Build Docker image
```
make build
```
2. Run dev container 

```
make up-dev
```
3. Access the API
```
http://localhost:8000/docs
```

### **5 Future Improvements**
- Future Improvements
- Enhance real-time dashboard integration.
- Optimize ML model performance and inference time.
- Improve anomaly detection with additional features.
- Implement a CI/CD pipeline for automated deployments.