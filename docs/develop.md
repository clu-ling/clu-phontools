## Develop


### Option 1: Anaconda
`clu-phontools` is written for **Python >= v3.8**.

```bash
conda create --name clu-phontools python=3.8 ipython
source activate clu-phontools
# execute the following command from the project root.
pip install -e ".[dev]"
```

`[dev]` will include dependencies for running tests and generating the documentation.



For those familiar with Docker, another option is to use a container with bind mounts as a development environment.  Note that the instructions below assume you're developing using a Linux-based environment (they've also been tested on MacOS Catalina).

## Option 2: Docker

First, you'll need to build the docker image:

```bash
docker build -f Dockerfile -t "parsertongue/clu-phontools:latest" .
```

Launch a container using this image and connect to it:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest /bin/bash"
```

Thanks to the bind mount, changes made to files locally (i.e., outside of the container) will be reflected inside the running container.  The `parsertongue/clu-phontools` includes Jupyter and iPython:

```bash
ipython
```

```python
from clu.phontools import ReAline

realigner = ReAline()
```

### Running the example notebooks

Jupyter is configured to run on port 9999, so you'll need a port mapping to access the notebook server:

```bash
docker run --rm -it \
  -p 7777:9999 \
  parsertongue/clu-phontools:latest
```

Open [localhost:7777](http://localhost:7777) and navigate to `notebooks` to view the notebooks.

## Removing old docker containers, images, etc.

If you want to save some space on your machine by removing images and containers you're no longer using, [see the instructions here](https://docs.docker.com/config/pruning/).  As always, use caution when deleting things.


## Testing

Tests are written by [extending the `TestCase` class](https://docs.python.org/3.7/library/unittest.html#unittest.TestCase) from the `unittest` module in the Python standard library.  All tests can be found in the [`tests`](./tests) directory.


All tests can be run using the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" test-all
```

To run just the unit tests (with code coverage), run the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" green -vvv --run-coverage
```


The code makes use of Python type hints.  To perform type checking, run the following command:

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" mypy --ignore-missing-imports --follow-imports=skip --strict-optional .
```

### Formatting and style
Code can be auto-formatted using [`black`](https://black.readthedocs.io/en/stable/):

```bash
docker run -it -v $PWD:/app "parsertongue/clu-phontools:latest" black
```
