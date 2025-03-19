# #!/bin/bash

# # Set variables
GITHUB_USER="yourusername"
GITHUB_TOKEN="your_personal_access_token"
REPO_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/McKelvey-Engineering-IT/makerspace.git"
REPO_DIR="/export/home/containerweb/ENGR-SVC-Makertech/deployable/makerspace"
SIF_FILE="app.sif"
MOUNT_POINT="/app"

if [ -d "$REPO_DIR/.git" ]; then
    echo "Updating existing repo..."
    cd "$REPO_DIR"
    git fetch --all
    git reset --hard origin/main
    git pull origin main
    echo "Done with Repo"
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"

echo "Running container with repo bind-mounted..."
apptainer run --bind "$REPO_DIR:$MOUNT_POINT" "$SIF_FILE"