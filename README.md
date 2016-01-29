# Company checker
A simple Python script for matching Australian company names to political donations and government contractors.

The script will optionally match against political donations, government contractors and the ASIC company register depending on the input options supplied.

## Usage

```
usage: company-check.py [-h] [--donors DONORS] [--contractors CONTRACTORS]
                        [--register REGISTER] [--threshold THRESHOLD]
                        input output
```

### Example
Assuming you have a donors file in the appropriate format (see below), the following will match company names in the first column of the input CSV with companies in the donors register and store the result in `output.csv`.

You should be able to run this example straight from the cloned repo.

```
./company-check.py input.csv output.csv --donors donors.json
```

## Requirements
You need Python, with a bunch of requirements installed.

```
pip install -r requirements.txt
```

## Donors file
The can be downloaded from the [Morph.io API](https://morph.io/documentation/api?scraper=nickjevershed%2Faec_party):

```
https://api.morph.io/nickjevershed/aec_party/data.json?key=[GetYourOwnAPIKey]&query=select%20cleanName%2C%20SUM(value)%20from%20data%20group%20by%20cleanName
```

Short demo file included.

Could almost certainly be executed in a more optimised and coherent fashion.
