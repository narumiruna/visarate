# visarate

## Installation

```sh
pip install visarate
```


## Usage

```python
from visarate import rates

r = rates(amount=1, from_curr='TWD', to_curr='USD', fee=0.0)

print(f'converted amount: {r.convertedAmount}')
```
