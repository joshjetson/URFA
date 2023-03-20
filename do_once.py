import os
import sys
import pandas as pd
import numpy as np
import mysql.connector as cnxtr
from mysql.connector import Error as err
from geopy.geocoders import Nominatim as nm
import ipaddress

#If the files exist delete them
os.system('rm latlon countries progress main_df.csv')

#Save the progress of the script in a file for debugging if running in the background through a crontab job
os.system('date >> progress')
df = pd.read_csv('nottys', delim_whitespace=True, on_bad_lines='skip')
os.system('echo read_in_nottys >> progress')

#An optional function to obtain the attackers city
''' Note:
        This function can take a fair amount of time to process so you may want to consider
        omitting it from your analysis or think of a more clever way of achieving this.
        You could alternatively use it and let it run in the background while you do something else.'''

geoloc = nm(user_agent='youremail@gmail.com')
def geo(latlon):
    gloc = '0'
    try:
        gloc = geoloc.reverse(f'{latlon}')
    except ValueError:
        gloc = '0.00, 0.00'
        print(f"{latlon} is not a valid lat lon")
    return gloc

# The initial dictionary containing all the segmented data and two dummy columns, we always need dummies.
''' But were going to populate them dummies later on so its not all bad for them.'''
df_dic = {'User_Name':df.iloc[:,0],
          'IP_Addresses': df.iloc[:,2],
          'Day':df.iloc[:,3],
          'Month':df.iloc[:,4],
          'D_of_M':df.iloc[:,5],
          'Time_24_CST':df.iloc[:,6],
          'Year':df.iloc[:,7],
          'LATLNG':df.iloc[:,6],
          'Country':df.iloc[:,6]}

# Creating a dataframe from the data to be more easily manipulated and analyzed.
df_main = pd.DataFrame(df_dic)
os.system('echo created_df_main_from_df_dic >> progress')

# Drop the duplicate records
df_main.drop_duplicates(inplace=True)

# Validate if an ip address is authentic and alive.
def validate_ip_address(index, ip_string):
    good = True
    try:
        ip_object = ipaddress.ip_address(ip_string)
    except ValueError:
        # If we get the value error the ip is no good lets just drop the whole row that had that ip its useless.
        df_main.drop(index, inplace=True)
        good = False
        print(f"The IP address '{ip_string}' is not valid")
    if good:# If not good we dont need to do none of this stuff.
        # Get the latitude and longitude as well as the country from the attackers address using geoiplookup
        # and grep them up for only what we need ,that we dont have, then save those things in two separate files.
        # You can get crafty and do this in one file its just gonna look hella gnarly. Also there are other
        # issues you have to sort out if you go that route you gotta just do whats best for you feel me.
        os.system(f'echo `geoiplookup {ip_string} | grep City | cut -d ":" -f2 | cut -d "," -f 6,7` >> latlon')
        os.system(f'echo `geoiplookup {ip_string} | grep Country | cut -d ":" -f2` >> countries')

        # Read the files you just created in so you can use the stuff you just stored in them.
        ltlg = pd.read_csv('latlon', sep="&", lineterminator="\n", low_memory=False,names=['ll'])
        countries = pd.read_csv('countries',sep="&",names=['cc'])

        # Instructions: Wherever you see this one address just copy these two things right next to it.
        df_main.LATLNG = np.where(df_main.IP_Addresses.eq(ip_string), ltlg.iloc[0][0], df_main.LATLNG)
        df_main.Country = np.where(df_main.IP_Addresses.eq(ip_string), countries.iloc[0][0], df_main.Country)

    # I found to speed things up and for more efficient book keeping
    '''     Create the two lat and lon files each iteration of the loop and remove them as well.
            This is a better approach then just creating two more files with a bunch of stuff 
            in them that you then have to loop through again later anyways. Also if you took
            that approach there is a higher chance that your data might not line up.'''
    os.system('rm latlon countries')# Get rid of latlon and countries files no matter what. Peace..
os.system('echo `date` Currently running the longest processing portion >> progress')

# This set and loop are used as a way to not have the machine work so hard.
''' Rational:
        I noticed many attackers are repeat offenders. With this in mind I decided that
        we only need to process each unique ip address once.
        No need to process the same ip address over and over when we already got all the
        related details regarding the address, feel me?'''
checked = set()
for x, y in df_main.iterrows():
    if y['IP_Addresses'] not in checked:
        validate_ip_address(x, y['IP_Addresses'])
        checked.add(y['IP_Addresses'])
df_main.reset_index(inplace=True,drop=True)
os.system('date >> progress')
os.system('echo validated_ips_and_dropped_invalid_rows >> progress')

df_main.to_csv('main_df.csv',index=True)
os.system('echo `date` FINISHED >> progress')
