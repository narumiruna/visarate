from __future__ import annotations

import logging
from datetime import UTC
from datetime import datetime
from decimal import Decimal
from typing import Self

from curl_cffi import requests as curl_requests
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer
from pydantic import field_validator
from pydantic import model_validator

logger = logging.getLogger(__name__)


class OriginalValues(BaseModel):
    from_currency: str = Field(validation_alias="fromCurrency")
    from_currency_name: str = Field(validation_alias="fromCurrencyName")
    to_currency: str = Field(validation_alias="toCurrency")
    to_currency_name: str = Field(validation_alias="toCurrencyName")
    as_of_date: datetime = Field(validation_alias="asOfDate")
    from_amount: Decimal = Field(validation_alias="fromAmount")
    to_amount_with_visa_rate: Decimal = Field(validation_alias="toAmountWithVisaRate")
    to_amount_with_additional_fee: Decimal = Field(validation_alias="toAmountWithAdditionalFee")
    fx_rate_visa: Decimal = Field(validation_alias="fxRateVisa")
    fx_rate_with_additional_fee: Decimal = Field(validation_alias="fxRateWithAdditionalFee")
    last_updated_visa_rate: datetime = Field(validation_alias="lastUpdatedVisaRate")
    benchmarks: list = Field(validation_alias="benchmarks")

    @field_validator("as_of_date", "last_updated_visa_rate", mode="before")
    @classmethod
    def convert_timestamp(cls, v: int | datetime) -> datetime:
        if isinstance(v, int):
            return datetime.fromtimestamp(v, tz=UTC)
        return v

    @field_validator(
        "from_amount",
        "to_amount_with_visa_rate",
        "to_amount_with_additional_fee",
        "fx_rate_visa",
        "fx_rate_with_additional_fee",
        mode="before",
    )
    @classmethod
    def convert_str(cls, v: str) -> Decimal:
        if isinstance(v, str):
            return Decimal(v.replace(",", ""))
        return v


class RateResponse(BaseModel):
    original_values: OriginalValues = Field(validation_alias="originalValues")
    conversion_amount_value: Decimal = Field(validation_alias="conversionAmountValue")
    conversion_bank_fee: Decimal = Field(validation_alias="conversionBankFee")
    conversion_input_date: datetime = Field(validation_alias="conversionInputDate")
    conversion_from_currency: str = Field(validation_alias="conversionFromCurrency")
    conversion_to_currency: str = Field(validation_alias="conversionToCurrency")
    from_currency_name: str = Field(validation_alias="fromCurrencyName")
    to_currency_name: str = Field(validation_alias="toCurrencyName")
    converted_amount: Decimal = Field(validation_alias="convertedAmount")
    bench_mark_amount: str = Field(validation_alias="benchMarkAmount")
    fx_rate_with_additional_fee: Decimal = Field(validation_alias="fxRateWithAdditionalFee")
    reverse_amount: Decimal = Field(validation_alias="reverseAmount")
    disclaimer_date: datetime = Field(validation_alias="disclaimerDate")
    status: str = Field(validation_alias="status")

    @field_validator("conversion_input_date", mode="before")
    @classmethod
    def parse_conversion_input_date(cls, v: str | datetime) -> datetime:
        if isinstance(v, str):
            return datetime.strptime(v, "%m/%d/%Y").replace(tzinfo=UTC)
        return v

    @field_validator("disclaimer_date", mode="before")
    @classmethod
    def parse_disclaimer_date(cls, v: str | datetime) -> datetime:
        if isinstance(v, str):
            return datetime.strptime(v, "%B %d, %Y").replace(tzinfo=UTC)
        return v

    @field_validator(
        "conversion_amount_value",
        "conversion_bank_fee",
        "converted_amount",
        "fx_rate_with_additional_fee",
        "reverse_amount",
        mode="before",
    )
    @classmethod
    def convert_str(cls, v: str) -> Decimal:
        if isinstance(v, str):
            return Decimal(v.replace(",", ""))
        return v


class RateRequest(BaseModel):
    amount: float
    from_curr: str = Field(serialization_alias="fromCurr")
    to_curr: str = Field(serialization_alias="toCurr")
    fee: float = Field(default=0.0)
    exchangedate: datetime = Field(default=datetime.now(tz=UTC), serialization_alias="exchangedate")
    utc_converted_date: datetime | None = Field(default=None, serialization_alias="utcConvertedDate")

    @field_serializer("exchangedate", "utc_converted_date")
    def validate_date(self, d: datetime) -> str:
        return d.strftime("%m/%d/%Y")

    @model_validator(mode="after")
    def set_utc_converted_date(self) -> Self:
        if self.utc_converted_date is None:
            self.utc_converted_date = self.exchangedate.astimezone(UTC)
        return self

    def do(self) -> RateResponse:
        url = "https://www.visa.com.tw/cmsapi/fx/rates"

        params = self.model_dump(by_alias=True)
        logger.debug("Request Parameters: %s", params)

        resp = curl_requests.get(
            url=url,
            params=params,
            impersonate="chrome",
            timeout=20,
        )
        logger.debug("Request URL: %s", resp.url)

        resp.raise_for_status()

        data = resp.json()
        logger.debug("Response Data: %s", data)

        return RateResponse.model_validate(data)
