# Week 2 Challenge: Customer Experience Analytics for Fintech Apps
## Task 1: Data Collection and Preprocessing
- Scraped 1,800 reviews from Google Play Store for CBE, BOA, and Dashen Bank.
- Preprocessed data: removed duplicates, handled missing values, normalized dates to YYYY-MM-DD format.
- Converted emojis to text using `emoji.demojize()` (e.g., 😊 to "smiling_face").
- Improved language detection using `fasttext` (previously `langdetect`) to accurately filter English reviews.
- English reviews saved in `data/clean_reviews.csv` (X reviews), non-English in `data/non_english_reviews.csv` (Y reviews).
- Used `google-play-scraper` for scraping and `pandas` for preprocessing.

## Task 2: Sentiment and Thematic Analysis
- Performed sentiment analysis using DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`).
- Classified reviews as positive, negative, or neutral (threshold: 0.6).
- Optimized DistilBERT usage with batch processing (e.g., 100-review chunks).
- Extracted keywords using spaCy and clustered into 5 themes per bank: Account Access Issues, Transaction Performance, User Interface Experience, Customer Support, App Reliability.
- Refined theme mappings using keyword frequencies (e.g., added 'screenshot' for CBE UI, 'crashes' for BOA reliability) with stemming to reduce 'Other' labels from X% to Y%.
- Results saved in `data/reviews_with_keywords.csv`, keyword frequencies in `data/keyword_frequencies.txt`, and theme statistics in `data/theme_statistics.txt`.