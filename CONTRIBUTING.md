# Contributing guidelines

## How to become a contributor and submit your own code

### Contribution guidelines and standards

Before sending your pull request for review, make sure your changes are consistent with the guidelines and follow the coding style

#### General guidelines and philosophy for contribution

* Include unit tests when you contribute new features, as they help to a) prove that your code works correctly, and b) guard against future breaking changes to lower the maintenance cost.
* Bug fixes also generally require unit tests, because the presence of bugs usually indicates insufficient test coverage.


#### Python coding style
Use `pylint` to check your Python changes. To install `pylint`:

```bash
pip install pylint
```

To check files with `pylint`:

```bash
pylint --rcfile=./.dev/pylintrc theconf/ tests/ bin/
```

Expected result:
```
No config file found, using default configuration

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

#### Running unit tests
Use `pytest` to check your Python changes. To install `pytest`:

```bash
pip install pytest pytest-cov
```

To check tests with `pytest`: 

```bash
py.test --cov=theconf tests
```
Expected result:

```
================================== test session starts ==================================
platform darwin -- Python 3.6.3, pytest-3.3.1, py-1.5.2, pluggy-0.6.0
rootdir: /Users/clint/workspace/deeplearning-template, inifile:
plugins: cov-2.5.1
collected 2 items

tests/test_sample.py ..                                                           [100%]

---------- coverage: platform darwin, python 3.6.3-final-0 -----------
Name                  Stmts   Miss  Cover
-----------------------------------------
modules/__init__.py       0      0   100%
modules/sample.py         7      0   100%
-----------------------------------------
TOTAL                     7      0   100%


=============================== 2 passed in 0.07 seconds ================================
```
