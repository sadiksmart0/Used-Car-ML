#!/bin/bash

# Set environment variable for the tracking URL where the Model Registry resides
set MLFLOW_TRACKING_URI=http://localhost:5000

# Serve the production model from the model registry
mlflow models serve --model-uri "models:/Model_A/Production" -p 1234 --no-conda
