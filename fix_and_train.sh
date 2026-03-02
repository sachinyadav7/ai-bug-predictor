#!/bin/bash

# Fix Environment and Run Training Script
# Usage: ./fix_and_train.sh

echo "1. Setting up Virtual Environment (to avoid system conflict)..."
# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate venv
source venv/bin/activate

echo "2. Upgrading PyTorch and Dependencies to fix security vulnerability..."
pip install --upgrade pip
pip install --upgrade torch transformers scikit-learn tqdm

echo "3. Regenerating dataset (Ensuring clean state)..."
python3 model/generate_synthetic_data.py

echo "4. Starting Training..."
python3 model/train_run.py

echo "5. Deploying Model..."
mkdir -p backend/models
cp best_model.pt backend/models/bug_predictor.pt

echo "Done! You can now verify with: ./venv/bin/python3 verify_prediction.py"
