import sqlite3
import pandas as pd

try:
    # Connect to the lesson database
    connection = sqlite3.connect('../db/lesson.db')
    
    # SQL query to join line_items and products tables
    query = '''
        SELECT 
            li.line_item_id,
            li.quantity,
            li.product_id,
            p.product_name,
            p.price
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
    '''
    
    # Read data into DataFrame
    df = pd.read_sql_query(query, connection)
    
    # Print first 5 lines
    print("--- First 5 lines of DataFrame ---")
    print(df.head())
    
    # Add total column (quantity * price)
    df['total'] = df['quantity'] * df['price']
    
    # Print first 5 lines with total column
    print("\n--- First 5 lines with total column ---")
    print(df.head())
    
    # Group by product_id and aggregate
    df_grouped = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    }).reset_index()
    
    # Rename columns for clarity
    df_grouped.columns = ['product_id', 'order_count', 'total_price', 'product_name']
    
    # Print first 5 lines of grouped data
    print("\n--- First 5 lines of grouped data ---")
    print(df_grouped.head())
    
    # Sort by product_name
    df_grouped = df_grouped.sort_values('product_name')
    
    # Write to CSV file
    df_grouped.to_csv('order_summary.csv', index=False)
    print("\n--- DataFrame written to order_summary.csv ---")
    
    # Display the final DataFrame
    print("\n--- Final DataFrame (sorted by product_name) ---")
    print(df_grouped)
    
    connection.close()
except Exception as e:
    print(f"An error occurred: {e}")
