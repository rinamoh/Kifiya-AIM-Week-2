import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Identify drivers and pain points (manual check based on output)
drivers = {}
pain_points = {}
banks = sentiment_df['bank'].unique()

for bank in banks:
    bank_data = sentiment_df[sentiment_df['bank'] == bank]
    # Drivers: High sentiment themes
    driver_themes = bank_data[bank_data['sentiment_score'] > 0.5].groupby('themes').size().nlargest(3).index
    drivers[bank] = list(driver_themes)
    # Pain points: Frequent negative themes or low sentiment
    pain_point_themes = bank_data[bank_data['sentiment_label'] == 'negative'].groupby('themes').size().nlargest(3).index
    pain_points[bank] = list(pain_point_themes)

print("Drivers by Bank:\n", drivers)
print("Pain Points by Bank:\n", pain_points)

# Compare banks based on sentiment and ratings
comparison = pd.DataFrame({
    'Average Sentiment': sentiment_by_bank,
    'Average Rating': reviews_df.groupby('bank')['rating'].mean()
})
print("Bank Comparison:\n", comparison)

# Plot comparison
comparison.plot(kind='bar', figsize=(10, 6))
plt.title('Bank Comparison: Sentiment and Rating')
plt.xlabel('Bank')
plt.ylabel('Score')
plt.savefig('visuals/bank_comparison.png')
plt.close()


import matplotlib.pyplot as plt
import seaborn as sns

# Create visuals folder
import os
os.makedirs('visuals', exist_ok=True)

# Plot 1: Sentiment Distribution
plt.figure(figsize=(10, 6))
sns.boxplot(x='bank', y='sentiment_score', data=sentiment_df)
plt.title('Sentiment Score Distribution by Bank')
plt.xlabel('Bank')
plt.ylabel('Sentiment Score')
plt.savefig('visuals/sentiment_distribution.png')
plt.close()

# Plot 2: Rating Distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='bank', hue='rating', data=reviews_df)
plt.title('Rating Distribution by Bank')
plt.xlabel('Bank')
plt.ylabel('Count')
plt.savefig('visuals/rating_distribution.png')
plt.close()

# Plot 3: Top Themes
top_themes = themes_by_bank.nlargest(5, 'count')
plt.figure(figsize=(12, 6))
sns.barplot(x='themes', y='count', hue='bank', data=top_themes)
plt.title('Top 5 Themes by Bank')
plt.xlabel('Theme')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig('visuals/top_themes.png')
plt.close()