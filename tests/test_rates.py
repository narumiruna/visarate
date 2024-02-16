from visarate.rate import query_rate


def test_query_rate():
    cases = [
        [1.0, "TWD", "USD", 0.015],
        [1_000.0, "TWD", "USD", 0.015],
        [1_000_000.0, "TWD", "USD", 0.015],
        [1.0, "USD", "TWD", 0.015],
        [1_000.0, "USD", "TWD", 0.015],
        [1_000_000.0, "USD", "TWD", 0.015],
    ]
    for amount, from_curr, to_curr, fee in cases:
        resp = query_rate(amount=amount, from_curr=from_curr, to_curr=to_curr, fee=fee)
        assert resp.original_values.from_amount == amount
        assert resp.original_values.from_currency == to_curr
        assert resp.original_values.to_currency == from_curr
        assert resp.conversion_amount_value == amount
        assert resp.conversion_from_currency == from_curr
        assert resp.conversion_to_currency == to_curr
        assert resp.conversion_bank_fee == fee
