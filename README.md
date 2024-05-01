# liberprimus-tool

**liberprimus-tool** is a Python library/program to decrypt the Liber Primus
from the 2014 Cicada 3301 puzzle.

## Requirements

* Python 3
* virtualenv

## Running

```bash
$ docker-compose up -d
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ./main.py <args here>
```

```
usage: main.py [-h] [--pages PAGES [PAGES ...]] [--lines LINES [LINES ...]] [--segments SEGMENTS [SEGMENTS ...]] [--paragraphs PARAGRAPHS [PARAGRAPHS ...]]
               [--clauses CLAUSES [CLAUSES ...]] [--words WORDS [WORDS ...]] [--runes | --no-runes] [--ga | --no-ga]

Options for Liber Primus Tool

options:
  -h, --help            show this help message and exit
  --pages PAGES [PAGES ...]
  --lines LINES [LINES ...]
  --segments SEGMENTS [SEGMENTS ...]
  --paragraphs PARAGRAPHS [PARAGRAPHS ...]
  --clauses CLAUSES [CLAUSES ...]
  --words WORDS [WORDS ...]
  --runes, --no-runes
  --ga, --no-ga
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
