import pytest

from visarate.api import RateRequest


@pytest.mark.parametrize(
    "amount, from_curr, to_curr, fee",
    [
        [1.0, "TWD", "USD", 0.015],
        [1_000_000.0, "TWD", "USD", 0.015],
        [1.0, "USD", "TWD", 0.015],
        [1_000_000.0, "USD", "TWD", 0.015],
    ],
)
def test_rate_request_do(amount: float, from_curr: str, to_curr: str, fee: float) -> None:
    req = RateRequest(
        amount=amount,
        from_curr=from_curr,
        to_curr=to_curr,
        fee=fee,
    )
    resp = req.do()
    assert float(resp.original_values.from_amount) == amount
    assert resp.original_values.from_currency == to_curr
    assert resp.original_values.to_currency == from_curr
    assert float(resp.conversion_amount_value) == amount
    assert resp.conversion_from_currency == from_curr
    assert resp.conversion_to_currency == to_curr
    assert float(resp.conversion_bank_fee) == fee
