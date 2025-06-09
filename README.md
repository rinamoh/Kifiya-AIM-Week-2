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
- Optimized DistilBERT with batch processing (e.g., 100-review chunks).
- Extracted keywords using spaCy with TF-IDF and n-grams (e.g., "login error"), lemmatized with spaCy.
- Clustered into 5 themes per bank: Account Access Issues, Transaction Performance, User Interface Experience, Customer Support, App Reliability.
- Fixed AttributeError in keyword frequency saving; results saved in `data/reviews_with_keywords.csv`, keyword frequencies in `data/keyword_frequencies.txt`, and theme statistics in `data/theme_statistics.txt`.

## Task 3 : Store Cleaned Data in Oracle
- created `bank_reviews` tablespace 
- defined schema 
- inserted >1,000 reviews using `scripts/insert_reviews_oracle.py` in Visual Studio Code, and saved SQL dump as `db/bank_reviews.dmp`.
- Results saved in `data/reviews_with_keywords.csv`, keyword frequencies in `data/keyword_frequencies.txt`, and theme statistics in `data/theme_statistics.txt`.
- Scraped 1,800 reviews from Google Play Store for CBE, BOA, and Dashen Bank.
- Created a database named bank_reviews and defined schema:
- Banks Table: Stores bank information.
- Reviews Table: Stores scraped and processed review data.
- Inserted over 1,000 reviews using Python script scripts/insert_reviews_oracle.py with cx_Oracle.
- Resolved SYS schema export issues by creating bank_user, moving tables, and generating SQL dump.

## Task 4: Insights and Recommendations
- Scraped 1,800 reviews from Google Play Store for CBE, BOA, and Dashen Bank.
- Derived insights from sentiment and theme analysis:
- Identified drivers (e.g., Customer Support, Transaction Performance) and pain points (e.g., App Reliability, Other) per bank.
- Compared banks using average sentiment (0.98–0.99) and ratings (BOA: 2.52, CBE: 4.09, Dashen: 4.41).
- Suggested 2+ improvements per bank (e.g., enhance app reliability, promote customer support).
- Created 3 visualizations: sentiment distribution, rating distribution, and top themes (saved in visuals/).
- Used pandas for analysis, matplotlib/seaborn for plots, and Git for version control.
 

  
