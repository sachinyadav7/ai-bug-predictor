#!/bin/bash

# Script to train on Defects4J dataset
# Usage: ./run_defects4j_training.sh

echo "1. Setting up environment..."
source venv/bin/activate

echo "2. Checking for Defects4J..."
if [ ! -d "/home/sachin/defects4j" ]; then
    echo "Warning: /home/sachin/defects4j not found."
    echo "Please ensure Defects4J is installed and the path in model/extract_defects4j.py is correct."
    echo "If you don't have Defects4J, the next step will fail."
fi

echo "3. Extracting and Splitting Defects4J Data..."
python3 model/extract_defects4j.py

echo "4. Starting Real-World Training..."
echo "Config: 3 Epochs, LR=3e-5, Class Weight=3.0"
python3 model/train_run.py

echo "5. Deploying Model..."
mkdir -p backend/models
cp best_model.pt backend/models/bug_predictor.pt

echo "Done! Verify with: ./venv/bin/python3 verify_prediction.py"
