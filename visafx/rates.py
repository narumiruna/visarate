import json
from datetime import datetime
from datetime import timedelta

import cloudscraper
from pydantic import BaseModel
from retry import retry


class OriginalValues(BaseModel):
    fromCurrency: str
    fromCurrencyName: str
    toCurrency: str
    toCurrencyName: str
    asOfDate: int
    fromAmount: str
    toAmountWithVisaRate: str
    toAmountWithAdditionalFee: str
    fxRateVisa: str
    fxRateWithAdditionalFee: str
    lastUpdatedVisaRate: int
    benchmarks: list


class Response(BaseModel):
    originalValues: OriginalValues
    conversionAmountValue: str
    conversionBankFee: str
    conversionInputDate: str
    conversionFromCurrency: str
    conversionToCurrency: str
    fromCurrencyName: str
    toCurrencyName: str
    convertedAmount: str
    benchMarkAmount: str
    fxRateWithAdditionalFee: str
    reverseAmount: str
    disclaimerDate: str
    status: str


@retry()
def rates(amount: float = 1.0,
          from_curr: str = 'TWD',
          to_curr: str = 'USD',
          fee: float = 0.0,
          date: datetime = None) -> Response:
    url = 'http://www.visa.com.tw/cmsapi/fx/rates'

    if date is None:
        date = datetime.now()

    params = dict(
        amount=amount,
        utcConvertedDate=date.strftime('%m/%d/%Y'),
        exchangedate=date.strftime('%m/%d/%Y'),
        fromCurr=from_curr,
        toCurr=to_curr,
        fee=fee,
    )

    scraper = cloudscraper.create_scraper()

    resp = scraper.get(url=url, params=params)

    try:
        response = Response.parse_obj(resp.json())
    except json.decoder.JSONDecodeError:
        yesterday = date - timedelta(days=1)
        params = dict(
            amount=amount,
            utcConvertedDate=yesterday.strftime('%m/%d/%Y'),
            exchangedate=yesterday.strftime('%m/%d/%Y'),
            fromCurr=from_curr,
            toCurr=to_curr,
            fee=fee,
        )
        resp = scraper.get(url=url, params=params)
        response = Response.parse_obj(resp.json())

    return response
