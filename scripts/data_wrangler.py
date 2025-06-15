import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from colorama import init, Fore
import os
import io

init()

def load_data(fname):
    try:
        return pd.read_csv(fname)
    except FileNotFoundError:
        print(Fore.LIGHTBLUE_EX + f"Error: The file '{fname}' was not found!")
        raise
    except pd.errors.ParserError:
        print(Fore.LIGHTRED_EX + f"Error: The file '{fname}' could not be parsed. Please check the file format.")
        raise
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error: {e}")
        raise

def show_df_info(df):
    print(Fore.MAGENTA + "\nDataFrame Info:")

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    print(Fore.LIGHTCYAN_EX + info_str)

    duplicates = df.duplicated().sum()
    print(Fore.MAGENTA + f"Number of duplicate rows:" + Fore.YELLOW + f" {duplicates}\n")
    return duplicates

def drop_duplicates(df):
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        confirm = input(Fore.MAGENTA + f"There are {duplicates} duplicate rows. Do you want to drop them? (y/n): ")
        if confirm.lower() == 'y':
            df = df.drop_duplicates()
            print(Fore.LIGHTGREEN_EX +"Duplicate rows removed.")
        else:
            print(Fore.LIGHTGREEN_EX + "No duplicates were dropped.")
    else:
        print(Fore.LIGHTGREEN_EX + "No duplicate rows found.")
    return df

def drop_columns(df, col_names):
    existing_cols = [col for col in col_names if col in df.columns]
    missing_cols = [col for col in col_names if col not in df.columns]
    
    if missing_cols:
        print(Fore.LIGHTYELLOW_EX + f"Warning: The following columns were not found and could not be dropped: {', '.join(missing_cols)}")

    if existing_cols:
        confirm = input(Fore.MAGENTA + f"Do you want to drop the columns {', '.join(existing_cols)}? (y/n): ")
        if confirm.lower() == 'y':
            df = df.drop(columns=existing_cols)
            print(Fore.LIGHTGREEN_EX + f"Columns dropped: {', '.join(existing_cols)}")
        else:
            print(Fore.LIGHTGREEN_EX + "No columns were dropped.")
    else:
        print(Fore.LIGHTGREEN_EX + "No columns were found to drop.")
    
    return df

def handle_missing_data(df, method='drop', fill_value=None):
    if method == 'drop':
        df = df.dropna()
        print(Fore.LIGHTGREEN_EX + "Rows with missing values dropped.")
    elif method == 'fill' and fill_value is not None:
        df = df.fillna(fill_value)
        print(Fore.LIGHTGREEN_EX + f"Missing values filled with {fill_value}.")
    elif method == 'mode':
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode()[0]
                df[col] = df[col].fillna(mode_value)
                print(Fore.LIGHTGREEN_EX + f"Missing values in column '{col}' filled with mode ({mode_value}).")
    else:
        print(Fore.LIGHTRED_EX  + "Invalid method or missing fill_value.")
    
    return df

def normalize_data(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
            print(Fore.LIGHTGREEN_EX + f"Column '{col}' normalized.")
        else:
            print(Fore.LIGHTRED_EX + f"Column '{col}' not found.")
    return df

def save_file(df, output_fname):
    if os.path.exists(output_fname):
        confirm = input(Fore.LIGHTYELLOW_EX +f"Warning: The file '{output_fname}' already exists. Do you want to overwrite it? (y/n): ")
        if confirm.lower() != 'y':
            print(Fore.LIGHTYELLOW_EX + "File not saved.")
            return
    
    df.to_csv(output_fname, index=False)
    print(Fore.LIGHTGREEN_EX + f"File saved as: {output_fname}")

def search_file_on_computer(filename):
    search_paths = ["/", "C:/", "D:/", "E:/", "F:/"]  
    print(Fore.LIGHTBLUE_EX + f"\nSearching for '{filename}'...")
    
    for search_path in search_paths:
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                full_path = os.path.join(root, filename)
                print(Fore.LIGHTGREEN_EX + f"\nFound: {full_path}")
                return full_path
    print(Fore.LIGHTRED_EX + "File not found!")
    return None

def main():
    fname = input(Fore.LIGHTGREEN_EX + '\nFile Name: ')
    if not fname.endswith('.csv'):
        fname += '.csv'

    full_path = search_file_on_computer(fname) 
    
    if full_path is None:
        return
    
    df = load_data(full_path)
    
    show_df_info(df)

    figsize = (min(20, len(df.columns)*2), 10)
    axes = df.hist(figsize=figsize)

    palette = sns.color_palette("husl", n_colors=len(df.columns))

    for ax, color in zip(axes.flatten(), palette):
        ax.grid(False)

        for patch in ax.patches:
            patch.set_facecolor(color)

    plt.tight_layout()
    plt.show(block= False)

    input(Fore.LIGHTGREEN_EX + "Press Enter to continue...\n") 
    
    drop_dupes = input(Fore.MAGENTA + "Do you want to drop duplicates? (y/n): ")
    if drop_dupes.lower() == 'y':
        df = drop_duplicates(df)
    
    drop_cols = input(Fore.MAGENTA + "Do you want to drop columns? (y/n): ")
    if drop_cols.lower() == 'y':
        col_names = input(Fore.MAGENTA + "Enter columns to drop (comma-separated): ").split(',')
        col_names = [col.strip() for col in col_names]
        df = drop_columns(df, col_names)
    
    missing_action = input(Fore.MAGENTA + "Do you want to handle missing data? (y/n): ")
    if missing_action.lower() == 'y':
        missing_method = input(Fore.MAGENTA + "Normalize, drop, or fill?: ")
        if missing_method.lower() == 'fill':
            fill_choice = input(Fore.MAGENTA + "Fill with 0 or mode? ")
            if fill_choice == '0':
                df = handle_missing_data(df, method='fill', fill_value=0)
            elif fill_choice.lower() == 'mode':
                df = handle_missing_data(df, method='mode')
        elif missing_method.lower() == 'normalize':
            normalize_columns = input(Fore.MAGENTA + "Enter columns to normalize (comma-separated): ").split(',')
            normalize_columns = [col.strip() for col in normalize_columns]
            df = normalize_data(df, normalize_columns)
    
    save_action = input(Fore.MAGENTA + "Do you want to save the file? (y/n): ")
    if save_action.lower() == 'y':
        output_fname = 'wrangled_' + f'{fname}'
        save_file(df, output_fname)

    print(Fore.LIGHTGREEN_EX + "\nData wrangled!\n")

if __name__ == '__main__':
    main()
    
