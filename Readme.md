# Blood Pressure Recording app

A Python Pyramid powered API that stores and retrieves Blood Pressure records.

Has a Swagger UI for documentation/testing.

Has a User UI powered with pure JavaScript (first attempts).

### BUGS

!!! Currently openapi validation not working out of the box. The easiest fix at this point is manually applying the changes below:
https://github.com/Pylons/pyramid_openapi3/issues/87

### Getting Started

#### With Docker
Clone the repository.

Spin up a docker container with
`docker-compose up`

#### With Linux Machine
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

### Running

Access Swagger UI at http://localhost:6543/docs
Access User UI at http://localhost:6543/table

### Next steps

* Visual User UI improvements (Html+CSS work)
* Adding Graph View (Python/JavaScript)
* Adding Authentication for multiple user use
* Restructuring DB/API to handle multiple users
