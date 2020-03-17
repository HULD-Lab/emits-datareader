# EMITS datareader 
> by [HULD](https://huld.io)
Reading and storing data from EMITS emails into DB.

# Setting the environment
## Update Secret.json
* See the examples in /secret_sample.json
* Update this file with outlook credentials and other parameters you wish tune
* Save it as a secret.json under /code/ directory (i.e /code/secret.json)

## Run following commands:
```
docker-compose build
docker-compose up
```
## Automation
Set `cron` for the following command.
```
docker start emits-datareader_app_1
```
This command updates the database.

# Connection to PowerBI on windows
Pre-Condition: mongo db container up and running
1. Install Mongo Connector for BI
2. Run  the following in windows command line 
```PowerShell
C:\Program Files\MongoDB\Connector for BI\2.13\bin>mongosqld.exe --mongo-uri <ip address on which a container has been exposed> -u <mongo user name from secret.json> -p <password from secret.json>
```
3. Install and Mongo ODBC driver, under system DSN 
4. Test connection on localhost that has been created by Mongo Connector for BI that is connected to remote instance and translate the connection onto localhost.
5. Open PowerBI and under Other select ODBC, from the list select Mongo

for detailed guide see [Mongo help](http://docs.mongodb.com/bi-connector/master/reference/odbc-driver/)