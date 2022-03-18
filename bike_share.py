#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months={1:"january",2:"february",3:"march",4:"april",5:"may",6:"june"}
days = {1: 'sunday', 2: 'monday', 3: 'tuesday',4: 'wednesday', 5: 'thursday', 6: 'friday', 7: 'saturday'}


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    day=" "
    month=" "
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities={"1":"chicago","2":"new york city","3":"washington"}
    city=input("Would you like to see data for chicago, new york city or washington \n").lower()
    while city  not in list(cities.values()):
        print("Invalid city,try again")
        city=input("Would you like to see data for chicago, new york city or washington \n").lower()
        continue

    # get user input for month (all, january, february, ... , june)
    def month_filter():
        month=input("Which month,January,February , March, April, May or June \n").lower()
        while month not in list(months.values()):
            print("Invalid month,try again")
            month=input("Which month,January ,February , March, April, May or June \n").lower()
            continue
        return month

    # get user input for day of week (all, monday, tuesday, ... sunday)
    def day_filter():
        day=int(input("Which day? Please type your response as an integer(e-g .,)1=Sunday \n"))
        while day not in list(days.keys()):
            print("Invalid day, try again")
            day=int(input("Which day? Please type your response as an integer(e-g .,)1=Sunday \n"))
            continue
        return day
    filters={'1':'month','2':'day','3':'both','4':'none'}
    time_filter=input("would you like to filter the day by month, day, both, or not at all? Type \"none\" for no time filter").lower()
    while time_filter not in list(filters.values()):
        print("Invalid time filter,Try again")
        time_filter=input("would you like to filter the day by month, day, both, or not at all? Type \"none\" for no time filter").lower()
        continue   
    if time_filter in ('month',1):
        month= month_filter()
        day='all'
    elif time_filter in ('day',2):
        month='all'
        day= day_filter()
    elif time_filter in ('both',3):
        month= month_filter()
        day= day_filter()
    elif time_filter in ('none',4):
        month='all'
        day='all'
    print('-'*40)
    return city, month, day


# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day -  of week to filter by, or "all" to apply no day filter
    Returns:name of the day
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df["Start Time"]=pd.to_datetime(df["Start Time"])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.day
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month=df["month"].value_counts().idxmax()
    print(f"Most popular Start Month: {months[popular_month]}")

    # display the most common day of week
    popular_day=df["day_of_week"].value_counts().idxmax()
    print(f"Most popular Start day: {popular_day}")

    # display the most common start hour
    df["start_hour"]=df["Start Time"].dt.hour
    popular_hour=df["start_hour"].value_counts().idxmax()
    print(f"Most popular Start hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_StartStation=df["Start Station"].value_counts().idxmax()
    print(f"Most Common Start Station: {popular_StartStation}")
    # display most commonly used end station
    popular_EndStation=df["End Station"].value_counts().idxmax()
    print(f"Most Common End Station: {popular_EndStation}")

     # display most frequent combination of start station and end station trip
    common_trip=(df['Start Station']+" to "+ df['End Station']).mode()[0]
    print("most common trip: ", common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"The Total Travel Time: {df['Trip Duration'].sum()}")
    
    # display mean travel time
    print(f"The Total Travel Time: {df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"The Count of user types:\n{df['User Type'].value_counts()}")
    # Display counts of gender
    if "Gender" not in df:
        print("No gender to share")
    else:
        print(f"The Count of gender:\n {df['Gender'].value_counts()}")
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" not in df:
        print("No birth year to share")
    else:
        print(f"The earlist year of birth: {df['Birth Year'].min()}")
        print(f"The most recent year of birth: {df['Birth Year'].max()}")
        print(f"The most common year of birth: {df['Birth Year'].value_counts().idxmax()}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def data(df):
    raw_data = 0
    while True:
        answer = input("Do you want to see the raw data? Yes or No").lower()
        if answer not in ['yes', 'no']:
            answer = input("You wrote the wrong word. Please type Yes or No.").lower()
        elif answer == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
            again = input("Do you want to see more? Yes or No").lower()
            if again == 'no':
                break
        elif answer == 'no':
            return


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df=load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:




