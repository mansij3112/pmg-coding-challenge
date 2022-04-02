#Mansi Jadhav

from sys import argv
from pandas.api.types import union_categoricals
import pandas as pd
import psutil
import numpy as np

#Splitting the path string into an array of path segments 
def getFilenameFromPath(path: str):
    patharray = path.split("/")
    return patharray[2]


#Returns the CSV files as a list 
def getCsvFiles(filenames: list):
    files = []
    for file in filenames:
        filenamesplit = file.split(".")
        if filenamesplit[1] == "csv":
            files.append(file)

    return files


#Function creates categoricals, concatenates them, and returns a combined data frame. 
def processCategoricalsAndConcat(list_of_dataframes: list):
    categorical1 = []
    categorical2 = []
    for df in list_of_dataframes:
        categorical1.append(df.category)
        categorical2.append(df.filename)

    #Use the union_categoricals() function to merge the two lists into a single list of categories.
    uc1 = union_categoricals(categorical1)
    uc2 = union_categoricals(categorical2)

    for df in list_of_dataframes:
        df.category = pd.Categorical(df.category, categories=uc1.categories)
        df.filename = pd.Categorical(df.filename, categories=uc2.categories)

    combined_df = pd.concat(list_of_dataframes)
    return combined_df

#Generates a combined CSV file from a list of files.
def generateCombinedCsvFile(fixtures: list):
    data_type_conversion_metric = {
        "category": "category"
    }

    list_of_df = []

    for file in fixtures:
        temp_df = pd.read_csv("./fixtures/" + file, encoding='utf-8', dtype=data_type_conversion_metric)
        print( f" ** Memory usage of the file - {sum(temp_df.memory_usage()) * 0.000001} MB for {len(temp_df.index)} Rows")
        no_of_rows = temp_df.shape[0]
        filenames = []
        
        for i in range(no_of_rows):
            filenames.append(file)
        
        temp_df_filename = temp_df.assign(filename=pd.Series(filenames, dtype="category"))
        list_of_df.append(temp_df_filename)

    combined_df = processCategoricalsAndConcat(list_of_df)
    print(f" {combined_df.info()}")
    print(f" ** Summarize the data types and count of columns \n{combined_df.dtypes.value_counts()}")
    combined_df.to_csv('combined.csv', index=False)


#Prints amount of free and used memory
def checkMemoryUsage():
    memory = psutil.virtual_memory()
    print(f" {'*' * 3} Memory used percentage - {memory.percent} \n {'*' * 4} Free Memory available - { round(memory.free / (1024.0 ** 3))} GB")


#Main function
if __name__ == "__main__":
    fixtures = []
    for i in range(1, len(argv)):
        fixtures.append(getFilenameFromPath(argv[i]))

    checkMemoryUsage()

    csvFiles = getCsvFiles(fixtures)
    generateCombinedCsvFile(csvFiles)
