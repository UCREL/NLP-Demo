# Word Cloud Statistics

**Note** All of the following code has been written and tested on a linux based operating system, it may work on a windows based operating system with some changes.

Given the newly exported texts that are stored in the `../export_directory`, here they shall be processed using the [USAS tagger](http://ucrel.lancs.ac.uk/usas/), via the [USAS Python API](https://ucrel.github.io/ucrel-python-api/api.html#UCREL_API.usas), to create token and USAS tag statistics that can be used in a word cloud generator. The token and tag statistics are the output of the [./token_tag_statistics.py](./token_tag_statistics.py) script, of which the sections below describe that script in great detail.

By running the bash script below it runs the docker compose script that will generate the token and tag statistics to the files at the following environment variables `$TOKEN_STATISTICS_FILE` and `$TAG_STATISTICS_FILE` respectively, these environment variables are explained next.

``` bash
bash build_and_run_docker.sh
```

If successful you should see this line within the log output:

``` bash
word_cloud_statistics_python_1 exited with code 0
```

The `build_and_run_docker` script creates the following environment variables:

1. `DOCKER_EXPORT_DIRECTORY`: that is used to define where the directory that is storing the exported text versions of the theses. By default this is `$PWD/../export_directory`.
2. `TOKEN_STATISTICS_FILE`: File that will store the token statistics too. By default this is `$PWD/../thesis_token_statistics.json`.
3. `TAG_STATISTICS_FILE`: File that will store the tag statistics too. By default this is `$PWD/../thesis_usas_tag_statistics.json`.
4. `USAS_CACHE_DIRECTORY`: Directory that will store the USAS tag data for each thesis for caching purposes. This directory can be deleted afterwards, but can come in useful if you want to try different pre-processing methods that are specified through the optional commands that are passed to the [./token_tag_statistics.py](./token_tag_statistics.py) python script, once deleted if you run the `build_and_run_docker` script again it will process the text data through USAS again. By default this is `$PWD/usas_cache_directory`.

For full details on the docker compose file see the [docker compose script section below](#docker-compose-script). 

## Docker compose script

The docker compose file, [./docker-compose.yaml](./docker-compose.yaml), performs the following steps:

1. Runs the [./token_tag_statistics.py](./token_tag_statistics.py) python script with all of the position/required arguments specified using the environment variables defined in the `build_and_run_docker` script. The positional arguments passed to the python script are defined in the `command` argument within the docker compose script. This python script is ran in a custom Python docker container, code in [./Dockerfile](./Dockerfile), this container runs as the current user on the host machine e.g. your home/server machine. To run as your home/server machine the [./build_and_run_docker.sh](./build_and_run_docker.sh) script exports your user and group id to the python docker container. If you are running a non linux/mac OS then you may need to modify this script so that it correctly exports your user and group id. The reason it needs to run as you is so that the file permissions when writing to USAS cache directory, token and tag statistics files on your machine are correct e.g. the files are written to the USAS cache directory as you. 

Further when running the python container the [./docker-compose.yaml](./docker-compose.yaml) states the optional arguments to pass to the [./token_tag_statistics.py](./token_tag_statistics.py) python script through the `command` argument on line 20 of [./docker-compose.yaml](./docker-compose.yaml). For more details on the [./token_tag_statistics.py](./token_tag_statistics.py) python script see the [Token Tag Statistics script section below.](#token-tag-statistics)

## Token Tag Statistics

### Arguments

The [./token_tag_statistics.py](./token_tag_statistics.py) script takes many arguments of which all are explained when you run:

``` bash
python token_tag_statistics.py --help
```

### Output

The [./token_tag_statistics.py](./token_tag_statistics.py) script generates two JSON files one for the tokens and the other for the USAS tags. Each of these JSON files contains the following information for each token/tag:

1. `Log Likelihood` example value: `1279.54`
2. `Log Ratio` example value: `1.46` 
3. `Frequency` example value: `3456`
4. `Relative Frequency (%)` example value: `0.5`

The token file contains the following additional information:

1. `Common associated USAS tags (%)` example value: `[["The Media: Books", 84.25760286225402], ["People - m", 7.8711985688729875]]`

This additional information can be just an empty array e.g. `[]` when the token has had no USAS tag associated with it ever in the given texts. When it does contain a value it will have up to 2 entries and each entry is a USAS tag and the percentage of times that USAS tag occurs with that token in the given texts.

### Example

The following example of running the script would first perform the following pre-processing steps on the texts within the `../export_directory`, this will be called the target corpus:

**Note** USAS is ran before any pre-processing.

1. Lower case all tokens.
2. Remove all punctuation tokens.
3. Remove all tokens that have a determiner POS tag e.g.
4. Remove all stop word tokens.
5. Remove all digit like tokens. e.g. `1` and `one`

After which all of the remaining target tokens and target USAS tags are compared to the reference token and tag lists, which in this case are stored in `./BncSampWr.wrd.fql` and `./BncSampWr.sem.fql` respectively, only token and tags that are significantly more likely to occur in the target corpus are kept. These tokens and tags are then written to the `./thesis_tokens.json` and `./thesis_tags.json` JSON files in the format specified in the [output section above](#output).

The `--USAS-tags-to-labels` flag means that all of the USAS tags written to the output files, `./thesis_tokens.json` and `./thesis_tags.json`, will be the USAS label rather than the tag e.g. the USAS tag `T` has the label `Time`. The tags to labels comes from the 8th argument to the script, which in this case is `./semtags_subcategories_utf_8.txt`

To perform the statistical significance comparison of the target to reference corpus the `./sigeff/sigeff` tool is used which requires the `./semtags_subcategories_utf_8.txt` file. The `./sigeff/sigeff` tool is the compiled C program from the [UCREL/SigEff repository](https://github.com/UCREL/SigEff), follow the README on how to compile the C program. The `./semtags_subcategories_utf_8.txt` file can be found at the following [link](http://ucrel.lancs.ac.uk/usas/semtags_subcategories.txt) **Note** the file at that link is in `ISO-8859-1` encoding the script requires it to be in `UTF-8`.

``` bash
python token_tag_statistics.py ../export_directory/ ./usas_cache_directory ./thesis_tokens.json ./thesis_tags.json ./BncSampWr.wrd.fql ./BncSampWr.sem.fql ./sigeff/sigeff ./semtags_subcategories_utf_8.txt --remove-punctuation --remove-determiners --remove-stop-words --remove-digits --lower-case --USAS-tags-to-labels
```