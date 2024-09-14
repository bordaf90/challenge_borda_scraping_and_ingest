#!/bin/bash

# Variables
PROJECT_ID="challenge-borda"  # Replace with your Google Cloud project ID
REGION="us-central1"          # Change to your preferred region
IMAGE_NAME="challenge_image"  # Docker image name
REPO_NAME="challenge_repo"    # Name of the artifact repository (Artifact Registry or Container Registry)
SERVICE_NAME="challenge_service" # Name of the Cloud Run service
TAG="latest"                  # Tag for the image

# Authenticate with Google Cloud (optional if already authenticated)
gcloud auth login

# 1. Build the Docker image
echo "Building the Docker image..."
docker build -t "$IMAGE_NAME:$TAG" .

# 2. Tag the image for the Google repository
echo "Tagging the image for the repository..."
docker tag "$IMAGE_NAME:$TAG" "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$TAG"

# 3. Push the image to the artifact repository
echo "Pushing the image to the Artifact Registry..."
docker push "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$TAG"

# 4. Deploy the image to Cloud Run
echo "Deploying the image to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
  --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$TAG" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --timeout=300

echo "Deployment successfully completed."
