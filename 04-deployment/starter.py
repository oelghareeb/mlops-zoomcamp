#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import argparse

# Function to read data from a parquet file
def read_data(year, month):
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    df = pd.read_parquet(url)
    
    # Calculate duration in minutes
    df['duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    
    # Filter data based on duration
    df = df[(df['duration'] >= 1) & (df['duration'] <= 60)].copy()
    
    # Convert categorical columns to strings
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate mean predicted duration for a given month and year.')
    parser.add_argument('year', type=int, help='Year of the data (e.g., 2023)')
    parser.add_argument('month', type=int, help='Month of the data (e.g., 3 for March)')
    args = parser.parse_args()

    # Load the trained model and data vectorizer
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)

    # Read data for the specified year and month
    df = read_data(args.year, args.month)

    # Transform categorical columns and predict durations
    dicts = df[['PULocationID', 'DOLocationID']].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    # Calculate mean predicted duration
    mean_predicted_duration = y_pred.mean()

    # Print the mean predicted duration
    print(f"The mean predicted duration for {args.year}/{args.month} is: {mean_predicted_duration:.2f} minutes.")
