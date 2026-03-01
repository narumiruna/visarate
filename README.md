# visarate

## Installation

```sh
pip install visarate
```


## Usage

```python
import visarate

r = visarate.query(amount=1, from_curr='TWD', to_curr='USD', fee=0.0)

print(f'converted amount: {r.converted_amount}')
```
