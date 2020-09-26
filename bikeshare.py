import time
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import calendar
import datetime


"""
# Exploring US Bikeshare Data.
This script makes use of data provided by Motivate- https://www.motivateco.com/, a bike-share system \
    provider for three major US cities in the USA - Chicago, New York City and Washington. \
    Bikeshare data in New York City, Washington, Chicago.

- Kindly Ignore the DuplicateWidgetID error. The Invalid Input box should be used when an input is not accepted. The library used in the development of this cript is still a work in progress. While it mostly works well now, it still requires more work. Github: https://github.com/streamlit/streamlit/blob/5acfca162b0efd55a4c8e354804aa72c00a86f56/docs/main_concepts.md
"""

a,b,c,d,e,f,g,h,i = 1,2,3,4,5,6,7,8,9
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    """
    ## Hello! Let\'s explore some US bikeshare data!
    """
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
     
    city = (st.text_input(label='Which city would you like to analyze? Chicago, New York City or Washington? ',key = a)).lower()
    while city not in ("chicago", "new york city", "washington"):
        city = (st.text_input(label='Invalid input. Select from one of these 3 options: Chicago, New York City or Washington? ',key = b)).lower()
    
    # get user input for month (all, january, february, ... , june)                                                          
    month = (st.text_input('Which month would you like to analyze? ',key=c)).lower()
    while month not in ("all", "january", "february", "march", "april", "may", "june"):
      month = (st.text_input('Input a valid month or \'all\' for all the months: ',key=d)).lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = (st.text_input('Which day would you like to analyze? ',key=e)).lower()                           
    while day not in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
      day = (st.text_input('Input a valid day or \'all\' for all the days: ',key=f)).lower()
        
    st.write('-'*40)
    return city, month, day

#Load and Filter the Dataset
#This is a bit of a bigger task, which involves choosing a dataset to load and filtering it based on a specified month and day.
#In the quiz below, you'll implement the load_data() function, which you can use directly in your project. There are four steps:
#Load the dataset for the specified city. Index the global CITY_DATA dictionary object to get the corresponding filename for the
#given city name.
#Create month and day_of_week columns. Convert the "Start Time" column to datetime and extract the month number and weekday name into separate columns using the datetime module.
#Filter by month. Since the month parameter is given as the name of the month, you'll need to first convert this to the corresponding month number. Then, select rows of the dataframe that have the specified month and reassign this as the new dataframe.
#Filter by day of week. Select rows of the dataframe that have the specified day of week and reassign this as the new dataframe. (Note: Capitalize the day parameter with the title() method to match the title case used in the day_of_week column!

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    raw = (st.text_input('Would you like to see a sample of the data?',value='Yes.',key=g)).lower()
    if raw == 'no':
      # load data file into a dataframe
      df = pd.read_csv(CITY_DATA[city])

      # convert the Start Time column to datetime
      df['Start Time'] = pd.to_datetime(df['Start Time'])

      # extract month and day of week from Start Time to create new columns
      df['month'] = df['Start Time'].dt.month
      df['day_of_week'] = df['Start Time'].dt.day_name()
      

      # filter by month if applicable
      if month != 'all':
          # use the index of the months list to get the corresponding int
          months = ['january', 'february', 'march', 'april', 'may', 'june']
          month = months.index(month)+1
          
          # filter by month to create the new dataframe
          df = df[df['month'] == month]

      # filter by day of week if applicable
      if day != 'all':
          # filter by day of week to create the new dataframe
          df = df[df['day_of_week'] == day.title()]
          
    else:
      raw_df = pd.read_csv(CITY_DATA[city])
      raw_rows = 5
      df = raw_df.head()
      df.rename(columns={ 'Unnamed: 0' : 'User ID'}, inplace = True)
      st.table(df)
      
      raw_rerun = (st.text_input('Would you like to view 5 more rows of raw data? Yes/No ', key=h)).lower()   
      while raw_rerun == 'yes':                                                                                                                 
        df = raw_df.loc[raw_rows:raw_rows+5]
        df.rename(columns={ 'Unnamed: 0' : 'User ID'}, inplace = True)
        st.table(df)
        raw_rows +=5
        raw_rerun = (st.text_input('Would you like to view 5 more rows of raw data? Yes/No ', key=i)).lower() 
     
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    st.write('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    try:
        
        # convert the start time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        
        #extract the month from the "Start Time" column to create a month column
        df['month_of_year'] = df['Start Time'].dt.month
        #find the most common month
        common_month = df['month_of_year'].value_counts().idxmax()
        
        #extract the day of the week from the "Start Time" column to create a day_of_week column
        df['day_of_week'] = df['Start Time'].dt.day_name()
        #find the most common day of the week
        common_day = df['day_of_week'].value_counts().idxmax()
        
        # extract the hour from the start time column to create an time_hour column
        df['time_hour'] = df['Start Time'].dt.hour
        
        # display the most common month
        st.write('The most common month is ', datetime.date(1900, common_month, 1).strftime('%B'))
        
        # display the most common day of week
        st.write('The most common day of the week is ', common_day)
        
        # display the most common start hour
        st.write('The most common start hour is', df['time_hour'].value_counts().idxmax(),':00 Hours')
        
    except ValueError as e:
        st.write('Unable to perform calculation, an Error occurred: {}'.format(e))
    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    st.write('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    try:
        # display most commonly used start station
        common_start = df['Start Station'].value_counts().idxmax()
        st.write('Most commonly used start station is:', common_start)

        # display most commonly used end station
        common_end = df['End Station'].value_counts().idxmax()
        st.write('Most commonly used end station is:', common_end)

        # display most frequent combination of start station and end station trip
        common_combo = df.groupby('Start Station')['End Station'].value_counts().idxmax()
        st.write('Most commonly used combination: ', common_combo)
        
    except ValueError as e:
        st.write('Unable to perform calculation, an Error occurred: {}'.format(e))

    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    st.write('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip = df['Trip Duration'].sum()
    st.write('Total travel time: ', str(total_trip))
    
    # display mean travel time
    mean_trip = df['Trip Duration'].mean()
    st.write('Mean travel time: ', str(mean_trip))
    
    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)    

def user_stats(df):
    """Displays statistics on bikeshare users."""
    st.write('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user_types
    user_type = df['User Type'].value_counts()

    st.write("The types of users by number are given below:\n", user_type)

    #Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        st.write("\nThe types of users by gender are given below:\n", gender)
    except:
        st.write("\nThere is no 'Gender' column in this file.")

    #Display earliest, most recent and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        
        st.write("\nThe earliest year of birth: {0}\n\nThe most recent year of birth: {1}\n\nThe most common year of birth: {2}".format(earliest, recent, common_year))
    except:
        st.write("There are no birth year details in this file.")

    st.write("\nThis took %s seconds." % (time.time() - start_time))
    st.write('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        break

        #restart = st.text_input('input new value.',key=h).lower()
        #if restart != 'yes':
        #    break

if __name__ == "__main__":
    main()


"""
### Reload the page to run another inquiry.
### Contributors:
* @Adedolapo - Team Lead
* @Chiagozie.Robert - Asst. Team Lead
* @BigBadWolf 
* @Zac
* @Tejumade97
"""