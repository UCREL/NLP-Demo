from python:3.7.10-slim
# This is required for chardet
ENV PATH="$PATH:/home/python/.local/bin"

ARG USER_ID
ARG GROUP_ID

RUN apt-get update && apt-get install -y \
    gcc
RUN groupadd --gid $GROUP_ID python && useradd -r --create-home -g $GROUP_ID --uid $USER_ID python
RUN mkdir -p /usr/src/myapp && \
    mkdir /usas_cache && \
    chown -R python:python /usr/src/myapp && \
    chown -R python:python /usas_cache
USER python

WORKDIR /usr/src/myapp
COPY --chown=python:python token_tag_statistics.py .
COPY --chown=python:python semtags_subcategories_utf_8.txt .
COPY --chown=python:python BncSampWr* ./
COPY --chown=python:python sigeff/sigeff.c .
RUN gcc -g -o sigeff sigeff.c -lm
COPY --chown=python:python requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "token_tag_statistics.py", "/usr/src/export_directory", "/usas_cache", "/usr/src/thesis_token_statistics.json", "/usr/src/thesis_usas_tag_statistics.json", "./BncSampWr.wrd.fql", "./BncSampWr.sem.fql", "./sigeff" , "./semtags_subcategories_utf_8.txt"]