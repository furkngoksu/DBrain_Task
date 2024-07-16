# Scraper and Kafka Consumer Project

This project demonstrates how to scrape product data from a website, send it to a Kafka topic, and consume the data from the Kafka topic using a consumer service. The data is then served via a Flask API.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

- `Dockerfile`: Defines the Docker image for the project.
- `docker-compose.yml`: Defines the multi-container Docker application.
- `app.py`: Flask application to serve product data.
- `scraper.py`: Script to scrape product data and send it to Kafka.
- `consumer.py`: Script to consume data from Kafka and save it to `data.json`.
- `requirements.txt`: Python dependencies for the project.

## Setup

1. Clone the repository to your local machine:
    ```sh
    git clone [https://your-repo-url.git](https://github.com/furkngoksu/DBrain_Task.git)
    cd your-repo-directory
    ```

2. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```

## Usage

### Continuous Data Flow

- **Scraper Service**
  - Continuously scrapes product data from the specified website every second.
  - Sends the data to the Kafka topic `test-topic`.

- **Consumer Service**
  - Continuously consumes messages from the Kafka topic `test-topic`.
  - Updates the `data.json` file with the latest product data.

### Flask API

- Serves the product data stored in `data.json` at the endpoint `/products`.
- To access the product data, send a GET request to:
    ```
    http://127.0.0.1:5000/products
    ```
- The API returns the latest product data in JSON format, fetched from `data.json`.

### Example API Response

```json
[
    {
        "name": "Bulbasaur",
        "price": "£63.00",
        "description": "Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun’s rays, the seed grows progressively larger.",
        "stock": "45 in stock"
    },
    {
        "name": "Ivysaur",
        "price": "£87.00",
        "description": "There is a bud on this Pokémon’s back. To support its weight, Ivysaur’s legs and trunk grow thick and strong. If it starts spending more time lying in the sunlight, it’s a sign that the bud will bloom into a large flower soon.",
        "stock": "142 in stock"
    },
    ...
]
```

## Troubleshooting

- If you encounter any issues with Kafka connectivity, ensure that the `KAFKA_ADVERTISED_LISTENERS` and `KAFKA_ZOOKEEPER_CONNECT` environment variables in `docker-compose.yml` are correctly set.
- Ensure that all services are up and running by checking the Docker logs:
    ```sh
    docker-compose logs
    ```
- If `data.json` does not exist, it will be created by the consumer service. Ensure that the `consumer.py` script is running and consuming data from the Kafka topic.

## Notes

- The `data.json` file is initially empty. It will be populated by the consumer service as it consumes messages from the Kafka topic.
- Ensure the website being scraped is accessible and the structure of the HTML has not changed.

## Contributing

- Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
```
