# Testing

Tests are written by [extending the `TestCase` class](https://docs.python.org/3.7/library/unittest.html#unittest.TestCase) from the `unittest` module in the Python standard library.  All tests can be found in the [`tests`](./tests) directory.

## Docker

All tests can be run using the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" test-all
```

To run just the unit tests (with code coverage), run the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" green -vvv --run-coverage
```

## Anaconda

```bash
source activate clu-phontools
# execute the following command from the project root:
green -vvv .
```


# Typehints

The code makes use of Python type hints.


## Docker

To perform type checking, run the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" mypy --ignore-missing-imports --follow-imports=skip --strict-optional .
```

## Anaconda

```bash
source activate clu-phontools
# execute the following command from the project root:
mypy --ignore-missing-imports --follow-imports=skip --strict-optional .
```
