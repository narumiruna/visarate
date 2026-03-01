from datetime import datetime
from zoneinfo import ZoneInfo

from rich import print

from visarate import query_rate
from visarate.api import RateRequest


def main() -> None:
    # https://usa.visa.com/support/consumer/travel-support/exchange-rate-calculator.html

    req = RateRequest(
        amount=100,  # Amount you paid
        from_curr="TWD",
        to_curr="USD",
        fee=2,  # 2% fee
        exchangedate=datetime.now(tz=ZoneInfo("Asia/Taipei")),  # Transaction date
    )
    resp = req.do()
    print(resp)

    rate = query_rate(
        base_currency="USD",
        quote_currency="TWD",
    )
    print(rate)


if __name__ == "__main__":
    main()
