# liberprimus-tool

**liberprimus-tool** is a Python library/program to decrypt the Liber Primus
from the 2014 Cicada 3301 puzzle.

## Requirements

* Python 3
* virtualenv

## Running

To decrypt pages with known solutions:

```bash
$ ./scripts/setup-db.sh # Create database with DDL specified in db/sql/ddl.sql
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ./main.py <args here>
```

### Genetic Algorithm

```bash
(venv) $ ./main.py --ga
```

### Known Solutions

```bash
(venv) $ ./main.py
```

## Design

See [DESIGN.md](./DESIGN.md)
