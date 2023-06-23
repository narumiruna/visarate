# visafx

## Installation

```sh
pip install visafx
```


## Usage

```python
from visafx import rates

r = rates(amount=1, from_curr='TWD', to_curr='USD', fee=0.0)

print(f'converted amount: {r.convertedAmount}')
```
