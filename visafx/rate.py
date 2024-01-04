import json
from datetime import datetime
from datetime import timedelta

import cloudscraper
from loguru import logger
from pydantic import BaseModel
from retry.api import retry_call


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


def _rates(amount: float = 1.0,
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

    return Response.parse_obj(resp.json())


def rates(amount: float = 1.0,
          from_curr: str = 'TWD',
          to_curr: str = 'USD',
          fee: float = 0.0,
          date: datetime = None) -> Response:
    if date is None:
        date = datetime.now()

    try:
        resp = retry_call(
            _rates,
            fkwargs=dict(
                amount=amount,
                from_curr=from_curr,
                to_curr=to_curr,
                fee=fee,
                date=date,
            ),
            tries=100,
            delay=1,
        )
    except json.decoder.JSONDecodeError as e:
        logger.error(e)
        resp = retry_call(
            _rates,
            fkwargs=dict(
                amount=amount,
                from_curr=from_curr,
                to_curr=to_curr,
                fee=fee,
                date=date - timedelta(days=1),
            ),
            tries=100,
            delay=1,
        )

    return resp
