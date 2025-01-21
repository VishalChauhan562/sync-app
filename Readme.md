# Sync App ( Local env setup )  

## Live -> https://sync-app-1.onrender.com/

## Note 
You can add dummy users using the below buttons to test the flow back and forth.
<img width="781" alt="Screenshot 2025-01-22 at 1 52 36 AM" src="https://github.com/user-attachments/assets/dfce3b42-f737-440d-8a3b-962ff125bc41" />

This repository contains the frontend and backend services of the **Sync App**. The app is containerized using Docker and can be easily started using Docker Compose.

## Prerequisites

Ensure that you have the following tools installed on your machine:
- [Docker](https://www.docker.com/get-started) (includes Docker Compose)

## Getting Started

Follow the steps below to build and start the app using Docker Compose.

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/VishalChauhan562/sync-app.git
cd sync-app
```

### 2. Setup backend env variable

Create .env and add variables as mentioned in .env-example

### 3. Build Docker images and start

```bash
# to build docker images
docker-compose build
 
# to start 
docker-compose up
```
