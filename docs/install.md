# Installation

`clu-phontools` can be run one of two ways:

1. Local installation of [Python library (>= v3.8)](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Using [Docker](https://docs.docker.com/get-docker/)

## Python

### Requirements
- [Python (>= v3.8)](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)


### Install
To install directly from the default branch of the repository:

```bash
pip install git+https://github.com/clu-ling/clu-phontools.git
```

<!-- !!! note "Not published to the pypi registry"
    `clu-phontools` is not currently published to [PyPi](https://pypi.org/) -->

## Docker

### Requirements
- [Docker](https://docs.docker.com/get-docker/)

### Install
Docker images are periodically published to [DockerHub](https://hub.docker.com/r/parsertongue/clu-phontools):

```bash
docker pull "parsertongue/clu-phontools:latest"
```
