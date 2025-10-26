import time
import pandas as pd

# Dictionary with relative paths
CITY_DATA = {
    'chicago': 'data/chicago.csv',
    'new york city': 'data/new_york_city.csv',
    'washington': 'data/washington.csv'
}

def get_filters():
    """
    Demana a l'usuari especificar ciutat, mes i dia per analitzar.
    Retorna:
        city (str), month (str), day (str)
    """
    
    print("Hello! Let's explore some US bikeshare data!")

    cities = list(CITY_DATA.keys())

    while True:
        city = input("Enter city (chicago, new york city, washington): ").strip().lower()
        if city in cities:
            break
        else:
            
            print("Invalid input. Please try again.")

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']

    while True:
        month = input("Enter month (all or name of the month): ").strip().lower()
        if month in months:
            break
        else:
            
            print("Invalid input. Please try again.")

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input("Enter day (all or name of the day): ").strip().lower()
        if day in days:
            break
        else:
            
            print("Invalid input. Please try again.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """Loads data for the specified city and applies filters by month and day if needed."""
    try:
        file_path = CITY_DATA[city]
        df = pd.read_csv(file_path)
    except KeyError:
        
        print(f"Error: The city '{city}' is not valid.")
        return pd.DataFrame()
    except FileNotFoundError:
        
        print(f"File not found for city: {city}")
        return pd.DataFrame()

    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df = df.dropna(subset=['Start Time'])

    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    
    print(f"Number of records after filtering: {len(df)}")
    return df


def time_stats(df):
    """Displays statistics on the most frequent travel times."""
    
    print("Calculating the most frequent travel times...")
    start_time = time.time()

    if not df.empty:
        
        print("Most common month:", df['month'].mode()[0])
        
        print("Most common day:", df['day_of_week'].mode()[0])
        
        print("Most common start hour:", df['hour'].mode()[0])
    else:
        
        print("No data available to show time statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""
    
    print("Calculating the most popular stations...")
    start_time = time.time()

    if not df.empty:
        
        print("Most commonly used start station:", df['Start Station'].mode()[0])
        
        print("Most commonly used end station:", df['End Station'].mode()[0])
        df['trip'] = df['Start Station'] + " -> " + df['End Station']
        
        print("Most frequent combination:", df['trip'].mode()[0])
    else:
        
        print("No data available to show station statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on trip duration."""
    
    print("Calculating trip duration statistics...")
    start_time = time.time()

    if not df.empty:
        
        print("Total travel time (seconds):", df['Trip Duration'].sum())
        
        print("Average travel time (seconds):", df['Trip Duration'].mean())
    else:
        
        print("No data available to show trip duration statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    display_raw_data(df)
    """Displays statistics on users."""
    
    print("Calculating user statistics...")
    start_time = time.time()

    if not df.empty:
        
        print("Counts by user type:\n", df['User Type'].value_counts())

        if 'Gender' in df.columns:
            
            print("Counts by gender:\n", df['Gender'].value_counts())
        else:
            
            print("No gender data available.")

        if 'Birth Year' in df.columns:
            
            print("Earliest birth year:", int(df['Birth Year'].min()))
            
            print("Most recent birth year:", int(df['Birth Year'].max()))
            
            print("Most common birth year:", int(df['Birth Year'].mode()[0]))
        else:
            
            print("No birth year data available.")
    else:
        
        print("No data available to show user statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)



def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    start_row = 0
    end_row = 5

    while start_row < len(df):
        show_data = input("Would you like to see 5 lines of raw data? (yes/no): ").strip().lower()
        if show_data != 'yes':
            print("Stopping raw data display.")
            break

        print(df.iloc[start_row:end_row])
        start_row += 5
        end_row += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("Do you want to reset (yes/no): ").strip().lower()
        if restart != 'yes':
            
            print("Ending the program. Thank you!")
            break


if __name__ == "__main__":
    main()
