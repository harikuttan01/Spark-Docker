from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import date

spark = SparkSession.\
        builder.\
        appName("pyspark").\
        master("local[*]").\
        config("spark.executor.memory", "512m").\
        getOrCreate()

schema = StructType([
    StructField('AirportCode', StringType(), False),
    StructField('Date', DateType(), False),
    StructField('TempHighF', IntegerType(), False),
    StructField('TempLowF', IntegerType(), False)
])

data = [
    [ 'BLI', date(2021, 4, 3), 52, 43],
    [ 'BLI', date(2021, 4, 2), 50, 38],
    [ 'BLI', date(2021, 4, 1), 52, 41],
    [ 'PDX', date(2021, 4, 3), 64, 45],
    [ 'PDX', date(2021, 4, 2), 61, 41],
    [ 'PDX', date(2021, 4, 1), 66, 39],
    [ 'SEA', date(2021, 4, 3), 57, 43],
    [ 'SEA', date(2021, 4, 2), 54, 39],
    [ 'SEA', date(2021, 4, 1), 56, 41]
]

temps = spark.createDataFrame(data, schema)
temps.show()
spark.sql('USE default')
spark.sql('DROP TABLE IF EXISTS demo_temps_table')
temps.write.saveAsTable('demo_temps_table')
spark.sql("SHOW TABLES").show()
df_temps = spark.sql("SELECT * FROM demo_temps_table " \
    "WHERE AirportCode != 'BLI' AND Date > '2021-04-01' " \
    "GROUP BY AirportCode, Date, TempHighF, TempLowF " \
    "ORDER BY TempHighF DESC")
df_temps.show()

print("--------------------------------------------------------------------------------------------------------------------------------------------------")

print("Reading from files.....\n")
dataframe = spark.read.json('nyt2.json')

dataframe.show()

print("Dropping duplicates.....\n")
dataframe_dropdup = dataframe.dropDuplicates() 
dataframe_dropdup.show(10)

print("Selecting specific columns without sql.....\n")
dataframe.select("author", "title", "rank", "price").show(10)

print("Matching entries using values.....\n")
dataframe [dataframe.author.isin("John Sandford", 
"Emily Giffin")].show(5)

print("Matching entries with expressions.....\n")
dataframe.select("author", "title",dataframe.title.like("% THE %")).show(15)

print("Groupby function.....\n")
dataframe.groupBy("author").count().show(10)

print("Using filters.....\n")
dataframe.filter(dataframe["title"] == 'THE HOST').show(5)

print("Creating partitions.....\n")
dataframe.repartition(10).rdd.getNumPartitions()

print("Performing SQL queries.....\n")
dataframe.createOrReplaceTempView("df")
spark.sql("select * from df").show(3)
try:
    dft = spark.sql("select " \
        "CASE WHEN description LIKE '%love%' THEN 'Love_Theme' " \
            "WHEN description LIKE '%hate%' THEN 'Hate_Theme' " \
                "WHEN description LIKE '%happy%' THEN 'Happiness_Theme' " \
                    "WHEN description LIKE '%anger%' THEN 'Anger_Theme' " \
                        "WHEN description LIKE '%horror%' THEN 'Horror_Theme' " \
                            "WHEN description LIKE '%death%' THEN 'Criminal_Theme' " \
                                "WHEN description LIKE '%detective%' THEN 'Mystery_Theme' " \
                                    "ELSE 'Other_Themes' " \
                                        "END Themes " \
                                            "from df ")
    dft.groupBy('Themes').count().show()
except:
    pass