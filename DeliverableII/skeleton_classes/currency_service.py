from .currency_rate import CurrencyRate

class CurrencyService:
    def getRate(self, homeCurrency: str, destCurrency: str) -> CurrencyRate:
        pass
