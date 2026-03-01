from rich import print

from visarate import query_rate


def main() -> None:
    resp = query_rate(amount=1, from_curr="TWD", to_curr="USD", fee=0.0)
    print(resp)
    resp = query_rate(amount=1, from_curr="USD", to_curr="TWD", fee=0.0)
    print(resp)


if __name__ == "__main__":
    main()
