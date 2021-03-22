# Use as template for extracting data from XML or HTTP files

import pandas as pd
import os
from bs4 import BeautifulSoup

 

root_path = r"CI Reporting\1_Products and Services\PAS\Advice\Tableau"
folder = os.path.abspath(r"C:\Users\u4zt\OneDrive - Vanguard\Projects Folder\RDAS Internship\XML Files")
df_aggregate1 = pd.DataFrame()
df_aggregate2 = pd.DataFrame()
df_aggregate3 = pd.DataFrame()
print(root_path)

 

def append_list(path):
    with open(path, encoding='utf8') as fp:
        soup = BeautifulSoup(fp, 'xml')
        
    global package_name

    package_name = soup.find('modelPath').string

    print(package_name[str(package_name).find('@name=')+7:str(package_name).find(']', str(package_name).find('@name=')+7)-1])

    package_name = package_name[str(package_name).find('@name=')+7:str(package_name).find(']', str(package_name).find('@name=')+7)-1]

 

    queries = soup.find_all('query')

    find_tags = ['model', 'sqlQuery']

    ref_data_items = soup.find_all('dataItemLabel')

    page = soup.find('page')

    ref_query = soup.find('list')

    global data_list

    global query_list

    global filter_data_list

    global filter_query_list

    global page_name

    global page_query

    global page_item_list

    data_list = []

    query_list = []

    filter_data_list = []

    filter_query_list = []

    page_item_list = []

   

    # Get Data Items, Filters, and Associated Queries and Append to List

    for query in queries:

        if query.find_all(find_tags):

            expressions = query.find_all('expression')

            filter_queries = query.find_all('filterExpression')

            for expression in expressions:

                data_list.append(*expression)

                query_list.append(query['name'])

            for filter in filter_queries:

                filter_data_list.append(*filter)

                filter_query_list.append(query['name'])

 

    # Get Page Variables and Table and Append to List

    page_name = page['name']

    page_query = ref_query['refQuery']

    for data_item in ref_data_items:

        page_item_list.append(data_item['refDataItem'])

 

# Iterate Through All XML Files in Root Path and Feed to Function to Extract Data

for root, dirs, files in os.walk(folder):

    for file in files:

        file_path = os.path.join(root, file)

        ext = file_path[(file_path.find('XML Files')+10):(len(file_path)-len(os.path.basename(file_path))-1)]

        file_dir = os.path.join(root_path, ext)

        file_name = os.path.basename(file)

        append_list(file_path)

        d1 = {'Report Name': file_name, 'Report Path': file_dir, 'Cognos Package': package_name, 'Query': query_list,'Cognos Data Item': data_list}

        df1 = pd.DataFrame(data=d1)

        df_aggregate1 = df_aggregate1.append(df1, ignore_index=True)

        d2 = {'Report Name': file_name, 'Report Path': file_dir, 'Cognos Package': package_name, 'Query': filter_query_list,'Filter Expressions': filter_data_list}

        df2 = pd.DataFrame(data=d2)

        df_aggregate2 = df_aggregate2.append(df2, ignore_index=True)

        d3 = {'Report Name': file_name, 'Report Path': file_dir, 'Cognos Package': package_name, 'Page Name': page_name, 'Page Query': page_query, 'Page Table': page_item_list}

        df3 = pd.DataFrame(data=d3)

        df_aggregate3 = df_aggregate3.append(df3, ignore_index=True)

        print(file_dir)

        print(file_name)

print(df_aggregate1)

print(df_aggregate2)

print(df_aggregate3)

 

with pd.ExcelWriter("Output.xlsx") as writer:

    df_aggregate1.to_excel(writer, index=False, sheet_name='Data Items')

    df_aggregate2.to_excel(writer, index=False, sheet_name='Filter Expressions')

    df_aggregate3.to_excel(writer, index=False, sheet_name='Page View')
