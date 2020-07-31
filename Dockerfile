FROM python:3.7

LABEL author="Gus Hahn-Powell"
LABEL description="Default container definition for jupyter-based demos."

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

RUN mv scripts/* /usr/local/bin/
RUN rmdir scripts

# Install python dependencies
RUN pip install -U pip
# Jupyter deps
RUN pip install -U jupyter==1.0.0
RUN pip install -U jupyter-contrib-nbextensions==0.5.1
RUN jupyter contrib nbextension install --user
# Commonly used test utils
RUN pip install -U pytest==5.3.4
# Assignment-specific deps
RUN pip install -r requirements.txt
# Launch jupyter
CMD ["/bin/bash", "/usr/local/bin/launch-notebook.sh"]
