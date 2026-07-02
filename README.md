# kvitto — Dela noten enkelt

Ett enkelt **CLI-verktyg** för att dela på restaurangnoter med eller utan dricks.

Stödjer både **jämn delning** och **ojämn delning** där en person betalar en angiven procentandel av totalbeloppet.

## Installation

Kraven är Python 3.6+ och inga externa beroenden — bara standardbiblioteket.

```bash
# Klona repo
gh repo clone TandemAI/tandem-kvitto
cd kvitto
```

## Användning

### Jämn delning

Dela ett belopp jämnt mellan alla personer:

```bash
python main.py 1000 4 10
```

| Argument       | Beskrivning                          |
|----------------|--------------------------------------|
| `amount`       | Totalbelopp (t.ex. `1000`)           |
| `people`       | Antal personer (t.ex. `4`)           |
| `tip_percent`  | Dricksprocent (t.ex. `10`)           |

**Exempel:**

```
$ python main.py 1000 4 10
Totalbelopp med dricks: 1100.00
Varje person betalar: 275.00
```

### Ojämn delning (specialperson)

Låt en person betala en angiven procent av totalbeloppet:

```bash
python main.py 1000 4 10 --special-percent 50
```

**Exempel:**

```
$ python main.py 1000 4 10 --special-percent 50
Totalbelopp med dricks: 1100.00
Specialperson (50%): 550.00
Övriga 3 personer: 183.33 var
```

## Tester

Kör testerna med pytest:

```bash
python -m pytest test_logic.py -v
```

## Exempel på utdata

```
$ python main.py 2000 5 20 --special-percent 25
Totalbelopp med dricks: 2400.00
Specialperson (25%): 600.00
Övriga 4 personer: 450.00 var
```

## Projektstruktur

```
kvitto/
├── main.py          # CLI-ingångspunkt
├── logic.py         # Beräkningslogik
├── test_logic.py    # Testfall
└── README.md        # Denna fil
```

## Licens

MIT
