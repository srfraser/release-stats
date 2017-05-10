#!/usr/bin/env python3

"""
Highest duration and delay
Highest Variation in duration and delay
Largest outliers (solid core, low stddev, outliers)
"""

import pandas as pd


def main():
    df = pd.read_csv('rundata1.csv')
    # convert from strings
    df['duration'] = pd.to_timedelta(df['duration'])
    df['delay'] = pd.to_timedelta(df['delay'])

    print(df.groupby('workertype')['duration'].describe())
    print(df.groupby('workertype')['delay'].describe())


if __name__ == '__main__':
    main()
