FROM python:3.8

LABEL author="Gus Hahn-Powell"
LABEL description="Image defintion for Python-based clu-phontools project."

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

RUN chmod u+x scripts/* && \
    mv scripts/* /usr/local/bin/ && \
    rmdir scripts

# Update
RUN apt -y update && \
    apt -y upgrade

# Install python dependencies
RUN pip install -U pip

# Dot and graphviz
RUN apt install -y graphviz && \
    pip install graphviz

# Jupyter deps
RUN pip install -U jupyter==1.0.0 jupyter-contrib-nbextensions==0.5.1 && \
    jupyter contrib nbextension install --user
# Commonly used test utils
RUN pip install -U pytest==5.3.4
# Assignment-specific deps
RUN pip install -e ".[dev]"

# Launch jupyter
CMD ["/bin/bash", "launch-notebook"]
