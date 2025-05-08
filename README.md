# Database-Server-Project

Below are the 6 operations for the assignment and databases that they will touch:

1. Upload a post (Relational, Time Series, Object)
2. List all posts by most recent (Relational, Time series)
3. Get details of the post (Relational, Object)
4. Delete a post (Relational, Time Series, Object)
5. Edit a post (relational, object)
6. Upvote a post (relational, time series)

# Docker Setup
1. Install Docker desktop
2. Add the `.env` file to `.\GitHub\Database-Server-Project\`
3. Then, run `docker compose up -d` to start the databases
4. run `docker compose down` when finished with databases

# Installing Python Libraries
To interact with the 3 databases, 3 python packages will be needed.
1. In a terminal, run `pip install azure-storage-blob azure-identity` to install the Azure packages.
2. Run `pip install influxdb-client` to install the InfluxDB package.
3. Run `pip install mysql-connector-python` to install the package for MariaDB.

# Testing the 6 operations
Running the main.py file should demonstrate all 6 operations outlined above.