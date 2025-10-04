import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(description="Process 311 service request data to count complaints type by borough.")
    parser.add_argument("-i","--input_file", help="Path to the input CSV file containing 311 service request data.")
    parser.add_argument("-s","--start_date", help="Start date (MM/DD/YYYY).")
    parser.add_argument("-e","--end_date", help="End date (MM/DD/YYYY).")
    parser.add_argument("-o","--output_file", default=None, help="Path to the output CSV file to save the borough complaint counts.")
    args = parser.parse_args()
    
    # Read file
    df = pd.read_csv(args.input_file, usecols=["Created Date", "Borough", "Complaint Type"])
    
    df["Created Date"] = pd.to_datetime(df["Created Date"], errors="coerce")
    
    print("Sample raw Created Date values:")
    print(df["Created Date"].head(20))   # show first 20 parsed dates
    print("Number of NaT values:", df["Created Date"].isna().sum())
    print("Earliest date:", df["Created Date"].min())
    print("Latest date:", df["Created Date"].max())
    # Convert CLI args to datetime
    start_date = pd.to_datetime(args.start_date, format="%m/%d/%Y")
    end_date   = pd.to_datetime(args.end_date, format="%m/%d/%Y") + pd.Timedelta(days=1)

    dfrange = df[(df["Created Date"] >= start_date) & (df["Created Date"] < end_date)]

    print("Start:", start_date, " End:", end_date)
    print("Sample dates:", df["Created Date"].head())
    print("Rows after filter:", len(dfrange))


    if dfrange.empty:
        print("⚠️ No records found for the given date range.", file=sys.stderr)
        return
    
    # Group
    counts = dfrange.groupby(["Complaint Type", "Borough"]).size().reset_index(name='Count')
    
    # Save
    if args.output_file:
        counts.to_csv(args.output_file, index=False)
    else:
        counts.to_csv(sys.stdout, index=False)

if __name__ == "__main__":
    main()

'''
import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(description="Process 311 service request data to count complaints type by borough.")

    parser.add_argument("-i","--input_file", help="Path to the input CSV file containing 311 service request data.")
    parser.add_argument("-s","--start_date", help="start date.")
    parser.add_argument("-e", "--end_date", help="end date.")
    parser.add_argument("-o", "--output_file", default = None, help="Path to the output CSV file to save the borough complaint counts.")
    args = parser.parse_args()
    
    #Read file given by user
    df = pd.read_csv(args.input_file, usecols=["Created Date", "Borough", "Complaint Type"])
    df["Created Date"] = pd.to_datetime(df["Created Date"], format="%m/%d/%Y", errors='coerce')
    start_date = pd.to_datetime(args.start_date, format="%m/%d/%Y")
    end_date   = pd.to_datetime(args.end_date, format="%m/%d/%Y")
    dfrange = df[(df["Created Date"] >= start_date) & (df["Created Date"] <= end_date)]

    #Group by borough and complaint type, count occurrences
    counts = dfrange.groupby(["Complaint Type", "Borough"]).size().reset_index(name ='Count')
    
    #Save to output file or print to stdout
    if args.output_file:
        counts.to_csv(args.output_file, index=False)
    else:
        counts.to_csv(sys.stdout, index=False)

if __name__ == "__main__":
   main()
'''