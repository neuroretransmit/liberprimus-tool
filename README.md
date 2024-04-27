# liberprimus-tool

**liberprimus-tool** is a Python library/program to decrypt the Liber Primus
from the 2014 Cicada 3301 puzzle.

## Requirements

* Python 3
* virtualenv

## Running

To decrypt pages with known solutions:

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
(venv) $ 
(venv) $ ./main.py
```

## Usage

```python
from gematria import ATBASH, RUNE_LOOKUP, direct_translation, rot, vigenere
# etc
```
