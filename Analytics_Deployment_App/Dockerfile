FROM python:3.7
EXPOSE 8501
WORKDIR /Analytics_Deployment_App
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run streamlit_app.py
# The following command is only for the purpose of building and deploying a Docker container 
# to a Heroku app running streamlit.
# CMD streamlit run --server.port $PORT streamlit_app.py