# Invsto Backend 

This project is a backend service built for the Invsto Backend Intern assignment. It features a containerized FastAPI application that provides API endpoints to interact with time-series stock data stored in a PostgreSQL database. The application also includes functionality to analyze this data using a simple moving average crossover trading strategy.

-----

## Demo 

https://github.com/user-attachments/assets/466e665c-ff72-4f67-8b56-13da9688f36a

-----

## Features

  * **REST API**: A robust API built with FastAPI for all data interactions.
  * **Database**: Utilizes PostgreSQL for persistent data storage, managed via **Docker**.
  * **ORM**: Uses SQLAlchemy for elegant and efficient database communication.
  * **Containerized**: Fully containerized with Docker and Docker Compose, including a `Makefile` to simplify project management.
  * **Trading Strategy**: Implements a Moving Average Crossover strategy to generate buy/sell signals.
  * **Tested**: Includes a suite of unit tests with over 90% code coverage.

-----

## Prerequisites

Before you begin, ensure you have the following installed on your system:

  * Docker
  * Docker Compose
  * Make

-----

## Getting Started

To get the application running locally, follow these steps:

1.  **Clone the repository**

    ```sh
    git clone https://github.com/ryu-ryuk/inv
    cd inv
    ```

2.  **Build and run the containers**
    This command builds the necessary Docker images and starts the API and database services in the background.

    ```sh
    make up
    ```

3.  **Populate the database**
    Execute the import script to load the sample data from the CSV file into the database.

    ```sh
    make import-data
    ```

4.  **Verify the application is running**
    You can now access the application endpoints. For example, navigate to `http://localhost:8000/data` in your browser.

-----

## Makefile Commands

This project includes a `Makefile` to simplify common tasks. You can view all available commands and their descriptions by running `make` in your terminal. Key commands include:

  * `make up`: Builds and starts all services.
  * `make down`: Stops all services and removes the database volume.
  * `make test`: Runs the full test suite and generates a coverage report.

-----

## API Endpoints

The following endpoints are available:

  * `GET /data`

      * **Description**: Fetches all stock data records from the database, ordered by date.
      * **Response**: A JSON array of stock data objects.

  * `POST /data`

      * **Description**: Adds a new stock data record to the database.
      * **Body**: Requires a JSON object matching the stock data schema.

  * `GET /strategy/performance`

      * **Description**: Runs the Moving Average Crossover strategy on the entire dataset and returns a performance report.
      * **Response**: A JSON object containing strategy parameters, total trades, profit/loss, and a list of buy/sell signals.

-----

## Running Tests

To run the unit test suite and generate a coverage report, use the simplified `make` command:

```sh
make test
```

---

[LICENSE](LICENSE)
