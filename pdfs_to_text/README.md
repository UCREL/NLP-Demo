# PDFs to Text

**Note** All of the following code has been written and tested on a linux based operating system, it may work on a windows based operating system with some changes.

To extract the text data from the theses stored in the thesis folder, `../thesis_directory/`, to the export directory, `../export_directory`, run the following bash script which will run the docker-compose file [./docker-compose.yaml](./docker-compose.yaml):

``` bash
bash build_and_run_docker.sh
```

If successful you should see this line near the end of the log output:

``` bash
pdfs_to_text_python_1 exited with code 0
```

For full details on the docker compose file see the [docker compose script section below](#docker-compose-script). 

For details on the data that is logged see the [logged data sub-section of Extract text from thesis script section below.](#logged-data)

If you would like to remove the images that were created using docker run:

``` bash
docker rmi nlp_demo_pdf_to_text_python:0.0.1
docker rmi ucrel/ucrel-science-parse:3.0.1
```

## Docker Compose Script

The docker compose file, [./docker-compose.yaml](./docker-compose.yaml), performs the following steps:

1. Starts the Science Parse server. This server is not visible outside of docker as [./extract_text_from_thesis.py](./extract_text_from_thesis.py) is the only script that needs to use it of which this is also ran inside the same docker network. The science parse server uses in total 6GB of Memory and 2 CPUs, this can be changed by changing the environment variables in [./.env](./.env).
2. Wait for the Science Parse server to start.
3. Run the [./extract_text_from_thesis.py](./extract_text_from_thesis.py) using a separate Python docker container but within the same docker network as the Science Parse server. This python docker container, is a custom container, code in [./Dockerfile](./Dockerfile), this container runs as the current user on the host machine e.g. your home/server machine. To run as your home/server machine the [./build_and_run_docker.sh](./build_and_run_docker.sh) script exports your user and group id to the python docker container. If you are running a non linux/mac OS then you may need to modify this script so that it correctly exports your user and group id. The reason it needs to run as you is so that the file permissions when writing to export directory on your machine are correct e.g. the files are written to the export directory as you.

Further when running the python container the [./docker-compose.yaml](./docker-compose.yaml) states the arguments to pass to the [./extract_text_from_thesis.py](./extract_text_from_thesis.py) python script through the `command` argument on line 20 of [./docker-compose.yaml](./docker-compose.yaml). For more details on the [./extract_text_from_thesis.py](./extract_text_from_thesis.py) python script see the [Extract text from thesis script section below.](#extract-text-from-thesis-script)

## Extract text from thesis script

When running this script ensure that you are running the Science Parse server locally at the following address: `127.0.0.1:8080`, we suggest doing this through the following [docker image.](https://hub.docker.com/r/ucrel/ucrel-science-parse)

The [./extract_text_from_thesis.py](./extract_text_from_thesis.py) has various optional flags:

1. **--science-parse-server-url** -- This allows a user to choose a different URL for the science parse server.
2. **--science-parse-server-port** -- This allows a user to choose a different port for the science parse server.
3. **--debug** -- Instead of exporting the data it will give you various dataset statistics for the given thesis directory. See the `debug` function in [./extract_text_from_thesis.py](./extract_text_from_thesis.py).
4. **--min-number-words** -- The minimum number of words, based on whitespace, that a thesis has to contain to be exported into the export directory. This is here so that a thesis that may not have been parsed correctly by Science Parse is not exported. **default** is 1000.
5. **--replace** -- Replace/overwrite data that already exists in the export directory. **By default** if an export file already exists then it does not overwrite it.

### Pre-Processing

When extracting text various pre-processing steps are performed so that text that is likely to come from the following sections are removed:

1. Table of contents.
2. List of tables (like table of contents).
3. List of figures (like table of contents).
4. Acknowledgements. 
5. Declaration of originality. 
6. Bibliography/References. 
7. Any Appendix sections.

This pre-processing is never going to be perfect, so some mistakes maybe made.

### Logged data

The following is logged after running the script:

1. Number of files that were not PDFs in the thesis directory.
2. Number of PDF files that could not be parsed by the Science Parse server.
3. Number of PDF files that Science Parse could not extract any text from.
4. Number of PDF files that contain less than the minimum number of words/tokens.
5. Total number of files in the thesis directory.
6. Number of files replaced in the export directory.
7. Number of files exported to the export directory.

**Note** it will also log all the PDF file names that are not PDF's (point 1 above), failed to parse (point 2), failed to extract text from (point 3), or failed to meet the minimum number of words threshold (point 4).