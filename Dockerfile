FROM python:3.7

LABEL author="Gus Hahn-Powell"
LABEL description="Image defintion for Python-based re-aline project."

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

RUN mv scripts/* /usr/local/bin/
RUN chmod u+x /usr/local/bin/test-all
RUN rmdir scripts

# Update
RUN apt -y update
RUN apt -y upgrade

# Install python dependencies
RUN pip install -U pip

# Dot and graphviz
RUN apt install -y graphviz
RUN pip install graphviz

# Jupyter deps
RUN pip install -U jupyter==1.0.0
RUN pip install -U jupyter-contrib-nbextensions==0.5.1
RUN jupyter contrib nbextension install --user
# Commonly used test utils
RUN pip install -U pytest==5.3.4
# Assignment-specific deps
RUN pip install -e ".[all]" .
# Launch jupyter
CMD ["/bin/bash", "/usr/local/bin/launch-notebook.sh"]