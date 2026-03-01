# visarate

## Installation

```sh
pip install visarate
```


## Usage

```python
from visarate import query_rate

r = query_rate(amount=1, from_curr='TWD', to_curr='USD', fee=0.0)

print(f'converted amount: {r.converted_amount}')
```
