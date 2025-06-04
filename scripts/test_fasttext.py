import fasttext

# Load the model
model = fasttext.load_model("lid.176.bin")

# Test language detection
text = "This is an English review"
prediction = model.predict(text)[0][0]
print(prediction)  # Should print '__label__en'