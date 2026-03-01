from rich import print

from visarate import query_rate


def main() -> None:
    resp = query_rate(
        amount=1,
        quote_currency="TWD",  # quote currency
        base_currency="USD",  # base currency
        fee=0.0,
    )
    print(resp)

    resp = query_rate(
        amount=1,
        quote_currency="USD",
        base_currency="TWD",
        fee=0.0,
    )
    print(resp)


if __name__ == "__main__":
    main()
