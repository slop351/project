import time
import pandas as pd

# Dictionary with relative paths
CITY_DATA = {
    'chicago': 'data/chicago.csv',
    'new york city': 'data/new_york_city.csv',
    'washington': 'data/washington.csv'
}

#Data filters

def get_filters():
    """
    Demana a l'usuari especificar ciutat, mes i dia per analitzar.
    Retorna:
        city (str), month (str), day (str)
    """
    
    print("Hello! Let's explore some US bikeshare data!")

    cities = list(CITY_DATA.keys())

# User inputs

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

#Loading city data 

def load_data(city, month, day):
    """Loads data for the specified city and applies filters by month and day if needed."""
    try:
        file_path = CITY_DATA[city]
        data_frame = pd.read_csv(file_path)
    except KeyError:
        
        print(f"Error: The city '{city}' is not valid.")
        return pd.DataFrame()
    except FileNotFoundError:
        
        print(f"File not found for city: {city}")
        return pd.DataFrame()

    data_frame['Start Time'] = pd.to_datetime(data_frame['Start Time'], errors='coerce')
    data_frame = data_frame.dropna(subset=['Start Time'])

    data_frame['month'] = data_frame['Start Time'].dt.month_name().str.lower()
    data_frame['day_of_week'] = data_frame['Start Time'].dt.day_name().str.lower()
    data_frame['hour'] = data_frame['Start Time'].dt.hour

    if month != 'all':
        data_frame = data_frame[data_frame['month'] == month]

    if day != 'all':
        data_frame = data_frame[data_frame['day_of_week'] == day]

    
    print(f"Number of records after filtering: {len(data_frame)}")
    return data_frame

#Calculate Data

def time_stats(data_frame):
    """Displays statistics on the most frequent travel times."""
    
    print("Calculating the most frequent travel times...")
    start_time = time.time()

    if not data_frame.empty:
        
        print("Most common month:", data_frame['month'].mode()[0])
        
        print("Most common day:", data_frame['day_of_week'].mode()[0])
        
        print("Most common start hour:", data_frame['hour'].mode()[0])
    else:
        
        print("No data available to show time statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(data_frame):
    """Displays statistics on the most popular stations and trips."""
    
    print("Calculating the most popular stations...")
    start_time = time.time()

    if not data_frame.empty:
        
        print("Most commonly used start station:", data_frame['Start Station'].mode()[0])
        
        print("Most commonly used end station:", data_frame['End Station'].mode()[0])
        data_frame['trip'] = data_frame['Start Station'] + " -> " + data_frame['End Station']
        
        print("Most frequent combination:", data_frame['trip'].mode()[0])
    else:
        
        print("No data available to show station statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(data_frame):
    """Displays statistics on trip duration."""
    
    print("Calculating trip duration statistics...")
    start_time = time.time()

    if not data_frame.empty:
        
        print("Total travel time (seconds):", data_frame['Trip Duration'].sum())
        
        print("Average travel time (seconds):", data_frame['Trip Duration'].mean())
    else:
        
        print("No data available to show trip duration statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(data_frame):
    display_raw_data(data_frame)
    """Displays statistics on users."""
    
    print("Calculating user statistics...")
    start_time = time.time()

    if not data_frame.empty:
        
        print("Counts by user type:\n", data_frame['User Type'].value_counts())

        if 'Gender' in data_frame.columns:
            
            print("Counts by gender:\n", data_frame['Gender'].value_counts())
        else:
            
            print("No gender data available.")

        if 'Birth Year' in data_frame.columns:
            
            print("Earliest birth year:", int(data_frame['Birth Year'].min()))
            
            print("Most recent birth year:", int(data_frame['Birth Year'].max()))
            
            print("Most common birth year:", int(data_frame['Birth Year'].mode()[0]))
        else:
            
            print("No birth year data available.")
    else:
        
        print("No data available to show user statistics.")

    
    print("Execution time: %.2f seconds." % (time.time() - start_time))
    print('-' * 40)



def display_raw_data(data_frame):
    """Displays raw data 5 rows at a time upon user request."""
    start_row = 0
    end_row = 5

    while start_row < len(data_frame):
        show_data = input("Would you like to see 5 lines of raw data? (yes/no): ").strip().lower()
        if show_data != 'yes':
            print("Stopping raw data display.")
            break

        print(data_frame.iloc[start_row:end_row])
        start_row += 5
        end_row += 5

#Main Programm
def main():
    while True:
        city, month, day = get_filters()
        data_frame = load_data(city, month, day)

        time_stats(data_frame)
        station_stats(data_frame)
        trip_duration_stats(data_frame)
        user_stats(data_frame)
        display_raw_data(data_frame)

        restart = input("Do you want to reset (yes/no): ").strip().lower()
        if restart != 'yes':
            
            print("Ending the program. Thank you!")
            break


if __name__ == "__main__":
    main()
