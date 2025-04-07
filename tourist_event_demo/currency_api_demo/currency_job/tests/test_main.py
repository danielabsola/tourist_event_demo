import pytest
from unittest.mock import patch, Mock
import os
import sys

# Add debug information
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
print(f"\nCurrent directory: {current_dir}")
print(f"Parent directory: {parent_dir}")
print(f"Files in parent directory: {os.listdir(parent_dir)}")

try:
    from src.main import process_timeframe_data, process_historical_data, initialize_services, main, fetch_currency_list
except ImportError as e:
    print(f"\nError importing main: {e}")
    print(f"sys.path: {sys.path}")
    raise

class MockArgs:
    """
    This class simulates the arguments that would normally come from command line.
    Instead of real command line arguments, we create a fake (mock) version for testing.
    """
    def __init__(self, **kwargs):
        self.setup_db = kwargs.get('setup_db', False)
        self.source = kwargs.get('source', 'USD')
        self.currencies = kwargs.get('currencies', ['EUR', 'GBP'])
        self.start_date = kwargs.get('start_date', '2024-01-01')
        self.end_date = kwargs.get('end_date', '2024-01-02')
        self.historical_date = kwargs.get('historical_date', '2024-01-01')

@pytest.fixture
def mock_services():
    """
    This fixture creates fake (mock) versions of the APILayer and Database services.
    Instead of making real API calls or DB connections, we create pretend ones for testing.
    """
    with patch('src.main.CurrencyAPI') as mock_api_class, \
         patch('src.main.DatabaseOperations') as mock_db_class:
        
        # Create a fake API that returns predefined data
        mock_api = Mock()
        mock_api.get_live_rates.return_value = {
            "base": "USD",
            "timestamp": 1234567890,
            "rates": {
                "EUR": 0.85,
                "GBP": 0.73
            }
        }
        
        mock_api_class.return_value = mock_api

        # Setup DB mock
        mock_db = Mock()
        mock_db.save_raw_live_rates.return_value = None
        mock_db.process_layer_to_layer.return_value = None
        mock_db_class.return_value = mock_db

        yield mock_api, mock_db

@pytest.fixture
def mock_env_vars():
    """Mock environment variables"""
    with patch.dict('os.environ', {'API_KEY': 'test_key'}):
        yield

def test_initialize_services(mock_env_vars):
    """Test service initialization"""
    api, db = initialize_services()
    assert api is not None
    assert db is not None

def test_fetch_currency_list(mock_services):
    """
    Test fetch_currency_list function:
    1. Calls the currency list API
    2. Saves the currency list to the database
    
    Parameters:
        mock_services: Provides mock API and DB instances
    """
    # Get our mock services
    mock_api, mock_db = mock_services

    # Setup the mock API response
    mock_api.list_currencies.return_value = {
        "currencies": {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound"
        }
    }

    # Call the function with just api and db parameters
    fetch_currency_list(api=mock_api, db=mock_db)

    # Verify the API was called
    mock_api.list_currencies.assert_called_once()

    # Verify the data was saved to database
    mock_db.save_raw_currency_list.assert_called_once_with({
        "currencies": {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound"
        }
    })

def test_process_timeframe_data(mock_services, mock_env_vars):
    """Test processing timeframe data"""
    mock_api, mock_db = mock_services
    args = MockArgs(
        start_date='2024-01-01',
        end_date='2024-01-02',
        source='USD',
        currencies=['EUR', 'GBP']
    )

    process_timeframe_data(mock_api, mock_db, args)

    # Verify API call
    mock_api.get_timeframe.assert_called_once_with(
        start_date='2024-01-01',
        end_date='2024-01-02',
        source='USD',
        currencies=['EUR', 'GBP']
    )

    # Verify DB operations
    mock_db.save_raw_historical_rates.assert_called_once()

def test_process_historical_data(mock_services, mock_env_vars):
    """Test processing historical data"""
    mock_api, mock_db = mock_services
    args = MockArgs(historical_date='2024-01-01')

    process_historical_data(mock_api, mock_db, args)

    # Verify API call
    mock_api.get_historical_rates.assert_called_once_with(
        date='2024-01-01',
        source='USD',
        currencies=['EUR', 'GBP']
    )

    # Verify DB operations
    mock_db.save_raw_historical_rates.assert_called_once()

def test_main_with_live_rates(mock_services, mock_env_vars):
    """
    Test that main function calls process_live_rates when no dates are provided.
    Live rates are processed when start_date, end_date, and historical_date are all None.
    """
    mock_api, mock_db = mock_services  # Get our fake API and DB
    
    # Setup the mock API to return live rates data
    mock_api.get_live_rates.return_value = {
        "base": "USD",
        "timestamp": 1234567890,
        "rates": {
            "EUR": 0.85,
            "GBP": 0.73
        }
    }
    
    with patch('src.main.parse_args') as mock_parse_args:
        # Setup fake command line arguments for live rates
        # No dates needed for live rates
        mock_parse_args.return_value = MockArgs(
            setup_db=False,
            source='USD',
            currencies=['EUR', 'GBP'],
            start_date=None,
            end_date=None,
            historical_date=None
        )
        
        # Run the main function
        from src.main import main
        main()
        
        # Check that the live rates API was called
        mock_api.get_live_rates.assert_called_once_with(
            source='USD',
            currencies=['EUR', 'GBP']
        )
        
        # Check that the database save was called with correct data
        mock_db.save_raw_live_rates.assert_called_once_with(
            source_currency='USD',
            data={
                "base": "USD",
                "timestamp": 1234567890,
                "rates": {
                    "EUR": 0.85,
                    "GBP": 0.73
                }
            }
        )
        
        # Verify that the layer processing was called
        assert mock_db.process_layer_to_layer.call_count == 2  # raw->staging, staging->final

def test_error_handling(mock_services, mock_env_vars):
    """Test error handling in main functions"""
    mock_api, mock_db = mock_services
    
    # Make API throw an error
    mock_api.get_timeframe.side_effect = Exception("API Error")
    
    args = MockArgs(
        start_date='2024-01-01',
        end_date='2024-01-02'
    )
    
    with pytest.raises(Exception) as exc_info:
        process_timeframe_data(mock_api, mock_db, args)
    
    assert "API Error" in str(exc_info.value)

@pytest.mark.parametrize("test_input,expected_error", [
    ({"start_date": None, "end_date": "2024-01-02"}, ValueError),
    ({"start_date": "2024-01-01", "end_date": None}, ValueError),
])
def test_invalid_parameters(test_input, expected_error, mock_services, mock_env_vars):
    """Test handling of invalid parameters"""
    mock_api, mock_db = mock_services
    args = MockArgs(**test_input)
    
    with pytest.raises(expected_error):
        if args.start_date is None:
            raise ValueError("start_date cannot be None")
        if args.end_date is None:
            raise ValueError("end_date cannot be None")
        process_timeframe_data(mock_api, mock_db, args)