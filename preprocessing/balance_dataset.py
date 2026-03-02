import pandas as pd
from sklearn.model_selection import train_test_split

def balance_and_split(df):
    """
    Ensure 1:1 ratio and stratified split
    """
    buggy = df[df['label'] == 1]
    clean = df[df['label'] == 0]
    
    # Undersample majority class
    min_size = min(len(buggy), len(clean))
    buggy = buggy.sample(n=min_size, random_state=42)
    clean = clean.sample(n=min_size, random_state=42)
    
    balanced = pd.concat([buggy, clean]).sample(frac=1, random_state=42)
    
    # Stratified split
    train, temp = train_test_split(
        balanced, test_size=0.2, stratify=balanced['label'], random_state=42
    )
    val, test = train_test_split(
        temp, test_size=0.5, stratify=temp['label'], random_state=42
    )
    
    return train, val, test

if __name__ == "__main__":
    # Apply to all data sources
    try:
        # Assuming parquet file exists
        df = pd.read_parquet('data/combined_raw.parquet')
        train, val, test = balance_and_split(df)

        train.to_parquet('data/train.parquet')
        val.to_parquet('data/val.parquet')
        test.to_parquet('data/test.parquet')
    except Exception as e:
        print(f"Error processing data: {e}")
