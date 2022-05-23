import os

import mlflow
import pandas as pd
from dotenv import load_dotenv
import unicorn
from fastapi import FastAPI, File, UploadFile, HTTPException


# Load the environment variables from the .env file into application
load_dotenv()

# Initialize the FastAPI application
app = FastAPI()

os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.getenv("MLFLOW_S3_ENDPOINT_URL")


class Model:
    def __init__(self, model_name, model_stage):
        """

        :param model_name:
        :param model_stage:
        """
        # Load the model from Registry
        self.model = mlflow.pyfunc.load_model(
            f"models:/{model_name}/{model_stage}"
        )

    def predict(self, data):
        """

        :param data:
        :return:
        """
        predictions = self.model.predict(data)
        return predictions


# Create model
model = Model(model_name="forest_model",
              model_stage="Staging")


# Create the POST endpoint with path '/invocation'
@app.post("/invocation")
async def create_upload_file(file: UploadFile = File(...)):
    """

    :param file:
    :return:
    """
    if file.filename.endswith(".csv"):
        # Create a temporary file with the same name as the uploaded
        # CSV file to load the data into a pandas DataFrame
        with open(file.filename, 'wb') as f:
            f.write(file.file.read())
        data = pd.read_csv(file.filename)
        os.remove(file.filename)
        return list(model.predict(data))

    else:
        raise HTTPException(status_code=400, detail="Invalid file format")


# Check if environment variables for AWS access are available
# If not, exit the programm
if os.getenv("AWS_ACCESS_KET_ID") is None or \
        os.getenv("AWS_SECRET_ACCESS_KEY") is None:
    exit(1)

