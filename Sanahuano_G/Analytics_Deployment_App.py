# Databricks notebook source
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from plotnine import *
import pandas as pd
from pyspark.sql.types import MapType, StringType, IntegerType
from pyspark.sql.functions import udf

dataset = spark.read.parquet("dbfs:/FileStore/dat/owhekdudn.parquet")

# COMMAND ----------

#Extract the columns needed for the analysis process of the brand columns.
app_dataset = dataset.select("placekey", "location_name", "street_address", "city", "region", "date_range_start", "latitude", "longitude", "raw_visit_counts", "related_same_day_brand", "related_same_month_brand")
display(app_dataset)

# COMMAND ----------

#create a row column with the number of the corresponding row. I will use this column further to perform operations in the data.
posexp_window_partition = Window.orderBy(F.lit('A'))
app_dataset = app_dataset.withColumn("row", F.row_number().over(posexp_window_partition))

#posexplode the same-day brand column to extract separately the percentage values of each brand and check who had the biggest percentage values
posexp_app_dataset = app_dataset.select("*", F.posexplode("related_same_day_brand"))

#filter the dataset to get the top 4 brands that got the highest values.
posexp_app_dataset = posexp_app_dataset.withColumn("pos", posexp_app_dataset.pos + 1).filter(posexp_app_dataset.pos <= 3)

#the rest of the code basically restores the posexploded data to the original map type and collected the top 4 brands into a column. The key of the map is the ranking number of the brand with a range bewteen 1 and 4

top4_app_dataset1 = posexp_app_dataset.withColumn("brands_same_day", F.create_map(F.col("key"), F.col("value"))).drop("key", "value")
top4_app_dataset = top4_app_dataset1.withColumn("pos", F.create_map(F.col("pos"), F.col("brands_same_day"))).drop("brands_same_day")

top4_app_dataset = top4_app_dataset.groupBy('row').agg(F.first('placekey').alias("placekey"), F.first('location_name').alias("location_name"), F.first('city').alias("city"), F.first('region').alias("region"), F.first('date_range_start').alias("date_range_start"), F.first('latitude').alias("latitude"), F.first('longitude').alias("longitude"), F.first('raw_visit_counts').alias("raw_visit_counts"), F.first('related_same_day_brand').alias("related_same_day_brand"), F.first('related_same_month_brand').alias("related_same_month_brand"), F.collect_list('pos').alias("top4_same_day_brand"))

display(top4_app_dataset)

# COMMAND ----------

#This code is the same that I described in the last cell. I just rewrote it to apply it to the same-month values and get the top 4 of the same-month brands.

posexp_app_dataset2 = top4_app_dataset.select("*", F.posexplode("related_same_month_brand"))

posexp_app_dataset2 = posexp_app_dataset2.withColumn("pos", posexp_app_dataset2.pos + 1).filter(posexp_app_dataset2.pos <= 3)

top4_app_dataset2 = posexp_app_dataset2.withColumn("brands_same_month", F.create_map(F.col("key"), F.col("value"))).drop("key", "value")
top4_app_dataset2 = top4_app_dataset2.withColumn("pos", F.create_map(F.col("pos"), F.col("brands_same_month"))).drop("brands_same_month")

top4_app_dataset_table = top4_app_dataset2.groupBy('row').agg(F.first('placekey').alias("placekey"), F.first('location_name').alias("location_name"), F.first('city').alias("city"), F.first('region').alias("region"), F.first('date_range_start').alias("date_range_start"), F.first('latitude').alias("latitude"), F.first('longitude').alias("longitude"), F.first('raw_visit_counts').alias("raw_visit_counts"), F.first('related_same_day_brand').alias("related_same_day_brand"), F.first('related_same_month_brand').alias("related_same_month_brand"), F.first('top4_same_day_brand').alias("top4_same_day_brand"), F.collect_list('pos').alias("top4_same_month_brand")).drop('row')

#The following is the final table that I will use in my streamlit app to show visualizations for the dashboard.

display(top4_app_dataset_table)

# COMMAND ----------

#The following code converts the StructType columns of the final table into a JSON format so I can fully download the whole csv file. This will also be an easier format to be handled by Pandas.  
pandas_top4_app_dataset = top4_app_dataset_table.withColumn("top4_same_day_brand", F.to_json("top4_same_day_brand")).withColumn("top4_same_month_brand", F.to_json("top4_same_month_brand")).withColumn("related_same_day_brand", F.to_json("related_same_day_brand")).withColumn("related_same_month_brand", F.to_json("related_same_month_brand"))

display(pandas_top4_app_dataset)

# COMMAND ----------

#Creating two columns with the name of the brand and percentage value to be filtered and get the top 4 brands. The purpose here is to check how many times a brand made it to the top 4. This will tell us which are the companies most visited either the same day or month when they visit Chipotle as well
posexp_app_dataset1 = app_dataset.select("latitude", "longitude", F.posexplode("related_same_day_brand"))
posexp_app_dataset2 = top4_app_dataset.select("latitude", "longitude", F.posexplode("related_same_month_brand"))

#Renaming some columns
posexp_app_dataset1 = posexp_app_dataset1.withColumnRenamed("pos", "same_day_top_rank").withColumnRenamed("key", "same_day_brand").withColumnRenamed("value", "day_%_value")

posexp_app_dataset2 = posexp_app_dataset2.withColumnRenamed("pos", "same_month_top_rank").withColumnRenamed("key", "same_month_brand").withColumnRenamed("value", "month_%_value")

#Filtering the data to get the top 4 brands
day_app_dataset = posexp_app_dataset1.withColumn("same_day_top_rank", posexp_app_dataset1.same_day_top_rank + 1).filter(posexp_app_dataset1.same_day_top_rank <= 3)
day_app_dataset2 = posexp_app_dataset2.withColumn("same_month_top_rank", posexp_app_dataset2.same_month_top_rank + 1).filter(posexp_app_dataset2.same_month_top_rank <= 3)

display(day_app_dataset)
display(day_app_dataset2)

# COMMAND ----------

#Get the count value of how many times a specific company made it to the top 4, and order it by descending. Then limit the columns to display only the top 10 to get most popular brands.
top10_most_popular_same_day = day_app_dataset.groupBy('same_day_brand').count().orderBy('count' , ascending=False).withColumnRenamed("count", "same_day_numOfTimes_reached_top4").limit(10)
top10_most_popular_same_month = day_app_dataset2.groupBy('same_month_brand').count().orderBy('count' , ascending=False).withColumnRenamed("count", "month_day_numOfTimes_reached_top4").limit(10)

#Convert data to pandas to plot the charts.
top10_most_popular_same_day_table = top10_most_popular_same_day.toPandas()
top10_most_popular_same_month_table = top10_most_popular_same_month.toPandas()

display(top10_most_popular_same_day_table)

#display chart for the top 10 most visited in the same day.
(ggplot(top10_most_popular_same_day_table)
 + geom_col(aes(x='same_day_brand', y ='same_day_numOfTimes_reached_top4'), width = 0.50, fill = '#0080ff')
 + theme(figure_size=(23, 8))
 + labs(x='Top 10 Brands that reached Top 4', y='Number of Times the brand reached the top 4', title="Top 10 Companies that most reached the Top 4")
)

# COMMAND ----------

# MAGIC %md
# MAGIC The chart above shows us the dominance of these companies in the United States. They are the most visited brands and they usually will be the favorite place to go if you visit Chipotle. This information is crusial to understand consumer behavior of Chipotle customer and their favorite places to go when they visited Chipotle the same day.  

# COMMAND ----------

display(top10_most_popular_same_month_table)

#display chart for the top 10 most visited in the same month.
(ggplot(top10_most_popular_same_month_table)
 + geom_col(aes(x ='same_month_brand', y ='month_day_numOfTimes_reached_top4'), width = 0.50, fill = 'red')
 + theme(figure_size=(13.5, 10))
 + labs(x='Top 10 Brands that reached Top 4 in the month', y='Number of Times the brand reached the top 4', title="Top 10 Companies that most reached the Top 4")
)

# COMMAND ----------

# MAGIC %md
# MAGIC The chart above confirms the dominance of these companies, this time the top 10 companies that reached the top 4 the most in the month. If you take a look at it you will see that 8 of the top same-day companies also were present in the same-month top 10. Being McDonalds the #1 in both charts. This is very important because you can predict, by just looking at the top 4 same-day companies, what companies Chipotle customers are more likely to go during the month if they visit Chipotle. This can lead to partnership between brands, increase revenue, and help each other to grow. 

# COMMAND ----------

#Retrieving the latitude and longitude of top 10 brands in both same_day and same_month. I will use this information to plot the spatial maps.

lat_long_same_day_topBrands = day_app_dataset.filter((day_app_dataset.same_day_brand == "McDonald's") | (day_app_dataset.same_day_brand == "Walmart") | (day_app_dataset.same_day_brand == "Starbucks") | (day_app_dataset.same_day_brand == "Target") | (day_app_dataset.same_day_brand == "Chick-fil-A") | (day_app_dataset.same_day_brand == "Dunkin'") | (day_app_dataset.same_day_brand == "Shell Oil") | (day_app_dataset.same_day_brand == "Wawa") | (day_app_dataset.same_day_brand == "7-Eleven") | (day_app_dataset.same_day_brand == "Walgreens"))

lat_long_month_topBrands = day_app_dataset2.filter((day_app_dataset2.same_month_brand == "McDonald's") | (day_app_dataset2.same_month_brand == "Walmart") | (day_app_dataset2.same_month_brand == "Starbucks") | (day_app_dataset2.same_month_brand == "Target") | (day_app_dataset2.same_month_brand == "Chick-fil-A") | (day_app_dataset2.same_month_brand == "Dunkin'") | (day_app_dataset2.same_month_brand == "Shell Oil") | (day_app_dataset2.same_month_brand == "Publix Super Markets") | (day_app_dataset2.same_month_brand == "Kroger") | (day_app_dataset2.same_month_brand == "Walgreens"))

display(lat_long_same_day_topBrands)
display(lat_long_month_topBrands)
