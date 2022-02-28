# Python-Postgres
#
Catchpoint Integration with PostgreSQL
---

PostgreSQL is a powerful, open source object-relational database system.
This integration relies on a Python script that runs once every15 minutes to pull raw performance data of synthetic tests. The raw performance data pulled through REST API is parsed with correct timestamp, breakdowns and all performance metrics to be stored in PostgreSQL. Once the data is stored in PostgreSQL, it can be connected to any analytics tools and plot similar graphs to Catchpoint with ease.


### Prerequisites
---
1. Python v3.x
2. [PostgreSQL v13.x](https://www.postgresql.org/download/)
3. Catchpoint account with a REST API consumer

# Installation and Configuration

Copy the Postgres-Python folder to your machine
Run following commands in the directory /Postgres-Python
   - python -m pip install requests
   - pip install pyyaml
   - pip install logger
   - pip install psycopg2
   - pip install python-dateutil
   
   
### Configuration
In the config_catchpoint.yaml file under config sub-directory, enter your [Catchpoint API consumer key and secret](https://portal.catchpoint.com/ui/Content/Administration/ApiDetail.aspx)
In the test_ids object of the config_catchpoint.yaml file, enter the test IDs you want to pull the data for in a dictionary of array format.

*Example:*

    test_ids: { 
              web : ['142619','142620','142621','142622'],
              traceroute : ['142607','142608','142609'], 
              api : ['142637','142638','142683','142689'],
              transaction: ['142602','142603'],
              dns : '142644','142645','142646','142647'],
              smtp : ['142604'],
              websocket: ['842700'],
              ping : ['142599','142600','142601']
              
          }
---       
In the config_mongo.py file, enter your MongoDB url, database name and collection name where the data will be stored. The default MongoDB URL for a local installation is http://localhost:27017


### How to run

 
- Create a cronjob to run the application.py file every 15 minutes.

*Example crontab entry, if the file resides in /usr/local/bin/application.py*

`*/15 * * * * cd /usr/local/bin/ && python /usr/local/bin/application.py > /usr/local/bin/logs/cronlog.log 2>&1`


or 

- In the /python-mongo directory, run appliaction.py after uncommenting the while true: and time.sleep.




## File Structure

    Postgres-Python/
    ├── request_handler.py          ## Contains APIs related to authentication       
    ├── config
    | ├── config_catchpoint.yaml    ## Configuration file for Catchpoint 
    | ├── config_postgres.yaml        ## Configuration file for PostgreSQL 
    ├── log
    | ├── app.log                   ## Contains informational and error logs. 
    ├── application.py              ## main file
    ├── log.py                      ## custom logger function
    ├── request_handler.py          ## Contains API requests for token and raw endpoint 
    ├── utils.py                    ##  utility for parsing data, inserting it to postgres and validating configurations
           

Once the script starts running and data is inserted into PostgreSQL, it can queried using PsQL.
