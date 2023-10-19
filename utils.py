"""
Author: Ali Binkowska
Date: August 2023
Classes & functions
"""
import logging
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime, timedelta
import mlflow
import pandas as pd

logging.basicConfig(level=logging.INFO, format="(%(levelname)s):  %(message)s")
log = logging.getLogger()


class ModelLoader:
    def __init__(self, server_uri, model_name, stage):
        # Mock initialization
        self.server_uri = server_uri
        self.model_name = model_name
        self.stage = stage
        self.is_prod_model = True


    def load_artifacts(self):

        mlflow.set_tracking_uri(self.server_uri)
        model_uri = f"models:/{self.model_name}/{self.stage}"

        try:
            self.model = mlflow.sklearn.load_model(model_uri)
            self.is_prod_model = True
            log.info(f"app: model has been loaded successfully")
        except:
            log.warning("app: model is not available!")

    def check_and_reload(self):
        if not self.is_prod_model:
            self.load_artifacts()

    def change_model_status(self):
        self.is_prod_model = False
        log.info(f"app: model reload request received")


    @property
    def model(self):
        # Return a mock model.
        class DummyModel:
            def predict(self, X):
                return [1 for _ in X]

        return DummyModel()

    @property
    def encoder(self):
        # Return a mock encoder.
        class DummyEncoder:
            def transform(self, df, ranking_tables=None):
                return [[1 for _ in row] for row in df.values]

        return DummyEncoder()


class RequestInterferenceData(BaseModel):
    def __init__(self):
        # Mock initialization
        self.cases = [self.DummyCase() for _ in range(5)]  # Create 5 dummy cases

    class DummyCase:
        # Mock attributes
        dummy_1 = 1



class ResponseData(BaseModel):
    predictions: List[float]