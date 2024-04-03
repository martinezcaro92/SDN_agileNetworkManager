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
            |- provisioning.py
            |- topologies.py
            |- models.py
        |- __init__.py
        |- main.py
        |- DatabaseHandler.py
        |- EWBI_client_module.py
        |- SBI_client_module.py
    |- mocks
        |- Dockerfile
        |- requirements.txt
        |- sdn_controllers.py
    |- tests
        |- __init__.py
        |- conftest.py
        |- DT_rabbitmq_test_rx.py
        |- rabbitmq_test_tx1.py
        |- rabbitmq_test_tx2.py
        |- test_controllers.py
        |- test_provisioning.py
        |- test_topology.py
        |- test_zpurge.py
    |- Dockerfile
    |- requirements.txt
|- .gitignore
|- docker-compose.yml
|- README.md
|- LICENSE
``` 

## Requirements installed on your PC

-   Docker (or Docker Desktop on Windows)
-   Docker Compose
-   Python
-   Git

## Getting Started

1.  Clone this repository to your local machine.
2.  Open a terminal and navigate to the project directory.

## Running the Services

Run the following command to start the services using Docker Compose:

`docker-compose up --build`, if previous command does not work, please try `docker compose up --build`. The previous command requires 5 minutes aprox to complete the set-up

This will build and start the following services:

-   **mongodb**: MongoDB database service, accessible at [http://localhost:27017](http://localhost:27017/)
-   **mongo-express**: MongoDB web-based administration tool, accessible at [http://localhost:8081](http://localhost:8081/)
-   **api-test**: Python microservice, accessible at [http://localhost:8003/docs](http://localhost:8003/docs)
-   **rabbitmq**: RabbitMQ message broker service, accessible at [http://localhost:5672](http://localhost:5672/) and [http://localhost:15672](http://localhost:15672/) (management UI that requires authentication)

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

### API Test

This service runs the Python microservice.

-   Access the microservice at [http://localhost:8080](http://localhost:8080/)
-   Environment Variable: PYTHONDONTWRITEBYTECODE=1
-   The service depends on the MongoDB service.

### RabbitMQ

-   Access the broker at [http://localhost:5672](http://localhost:5672/)
-   Management UI: [http://localhost:15672](http://localhost:15672/)
-   Username: admin
-   Password: admin123

To listen the RabbitMQ channel, please lauches the test script `DT_rabbitmq_test_rx`. The script keeps the terminal open and print if a new message is received.

Otherwise, the test script `rabbitmq_test_tx1` and `rabbitmq_test_tx2` send messages by rabbitmq channels and is received in `DT_rabbitmq_test_rx`.

The commands to test the performance are:
``` bash
# Terminal 1
python -B ./src/test/DT_rabbitmq_test_rx.py

# Terminal 2
python -B ./src/test/rabbitmq_test_tx1.py
python -B ./src/test/rabbitmq_test_tx2.py
```

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

The response is:

``` bash
====================================================================================================================== test session starts ======================================================================================================================
platform linux -- Python 3.11.0, pytest-7.2.0, pluggy-1.2.0
rootdir: /usr/src/app
plugins: anyio-3.7.1
collected 23 items

tests/test_controllers.py ........                                                                                                                                                                                                                        [ 34%]
tests/test_provisioning.py .....                                                                                                                                                                                                                          [ 56%]
tests/test_topology.py .......                                                                                                                                                                                                                            [ 86%]
tests/test_zpurge.py ...                                                                                                                                                                                                                                  [100%]

======================================================================================================================= warnings summary ========================================================================================================================
tests/test_controllers.py::test_post_controllers
  /usr/local/lib/python3.11/site-packages/_pytest/python.py:199: PytestReturnNotNoneWarning: Expected None, but tests/test_controllers.py::test_post_controllers returned ('cdf51a06-2d5c-4065-9070-39b60269fb7b', <Response [200 OK]>), which will be an error in a future version of pytest.  Did you mean to use `assert` instead of `return`?
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================================= 23 passed, 1 warning in 1.76s =================================================================================================================
```

### Unit tests (mock microservice)

To run unit tests for all components within the project, you can execute the following command using Docker Compose:

```bash
docker-compose exec mock pytest .
```

The response is:

``` bash

====================================================================================================================== test session starts ======================================================================================================================
platform linux -- Python 3.11.0, pytest-7.2.0, pluggy-1.2.0
rootdir: /usr/src/mocks
plugins: anyio-3.7.1
collected 6 items

tests/test_externalIntegrations.py ......                                                                                                                                                                                                                 [100%]

======================================================================================================================= 6 passed in 1.19s =======================================================================================================================

```
