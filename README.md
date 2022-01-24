# postgres-python




## File Structure

    Python-Influx/
    ├── request_handler.py          ## Contains APIs related to authentication       
    ├── config
    | ├── config_catchpoint.yaml    ## Configuration file for Catchpoint 
    | ├── config_postgres.yaml        ## Configuration file for PostgreSQL 
    ├── log
    | ├── app.log                   ## Contains informational and error logs. 
    ├── application.py              ## main file
    ├── log.py
    ├── request_handler.py          ## Contains API requests for token and raw endpoint 
    ├── utils.py                    ##  utility fot partsing data, inserting it to postgres and validating configurations
           
