#!/bin/bash
source /export/home/containerweb/ENGR-SVC-Makertech/deployable/config.sh

cd "$REPO_DIR"

# Build the Apptainer container
echo "Building Apptainer container..."
apptainer build "$SIF_FILE" "$DEF_FILE"