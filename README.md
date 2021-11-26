# stackpathApp

Instructions:
1. i added to the app DB as redis and docker.
2. the controller file is the main code which run the app.
3. the program come with redis db so on the docker i added the link that needed to run the server.
4. I added requirements text files to make it easy to add the modules and install them by one command.
5. i used on OrderedDict on the date_data_object so i can sort the object by the key which is the datetime
6. i did an endpoint of clear all data because i had to test it few times with clean database.
7. i did a properties file to configurable all the details that need.
8. i had to create docker compose for redis. it's like two containers run separately, so i had to link redis to the server on the docker compose file.
9. i started the flask app in port 5000 and redis db in port 6000.
10. if you want to run the app without the docker, you must change on the config file the DB_HOST and DB_PORT. DB_HOST must be localhost and DB_PORT must be 6379 to run on local.
11. The rest api gets json data and returns a json response.
12. to get stats, you need to send a json request with json object. the type text is minute or hour:
    {
      "type":"minute"
    }
    
