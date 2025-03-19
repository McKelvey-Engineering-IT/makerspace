#!/bin/bash

# Set variables
REPO_DIR="/export/home/containerweb/ENGR-SVC-Makertech/deployable/makerspace"
DEF_FILE="app.def"
SIF_FILE="app.sif"

cd "$REPO_DIR"

# Build the Apptainer container
echo "Building Apptainer container..."
apptainer build "$SIF_FILE" "$DEF_FILE"