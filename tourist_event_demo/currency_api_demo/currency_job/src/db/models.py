# src/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, Numeric, JSON, Date, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# RAW LAYER
class RawCurrencyList(Base):
    __tablename__ = 'raw_currency_list'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    raw_data = Column(JSON) 
    status = Column(String(50))

class RawLiveRates(Base):
    __tablename__ = 'raw_live_rates'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    source_currency = Column(String(5))
    raw_data = Column(JSON)  
    status = Column(String(50))

class RawHistoricalRates(Base):
    __tablename__ = 'raw_historical_rates'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    date = Column(Date)
    source_currency = Column(String(5))
    raw_data = Column(JSON)  
    status = Column(String(50))

# STAGING LAYER
class StagingCurrencies(Base):
    __tablename__ = 'stg_currencies'
    id = Column(Integer, primary_key=True)
    currency_code = Column(String(3), unique=True)
    currency_name = Column(String(100))
    processed_at = Column(DateTime)
    source_id = Column(Integer, ForeignKey('raw_currency_list.id'))

class StagingRates(Base):
    __tablename__ = 'stg_rates'
    id = Column(Integer, primary_key=True)
    rate_date = Column(DateTime)
    source_currency = Column(String(5))
    target_currency = Column(String(5))
    rate = Column(Numeric(20,6))
    is_live = Column(Boolean, default=True)
    processed_at = Column(DateTime)
    source_id = Column(Integer)  # References either raw_live or raw_historical

# FINAL LAYER
class Currencies(Base):
    __tablename__ = 'currencies'
    currency_code = Column(String(5), primary_key=True)
    currency_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime)

class ExchangeRates(Base):
    __tablename__ = 'exchange_rates'
    id = Column(Integer, primary_key=True)
    rate_date = Column(DateTime)
    source_currency = Column(String(5), ForeignKey('currencies.currency_code'))
    target_currency = Column(String(5), ForeignKey('currencies.currency_code'))
    rate = Column(Numeric(20,6))
    is_live = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Unique constraint for no duplicates
    __table_args__ = (
        UniqueConstraint('rate_date', 'source_currency', 'target_currency'),
    )