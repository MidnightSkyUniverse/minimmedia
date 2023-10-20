![name-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]


## MLFlow + FastAPI model serving

The code has been used to create model serving  API  with FastAPI and MLFlow.
The requirements were to start API without an existing model and load a model once it becomes available.

The code introduces a loop that awaits status change - the status indicate that the new Production model is ready
and can be loaded. The status change is initiated by GET request sent to URL.



## Preliminary steps

### Create environment
Using conda or miniconda install virtual environment:

```bash
> conda env create -n <env_name>
> conda activate <env_name>
> pip install ir requirements.txt
```

### Start MLFlow server
`mlflow server -p 5001 --host 0.0.0.0`

### Start FastAPI server
`gunicorn app:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5002 --timeout 120`

First you see warning about missing model.
```commandline
[2023-10-20 07:52:24 +0200] [9776] [INFO] Waiting for application startup.
(WARNING):  app: model is not available!
[2023-10-20 07:52:24 +0200] [9776] [INFO] Application startup complete.

```

The code checks for model once and while there is a loop checking status of a model every 10 seconds,
the status is set to True to model so we don't try to load the model until we are sure MLFlow server can serve a model.

GET request sent to localhost:5002/reload will change status of a variable to False,
and since that moment there will be a funciton querying MLFlow for a model until one is available to be loaded.

This will result in logs showing
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
