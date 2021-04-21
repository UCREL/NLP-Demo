## makefile

A good tutorial on [makefiles](https://makefiletutorial.com/)

The [./makefile](./makefile) has 3 main variables:

1. `APP_NAME` -- this is used to determine the name of the folder that the website should be written to within this directory. By default this is `nlp_demo`. If you are running `create_app` for the first time the directory that the `APP_NAME` points to should not exist.
2. `USER_ID` -- this is the id of your user name on your home computer. This is required so that docker can write to files on your computer as you rather than as a random user. **This may need changing if you are on windows, but for Mac and Linux users this is automatically done for you through the `id -u` command.**
3. `GROUP_ID` -- similar to `USER_ID` but the group id of your user name on your home computer.

The [./makefile](./makefile) has 4 commands, all of which use docker via the services provided in the [docker compose file](./docker_compose.yaml):

1. `create_app` -- This creates the React frontend application, in essence it creates the [./nlp_demo](./nlp_demo) folder and the original website files that have been extended upon. Command: `make create_app`. **NOTE** this never needs to be ran as the web application is now complete. If you run this command you would ideally delete the `nlp_demo` folder and then run this command.
2. `run_app` -- This runs the react server locally at [http://localhost:3000/](http://localhost:3000/), allowing you to debug the code, the server on refresh will include your new code changes/updates. Command: `make run_app`. For more details on the script that runs the react server see [https://create-react-app.dev/docs/available-scripts#npm-start](https://create-react-app.dev/docs/available-scripts#npm-start).
3. `build_app` -- This bundles the website code ready for deployment/production and saves it to the [./nlp_demo/build folder](./nlp_demo/build). Command: `make build_app`. For more details on the script that bundles the website code see [https://create-react-app.dev/docs/available-scripts#npm-run-build](https://create-react-app.dev/docs/available-scripts#npm-run-build).
4. `interact_app` -- This is a way of interacting with the docker container that has been used to create, run, and build the react website. This in affect allows you to run commands like `npm` that will affect the website. For example if you would like to install a new `npm` package you can do so like so: `make interact_app cmd="npm install --save bootstrap"`, this would install the bootstrap npm package to this website project. The `cmd` argument is where you add your command that you want the docker container to run.