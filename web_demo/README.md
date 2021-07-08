## Generate semantic tagging example

Ensure that you have installed the required python requirements:

``` bash
pip install -r requirements.txt
```

If you want to use a different example change the example text that is within [./usas_example.txt](./usas_example.txt).

Run the following:

``` bash
bash generate_usas_example.sh
```

This will then output the relevant JSON to: [./nlp_demo/public/data/usas_example.json](./nlp_demo/public/data/usas_example.json).

If this file does not exist it will then generate the following message on the Semantic Tagging section of the website:

```
Error: Example document not in the correct location.
```

## To Enable caching of static files on the Apache web server

In general this should improve speeds as files are cached.

The following files in the [./nlp_demo/build/static](./nlp_demo/build/static) can be cached for a long time as different file names are generated if any of the content is changed, for more details on this see this [post](https://create-react-app.dev/docs/production-build#static-file-caching).

1. Ensure that the [headers module](https://httpd.apache.org/docs/current/mod/mod_headers.html) is enabled: `sudo a2enmod headers`
2. Add the following to the `apache2.conf`, which is typically found at `/etc/apache2/apache2.conf`, (this assumes that the NLP demo main `index.html` is at the following location on the web server `/srv/www/html/demo/index.html`):
``` bash
<Directory /srv/www/html/demo/static>
        Header set Cache-Control max-age=31536000
</Directory>
```
3. To activate this cache control you need to restart the apache web server like so: `sudo systemctl restart apache2`


## makefile

A good tutorial on [makefiles](https://makefiletutorial.com/)

The [./makefile](./makefile) has 3 main variables:

1. `APP_NAME` -- this is used to determine the name of the folder that the website should be written to within this directory. By default this is `nlp_demo`. If you are running `create_app` for the first time the directory that the `APP_NAME` points to should not exist.
2. `USER_ID` -- this is the id of your user name on your home computer. This is required so that docker can write to files on your computer as you rather than as a random user. **This may need changing if you are on windows, but for Mac and Linux users this is automatically done for you through the `id -u` command.**
3. `GROUP_ID` -- similar to `USER_ID` but the group id of your user name on your home computer.

The [./makefile](./makefile) has 5 commands, all of which use docker via the services provided in the [docker compose file](./docker_compose.yaml):

1. `create_app` -- This creates the React frontend application, in essence it creates the [./nlp_demo](./nlp_demo) folder and the original website files that have been extended upon. Command: `make create_app`. **NOTE** this never needs to be ran as the web application is now complete. If you run this command you would ideally delete the `nlp_demo` folder and then run this command.
2. `run_app` -- This runs the react server locally at [http://localhost:3000/](http://localhost:3000/), allowing you to debug the code, the server on refresh will include your new code changes/updates. Command: `make run_app`. For more details on the script that runs the react server see [https://create-react-app.dev/docs/available-scripts#npm-start](https://create-react-app.dev/docs/available-scripts#npm-start).
3. `build_app` -- This bundles the website code ready for deployment/production and saves it to the [./nlp_demo/build folder](./nlp_demo/build). Command: `make build_app`. For more details on the script that bundles the website code see [https://create-react-app.dev/docs/available-scripts#npm-run-build](https://create-react-app.dev/docs/available-scripts#npm-run-build).
4. `interact_app` -- This is a way of interacting with the docker container that has been used to create, run, and build the react website. This in affect allows you to run commands like `npm` that will affect the website. For example if you would like to install a new `npm` package you can do so like so: `make interact_app cmd="npm install --save bootstrap"`, this would install the bootstrap npm package to this website project. The `cmd` argument is where you add your command that you want the docker container to run. A full list of [npm commands.](https://docs.npmjs.com/cli/v7/commands)
5. `profile-and-server-app` -- This is a way of running the production version of the application. Compared to `run_app` this is running the version that will be used in production, the main difference here is run time optimisation, **there should be no difference in the content of the application just load/run time speeds of the application**. When you run this `make` command, like so `make profile-and-server-app`, it will run the application locally at [http://localhost:5000/](http://localhost:5000/). It will also run the production version of the application in `profile` mode, so that you can profile load/run time speeds using the [react profiler](https://reactjs.org/blog/2018/09/10/introducing-the-react-profiler.html), see this [post as well on the profiler](https://reactjs.org/docs/optimizing-performance.html), lastly the profiler is a browser extension e.g. here is a [link to the react dev tools extension for Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en).