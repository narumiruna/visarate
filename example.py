from rich import print

from visarate import query_rate


def main() -> None:
    resp = query_rate(
        base_currency="USD",
        quote_currency="TWD",
    )
    print(resp)


if __name__ == "__main__":
    main()
