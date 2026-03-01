from __future__ import annotations

import logging
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


@retry(
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(CurlRequestException),
    reraise=True,
)
def query(
    amount: float = 1,
    from_curr: str = "TWD",
    to_curr: str = "USD",
    fee: float = 0,
    date: datetime | None = None,
) -> RateResponse:
    if date is None:
        date = datetime.now(tz=UTC)

    req = RateRequest(
        amount=amount,
        from_curr=from_curr,
        to_curr=to_curr,
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

    return resp
