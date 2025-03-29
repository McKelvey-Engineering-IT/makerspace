# # #!/bin/bash
source /export/home/containerweb/ENGR-SVC-Makertech/deployable/config.sh

cd "$REPO_DIR"

# Navigate to frontend folder and create .env file
if [ -d "$FRONTEND_DIR" ]; then
    cd "$FRONTEND_DIR"
    echo "REACT_APP_API_URL=https://makertech.engr.wustl.edu/" > .env
    echo "Created .env file in $FRONTEND_DIR"
else
    echo "Frontend directory not found: $FRONTEND_DIR"
fi


echo "Shutting down previous container"
apptainer instance stop makerspace

# Run Apptainer instance with bind mount
echo "Running container with repo bind-mounted..."
apptainer instance start --bind "$REPO_DIR:$MOUNT_POINT" "$SIF_FILE" makerspace
