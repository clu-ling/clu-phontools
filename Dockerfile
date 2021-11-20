FROM parsertongue/python:3.8

LABEL author="Gus Hahn-Powell"
LABEL description="Image definition for Python-based clu-phontools project."

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

RUN chmod u+x scripts/* && \
    mv scripts/* /usr/local/bin/ && \
    rmdir scripts

# Assignment-specific deps
RUN pip install -e ".[all]"

# Launch jupyter
EXPOSE 9999
#CMD ["/bin/bash", "launch-notebook"]
EXPOSE 8000
CMD ["clu-phontools-rest-api"]
