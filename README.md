# TraCAD - Python Application

Backend service for ICAT Climate Action Assessment Tool for Transport Sector - TraCAD.

Supported by [Initiative for Climate Action Transparency - ICAT](https://climateactiontransparency.org/).

Built using [Python 3](https://www.python.org/) and [FastAPI](https://fastapi.tiangolo.com/) framework.

## Manual Installation

1. Download and install the [Python 3](https://www.python.org/downloads) for your operational system.

2. Download or clone this repository.

3. In the terminal, go to this repository's main folder.

4. Install the Pip dependencies with the command:

```bash
$ pip3 install -r requirements.txt
```

5. Run the app:

```bash
$ uvicorn main:app --reload
```

## Google Cloud Installation with Docker

> This is an example cloud installation using [Docker](https://www.docker.com/) and Google Cloud Plataform. The provided `Dockerfile` can be used for local or cloud installation with different services.

1. In GCP Console, go to [Artifact Registry](https://console.cloud.google.com/artifacts) and enable the Artifact Registry API

2. In the Artifact Registry, create a new repository:

   - **Format:** Docker
   - **Type:** Standard
   - **Location:** desired application location
   - **Encryption:** Google-managed key

3. Download and install [gcloud CLI](https://cloud.google.com/sdk/docs/install).

4. Download or clone this repository.

5. In the terminal, go to this repository's main folder.

6. Build your container in the Artifacts Register using the provided `Dockerfile`. The container path can be found on the Artifact Registry's repository page.

```bash
$ gcloud builds submit --tag [CONTAINER PATH]
```

7. Go to [Cloud Run](https://console.cloud.google.com/run) and create a New Service:
   - Choose the option `Deploy one revision from an existing container image` and select the container image updated in the previous step
   - Add a service name
   - Select the application region
   - Select `Allow unauthenticated invocations` in the Authentication option
   - In the **Container section**:
     - Select Container port 80

> Noticed that some [special permissions in GCP](https://cloud.google.com/run/docs/reference/iam/roles#additional-configuration) can be necessary to perform these tasks.

## API Documentation

After the application installation, the API Documentation is available in the application URL + `/docs/` with [Swagger](https://swagger.io/solutions/api-documentation/).

## License

TraCAD - CountryPortalService is [Affero GPL licensed](https://www.gnu.org/licenses/agpl-3.0.en.html).
