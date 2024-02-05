import json
from datetime import datetime
from datetime import timedelta

import cloudscraper
from loguru import logger
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer
from retry.api import retry_call


class OriginalValues(BaseModel):
    from_currency: str = Field(validation_alias="fromCurrency")
    from_currency_name: str = Field(validation_alias="fromCurrencyName")
    to_currency: str = Field(validation_alias="toCurrency")
    to_currency_name: str = Field(validation_alias="toCurrencyName")
    as_of_date: int = Field(validation_alias="asOfDate")
    from_amount: str = Field(validation_alias="fromAmount")
    to_amount_with_visa_rate: str = Field(validation_alias="toAmountWithVisaRate")
    to_amount_with_additional_fee: str = Field(validation_alias="toAmountWithAdditionalFee")
    fx_rate_visa: str = Field(validation_alias="fxRateVisa")
    fx_rate_with_additional_fee: str = Field(validation_alias="fxRateWithAdditionalFee")
    last_updated_visa_rate: int = Field(validation_alias="lastUpdatedVisaRate")
    benchmarks: list = Field(validation_alias="benchmarks")


class RateResponse(BaseModel):
    original_values: OriginalValues = Field(validation_alias="originalValues")
    conversion_amount_value: str = Field(validation_alias="conversionAmountValue")
    conversion_bank_fee: str = Field(validation_alias="conversionBankFee")
    conversion_input_date: str = Field(validation_alias="conversionInputDate")
    conversion_from_currency: str = Field(validation_alias="conversionFromCurrency")
    conversion_to_currency: str = Field(validation_alias="conversionToCurrency")
    from_currency_name: str = Field(validation_alias="fromCurrencyName")
    to_currency_name: str = Field(validation_alias="toCurrencyName")
    converted_amount: str = Field(validation_alias="convertedAmount")
    bench_mark_amount: str = Field(validation_alias="benchMarkAmount")
    fx_rate_with_additional_fee: str = Field(validation_alias="fxRateWithAdditionalFee")
    reverse_amount: str = Field(validation_alias="reverseAmount")
    disclaimer_date: str = Field(validation_alias="disclaimerDate")
    status: str = Field(validation_alias="status")


class RateRequest(BaseModel):
    amount: float
    from_curr: str = Field(serialization_alias="fromCurr")
    to_curr: str = Field(serialization_alias="toCurr")
    fee: float = Field(default=0.0)
    utc_converted_date: datetime = Field(default_factory=datetime.utcnow, serialization_alias="utcConvertedDate")
    exchangedate: datetime = Field(default_factory=datetime.utcnow, serialization_alias="exchangedate")

    @field_serializer("exchangedate", "utc_converted_date")
    def validate_date(self, d: datetime) -> str:
        return d.strftime("%m/%d/%Y")

    def do(self) -> RateResponse:
        url = "http://www.visa.com.tw/cmsapi/fx/rates"

        scraper = cloudscraper.create_scraper()

        resp = scraper.get(url=url, params=self.model_dump(by_alias=True))

        return RateResponse(**resp.json())


def _rates(
    amount: float = 1.0,
    from_curr: str = "TWD",
    to_curr: str = "USD",
    fee: float = 0.0,
    date: datetime = None,
) -> RateResponse:
    url = "http://www.visa.com.tw/cmsapi/fx/rates"

    if date is None:
        date = datetime.now()

    params = {
        "amount": amount,
        "utcConvertedDate": date.strftime("%m/%d/%Y"),
        "exchangedate": date.strftime("%m/%d/%Y"),
        "fromCurr": from_curr,
        "toCurr": to_curr,
        "fee": fee,
    }

    scraper = cloudscraper.create_scraper()

    resp = scraper.get(url=url, params=params)

    return RateResponse.model_validate(resp.json())


def query_rate(
    amount: float = 1.0,
    from_curr: str = "TWD",
    to_curr: str = "USD",
    fee: float = 0.0,
    date: datetime = None,
    tries: int = 100,
    delay: int = 1,
) -> RateResponse:
    if date is None:
        date = datetime.now()

    try:
        resp = retry_call(
            _rates,
            fkwargs={
                "amount": amount,
                "from_curr": from_curr,
                "to_curr": to_curr,
                "fee": fee,
                "date": date,
            },
            tries=tries,
            delay=delay,
        )
    except json.decoder.JSONDecodeError as e:
        logger.error(e)
        resp = retry_call(
            _rates,
            fkwargs={
                "amount": amount,
                "from_curr": from_curr,
                "to_curr": to_curr,
                "fee": fee,
                "date": date - timedelta(days=1),
            },
            tries=tries,
            delay=delay,
        )

    return resp
