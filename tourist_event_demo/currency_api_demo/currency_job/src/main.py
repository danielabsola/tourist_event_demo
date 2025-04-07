# main.py
import logging
import os
import argparse
from datetime import datetime
from typing import List, Optional

from currencyAPI import CurrencyAPI
from db.operations import DatabaseOperations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description='Currency Exchange Rate ETL')
    parser.add_argument('--setup-db', action='store_true', help='Setup database procedures')
    parser.add_argument('--start-date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, help='End date in YYYY-MM-DD format') 
    parser.add_argument('--source', type=str, default='USD', help='Source currency code')
    parser.add_argument('--currencies', type=str, nargs='+', help='List of target currencies')
    parser.add_argument('--historical-date', type=str, help='Historical date in YYYY-MM-DD format')
    return parser.parse_args()

def initialize_services():
    """Initialize API and database services"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        logger.error("API_KEY environment variable not set")
        raise ValueError("API_KEY environment variable is required")

    return CurrencyAPI(api_key=api_key), DatabaseOperations()

def setup_database(db: DatabaseOperations):
    """Setup database procedures"""
    logger.info("Setting up database procedures...")
    db.setup_database()
    logger.info("Database setup completed")

def fetch_currency_list(api: CurrencyAPI, db: DatabaseOperations):
    """Fetch and save currency list"""
    logger.info("Fetching currency list...")
    currencies_data = api.list_currencies()
    db.save_raw_currency_list(currencies_data)
    logger.info("Currency list saved to raw layer")

def process_timeframe_data(api: CurrencyAPI, db: DatabaseOperations, args):
    """Process timeframe data"""
    if args.start_date is None:
        raise ValueError("start_date cannot be None")
    if args.end_date is None:
        raise ValueError("end_date cannot be None")
    logger.info(f"Fetching timeframe data from {args.start_date} to {args.end_date}")
    timeframe_data = api.get_timeframe(
        start_date=args.start_date,
        end_date=args.end_date,
        source=args.source,
        currencies=args.currencies
    )
    db.save_raw_historical_rates(
        date=args.start_date,
        source_currency=args.source,
        data=timeframe_data
    )
    logger.info("Timeframe data saved to raw layer")

def process_historical_data(api: CurrencyAPI, db: DatabaseOperations, args):
    """Process historical data"""
    logger.info(f"Fetching historical rates for {args.historical_date}")
    historical_data = api.get_historical_rates(
        date=args.historical_date,
        source=args.source,
        currencies=args.currencies
    )
    db.save_raw_historical_rates(
        date=args.historical_date,
        source_currency=args.source,
        data=historical_data
    )
    logger.info("Historical rates saved to raw layer")

def process_live_rates(api: CurrencyAPI, db: DatabaseOperations, args):
    """Process live rates"""
    logger.info("Fetching live rates")
    live_rates = api.get_live_rates(
        source=args.source,
        currencies=args.currencies
    )
    db.save_raw_live_rates(
        source_currency=args.source,
        data=live_rates
    )
    logger.info("Live rates saved to raw layer")

def main():
    args = parse_args()
    
    try:
        # Initialize services
        api, db = initialize_services()

        # Setup database if requested
        if args.setup_db:
            setup_database(db)
            return

        # Fetch and save currency list
        fetch_currency_list(api, db)
        
        # Process data based on arguments
        if args.start_date and args.end_date:
            process_timeframe_data(api, db, args)
            
        if args.historical_date:
            process_historical_data(api, db, args)
            
        if not any([args.start_date, args.end_date, args.historical_date]):
            process_live_rates(api, db, args)

        # Process through layers
        # Process data through raw -> staging -> final layers
        # First processes raw data into staging tables using process_raw_to_staging() procedure
        # Then processes staging data into final tables using process_staging_to_final() procedure
        for layer_pair in [('raw', 'staging'), ('staging', 'final')]:
            layer_from, layer_to = layer_pair
            logger.info(f"Processing data through {layer_from} to {layer_to} layer")
            db.process_layer_to_layer(layer_from=layer_from, layer_to=layer_to)
            logger.info("Data processing completed")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    logger.info("Starting currency ETL job")
    main()
    logger.info("Currency ETL job completed")