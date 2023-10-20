![name-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]
![website-shield]


## MLFlow + FastAPI model serving

This repository provides code for serving models via an API using FastAPI and MLFlow. 
A distinctive feature is that the API can start even if a model is not yet available. 
The system will then periodically check for the availability of a new production model and load it once ready.

### How it works
The code continuously monitors a status indicating the availability of a new production model. 
A status change, signaling that the model is ready to be loaded, is triggered by a GET request to a specific URL.

## Preliminary steps

### Set Up the Environment
To prepare your environment, you can use either conda or miniconda:

```bash
> conda env create -n <env_name>
> conda activate <env_name>
> pip install -r requirements.txt
```

### Launch MLFlow Server
`mlflow server -p 5001 --host 0.0.0.0`

### Start the FastAPI Server
`gunicorn app:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5002 --timeout 120`

Upon initialization, you may notice a warning about a missing model:
```commandline
[2023-10-20 07:52:24 +0200] [9776] [INFO] Waiting for application startup.
(WARNING):  app: model is not available!
[2023-10-20 07:52:24 +0200] [9776] [INFO] Application startup complete.
```

The code checks for model once and while there is a loop checking status of a model every 10 seconds,
the status is set to True to model so we don't try to load the model until we are sure MLFlow server can serve a model.
The system checks the model's status periodically. While in monitoring mode, the system will not attempt to load a model unless it's certain the MLFlow server can serve it.

Sending a GET request to localhost:5002/reload will change the status, prompting the system to actively query the MLFlow server until a model becomes available.

Repeated logs may appear as:This will result in logs showing
```
(WARNING):  app: model is not available!
(WARNING):  app: model is not available!
...
```



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[name-shield]: https://img.shields.io/badge/Author-Ali%20Binkowska-blueviolet?style=for-the-badge
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/alibinkowska
[website-shield]: https://img.shields.io/badge/Website%20-%20Ali%20Binkowska%20-%2000CCFF?style=for-the-badge&color=00CCFF&link=https%3A%2F%2Falibinkowska.co


