Auto Paper Fetch
================

Supported conference
* NeurIPS2021 (initial accepted paper list), Updated Date: 11/02/2021

Usage:
```
usage: paper_fetcher.py [-h] [--download] keyword

Automatically search and download papers from conference.

positional arguments:
  keyword     download pdf files if available on ArXiv.

optional arguments:
  -h, --help  show this help message and exit
  --download  download pdf files if available on ArXiv.
```

Example: Search for keyword `federated`:
```shell
python paper_fetcher.py federated --download
```

----------
Author: Junyuan Hong
