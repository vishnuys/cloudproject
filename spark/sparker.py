import os
from pyspark import SparkContext
from pyspark.sql import SparkSession
from .schemas import *
import json

sc = SparkContext('local', 'cloud')
spark = SparkSession(sc)


def execute_query1(t1, t1_alias, t2, t2_alias, c1, c2):
    if '.' in c1[0]:
        t1_alias_obt, attr1 = c1[0].split('.')
    else:
        attr1 = c1[0]
    if '.' in c1[2]:
        t2_alias_obt, attr2 = c1[2].split('.')
    else:
        attr2 = c1[2]
    file_one = os.path.join('files', t1 + '.csv')
    file_two = os.path.join('files', t2 + '.csv')
    if t1 == 'users':
        df1 = spark.read.csv(file_one, header=False, schema=users_schema)
    elif t1 == 'zipcodes':
        df1 = spark.read.csv(file_one, header=False, schema=zipcodes_schema)
    elif t1 == 'movies':
        df1 = spark.read.csv(file_one, header=False, schema=movies_schema)
    elif t1 == 'rating':
        df1 = spark.read.csv(file_one, header=False, schema=rating_schema)

    if t2 == 'users':
        df2 = spark.read.csv(file_two, header=False, schema=users_schema)
    elif t2 == 'zipcodes':
        df2 = spark.read.csv(file_two, header=False, schema=zipcodes_schema)
    elif t2 == 'movies':
        df2 = spark.read.csv(file_two, header=False, schema=movies_schema)
    elif t2 == 'rating':
        df2 = spark.read.csv(file_two, header=False, schema=rating_schema)
    # df1.show()
    # df2.show()
    joined = df1.join(df2, attr1)
    # joined.show()
    c2_attr = c2[0].split('.')[-1]
    parameter = int(c2[2]) if c2[2].isnumeric() else c2[2].strip('"').strip("'")
    operator = c2[1]
    print("%r %r %r" % (c2_attr, operator, parameter))
    print(type(c2_attr), type(operator), type(parameter))
    if operator == '=':
        filtered = joined.filter(col(c2_attr) == parameter)
    elif operator == '<':
        filtered = joined.filter(col(c2_attr) < parameter)
    elif operator == '>':
        filtered = joined.filter(col(c2_attr) > parameter)
    elif operator == '<=':
        filtered = joined.filter(col(c2_attr) <= parameter)
    elif operator == '>=':
        filtered = joined.filter(col(c2_attr) >= parameter)
    elif operator == '<>' or operator == '!=':
        filtered = joined.filter(col(c2_attr) != parameter)

    # filtered.show(filtered.count())
    # print(joined.count(), filtered.count())
    return filtered.toJSON().map(lambda j: json.loads(j)).collect()


def execute_query2(table, groupParameters, havingCondition, formattedSelects):
    csv_file = os.path.join('files', table + '.csv')
    if table == 'users':
        dataframe = spark.read.csv(csv_file, header=False, schema=users_schema)
    elif table == 'zipcodes':
        dataframe = spark.read.csv(csv_file, header=False, schema=zipcodes_schema)
    elif table == 'movies':
        dataframe = spark.read.csv(csv_file, header=False, schema=movies_schema)
    elif table == 'rating':
        dataframe = spark.read.csv(csv_file, header=False, schema=rating_schema)

    dataframe.show()
    print(dataframe.count())
