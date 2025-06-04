import pandas as pd
import spacy
from collections import Counter

  # Load reviews with sentiment
df = pd.read_csv("data/reviews_with_sentiment.csv")

  # Initialize spaCy
nlp = spacy.load("en_core_web_sm")

  # Extract keywords (nouns, adjectives, and verbs for broader coverage)
def extract_keywords(review):
      doc = nlp(review.lower())
      keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"] and not token.is_stop and len(token.text) > 2]
      return keywords

print("Extracting keywords...")
df['keywords'] = df['review'].apply(extract_keywords)

  # Group keywords by bank and count frequency
def group_keywords(keywords_series):
      all_keywords = [kw for keywords in keywords_series for kw in keywords]
      return Counter(all_keywords).most_common(50)  # Top 50 for broader theme identification

print("Grouping keywords by bank...")
themes_by_bank = {}
for bank in df['bank'].unique():
      bank_keywords = df[df['bank'] == bank]['keywords']
      themes_by_bank[bank] = group_keywords(bank_keywords)

  # Define 5 themes per bank (manual clustering based on keyword frequency and domain knowledge)
theme_mappings = {
    "CBE": {
        "Account Access Issues": ["access", "login", "log", "fail", "error", "auth", "sign"],
        "Transaction Performance": ["transact", "transfer", "pay", "fast", "slow", "delay", "load"],
        "User Interface Experience": ["screenshot", "screen", "design", "navigat", "ui", "layout", "button"],
        "Customer Support": ["servic", "help", "support", "contact", "respond"],
        "App Reliability": ["update", "fix", "work", "bug", "crash", "freez", "stabl"]
    },
    "BOA": {
        "Account Access Issues": ["access", "login", "log", "fail", "error", "auth", "sign"],
        "Transaction Performance": ["transact", "transfer", "pay", "fast", "slow", "delay", "load"],
        "User Interface Experience": ["design", "navigat", "ui", "layout", "screen", "button"],
        "Customer Support": ["servic", "help", "support", "contact", "respond"],
        "App Reliability": ["work", "fix", "crash", "crashes", "bug", "freez", "update", "error"]
    },
    "Dashen": {
        "Account Access Issues": ["access", "login", "log", "fail", "error", "auth", "sign"],
        "Transaction Performance": ["transact", "transfer", "pay", "fast", "slow", "delay", "load"],
        "User Interface Experience": ["design", "navigat", "ui", "layout", "screen", "button", "feature", "step"],
        "Customer Support": ["servic", "help", "support", "contact", "respond", "chat"],
        "App Reliability": ["work", "fix", "crash", "bug", "freez", "stabl", "update"]
    }
}

  # Assign themes to reviews
def assign_themes(keywords, bank):
      themes = []
      for theme, theme_keywords in theme_mappings[bank].items():
          if any(kw in theme_keywords for kw in keywords):
              themes.append(theme)
      return themes if themes else ["Other"]

print("Assigning themes...")
df['themes'] = df.apply(lambda row: assign_themes(row['keywords'], row['bank']), axis=1)

  # Save keyword frequencies for reference
with open("data/keyword_frequencies.txt", "w") as f:
      for bank, freqs in themes_by_bank.items():
          f.write(f"\n{bank}:\n")
          for keyword, count in freqs:
              f.write(f"{keyword}: {count}\n")

  # Save results
df.to_csv("data/reviews_with_keywords.csv", index=False)
print(f"Saved {len(df)} reviews with keywords and themes to data/reviews_with_keywords.csv")