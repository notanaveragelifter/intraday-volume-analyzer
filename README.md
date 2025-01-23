Intraday Volume Analyzer
Analyze intraday trading data to identify the timestamp when the cumulative traded volume within a 60-minute rolling window first exceeds the stock’s 30-day average volume.

Features
30-Day Average Calculation: Calculates the average daily trading volume for each stock from prior 30 trading days.
Cumulative Volume Analysis: Tracks rolling 60-minute cumulative traded volume starting at 9:15 AM.
Threshold Detection: Identifies timestamps for volume crossover or returns None if no crossover occurs.
Files
main.py: Orchestrates the entire analysis, from loading data to identifying timestamps.
functions.py: Contains modular functions for calculations and processing.
Data Files: Input files include daily aggregated data and second-by-second intraday trading data.
Usage
Clone the repository:
bash
Copy
Edit
git clone https://github.com/notanaveragelifter/intraday-volume-analyzer.git
cd intraday-volume-analyzer
Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
Run the script:
bash
Copy
Edit
python main.py
Output
The script outputs timestamps for each stock when the 60-minute rolling volume exceeds the 30-day average, or None if no crossover occurs.

Example:

json
Copy
Edit
{
  "stock_name": "ABC Corp",
  "date": "2024-04-19",
  "threshold_cross_timestamp": "10:30:00"
}
Notes
Designed for large datasets with efficient rolling calculations.
Outputs results in CSV format.
