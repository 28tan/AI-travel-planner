import httpx
from typing import Optional, Dict

class CurrencyService:
    def __init__(self):
        self.api_url = "https://open.er-api.com/v6/latest"
        # Basic mapping, can be expanded
        self.country_currency_map = {
            "United States": "USD",
            "USA": "USD",
            "United Kingdom": "GBP",
            "UK": "GBP",
            "Japan": "JPY",
            "China": "CNY",
            "France": "EUR",
            "Germany": "EUR",
            "Italy": "EUR",
            "Spain": "EUR",
            "Australia": "AUD",
            "Canada": "CAD",
            "India": "INR",
            "Brazil": "BRL",
            "Mexico": "MXN",
            "Russia": "RUB",
            "South Korea": "KRW",
            "Singapore": "SGD",
            "Switzerland": "CHF",
            "Thailand": "THB",
            "Vietnam": "VND",
            "Indonesia": "IDR",
            "Malaysia": "MYR",
            "Philippines": "PHP",
            "Turkey": "TRY",
            "Egypt": "EGP",
            "South Africa": "ZAR",
            "Nigeria": "NGN",
            "Kenya": "KES",
            "Argentina": "ARS",
            "Chile": "CLP",
            "Colombia": "COP",
            "Peru": "PEN",
            "Saudi Arabia": "SAR",
            "United Arab Emirates": "AED",
            "Israel": "ILS",
            "Sweden": "SEK",
            "Norway": "NOK",
            "Denmark": "DKK",
            "Poland": "PLN",
            "New Zealand": "NZD"
        }

    def get_currency_code(self, country: str) -> str:
        if not country:
            return "USD"
        
        # Try exact match
        if country in self.country_currency_map:
            return self.country_currency_map[country]
        
        # Try partial match
        for c, code in self.country_currency_map.items():
            if c.lower() in country.lower():
                return code
        
        return "USD" # Default

    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> str:
        if from_currency == to_currency:
            return f"1 {from_currency} = 1 {to_currency}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.api_url}/{from_currency}")
                response.raise_for_status()
                data = response.json()
                
                if data["result"] == "success":
                    rates = data["rates"]
                    if to_currency in rates:
                        rate = rates[to_currency]
                        return f"1 {from_currency} = {rate} {to_currency}"
                
                return f"Could not fetch rate for {from_currency} to {to_currency}"
            except Exception as e:
                print(f"Currency API Error: {e}")
                return f"Rate unavailable ({from_currency} to {to_currency})"
