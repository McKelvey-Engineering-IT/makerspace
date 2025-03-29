source /export/home/containerweb/ENGR-SVC-Makertech/deployable/config.sh

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

# Move build.sh and deploy.sh to the parent directory
if [ -f "$REPO_DIR/build_image.sh" ]; then
    mv "$REPO_DIR/build_image.sh" "$PARENT_DIR/build_image.sh"
    echo "Moved build.sh to $PARENT_DIR"
fi

if [ -f "$REPO_DIR/deploy_app.sh" ]; then
    mv "$REPO_DIR/deploy_app.sh" "$PARENT_DIR/deploy_app.sh"
    echo "Moved deploy.sh to $PARENT_DIR"
fi

if [ -f "$REPO_DIR/refresh_repo.sh" ]; then
    mv "$REPO_DIR/refresh_repo.sh" "$PARENT_DIR/refresh_repo.sh"
    echo "Moved deploy.sh to $PARENT_DIR"
fi
