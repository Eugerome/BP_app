# Blood Pressure Recording app

Input records which get saved to database.

### Getting Started

#### Docker
Clone the repository.

Spin up a docker container with
`docker-compose up`

Access Swagger UI at http://localhost:6543/docs

#### Linux
Make sure python and virtualenv are installed

Clone the repository

In terminal
```
cd bp_app
virtualenv -p python3.8 .
source bin/activate
pip3 install -e .[development]
python bp_app/initialize_db.py development.ini
pserve development.ini
```

Access Swagger UI at http://localhost:6543/docs