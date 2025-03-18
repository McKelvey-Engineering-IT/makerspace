#!/bin/bash

# Set variables
GITHUB_USER="yourusername"
GITHUB_TOKEN="your_personal_access_token"
REPO_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/McKelvey-Engineering-IT/makerspace.git"
REPO_DIR="/export/home/containerweb/ENGR-SVC-Makertech/deployable/makerspace"
DEF_FILE="app.def"
SIF_FILE="app.sif"
MOUNT_POINT="/export/home/containerweb/ENGR-SVC-Makertech/deployable/makerspace/"

# Clone or update the repository
if [ -d "$REPO_DIR/.git" ]; then
    echo "Updating existing repo..."
    cd "$REPO_DIR"
    git fetch --all
    git reset --hard origin/main
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$REPO_DIR"
fi

# Go back to home directory
cd "$HOME"

# Build the Apptainer container
echo "Building Apptainer container..."
apptainer build "$SIF_FILE" "$DEF_FILE"

# Run the container with the GitHub repo mounted
echo "Running container with repo bind-mounted..."
apptainer run --bind "$REPO_DIR:$MOUNT_POINT" "$SIF_FILE"