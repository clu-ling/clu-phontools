# REALINE

## Develop

We recommend developing using Docker and bind mounts.  Note that the instructions below assume you're developing using a Linux-based environment (they've also been tested on MacOS Catalina).
## Building the docker image

```
docker build -f Dockerfile -t "parsertongue/re-aline:latest" .
```

## Running the example notebooks

### Option 2

```
docker run --rm -it \
  -p 7777:9999 \
  parsertongue/re-aline:latest 
```

Open [localhost:7777](http://localhost:7777) and navigate to `notebooks` to view the notebooks.


## Test

Tests are written by [extending the `TestCase` class](https://docs.python.org/3.7/library/unittest.html#unittest.TestCase) from the `unittest` module in the Python standard library.  All tests can be found in the [`tests`](./tests) directory.


All tests can be run using the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/re-aline:latest" test-all
```

To run just the unit tests, run the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/re-aline:latest" green -vvv --run-coverage
```


The code makes use of Python type hints.  To perform type checking, run the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/re-aline:latest" mypy --ignore-missing-imports --follow-imports=skip --strict-optional .
```

## Removing old docker containers, images, etc.

If you want to save some space on your machine by removing images and containers you're no longer using, [see the instructions here](https://docs.docker.com/config/pruning/).  As always, use caution when deleting things.

