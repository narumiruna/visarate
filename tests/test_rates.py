from visarate.rate import query_rate


def test_rates():
    amount = 1.0
    from_curr = "TWD"
    to_curr = "USD"
    resp = query_rate(amount=amount, from_curr=from_curr, to_curr=to_curr, fee=0.0)
    assert resp.original_values.from_amount == str(amount)
    assert resp.original_values.from_currency == to_curr
    assert resp.original_values.to_currency == from_curr
    assert resp.conversion_amount_value == str(amount)
    assert resp.conversion_from_currency == from_curr
    assert resp.conversion_to_currency == to_curr
