# Analytics Deployment App - Final Project

## Final Report:

### Driving Needs

_Accomplishments:_

1. I have used the Chipotle data provided during the last challenge, as well as, Pyspark/Databricks to build a dataset for my dashboard.
2. I have provided a compelling story comparing same_day_brands and same_month_brands for Chipotle stores.      
3. I built a dataset that is easy to use in Pandas in my app.   
4. I displayed my final Pyspark code in one of the pages of my app and a description of the data format I used and why.      
5. I displayed a table of SafeGraph data that includes:
    - Filter option to see locations with more than X visits.   
    - Displaying the following columns - `placekey, location_name, street_address, city, date_range_start, latitude, longitude, raw_visit_counts` and the brands columns.   
6. I have provided multiple visualizations and tables to provide more insight about the analysis done to the brands columns. The following has been completed:
    - A spatial map that displays insight about related brands.   
    - Charts facilitating comparison of brands and insights about them.   
7. I created an additional interactive element to allow the user to investigate the visualizations. An option to filter the dataset by state has been provided. As soon as the dataset is filtered by specific state, a spacial map will also be updated to display the Chipotle stores located at that state.
8. An app built with streamlit has been created and incorporated in a Docker container, working as expected.
9. My streamlit app container has been pushed and released to Heroku cloud and it's now accesible on a web browser.
10. Assignment report file has been submitted on Canvas.

### Vocabulary/Lingo Challenge

**1. Link to project repository:** https://github.com/Gabrielandres/DS460_app_challenge_sp22_Sanahuano <br>
**2. Link to my published Heroku app:** https://polar-springs-15307.herokuapp.com/ <br>
**3. Explain the added value of using DataBricks in your Data Science process (using text, diagrams, and/or tables).** <br>
Databricks is an environment to build Data Science projects of large-scale. Specially, I learned a technology tool that allows me to discover more comfortably the Big Data Analysis world. The opportunity to learn in deep SQL functions to perform calculations and analysis on millions of records is of enormous scope. I am a Computer Scientist with a passion for programming, but throught this semester I developed an interest and love for the data analysis. I am sure I will keep learning more about this fascinating field along with Databricks and Pyspark, and I will look for more technologies that I still don't know about it. <br>
**4. Compare and contrast PySpark to either Pandas or the Tidyverse (using text, diagrams, and/or tables).** <br>
Pyspark is very similar to pandas from my perspective because they have same functionality, and in several ways they can do the same thing. There's a main difference though, Pyspark is much faster than pandas when it comes to handle massive amounts of records, this is what we called Big Data. In a world where we get millions of data records to be analysed by companies, we need the output and results as soon as possible because time is money. This is when we should prefer Pyspark over pandas, if handling Big Data. <br>
**5. Explain Docker to somebody intelligent but not a tech person (using text, diagrams, and/or tables).** <br>
Docker is a software that provides fast and easy deployment for all types of programs and apps. Docker provides you with a virtual container where you can store your files and additional software needed to make a program run. Once the container is built you can transfer it to any machine, regardless of their OS requirements, and run it to make a program work. If you needed to install an specific software to be able to run a program, you no longer need to install that specific software anymore because it's already stored in the Docker container, and once you run the docker container in another machine, automatically, will make whatever program is needed to work. <br>
**6. Detail the difference between statistical regression and machine learning regression (compare and contrast).** <br>
Machine Learning is about the accuracy you can make in your predictions, and statistics is more about finding the relationship that exists between variables.
