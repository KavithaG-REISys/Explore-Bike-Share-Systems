import pandas as pd
import numpy as np


#Load Data form the follwoing files based on the users input

City_data = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
ip =['yes','no']

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
    
                 'Would you like to see data for Chicago, New York, or Washington?\n')
    city = city.lower()
    while city not in City_data.keys():
        city = input("\nTry again: Please enter which data you would like to see Chicago, New York or Washington\n")
    return city
    
    

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        TODO: fill out return type and description (see get_city for an example)
    '''
    month = input("\nWhich month would you like to explore? January, February, March, April, May, or June?\n")
    month = month.lower()
    while month not in months:
        month = input('\nTry Again: Which month would you like to explore? January, February, March, April, May, or June?\n')
    return month
    


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        TODO: fill out return type and description (see get_city for an example)
    '''
    day = input('\nWhich day would you like to explore? Please type your response as Sunday, Monday, Tuesday, Wednesday, Thursday , Friday or Saturday.\n')
    day=day.lower()
    while day not in days:
        day = input('\nTry Again: Which day would you like to explore? Please type your response as Sunday, Monday, Tuesday, Wednesday, Thursday , Friday or Saturday.\n')
    return day

def get_raw_data():
    raw_data = input('\nWould you like to look at sample data, type yes or no\n')
    raw_data = raw_data.lower()
    while raw_data not in ip:
        raw_data = input('\nTry Again. Would you like to look at sample data, type yes or no\n')
    return(raw_data)



def prepare_stats(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(City_data[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    popular_month = df['month'].mode()[0]
    popular_day_of_the_week = df['day_of_week'].mode()[0]
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print("Calculating the Statistics for : Popular Travel times")
    print("#####################################################")
    print ("The most popular hour of travel for the "+ city.title() +" data is " + str(popular_hour) + ".\n")
    print("The most popular month of travel for the "+ city.title()+" data is "+ months[popular_month-1].title() + ".\n")
    print("The most popular day of the week of travel for the "+ city.title()+" data is "+str(popular_day_of_the_week) + ".\n")
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]    
         
    #find the popular start Station
    print("Calculating the next statistics for : Popular Stations and Trip")
    print("################################################################")
    print("Most Popular Start Station: "+ df['Start Station'].value_counts().keys()[0] )
    print ("Most Popular Stat Station count " + str(df['Start Station'].value_counts().max()))
    print("Most Popular End Station: " + df['End Station'].value_counts().keys()[0])
    print("Most Popular End Station count " + str(df['End Station'].value_counts().max()))
    pop_trip = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Size')
    mval= pop_trip['Size'].max()
    tripstats = pop_trip.loc[pop_trip['Size'] == mval]
    print("Most Popular trip (from stat to end): ")
    print(tripstats.iloc[0])

    # Calculating the stats for total travel Time
    print("\n\nCalculating the next statistics for : Trip Duration")
    print("########################################################")
    total_travel_time = df['Trip Duration'].sum()
    avg_travel_time = df['Trip Duration'].mean()
    trip_count = df['Trip Duration'].count()
    print("Total Travel Time: " + str(total_travel_time))
    print("Avergar Travel time: " + str(avg_travel_time))
    
    # Calculating the stats for User Type 
    if city != "washington":
        user_types = df['User Type'].value_counts()
        gender_types = df['Gender'].value_counts()
        print("\n\nCalculating the next statistics for : User Types")
        print("####################################################")
        print("Count Of each user type:\n")
        print(user_types)
        print("Count of each gender:")
        print(gender_types[:]) 
        df['Birth Year'] = df['Birth Year'].replace(0, np.NaN)
        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        print("Earliest year of birth" )
        print(int(earliest))
        print("Latest year of birth" )
        print(int(latest))
        print("Most common year of birth" )
        print(int(df['Birth Year'].value_counts().keys()[0]))
        print("Total count for most common year of birth")
        print (df['Birth Year'].value_counts().max())
    return df

restart = True
while restart:
     city = get_city() 
     month = get_month()
     day = get_day()
     df = prepare_stats(city,month,day)
     # Ask User if they want to take a look at the data
     raw_data= get_raw_data()
     if (raw_data.lower() == 'yes'):
         print (df)
     restart = input('\nWould you like to load and analyze another data, type yes or no\n')
     while restart not in ip:
         restart = input('\nTry Again.Would you like to load and analyze another data, type yes or no\n')    
     if restart.lower() != "yes":
         restart = False
