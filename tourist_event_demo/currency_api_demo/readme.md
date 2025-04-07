
##########################################################################
                         Project structure
##########################################################################
currency_api_demo/
├── currency_job/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py 
│   │   ├── currencyAPI.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── operations.py
│   │       └── sql/
│   │           └── procedures/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_currency_api.py
│   │   └── test_db_operations.py
│   ├── dags/
│   │   ├── currency_update_dag.py
│   │   └── currency_process_dag.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│   ├── .env
│   └── .gitignore

##########################################################################
                         Docker commands
##########################################################################
# Build and start services
`docker-compose up -d --build`

# In case the image was already builed use this command to start the services
`docker-compose up -d`

# In case you need to stop existing containers
`docker-compose down`

# In case you need to remove old containers, images, and volumes (optional but recommended)
`docker system prune -a`

##########################################################################
                         Run Options
##########################################################################

# 1. Setup Database (creates tables and procedures)
`docker-compose run etl python src/main.py --setup-db`

# 2. Get Live Rates
`docker-compose run etl python src/main.py`
# 2.2 Get Live Rates with parameters
`docker-compose run etl python src/main.py --source USD --currencies EUR GBP JPY`

# 3. Get Historical Rates for specific date
`docker-compose run etl python src/main.py --historical-date 2024-01-01 --source USD --currencies EUR GBP`

# 4. Get Rates for a date range
`docker-compose run etl python src/main.py --start-date 2024-01-01 --end-date 2024-01-31 --source USD --currencies EUR GBP`

# 5. Examples with different source currencies
`docker-compose run etl python src/main.py --source EUR --currencies USD GBP JPY`
`docker-compose run etl python src/main.py --source GBP --currencies USD EUR JPY`

# 6. Multiple target currencies
`docker-compose run etl python src/main.py --source USD --currencies EUR GBP JPY CNY AUD NZD`

# 7. Historical data with multiple currencies
`docker-compose run etl python src/main.py --historical-date 2023-12-31 --source USD --currencies EUR GBP JPY CNY`

# 8. Date range with specific currencies
`docker-compose run etl python src/main.py --start-date 2023-01-01 --end-date 2023-12-31 --source USD --currencies EUR GBP`

##########################################################################
                         Parameter Descriptions
##########################################################################

--setup-db           : Initialize database tables and procedures
--source            : Base currency for rates (default: USD)
--currencies        : List of target currencies to fetch rates for
--historical-date   : Specific date for historical rates (YYYY-MM-DD)
--start-date        : Start date for date range (YYYY-MM-DD)
--end-date          : End date for date range (YYYY-MM-DD)

##########################################################################
                         Connect to the database
##########################################################################

# Connect to the database
`docker-compose exec postgres psql -U DANIELABSOLA -d FEVER`

# List all tables
`\dt`

 List of relations
 Schema |         Name         | Type  |    Owner     
--------+----------------------+-------+--------------
 public | currencies           | table | DANIELABSOLA
 public | exchange_rates       | table | DANIELABSOLA
 public | raw_currency_list    | table | DANIELABSOLA
 public | raw_historical_rates | table | DANIELABSOLA
 public | raw_live_rates       | table | DANIELABSOLA
 public | stg_currencies       | table | DANIELABSOLA
 public | stg_rates            | table | DANIELABSOLA
(7 rows)

# Check specific table structure
`docker-compose exec postgres psql -U DANIELABSOLA -d FEVER -c "\d raw_currency_list"`

# List all tables in the schema
"SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';"

# Check if specific table exists
"SELECT EXISTS (
   SELECT FROM information_schema.tables 
   WHERE table_schema = 'public' 
   AND table_name = 'raw_currency_list'
);"

# Count rows in tables
"SELECT 
    'raw_currency_list' as table_name, count(*) as row_count 
FROM raw_currency_list
UNION ALL
SELECT 
    'raw_live_rates', count(*) 
FROM raw_live_rates
UNION ALL
SELECT 
    'raw_historical_rates', count(*) 
FROM raw_historical_rates;"

# to test stored procedures manually
BEGIN;
SELECT COUNT(*) FROM raw_currency_list;
SELECT COUNT(*) FROM raw_live_rates;
CALL process_raw_to_staging();
SELECT COUNT(*) FROM stg_currencies;
SELECT COUNT(*) FROM stg_rates;
ROLLBACK;

# sql to check raw data
SELECT 
    rlr.source_currency,
    rate_data.key as target_currency,
    rate_data.value
FROM raw_live_rates rlr,
     jsonb_each(rlr.raw_data::jsonb) as rate_data
LIMIT 1;

# Exit the database
`\q`

##########################################################################
                         Log Commands
##########################################################################

# View logs from all services
`docker-compose logs`

# View logs from specific service
`docker-compose logs etl`
`docker-compose logs postgres`
`docker-compose logs airflow`

# Follow logs in real-time (like tail -f)
`docker-compose logs -f`
`docker-compose logs -f etl`
`docker-compose logs -f postgres`
`docker-compose logs -f airflow`

## Troubleshooting

If you encounter connection issues:
1. Ensure all services are running: `docker-compose ps`
2. Check logs for errors: `docker-compose logs`
3. Verify database connection: `docker-compose exec postgres pg_isready`
4. Restart services if needed: `docker-compose restart`

##########################################################################
                         Airflow Commands
##########################################################################
# Set AIRFLOW_HOME to a directory in your user space
export AIRFLOW_HOME=~/airflow
# Create directories
mkdir -p ~/airflow/dags
mkdir -p ~/airflow/src
# Copy DAGs and source code
cp -r dags/* ~/airflow/dags/
cp -r src/* ~/airflow/src/
# List the contents
ls -la ~/airflow/dags
ls -la ~/airflow/src
# Start Airflow
`docker-compose up airflow-init`
`docker-compose up airflow-webserver airflow-scheduler`

