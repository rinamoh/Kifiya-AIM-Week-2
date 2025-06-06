import pandas as pd
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

# Load reviews with sentiment
try:
    df = pd.read_csv("data/reviews_with_sentiment.csv")
    required_columns = ["review", "rating", "date", "bank", "source", "sentiment_label", "sentiment_score"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing columns: {missing_cols}")
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Preprocess text with lemmatization
def preprocess_text(review):
    doc = nlp(str(review).lower())
    tokens = [token.lemma_ for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"] and not token.is_stop and len(token.text) > 2]
    return " ".join(tokens) if tokens else "no_keywords"

print("Preprocessing reviews...")
df['processed_text'] = df['review'].apply(preprocess_text)

# Extract keywords using TF-IDF
tfidf = TfidfVectorizer(max_features=50, ngram_range=(1, 2))
tfidf_matrix = tfidf.fit_transform(df['processed_text'])
feature_names = tfidf.get_feature_names_out()

def extract_keywords_tfidf(row_idx, top_n=5):
    row = tfidf_matrix[row_idx].toarray()[0]
    if row.sum() == 0:
        return []
    keyword_indices = row.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in keyword_indices if row[i] > 0]

print("Extracting keywords with TF-IDF...")
df['keywords'] = [extract_keywords_tfidf(i) for i in range(len(df))]

# Group keywords by bank and count frequency
def group_keywords(keywords_series):
    all_keywords = [kw for keywords in keywords_series for kw in keywords]
    return Counter(all_keywords).most_common(50)

print("Grouping keywords by bank...")
themes_by_bank = {}
for bank in df['bank'].unique():
    bank_keywords = df[df['bank'] == bank]['keywords']
    themes_by_bank[bank] = group_keywords(bank_keywords)

# Theme mappings based on keyword frequencies
theme_mappings = {
    "CBE": {
        "Account Access Issues": ["access", "login", "error", "fail"],
        "Transaction Performance": ["transaction", "transfer", "slow", "fast"],
        "User Interface Experience": ["screenshot", "screen", "design", "ui"],
        "Customer Support": ["service", "support", "help"],
        "App Reliability": ["update", "fix", "work", "crash"]
    },
    "BOA": {
        "Account Access Issues": ["access", "login", "error", "fail"],
        "Transaction Performance": ["transaction", "transfer", "slow", "fast"],
        "User Interface Experience": ["design", "ui", "screen"],
        "Customer Support": ["service", "support", "help"],
        "App Reliability": ["work", "fix", "crash", "crashes", "error"]
    },
    "Dashen": {
        "Account Access Issues": ["access", "login", "error", "fail"],
        "Transaction Performance": ["transaction", "transfer", "slow", "fast"],
        "User Interface Experience": ["design", "ui", "feature", "step"],
        "Customer Support": ["service", "support", "help", "chat"],
        "App Reliability": ["work", "fix", "crash", "update"]
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

# Save keyword frequencies (fix for list of tuples)
with open("data/keyword_frequencies.txt", "w") as f:
    for bank, freqs in themes_by_bank.items():
        f.write(f"\n{bank}:\n")
        for keyword, count in freqs:  # Unpack tuple directly
            f.write(f"{keyword}: {count}\n")

# Aggregate theme frequencies
theme_stats = {}
for bank in df['bank'].unique():
    bank_reviews = df[df['bank'] == bank]
    all_themes = [theme for themes in bank_reviews['themes'] for theme in themes]
    theme_stats[bank] = Counter(all_themes)

# Save theme statistics
with open("data/theme_statistics.txt", "w") as f:
    for bank, stats in theme_stats.items():
        f.write(f"\n{bank}:\n")
        for theme, count in stats.items():
            f.write(f"{theme}: {count}\n")

# Save results
df.to_csv("data/reviews_with_keywords.csv", index=False)
print(f"Saved {len(df)} reviews with keywords and themes to data/reviews_with_keywords.csv")