import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, List

from .models import (
    Base, RawCurrencyList, RawLiveRates, RawHistoricalRates,
    StagingCurrencies, StagingRates)

logger = logging.getLogger(__name__)

class DatabaseOperations:
    def __init__(self):
        # Get database connection details from environment variables
        db_params = {
            'database': os.getenv('POSTGRES_DB', 'exchange_rates'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'password'),
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
        }
        
        self.engine = create_engine(
            f"postgresql://{db_params['user']}:{db_params['password']}@"
            f"{db_params['host']}:{db_params['port']}/{db_params['database']}"
        )

    def _read_sql_file(self, filename: str) -> str:
        """Read SQL file content"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(current_dir, 'sql', 'procedures', filename)
        with open(sql_path, 'r') as file:
            return file.read()

    def execute_database_object(self, procedure_name: str):
        """Create/Replace & Execute database scripts receiving the procedure name"""
        try:
            with self.engine.begin() as conn:  # Automatically handles commit/rollback insteadw USE self.engine.connect() as conn:
                # First create/replace the procedure
                logger.info(f"Creating/replacing procedure: {procedure_name}")
                sp_sql = self._read_sql_file(f'{procedure_name}.sql')
                conn.execute(text(sp_sql))
            
                # Then execute it
                logger.info(f"Executing procedure: {procedure_name}")
                conn.execute(text(f"CALL {procedure_name}()"))
            
                # No commit needed here as it's handled in the procedure
                logger.info(f"Successfully executed procedure: {procedure_name}")
        except SQLAlchemyError as e:
            logger.error(f"Error creating stored procedures: {str(e)}")
            raise
    
    def process_layer_to_layer(self, layer_from: str, layer_to: str):
        """
        Process data from source layer (raw or staging) tables to layer (staging or final) tables using stored procedures.
        """
        try:
            self.execute_database_object(f'process_{layer_from}_to_{layer_to}')
            logger.info(f"Successfully processed {layer_from} data to {layer_to} tables")
        except SQLAlchemyError as e:
            logger.error(f"Error processing {layer_from} to {layer_to} tables: {str(e)}")
            raise

    def setup_database(self):
        """Setup database procedures - can be called separately when needed"""
        Base.metadata.create_all(self.engine)

    def save_raw_currency_list(self, data: Dict[str, Any]) -> None:
        """Save raw currency list data"""
        try:
            with Session(self.engine) as session:
                raw_record = RawCurrencyList(
                    timestamp=datetime.now(),
                    raw_data=data,
                    status='success'
                )
                session.add(raw_record)
                session.commit()
                logger.info("Successfully saved raw currency list data")
        except SQLAlchemyError as e:
            logger.error(f"Error saving raw currency list: {str(e)}")
            raise

    def save_raw_live_rates(self, source_currency: str, data: Dict[str, Any]) -> None:
        """Save raw live rates data"""
        try:
            with Session(self.engine) as session:
                raw_record = RawLiveRates(
                    timestamp=datetime.now(),
                    source_currency=source_currency,
                    raw_data=data,
                    status='success'
                )
                session.add(raw_record)
                session.commit()
                logger.info("Successfully saved raw live rates data")
        except SQLAlchemyError as e:
            logger.error(f"Error saving raw live rates: {str(e)}")
            raise

    # src/db/operations.py

def save_raw_historical_rates(self, date: str, source_currency: str, data: Dict[str, Any]) -> None:
    """Save raw historical rates data"""
    try:
        with Session(self.engine) as session:
            raw_record = RawHistoricalRates(
                timestamp=datetime.now(),
                date=datetime.strptime(date, '%Y-%m-%d').date(),
                source_currency=source_currency,
                raw_data=data,
                status='success'
            )
            session.add(raw_record)
            session.commit()
            logger.info("Successfully saved raw historical rates data")
    except SQLAlchemyError as e:
        logger.error(f"Error saving raw historical rates: {str(e)}")
        raise

def save_staging_currencies(self, currency_data: List[Dict[str, Any]]) -> None:
    """Save staging currencies data"""
    try:
        with Session(self.engine) as session:
            for data in currency_data:
                stg_record = StagingCurrencies(
                    currency_code=data['code'],
                    currency_name=data['name'],
                    processed_at=datetime.now()
                )
                session.merge(stg_record)
            session.commit()
            logger.info("Successfully saved staging currencies data")
    except SQLAlchemyError as e:
        logger.error(f"Error saving staging currencies: {str(e)}")
        raise

def save_staging_rates(self, rates_data: List[Dict[str, Any]]) -> None:
    """Save staging rates data"""
    try:
        with Session(self.engine) as session:
            for data in rates_data:
                stg_record = StagingRates(
                    rate_date=data['date'],
                    source_currency=data['source'],
                    target_currency=data['target'],
                    rate=data['rate'],
                    is_live=data.get('is_live', False),
                    processed_at=datetime.now(),
                    source_id=data.get('source_id')
                )
                session.merge(stg_record)
            session.commit()
            logger.info("Successfully saved staging rates data")
    except SQLAlchemyError as e:
        logger.error(f"Error saving staging rates: {str(e)}")
        raise