from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from curl_cffi.requests.exceptions import RequestException as CurlRequestException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

from visarate.api import RateRequest
from visarate.api import RateResponse

logger = logging.getLogger(__name__)


@dataclass
class Rate:
    base_currency: str
    quote_currency: str
    rate: float
    updated_at: datetime


def convert_to_rate(resp: RateResponse) -> Rate:
    return Rate(
        base_currency=resp.original_values.from_currency,
        quote_currency=resp.original_values.to_currency,
        rate=float(resp.original_values.fx_rate_visa),
        updated_at=resp.original_values.last_updated_visa_rate,
    )


@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(CurlRequestException),
    reraise=True,
)
def query_rate(
    amount: float = 1,
    base_currency: str = "USD",
    quote_currency: str = "TWD",
    fee: float = 0,
    date: datetime | None = None,
) -> Rate:
    if date is None:
        date = datetime.now(tz=UTC)

    req = RateRequest(
        amount=amount,
        from_curr=quote_currency,
        to_curr=base_currency,
        fee=fee,
        utc_converted_date=date,
        exchangedate=date,
    )

    try:
        resp = req.do()
    except CurlRequestException:
        logger.warning("Request failed, retrying with previous date...")

        req.utc_converted_date = date - timedelta(days=1)
        req.exchangedate = date - timedelta(days=1)

        resp = req.do()

    return convert_to_rate(resp)
