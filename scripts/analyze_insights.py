import pandas as pd

# Load cleaned reviews from Task 1
reviews_df = pd.read_csv('data/clean_reviews.csv')
# Load sentiment and theme data from Task 2
sentiment_df = pd.read_csv('data/reviews_with_keywords.csv')
print("Reviews Data Preview:\n", reviews_df.head())
print("Sentiment Data Preview:\n", sentiment_df.head())
# Calculate average sentiment by bank
sentiment_by_bank = sentiment_df.groupby('bank')['sentiment_score'].mean()
print("Average Sentiment by Bank:\n", sentiment_by_bank)

# Count themes by bank
themes_by_bank = sentiment_df.groupby(['bank', 'themes']).size().reset_index(name='count')
print("Theme Counts by Bank:\n", themes_by_bank.sort_values(['bank', 'count'], ascending=[True, False]))