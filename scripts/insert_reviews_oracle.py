import pandas as pd
import cx_Oracle

# Load cleaned data
df = pd.read_csv("data/clean_reviews.csv")
sentiment_df = pd.read_csv("data/reviews_with_sentiment.csv")
df = df.merge(sentiment_df[['review', 'sentiment_label', 'sentiment_score']], on='review', how='left')

# Oracle connection
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
connection = cx_Oracle.connect(user="sys", password="pass123", dsn=dsn, mode=cx_Oracle.SYSDBA)  # Replace with your sys password
cursor = connection.cursor()

# Insert into Banks table
banks = {"CBE": 1, "BOA": 2, "Dashen": 3}
for bank_name, bank_id in banks.items():
    cursor.execute("INSERT INTO Banks (bank_id, bank_name) VALUES (:1, :2)", (bank_id, bank_name))

# Insert into Reviews table
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Reviews (review_id, bank_id, review_text, rating, date_posted, source, sentiment_label, sentiment_score)
        VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8)
    """, (index + 1, banks.get(row['bank'], 1), row['review'], row['rating'], row['date'], row['source'], row['sentiment_label'], row['sentiment_score']))

# Commit and close
connection.commit()
cursor.close()
connection.close()

print(f"Inserted {len(df)} reviews into Oracle database")