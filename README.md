# Microservice For Loan Approval

 [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
 [![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)](#)
 	[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)

This repository contains a microservice for loan approval hosted on Docker container with Flask API for access. User can send a POST request to the API with the required data, and it will return whether the loan is approved or not.

## Using This Repository

### If You Are Building This Repository ⛏️
1. Clone the repository:

```bash
git clone https://github.com/keanteng/microservice-loan-approval
```

2. Start the Docker container:

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### If You Pull From Docker Hub 🛜
1. Pull the Docker image:

```bash
# Pull the latest image from Docker Hub
docker pull keantengblog/microservice-loan-approval

# Run the Docker container
docker run -d -p 5000:5000 --name loan-approval-api keantengblog/microservice-loan-approval
```

### Work With the API 🚀
1. Access the API Using CLI:
```bash
# Check for health status
curl http://localhost:5000/health

# Check for model info
curl http://localhost:5000/model-info

# Send a POST request for prediction
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"person_gender\": 0, \"person_education\": 4, \"person_home_ownership\": 3, \"loan_intent\": 4, \"previous_loan_defaults_on_file\": 0, \"person_age\": -0.9535276419, \"person_income\": -0.1096838991, \"person_emp_exp\": -0.7273538377, \"loan_amnt\": 4.0249087102, \"loan_int_rate\": 1.6830201042, \"loan_percent_income\": 4.0163495163, \"cb_person_cred_hist_length\": -0.7391003235, \"credit_score\": -1.4197983033}"
```

2. Send the data using Python Script:
```bash
python bin/client.py
```

## Useful Docker Commands

```bash
# List all Docker containers
docker ps -a

# Stop the Docker container
docker stop loan-approval-api

# Remove the Docker container (use force if necessary)
docker rm loan-approval-api --force

# Prune unused Docker objects
docker system prune -a

# Push to Hub
docker tag microservice-loan-approval:latest keantengblog/microservice-loan-approval:v1.0
docker push keantengblog/microservice-loan-approval:v1.0
```
