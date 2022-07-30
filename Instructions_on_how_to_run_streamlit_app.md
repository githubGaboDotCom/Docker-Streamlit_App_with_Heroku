# Instructions and Settings to Deploy Docker Container with Streamlit App.

## Repository Contents:
- Sanahuano_G folder contains a source code, HTML file, and ipynb file with the Pyspark code used to perform computations on the data. 
- Analytics_Deployment_App folder contains all the files needed to run the strealit app through a Docker container.
- Challenge markdown file with instructions about this final project.
- README markdown file with my final summary report. This report will be uploaded in canvas as well.

## Intructions on how to run the Strealit App on the browser:
1. Fork this repository, and clone it into your computer.
2. Make sure you have docker installed and running on your computer.
3. Make sure you have docker added to your environmental variables and that you're able to run Docker commands on the terminal. Also, open up your docker desktop app.
4. On your terminal navigate to your repository folder, and then 'cd' to the Analytics_Deployment_App folder.
5. We have created a docker-compose.yml file for an easy docker deployment to your computer. Go ahead and run the following command <code>docker-compose up -d</code> on your terminal and from inside the Analytics_Deployment_App folder. That command will build a docker container with the streamlit app and it will automatically execute the app in the container.
6. Then go to your web browser and type <code>http://localhost:8501/</code> This will display our Streamlit app on the web browser.

### Additional Step:
Sometimes the configurations on your computer won't be correctly set up, and if that's the case you might run into some issues to execute the docker-compose.yml file. If that's the case, don't worry, there's an additional way to build the docker container and run it manually. Below are the instructions on how do it:
1. Follow the all the previos steps until step 4 has been completed.
2. Instead of following step 5, go ahead and run the following commands <code>docker build -f Dockerfile -t app:latest .</code> and then <code>docker run -p 8501:8501 app:latest</code> on your terminal and from inside the Analytics_Deployment_App folder. The first command builds a new container with the streamlit app in it, and the second one will run the docker container.
3. As a final step, go to your web browser and type <code>http://localhost:8501/</code> This will display our Streamlit app on the web browser.

**We have deployed our Streamlit app to Heroku. If you want to check it, go ahead and visit the following URL:** <br>

* https://polar-springs-15307.herokuapp.com/
