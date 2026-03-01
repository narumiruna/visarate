import pytest

from visarate.rate import query_rate


@pytest.mark.parametrize(
    "amount, quote_currency, base_currency, fee",
    [
        [1.0, "TWD", "USD", 0.015],
        [1_000_000.0, "TWD", "USD", 0.015],
        [1.0, "USD", "TWD", 0.015],
        [1_000_000.0, "USD", "TWD", 0.015],
    ],
)
def test_query_rate(amount: float, quote_currency: str, base_currency: str, fee: float) -> None:
    resp = query_rate(amount=amount, quote_currency=quote_currency, base_currency=base_currency, fee=fee)
    assert resp.base_currency == base_currency
    assert resp.quote_currency == quote_currency
    assert resp.rate > 0
    assert resp.updated_at.tzinfo is not None
