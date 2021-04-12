from python:3.7.10-slim
# This is required for chardet
ENV PATH="$PATH:/home/python/.local/bin"

ARG USER_ID
ARG GROUP_ID

RUN groupadd --gid $GROUP_ID python && useradd -r --create-home -g $GROUP_ID --uid $USER_ID python
RUN mkdir -p /usr/src/myapp && \
    chown -R python:python /usr/src/myapp
USER python

WORKDIR /usr/src/myapp
COPY --chown=python:python extract_text_from_thesis.py .
COPY --chown=python:python wait_for_it.sh .
RUN chmod 764 wait_for_it.sh
COPY --chown=python:python requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT ["bash", "./wait_for_it.sh", "--host=science-parse", "--port=8080", "--timeout=120", "--strict", "--", "python", "extract_text_from_thesis.py"]