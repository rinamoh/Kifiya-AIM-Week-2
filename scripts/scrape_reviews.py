from google_play_scraper import reviews
import pandas as pd
import fasttext
import emoji

# Load fasttext language detection model
model = fasttext.load_model("lid.176.bin")


  # App IDs for the banks (you can find these by searching the app on Google Play and checking the URL)
apps = {
      "CBE": "com.combanketh.mobilebanking",
      "BOA": "com.boa.boaMobileBanking",
      "Dashen": "com.dashen.dashensuperapp"
  }

  # Scrape reviews
all_reviews = []
for bank, app_id in apps.items():
      print(f"Scraping reviews for {bank}...")
      reviews_data = reviews(
          app_id,
          lang='en',  # English reviews
          country='et',  # Ethiopia
          count=600  # 400 reviews per bank
      )
      for review in reviews_data[0]:
          all_reviews.append({
              "review": review['content'],
              "rating": review['score'],
              "date": review['at'].strftime('%Y-%m-%d'),
              "bank": bank,
              "source": "Google Play"
          })

  # Save to CSV
df = pd.DataFrame(all_reviews)
df.to_csv("data/reviews.csv", index=False)
print(f"Saved {len(df)} reviews to data/reviews.csv")

 # Preprocess: remove duplicates, handle missing data, ensure date format
df = df.drop_duplicates(subset=["review"])  # Remove duplicate reviews
df = df.dropna()  # Remove rows with missing values
df["date"] = pd.to_datetime(df["date"]).dt.strftime('%Y-%m-%d')  # Ensure date format

#remove or convert emojis
df['review'] = df['review'].apply(lambda x: emoji.demojize(x, delimiters=(" ", " ")))

# Detect language
def detect_language(text):
    # Clean text: fasttext expects a single line with no newlines
    text = text.replace('\n', ' ')
    # Predict language
    prediction = model.predict(text)[0][0]  # e.g., '__label__en' or '__label__am'
    return prediction.replace('__label__', '')  # Returns 'en' or 'am'

print("Detecting languages...")
df['language'] = df['review'].apply(detect_language)

# Filter for English reviews
df_english = df[df['language'] == 'en']
df_non_english = df[df['language'] != 'en']

# Save both datasets
df_english.to_csv("data/clean_reviews.csv", index=False)
df_non_english.to_csv("data/non_english_reviews.csv", index=False)
print(f"Saved {len(df_english)} English reviews to data/clean_reviews.csv")
print(f"Saved {len(df_non_english)} non-English reviews to data/non_english_reviews.csv")