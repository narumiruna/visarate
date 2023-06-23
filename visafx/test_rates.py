from .rates import rates


def test_rates():
    amount = 1.0
    from_curr = 'TWD'
    to_curr = 'USD'
    resp = rates(amount=amount, from_curr=from_curr, to_curr=to_curr, fee=0.0)
    assert resp.originalValues.fromAmount == str(amount)
    assert resp.originalValues.fromCurrency == to_curr
    assert resp.originalValues.toCurrency == from_curr
    assert resp.conversionAmountValue == str(amount)
    assert resp.conversionFromCurrency == from_curr
    assert resp.conversionToCurrency == to_curr
