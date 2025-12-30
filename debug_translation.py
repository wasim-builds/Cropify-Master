from deep_translator import GoogleTranslator

text = "Delhi ka mausam kaisa hai"
translated = GoogleTranslator(source='auto', target='en').translate(text).lower()
print(f"Original: {text}")
print(f"Translated: {translated}")
