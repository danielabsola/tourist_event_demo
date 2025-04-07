import requests
from typing import Optional, Dict, Union, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CurrencyAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"apikey": self.api_key}
        self.base_url = "https://api.apilayer.com/currency_data"
        logger.info("CurrencyAPI client initialized")
        logger.debug("Base URL set to: %s", self.base_url)

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Helper method to make API requests with error handling"""
        try:
            logger.debug("Making request to endpoint: %s with params: %s", endpoint, 
                        {k:v for k,v in (params or {}).items() if k not in ['apikey']})
            
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()  # Raises exception for 4XX/5XX status codes
            
            data = response.json()
            if not data.get("success"):
                logger.error("API request failed: %s", data.get('error', 'Unknown error'))
                raise Exception(f"API Error: {data.get('error', 'Unknown error')}")
            
            logger.info("Successfully retrieved data from %s endpoint", endpoint)
            return data
            
        except requests.exceptions.HTTPError as http_err:
            logger.error("HTTP error occurred: %s", http_err)
            raise Exception(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logger.error("Connection error occurred: %s", conn_err)
            raise Exception(f"Error connecting to server: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logger.error("Request timed out: %s", timeout_err)
            raise Exception(f"Request timed out: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error("Request exception occurred: %s", req_err)
            raise Exception(f"An error occurred while fetching data: {req_err}")

    def list_currencies(self) -> Dict[str, str]:
        """Returns all available currencies."""
        logger.info("Retrieving list of available currencies")
        response = self._make_request("list")
        logger.debug("Retrieved %d currencies", len(response["currencies"]))
        return response["currencies"]

    def get_live_rates(self, 
                      source: Optional[str] = None, 
                      currencies: Optional[List[str]] = None) -> Dict:
        """
        Get the most recent exchange rate data.
        
        Args:
            source: Base currency (default: USD)
            currencies: List of target currencies (optional)
        """
        logger.info("Retrieving live rates. Source: %s", source or "USD")
        if currencies:
            logger.debug("Target currencies: %s", currencies)
        
        params = {}
        if source:
            params["source"] = source
        if currencies:
            params["currencies"] = ",".join(currencies)
            
        return self._make_request("live", params)

    def convert_currency(self,
                        from_currency: str,
                        to_currency: str,
                        amount: float,
                        date: Optional[str] = None) -> Dict:
        """
        Convert one currency to another.
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            amount: Amount to convert
            date: Optional date for historical conversion (YYYY-MM-DD)
        """
        logger.info("Converting %f from %s to %s", amount, from_currency, to_currency)
        if date:
            logger.debug("Using historical date: %s", date)
            
        params = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        }
        if date:
            params["date"] = date
            
        return self._make_request("convert", params)

    def get_historical_rates(self,
                           date: str,
                           source: Optional[str] = None,
                           currencies: Optional[List[str]] = None) -> Dict:
        """
        Get historical rates for a specific day.
        
        Args:
            date: Date in YYYY-MM-DD format
            source: Base currency (default: USD)
            currencies: List of target currencies (optional)
        """
        logger.info("Retrieving historical rates for date: %s", date)
        logger.debug("Source currency: %s, Target currencies: %s", 
                    source or "USD", currencies or "all")
        
        params = {
            "date": date
        }
        if source:
            params["source"] = source
        if currencies:
            params["currencies"] = ",".join(currencies)
            
        return self._make_request("historical", params)

    def get_timeframe(self,
                     start_date: str,
                     end_date: str,
                     source: Optional[str] = None,
                     currencies: Optional[List[str]] = None) -> Dict:
        """
        Request exchange rates for a specific period of time.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            source: Base currency (default: USD)
            currencies: List of target currencies (optional)
        """
        logger.info("Retrieving rates for timeframe %s to %s", start_date, end_date)
        logger.debug("Source currency: %s, Target currencies: %s",
                    source or "USD", currencies or "all")
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        if source:
            params["source"] = source
        if currencies:
            params["currencies"] = ",".join(currencies)
            
        return self._make_request("timeframe", params)

    def get_change(self,
                  start_date: str,
                  end_date: str,
                  source: Optional[str] = None,
                  currencies: Optional[List[str]] = None) -> Dict:
        """
        Request any currency's change parameters (margin, percentage).
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            source: Base currency (default: USD)
            currencies: List of target currencies (optional)
        """
        logger.info("Retrieving currency changes from %s to %s", start_date, end_date)
        logger.debug("Source currency: %s, Target currencies: %s",
                    source or "USD", currencies or "all")
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        if source:
            params["source"] = source
        if currencies:
            params["currencies"] = ",".join(currencies)
            
        return self._make_request("change", params)