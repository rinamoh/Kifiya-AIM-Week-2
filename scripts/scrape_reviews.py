from google_play_scraper import reviews
import pandas as pd

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
          count=500  # 400 reviews per bank
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
df.to_csv("data/clean_reviews.csv", index=False)
print(f"Saved {len(df)} cleaned reviews to data/clean_reviews.csv")