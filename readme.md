# Usage

Please Note this application/project uses python 3.9

- to run the application as below
  ```bash
  $ docker-compose up
  ```

- to use/test the endpoints please refer to [postman_collection.json](postman_collection.json)

# Challenge

Write an API using Django that fetches the price of BTC/USD from the alphavantage API
every hour, and stores it on postgres. This API must be secured meaning that you need an
API key to use it. There should be two endpoints: GET /api/v1/quotes - returns exchange rate
and POST /api/v1/quotes which triggers force requesting of the price from alphavantage. The
API & DB should be containerized using Docker as well.

- Every part should be as simple as possible.
-The project should be committed to GitHub.
- The sensitive data such as alphavantage API key, should be passed from the .env
"gitignored" file via environment variables.

## Assumptions

- migration and creation of user is automated
- since it is required to fetch data every hour, a background worker (similar to cron) must be included
- is waiting for an hour from start up is a bit long we should force the task to run once at start up
- test is created to ensure code quality
- since it is mentioned to create an endpoint that fetches 
  all the exchange rates it is handy to have another that returns only the latest.  

## Tasks

- [x] Create a background task that runs every 1 hour to fetch data from alpha vantange.
- [x] Configure the application to use postgresql as its main database.
- [x] Create endpoint `POST /api/v1/quotes` to trigger the background task that fetches data from alpha vantage.
- [x] Create endpoint `GET /api/v1/quotes` to retrieve the exchange rates.
- [x] Create endpoint `GET /api/v1/quotes/latest` to retrieve the single latest exchange rate.
- [x] Endpoints should be protected by `JWT`
- [x] Sensitive configuration/settings must be stored as environment variable or stored in `.env`.
- [x] Dockerize the services included the database.

## Technology Stack

- Django and Django REST Framework
- Celery
- Postgresql
- Traefik

## Note

Celery doesn't work well with windows. to make it work make sure you specify `solo` or `threads` as pool
  ```bash
  $ celery -A coin_mena_challenge.celery_app worker -l INFO -P solo
  ```