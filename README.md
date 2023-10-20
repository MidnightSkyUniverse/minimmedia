![name-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]


## MLFlow + FastAPI model serving

The code has been used to create model serving  API  with FastAPI and MLFlow.
The requirements were to start API without an existing model.

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

Since MLFlow has no models to serve, the API logs will show the warning about missing model.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[name-shield]: https://img.shields.io/badge/Author-Ali%20Binkowska-blueviolet?style=for-the-badge
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/alibinkowska
