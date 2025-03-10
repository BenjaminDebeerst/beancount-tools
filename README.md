# Beancount Tools

A collection of personal tooling for using Beancount.

Contains:

* importer implementations for CSV downloads from GLS Bank, ING Bank and BPGO.
* a fairly simple regex-based categorizer to simplify posting recurring/known transactions to the appropriate accounts.

## Example config

It took me a while until I had a fully working Fava setup with Beancount v3 and beangulp importers and categorization. Given that the importer rewrite in beangulp is fairly new, documentation and working examples are a bit scattered and dated. I hope that this example will help some others figure this out more easily.

Executing `make` in the top level directory will install beancount and fava in a virtual env and start the example ledger and configuration. In fava, check out the _Import_ page and start some imports.

The example consists of:

* `sample.bc`, a minimal beancount ledger file with a few dummy accounts,
* In the `import` dir, three mock CSV files as they could be provided by the banks GLS Gemeinschaftsbank, ING and BPGO, ready to be detected and imported by fava,
  * Of note: the non-UTF-8 encoded CSV that ING unfortunately delivers but is handled by the importer implementation,
* `config.py`, a fava config setting up the importers and a categorizer.

The config shows how a simplistic match-regex-on-narration categorizer can be used for all importers at once.
