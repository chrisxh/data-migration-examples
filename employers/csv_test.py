import logging
import pandas as pd
import json

logger  = logging.getLogger('console')
output_lst = []

##specify the first row as header
df = pd.read_csv('data_sample.csv', keep_default_na=False , header=0)

#hacky way to group by distinct employer, allowing a list of users per employer.  
#todo: implement with some fancy pandas groupby and agg functions
df.sort_values(by='name',inplace=True)
df['next_name'] = df['name'].shift(-1)

users_lst = []
##iterate through all the rows
for index, row in df.iterrows():
    logger.info('start row {}'.format(index))
    dict = {}
    ## billing address items in this row
    billing = {}
    
    ## column_list is a list of column headers
    column_list = df.columns.values
    for i, col_name in enumerate(column_list):
        ## for the first 6 columns simply copy the value into the dictionary.
        ## assume all rows from the same employer have duplicate values (except user info)
        if i<6:
            element = row[col_name]
            if isinstance(element, str):
            ## strip if it is a string type value
                element = element.strip()
            dict[col_name] = element
        elif "billing_address:" in col_name:
            ##add billing address item
            billing[col_name.split(':')[1]] = row[col_name]

        elif "user:first_name" in col_name:
            ## Assumes column order of [first_name, last_name, email, access_group] for each user
            user_dict  = {"first_name":row[col_name], "last_name":row[column_list[i+1]], "email":row[column_list[i+2]], "access_group":row[column_list[i+3]]}
            users_lst.append(user_dict)
    
    logger.info('end row {}'.format(index))
    #peek at next row to see if we're in the same group
    if row['next_name'] != row['name']:
        dict["billing_address"] = billing
        dict["users"] = users_lst
        ## clear out for next list of users
        users_lst = []
        output_lst.append(dict)
        
    
    

print(json.dumps(output_lst, indent=4))
