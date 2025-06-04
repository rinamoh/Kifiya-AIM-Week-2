# Week 2 Challenge: Customer Experience Analytics for Fintech Apps
## Task 1: Data Collection and Preprocessing
- Scraped 1,800 reviews from Google Play Store for CBE, BOA, and Dashen Bank.
- Preprocessed data: removed duplicates, handled missing values, normalized dates to YYYY-MM-DD format.
- Converted emojis to text using `emoji.demojize()` (e.g., 😊 to "smiling_face").
- Improved language detection using `fasttext` (previously `langdetect`) to accurately filter English reviews.
- English reviews saved in `data/clean_reviews.csv` (X reviews), non-English in `data/non_english_reviews.csv` (Y reviews).
- Used `google-play-scraper` for scraping and `pandas` for preprocessing.