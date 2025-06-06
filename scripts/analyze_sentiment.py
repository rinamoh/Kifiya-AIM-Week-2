import pandas as pd
from transformers import pipeline

# Load cleaned reviews
df = pd.read_csv("data/clean_reviews.csv")

# Initialize DistilBERT sentiment analysis pipeline
print("Loading DistilBERT model...")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Compute sentiment for each review
def get_sentiment(review):
    try:
        result = sentiment_analyzer(review)[0]
        return result['label'].lower(), result['score']
    except Exception as e:
        print(f"Error processing review: {review[:50]}... | Error: {e}")
        return "neutral", 0.0

print("Analyzing sentiment...")
df[['sentiment_label', 'sentiment_score']] = df['review'].apply(
    lambda x: pd.Series(get_sentiment(x))
)

# Map low-confidence scores to neutral
df['sentiment_label'] = df.apply(
    lambda row: 'neutral' if row['sentiment_score'] < 0.6 else row['sentiment_label'],
    axis=1
)

# Save results
df.to_csv("data/reviews_with_sentiment.csv", index=False)
print(f"Saved {len(df)} reviews with sentiment to data/reviews_with_sentiment.csv")