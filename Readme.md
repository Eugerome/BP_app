# Blood Pressure Recording app

Input records which get saved to database.

### Getting Started

#### Docker
Clone the repository.

Spin up a docker container with
`docker-compose up`

Access Swagger UI at http://localhost:6543/docs

#### Linux
Make sure python 3.8 and pip and venv are installed

Clone the repository

In terminal
```
cd bp_app
python3 -m venv .
pip3 install -e ".[dev]"
python3 bp_app/initialize_db.py development.ini
pserve development.ini
```

Access Swagger UI at http://localhost:6543/docs