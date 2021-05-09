# FASTAPI
https://fastapi.tiangolo.com/tutorial/

## how to install 
``` pip install fastapi'[all]' ```

or you can
``` pip install fastapi ```
``` pip install uvicorn[standard] ```

## Installing Postgress
``` sudo apt install postgresql postgresql-contrib ```
 
## starting postgress
``` sudo -u postgres psql ```

## How to run the api
``` uvicorn main:app --reload ```


# Errors
=> Postgresql: password authentication failed for user “postgres”

=> Fix
``` sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" ```
Done! You saved User = postgres and password = postgres.

