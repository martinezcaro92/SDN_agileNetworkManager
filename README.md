# SDN_agileNetworkManager

Welcome to the SDN_agileNetworkManager project! This is a microservices-based project designed to manage SDN architecture settings. This README will guide you through setting up and running the project using Docker and Docker Compose.

## Project Structure

```
SDN_agileNetworkManager
|- src
    |- app
        |- api
            |- __init__.py
            |- controllers.py
            |- topologies.py
            |- models.py
        |- __init__.py
        |- main.py
    |- tests
        |- __init__.py
        |- conftest.py
        |- test_controllers.py
        |- test_topology.py
        |- test_zpurge.py
    |- DatabaseHandler.py
    |- Dockerfile
    |- requirements.txt
|- .gitignore
|- docker-compose.yml
|- README.md
``` 

## Requirements installed on your PC

-   Docker (or Docker Desktop on Windows)
-   Docker Compose
-   Python
-   Git
-   Web Browser

### Recomendations
-   Visual Studio Code

## Getting Started

1.  Clone this repository to your local machine.
2.  Open a terminal and navigate to the project directory.

## Running the Services

Run the following command to start the services using Docker Compose:

`docker-compose up --build`, if previous command does not work, please try `docker compose up --build`. The previous command requires 5 minutes aprox to complete the set-up

This will build and start the following services:

-   **mongodb**: MongoDB database service, accessible at [http://localhost:27017](http://localhost:27017/). No GUI, only attending queries.
-   **mongo-express**: MongoDB web-based administration tool, accessible at [http://localhost:8081](http://localhost:8081/)
-   **web**: Python microservice, accessible at [http://localhost:8003/docs](http://localhost:8003/docs)

## Service Details

### MongoDB

-   Username: admin
-   Password: admin123
-   Database: You can create your databases as needed.

### Mongo Express

-   Username: admin
-   Password: admin123
-   MongoDB Server: mongodb
-   Access the admin panel at [http://localhost:8081](http://localhost:8081/)

### Web

This service runs the Python microservice.

-   Access the microservice at [http://localhost:8003/docs](http://localhost:8003/docs/)
-   Environment Variable: PYTHONDONTWRITEBYTECODE=1
-   The service depends on the MongoDB service.


## Project Usage

-   The `src` directory contains your `Python` application code.
-   The `app` directory contains the `FastAPI` implementation.
-   The `tests` directory contains test cases for the project using `pytest`.

Feel free to modify the project files and directory structure to suit your needs.


## Testing

### Unit tests (web microservice)

Previous to run the unit test, please make sure that there are not any `pytest_cache` directory at `app` and `mocks` folders.
Then, to run the unit tests for all components within the project, you can execute the following command using Docker Compose:

```bash
docker-compose exec web pytest .
```

If the previous command does not work on your PC, please try `docker compose exec web pytest .`

The response is:

``` bash
=PS C:\Repositorio\SDN_agileNetworkManager> docker compose exec web pytest .
================================================================================================================= test session starts =================================================================================================================
platform linux -- Python 3.11.0, pytest-7.2.0, pluggy-1.4.0
rootdir: /usr/src/app
plugins: anyio-3.7.1
collected 12 items

tests/test_controllers.py .....                                                                                                                                                                                                                 [ 41%]
tests/test_topology.py .....                                                                                                                                                                                                                    [ 83%]
tests/test_zpurge.py ..                                                                                                                                                                                                                         [100%]

================================================================================================================== warnings summary ===================================================================================================================
tests/test_controllers.py::test_post_controllers
  /usr/local/lib/python3.11/site-packages/_pytest/python.py:199: PytestReturnNotNoneWarning: Expected None, but tests/test_controllers.py::test_post_controllers returned ('dd0ff9ce-7fff-44bd-87bf-95c6d8122610', <Response [200 OK]>), which will be an error in a future version of pytest.  Did you mean to use `assert` instead of `return`?
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================================================================================ 12 passed, 1 warning in 0.45s ============================================================================================================
```
