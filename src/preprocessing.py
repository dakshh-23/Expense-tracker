import pandas as pd
import numpy as np

def get_cleaned_data():
    # 1. Synthetic Data Creation (Agar file na ho) [cite: 281]
    try:
        df = pd.read_csv("data/expenses.csv")
    except:
        data = {
            'Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'Category': np.random.choice(['Food', 'Transport', 'Rent', 'Shopping', 'Bills'], 100),
            'Description': 'Automatic Log',
            'Amount': np.random.randint(100, 5000, 100),
            'Type': 'Expense'
        }
        df = pd.DataFrame(data)
        # Salary data add karna income ke liye
        df.loc[0, ['Category', 'Amount', 'Type']] = ['Salary', 50000, 'Income']

    # 2. Cleaning [cite: 382, 385]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'])
    df['Category'] = df['Category'].str.strip().str.title()
    
    # 3. Feature Engineering [cite: 388, 390]
    df['Month'] = df['Date'].dt.month_name()
    df['Weekday'] = df['Date'].dt.day_name()
    df['Month_Num'] = df['Date'].dt.month
    
    return df