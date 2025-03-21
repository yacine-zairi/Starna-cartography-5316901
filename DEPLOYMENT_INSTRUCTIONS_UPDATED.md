# Deployment Guide: Celestial-Globe Project on Google Cloud

This guide outlines the steps to deploy the Celestial-Globe project on Google Cloud Run and Google Cloud Functions.

## Part 1: Google Cloud Run Deployment (Containerized Application)

This section details how to build a Docker image of the application, push it to Google Container Registry (GCR), and deploy it to Google Cloud Run.

### Prerequisites

*   **Google Cloud Account:** You need a Google Cloud account with a project set up.
*   **Google Cloud SDK:** Install the Google Cloud SDK (gcloud CLI) on your local machine.
*   **Docker:** Install Docker on your local machine.
*   **Node.js and npm:** Ensure you have Node.js and npm installed locally.

### Steps

1.  **Build the Application Locally:**

    *   Navigate to the project's root directory in your terminal.
    *   Install project dependencies:
```
bash
        npm install
        
```
*   Build the application:
```
bash
        npm run build
        
```
2.  **Create a Dockerfile:**

    *   Create a file named `Dockerfile` in the root of your project.
    *   Paste the following content into the `Dockerfile`:
```
dockerfile
        # Use the official Node.js image as the base image
        FROM node:18-alpine

        # Set the working directory
        WORKDIR /app

        # Copy package.json and package-lock.json to the working directory
        COPY package*.json ./

        # Install dependencies
        RUN npm install

        # Copy the rest of the application files
        COPY . .

        # Expose the port the app runs in
        EXPOSE 3000

        # Set the command to run when the container starts
        CMD ["npm", "start"]
        
```
3.  **Build the Docker Image:**

    *   In your terminal, navigate to the project root (where the `Dockerfile` is located).
    *   Build the Docker image and tag it:
```
bash
        docker build -t gcr.io/celestial-globe-142799011534/celestial-globe-image .
        
```
4.  **Authenticate Docker with Google Cloud:**

    *   Run the following command to authenticate Docker with Google Cloud:
```
bash
        gcloud auth configure-docker
        
```
5.  **Push the Docker Image to Google Container Registry (GCR):**

    *   Push the built image to GCR:
```
bash
        docker push gcr.io/celestial-globe-142799011534/celestial-globe-image
        
```
6.  **Deploy to Google Cloud Run:**

    *   Deploy the image from GCR to Cloud Run, using the service name `celestial-globe-service`. Replace `[REGION]` with your desired region:
```
bash
        gcloud run deploy celestial-globe-service --image gcr.io/celestial-globe-142799011534/celestial-globe-image --region [REGION] --project 142799011534
        
```
*   When prompted, choose the desired region and whether to allow unauthenticated invocations.

7.  **Access Your Deployed Application:**

    *   After successful deployment, the gcloud CLI will output the URL where your application is now accessible.

## Part 2: Google Cloud Functions Deployment (Serverless Logic)

This section outlines how to deploy the serverless logic (primarily Python code) to Google Cloud Functions.

### Prerequisites

*   **Google Cloud Account:** You need a Google Cloud account with a project set up.
*   **Google Cloud SDK:** Install the Google Cloud SDK (gcloud CLI) on your local machine.
*   **Python:** Ensure you have Python installed locally.

### Steps

1.  **Install Python Dependencies:**

    *   Navigate to the `src/serverless` directory in your terminal.
    *   Create a virtual environment (optional but recommended):
```
bash
        python3 -m venv venv
        source venv/bin/activate
        
```
*   Install the dependencies listed in `requirements.txt`:
```
bash
        pip install -r requirements.txt -t .
        
```
2.  **Create a Deployment Package:**

    *   Ensure you are in the `src/serverless` directory.
    *   Zip the contents of the `serverless` directory, including the installed dependencies. You should be in the `src/serverless` directory:
```
bash
        cd ..
        zip -r serverless.zip serverless -x "*.git*" -x "venv*"
        
```
This will create a file named `serverless.zip` in the `src` directory.

3.  **Deploy to Google Cloud Functions:**

    *   Use the gcloud CLI to deploy your function. Adjust the following:
        *   `[FUNCTION_NAME]` is the name you want for your function.
        *   `[REGION]` is the region for your function.
        *   `[ENTRY_POINT]` is the entry point (function name) in your `skyfield_api.py` file. (for example: hello_world)
    *   Be sure that you are in the project's root directory.
```
bash
        gcloud functions deploy [FUNCTION_NAME] --region=[REGION] --runtime=python312 --source=src/serverless --entry-point=[ENTRY_POINT] --trigger-http --project 142799011534
        
```
4.  **Test Your Cloud Function:**

    *   After deployment, the gcloud CLI will output the URL to trigger your function. You can test it by visiting this URL in your browser or using a tool like `curl`.