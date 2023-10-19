"""
Author: Ali Binkowska
Date: August 2023
Classes & functions
"""
import asyncio
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import pandas as pd
import logging

from utils import (
    ModelLoader,
    RequestInterferenceData,
    ResponseData
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s: (%(levelname)s):  %(message)s")
log = logging.getLogger()


async def check_status_and_reload(model_loader: ModelLoader):
    """
    This is a loop function that execute model method that checks
    status of the model and reloads it if necessary
    """
    loop = asyncio.get_running_loop()
    while True:
        await asyncio.sleep(10)
        await loop.run_in_executor(
            executor=None, func=model_loader.check_and_reload
        )

#@app.on_event("startup")#
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Main API endpoint that is responsible for loading model dynamically"""

    server_uri = 'http://127.0.0.1:5001'
    model_name = "ModelName"
    stage = "Production"
    app.model_loader = ModelLoader(server_uri, model_name, stage)

    app.model_loader.load_artifacts()
    app.model_loader_task = asyncio.create_task(check_status_and_reload(app.model_loader))

    yield
    """Execute when API is shutdown, cancels the task to monitor model status"""
    app.model_loader_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/reload")
async def realoding_model():
    """Endpoint called by MLOps process when new model is set to Production"""
    app.model_loader.change_model_status()
    return {"model reload has been initiated"}

@app.post("/predict", response_model=ResponseData)
async def preprocess_data(data: RequestInterferenceData):
    """ Endoint that receives data about case(s) and returns predicted factor(s)"""
    try:
        results = [
            [
                case.dummy_1,
            ] for case in data.cases
        ]

        df = pd.DataFrame(
            results,
            columns=['dummy_1']
        )

        model = app.model_loader.model
        data_encoder = app.model_loader.encoder
        X = data_encoder.transform(df)

        predictions = model.predict(X)

        return {"predictions": predictions.tolist()}

    except Exception as e:
        log.error(f"app: error during inference {e}")
        raise HTTPException(status_code=500, detail=f"{e}")

    return predictions.tolist()


