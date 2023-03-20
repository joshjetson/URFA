import os
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim as nm
import ipaddress
''' This program is aimed at them notty ones. Those would be system invaders. '''
#This file is just like the do_once file but the do_once file you do once and the do_many file ...you guessed it! 
os.system('rm latlon countries progress new_nottys')

os.system('echo `date` Starting.. >> progress')
#CREATE THE FILE TO BE POPULATED. THIS IS GOING TO BE THE RAW LIST OF NEW ATTACKERS

#GENERATE AN OUTPUT OF THE LAST 300 BAD LOGIN ATTEMPTS AND SAVE IT IN THE FILE JUST CREATED
os.system('cat nottys | tail -n 2000 >> new_nottys')

#READ IN THE PRE GENERATED FILE
df = pd.read_csv('new_nottys', delim_whitespace=True,on_bad_lines='skip')
#df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df_dic = {'User_Name':df.iloc[:,0],
          'IP_Addresses': df.iloc[:,2],
          'Day':df.iloc[:,3],
          'Month':df.iloc[:,4],
          'D_of_M':df.iloc[:,5],
          'Time_24_CST':df.iloc[:,6],
          'Year':df.iloc[:,7],
          'LATLNG':df.iloc[:,6],
          'Country':df.iloc[:,6]}

df_main = pd.DataFrame(df_dic)
os.system('echo created_df_main_from_df_dic >> progress')

df_main.drop_duplicates(inplace=True)

def validate_ip_address(index, ip_string):
    good = True
    try:
        ip_object = ipaddress.ip_address(ip_string)
    except ValueError:
        df_main.drop(index, inplace=True)
        good = False
        print(f"The IP address '{ip_string}' is not valid")
    if good:
        os.system(f'echo `geoiplookup {ip_string} | grep City | cut -d ":" -f2 | cut -d "," -f 6,7` >> latlon')
        os.system(f'echo `geoiplookup {ip_string} | grep Country | cut -d ":" -f2` >> countries')
        ltlg = pd.read_csv('latlon', sep="&", lineterminator="\n", low_memory=False,names=['ll'])
        countries = pd.read_csv('countries',sep="&",names=['cc'])
        df_main.LATLNG = np.where(df_main.IP_Addresses.eq(ip_string), ltlg.iloc[0][0], df_main.LATLNG)
        df_main.Country = np.where(df_main.IP_Addresses.eq(ip_string), countries.iloc[0][0], df_main.Country)
    os.system('rm latlon countries')

os.system('echo `date` Currently running the longest processing portion >> progress')

checked = set()
for x, y in df_main.iterrows():
    if y['IP_Addresses'] not in checked:
        validate_ip_address(x, y['IP_Addresses'])
        checked.add(y['IP_Addresses'])

os.system('date >> progress')
os.system('echo validated_ips_and_dropped_invalid_rows >> progress')

# Modify this to your specific needs
output = pd.read_csv('main_df.csv', index_col=0)

# This is me removing my own failed login attempts for my own server when my fingers she no worky. 
output.drop(output.loc[output['User_Name']=='ssh:notty'].index,inplace=True)
output.drop(output.loc[(output['IP_Addresses']=='fe80::8db3:de74:') | (output['IP_Addresses']=='2600:1700:2480:6') | (output['IP_Addresses']=='192.168.1.202')].index,inplace=True)
output = pd.concat([output, df_main], ignore_index=True)
output.drop_duplicates(inplace=True)
output.reset_index(inplace=True,drop=True)
output.to_csv('main_df.csv',index=True)
output.to_json('main.json')
output.to_json('/srv/http/your_folder/main.json')
os.system('echo Done >> progress')

os.system('date >> progress')
