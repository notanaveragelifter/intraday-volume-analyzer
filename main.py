import pandas as pd

ROLLING_WINDOW_SECONDS = 3600  # 60 minutes
MARKET_OPEN_TIME = "09:15:00"
   
    # Calculate the 30-day avg volumes for each stock on the target date
def calculate_30_day_average(day_data, target_date):
    start_date = pd.Timestamp(target_date) - pd.Timedelta(days=30)
    filtered_data = day_data[(day_data['Date'] >= start_date) & (day_data['Date'] < target_date)]
    
    avg_volumes = filtered_data.groupby('Stock Name')['Volume'].mean().reset_index()
    avg_volumes.rename(columns={'Volume': '30-Day Average Volume'}, inplace=True)
    
    return avg_volumes

    #Compute rolling 60-minute volumes and identify the crossover timestamps
def compute_rolling_volumes(intraday_data, avg_volumes, target_date):
   
    # Merge 30-day averages with intraday data
    intraday_data = intraday_data.merge(avg_volumes, on='Stock Name', how='left')
    
    # Ensure data is sorted by stock and timestamp
    intraday_data = intraday_data.sort_values(by=['Stock Name', 'Timestamp'])

    # Filter data to only include timestamps from market open (9:15 AM)
    intraday_data = intraday_data[intraday_data['Timestamp'].dt.time >= pd.to_datetime(MARKET_OPEN_TIME).time()]

    # Set Timestamp as the index for time-based rolling
    intraday_data.set_index('Timestamp', inplace=True)

    # Group by stock and calculate rolling cumulative volumes within 60 minutes
    intraday_data['Cumulative Volume'] = (
        intraday_data.groupby('Stock Name')['Last Traded Quantity']
        .rolling(window=pd.Timedelta(seconds=ROLLING_WINDOW_SECONDS), min_periods=1)
        .sum()
        .reset_index(level=0, drop=True)
    )

    # Identify the timestamp where cumulative volume exceeds 30-day avg
    def find_crossover(group):
        crossover = group[group['Cumulative Volume'] > group['30-Day Average Volume']]
        if not crossover.empty:
            return crossover.iloc[0].name  
        return None
    
    # Apply the find_crossover function to each stock
    results = (
        intraday_data.groupby('Stock Name')
        .apply(find_crossover)
        .reset_index(name='Crossover Timestamp')
    )
    
    # Add target date to the result
    results['Date'] = target_date
    
    return results


def main():
    # Loading the   data
    day_data = pd.read_csv('SampleDayData.csv')
    intraday_19 = pd.read_csv('19thAprilSampleData.csv')
    intraday_22 = pd.read_csv('22ndAprilSampleData.csv')
    
    # Standardizing the formats
    day_data['Date'] = pd.to_datetime(day_data['Date'], format='%d/%m/%y')
    intraday_19['Timestamp'] = pd.to_datetime(intraday_19['Date'] + ' ' + intraday_19['Time'], format='%d-%m-%Y %H:%M:%S')
    intraday_22['Timestamp'] = pd.to_datetime(intraday_22['Date'] + ' ' + intraday_22['Time'], format='%d/%m/%y %H:%M:%S')
    
    # Removing columns
    intraday_19 = intraday_19[['Timestamp', 'Stock Name', 'Last Traded Quantity']]
    intraday_22 = intraday_22[['Timestamp', 'Stock Name', 'Last Traded Quantity']]
    
    # Calculate 30-day avg pyvolumes
    avg_volumes_19 = calculate_30_day_average(day_data, '2024-04-19')
    avg_volumes_22 = calculate_30_day_average(day_data, '2024-04-22')
    
    # Compute results 
    results_19 = compute_rolling_volumes(intraday_19, avg_volumes_19, '2024-04-19')
    results_22 = compute_rolling_volumes(intraday_22, avg_volumes_22, '2024-04-22')
    
    # Combining results 
    final_results = pd.concat([results_19, results_22], ignore_index=True)
    final_results.to_csv('output.csv', index=False)
    print("Results saved to output.csv")

if __name__ == "__main__":
    main()
