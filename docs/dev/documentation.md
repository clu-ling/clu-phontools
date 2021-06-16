# Documentation

## API documentation

We use [`pdoc`](https://github.com/pdoc3/pdoc) to generate our API documentation. To develop with live reloading, use the following command:

!!! note "LaTeX math in docstrings"
    To use LaTeX-style equations, we recommend using [raw strings](https://docs.python.org/3.8/reference/lexical_analysis.html) for docstrings:

```python
r"""My docstring

Thanks to the r prefix, we can write math without needing to escape \:

$$\sum_{i=1}^{\vert X \vert} x_{i}$$
"""
```

### Docker

```bash
# execute the following command from the project root:
docker run --rm -it -v $PWD:/app \
  -p 8001:8001 \
  parsertongue/clu-phontools:latest \
  pdoc --html -c latex_math=True --force --output-dir docs/api --http 0.0.0.0:8001 clu
```

Open your browser to [localhost:8001/clu/phontools](localhost:8001/clu/phontools) to see live updates.

### Anaconda

```bash
source activate clu-phontools
# execute the following command from the project root:
pdoc --html -c latex_math=True --force --output-dir docs/api --http 0.0.0.0:8001 clu
```

Open your browser to [localhost:8001/clu/phontools](localhost:8001/clu/phontools) to see live updates.

## General documentation

We use `mkdocs` to generate our site documentation from markdown.  Markdown source files are located udner the `docs` directory.

### Docker

```bash
# execute the following command from the project root:
docker run --rm -it -v $PWD:/app \
  -p 8000:8000 \
  parsertongue/clu-phontools:latest \
  mkdocs serve -a 0.0.0.0:8000
```

Open your browser to [localhost:8000](localhost:8000) to see live updates.

### Anaconda

To develop the documentation with live reloading, run the following command:

```bash
source activate clu-phontools
# execute the following command from the project root:
mkdocs serve -a 0.0.0.0:8000
```

Open your browser to [localhost:8000](localhost:8000) to see live updates.
