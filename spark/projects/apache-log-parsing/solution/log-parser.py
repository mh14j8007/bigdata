from pyspark.sql import Row
import re

# This code is written by one of our student. Works only in Spark2.0 and above

#case class LogRecord( host: String, timeStamp: String, url:String,httpCode:Int)

PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)(.*)" (\d{3}) (\S+)'
line = 'slppp6.intermind.net - - [01/Aug/1995:00:00:39 -0400] "GET /history/skylab/skylab-logo.gif HTTP/1.0" 200 3274'


def parseLogLine(log):
    m = re.match(PATTERN, log)
    if m:
        return [Row(host=m.group(1), timeStamp=m.group(4),url=m.group(6), httpCode=int(m.group(8)))]
    else:
        print("Rejected Log Line: " + log)
        return []

#Test if it is working
parseLogLine(line)

logFile = sc.textFile("/data/spark/project/NASA_access_log_Aug95.gz")

accessLog = logFile.flatMap(parseLogLine)
accessDf = spark.createDataFrame(accessLog)
accessDf.printSchema
accessDf.createOrReplaceTempView("nasalog")
output = spark.sql("select * from nasalog")
output.createOrReplaceTempView("nasa_log")
spark.sql("cache TABLE nasa_log")

spark.sql("select url,count(*) as req_cnt from nasa_log where upper(url) like '%HTML%' group by url order by req_cnt desc LIMIT 10").show()

spark.sql("select host,count(*) as req_cnt from nasa_log group by host order by req_cnt desc LIMIT 5").show()

spark.sql("select substr(timeStamp,1,14) as timeFrame,count(*) as req_cnt from nasa_log group by substr(timeStamp,1,14) order by req_cnt desc LIMIT 5").show()

spark.sql("select substr(timeStamp,1,14) as timeFrame,count(*) as req_cnt from nasa_log group by substr(timeStamp,1,14) order by req_cnt  LIMIT 5").show()

spark.sql("select httpCode,count(*) as req_cnt from nasa_log group by httpCode ").show()

