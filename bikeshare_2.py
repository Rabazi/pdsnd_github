import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input(
            'Would you like to see data of chicago, New York City or Washington?\n').lower()
        if city not in cities:
            print('Invaild input, please try again\n')
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input(
            'Which month would you like to see? January, Febuary, March , April, May, June or all of them. Type "all" to not use a filter. \n').lower()
        if month not in months:
            print("invalid input, please try again!\n")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input(
            'Which day would you like so see? Type "all" for no filter\n').lower()
        if day not in days:
            print('invalid input, please try again!\n')
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data into Dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of the week and hour form column Start Time to make new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filters by day of the week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        #day = days.index(day) + 1

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)

    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].value_counts().index[0]
    print('The most often used Start Station ist: ', most_used_start_station)

    # display most commonly used end station
    most_used_end_station = df['End Station'].value_counts().index[0]
    print('The most common End Station is ', most_used_end_station)
    # display most frequent combination of start station and end station trip
    combination_stations = df.groupby(['Start Station', 'End Station']).count()
    print('Most Commonly used combination of start station and end station trip is: ',
          most_used_start_station, " & ", most_used_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', total_travel_time / 86400, "Days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_travel_time / 60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)
    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("\n Gender Types: \n", gender_types)
    except KeyError:
        print("\n Gender Types: \n No Data available!")

    # Display earliest, most recent, and most common year of birth
    # try and except to cover NAN´s
    try:
        earliest_year_of_birth = df['Birth Year'].min()
        print("\n The earliest year of birth is:", int(earliest_year_of_birth))
    except KeyError:
        print("\n earliest Year:\n No Data available!")

    try:
        most_recent_year_of_birth = df['Birth Year'].max()
        print("\n The most recent year of birth is: ",
              int(most_recent_year_of_birth))
    except KeyError:
        print("\n most recent Year:\n No Data available!")

    try:
        most_commen_year_of_birth = df['Birth Year'].mode()[0]
        print("\n The most commen year of birth is: ",
              int(most_commen_year_of_birth))
    except KeyError:
        print("\n most commen Year:\n No Data available!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # asking if they want to see raw input and displaying it
    x = 1
    while True:
        raw = input('\nWould you like to see some raw data? Enter yes or no.\n')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

    exit()


if __name__ == "__main__":
    main()

get_filters()
