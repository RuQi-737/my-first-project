# File: src/preprocessing.py
import sys
import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

# load function for 3.
def load_procurement(path):
    df = pd.read_csv(path, sep=";")
    for col in ["Planned Delivery Date", "Arrival Date", "Original Desired Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

# checks data format fr quantity columns for mixed localization formats and text-based corruption. Prints a report of the findings.
def audit_column_formats(df_dict, columns_to_check):
    """
    Scans specified columns and classifies the data format of every row to 
    identify mixed localization formats and text-based corruption.
    """
    print("--- DATA FORMAT AUDIT REPORT ---")

    # Regex patterns for classification
    us_pattern = re.compile(r'^-?\d+(?:\.\d+)?$')  # e.g., 98.0 or 1500
    eu_pattern = re.compile(
        r'^-?(?:\d{1,3}(?:\.\d{3})+|\d+)(?:,\d+)?$')  # e.g., 1.600.800,00
    # Contains letters (e.g., 'frog', 'pcs')
    text_pattern = re.compile(r'[a-zA-Z]')

    for key, df in df_dict.items():
        print(f"\nEvaluating Company {key}:")

        for col in columns_to_check:
            if col not in df.columns:
                continue

            # Convert to string, replace NaN strings with actual NaNs for counting
            s = df[col].astype(str).replace('nan', np.nan).dropna().str.strip()

            # Tally occurrences
            us_count = s.str.match(us_pattern).sum()
            eu_count = s.str.match(eu_pattern).sum()
            text_count = s.str.contains(text_pattern, na=False).sum()
            unclassified = len(s) - (us_count + eu_count + text_count)

            print(f"  Column: '{col}' | Total Valid Rows: {len(s)}")
            print(f"    - US/Standard Numeric (98.0):       {us_count}")
            print(f"    - European Numeric (1.600.800,00):  {eu_count}")
            print(f"    - Corrupt Text ('frog', '10 pcs'):  {text_count}")
            if text_count > 0:
                # Print exactly what the corrupt text is
                garbage_samples = s[s.str.contains(
                    text_pattern, na=False)].unique()[:5]
                print(f"      -> SAMPLES FOUND: {garbage_samples}")

# Removes duplicates and rows missing critical temporal/volumetric data. This is after step 4. .  After cleansing, prints the number of rows removed and remaining for each company.
def perform_structural_cleansing(df_dict):

    cleaned_dict = {}
    required_columns = ['Planned Delivery Date',
                        'Arrival Date', 'Ordered Quantity', 'Delivered Quantity']
    volume_columns = ['Ordered Quantity', 'Delivered Quantity']

    for key, df in df_dict.items():
        initial_rows = df.shape[0]
        df_clean = df.drop_duplicates()

        available_columns = [
            col for col in required_columns if col in df_clean.columns]
        df_clean = df_clean.dropna(subset=available_columns)

        # 2. Filter out European Data Formats
        for col in volume_columns:
            if col in df_clean.columns:
                # Cast safely to string for regex scanning
                raw_strings = df_clean[col].astype(str)

                # Flag strings that contain a comma OR have more than one dot
                is_european = raw_strings.str.contains(
                    r',', na=False) | (raw_strings.str.count(r'\.') > 1)

                # Drop flagged rows by keeping only what is NOT (~) European
                df_clean = df_clean[~is_european]

        final_rows = df_clean.shape[0]
        print(
            f"Company {key} Cleansing: Removed {initial_rows - final_rows} invalid rows. Remaining: {final_rows}")
        cleaned_dict[key] = df_clean

    return cleaned_dict

# After initial monovariat plot
# Executes secondary data cleansing by applying domain-specific volumetric and chronological threshold filters mapped to individual companies.
def data_cleansing_2(df_dict):

    cleaned_dict = {}

    for key, df in df_dict.items():
        initial_rows = df.shape[0]
        df_filtered = df.copy()

        # --- SHARED FILTER ---
        # Exclude zero or negative quantities (Addresses Company A Rule 2 & standardizes B)
        if 'Ordered Quantity' in df_filtered.columns and 'Delivered Quantity' in df_filtered.columns:
            df_filtered = df_filtered[(df_filtered['Ordered Quantity'] > 0) &
                                      (df_filtered['Delivered Quantity'] > 0)]

        # --- COMPANY A SPECIFIC FILTERS ---
        if key == 'A':
            # 1. Delete high quantities (>= 14000)
            if 'Ordered Quantity' in df_filtered.columns and 'Delivered Quantity' in df_filtered.columns:
                df_filtered = df_filtered[(df_filtered['Ordered Quantity'] < 14000) &
                                          (df_filtered['Delivered Quantity'] < 14000)]

            # (Dates for A appear in order, so no strict chronological filters applied here)

        # --- COMPANY B SPECIFIC FILTERS ---
        elif key == 'B':
            # 1. Restrict Arrival and Planned Dates to between 2010 and today
            if 'Arrival Date' in df_filtered.columns:
                df_filtered = df_filtered[(df_filtered['Arrival Date'].dt.year >= 2010) &
                                          (df_filtered['Arrival Date'].dt.year <= 2027)]

            if 'Planned Delivery Date' in df_filtered.columns:
                df_filtered = df_filtered[(df_filtered['Planned Delivery Date'].dt.year >= 2010) &
                                          (df_filtered['Planned Delivery Date'].dt.year <= 2027)]

            # 2. Cap/Filter Quantities at 100,000
            if 'Ordered Quantity' in df_filtered.columns and 'Delivered Quantity' in df_filtered.columns:
                df_filtered = df_filtered[(df_filtered['Ordered Quantity'] <= 100000) &
                                          (df_filtered['Delivered Quantity'] <= 100000)]

        # --- METRICS & RETURN ---
        final_rows = df_filtered.shape[0]
        dropped_rows = initial_rows - final_rows

        print(
            f"Company {key} Threshold Cleansing: Removed {dropped_rows} anomalous rows. Remaining: {final_rows}")
        cleaned_dict[key] = df_filtered

    return cleaned_dict


#After bivariate plot
# setting boundries on delays and quantity.
def data_clean_3(df_dict):

    cleaned_dict = {}

    for key, df in df_dict.items():
        initial_rows = df.shape[0]
        df_transformed = df.copy()

        # --- COMPANY A SPECIFIC FILTERS () ---
        if key == 'A':
            # 1. Cap Quantity at 250
            if 'Ordered Quantity' in df_transformed.columns:
                df_transformed['Ordered Quantity'] = df_transformed['Ordered Quantity'].clip(
                    upper=250)

        # --- COMPANY B SPECIFIC FILTERS () ---
        elif key == 'B':
            # 1. Cap Quantity at 10,000
            if 'Ordered Quantity' in df_transformed.columns:
                df_transformed['Ordered Quantity'] = df_transformed['Ordered Quantity'].clip(
                    upper=10000)

            # 2. Cap Delivery Delta between -30 and +400 days
            if 'Delivery_Delay_Days' in df_transformed.columns:
                df_transformed['Delivery_Delay_Days'] = df_transformed['Delivery_Delay_Days'].clip(
                    lower=-30, upper=400)

        # --- METRICS & RETURN ---
        final_rows = df_transformed.shape[0]

        # Validation print matching your style (Note: Winsorization does not drop rows)
        print(
            f"Company {key}: Capped extreme values. Total rows maintained: {final_rows}")

        cleaned_dict[key] = df_transformed

    return cleaned_dict
