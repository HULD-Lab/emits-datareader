# EMITS datareader

Reading and storing data from EMITS emails into DB.

# Setting the environment

Run following commands:
```
docker-compose build
docker-compose up
```

Set `cron` for the following command.
```
docker start emits-datareader_app_1
```
This command updates the database.
