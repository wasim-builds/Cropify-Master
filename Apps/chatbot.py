from flask import Blueprint, request, jsonify

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/chat-api', methods=['POST'])
def chat_api():
    from Apps.crop import get_weather 
    import re
    from deep_translator import GoogleTranslator

    data = request.json
    user_message = data.get('message', '').lower()
    lang = data.get('language', 'en-US') # Default to English
    
    # Extract language code (e.g., 'hi-IN' -> 'hi')
    target_lang = lang.split('-')[0] if '-' in lang else lang

    # Translate to English if not already
    try:
        if target_lang != 'en':
            translated_text = GoogleTranslator(source='auto', target='en').translate(user_message).lower()
            if translated_text:
                user_message = translated_text
            print(f"DEBUG: Input: {data.get('message')} | Translated: {user_message}")
    except Exception as e:
        print(f"Translation Error: {e}")

    bot_reply = "I am still learning. Please try asking about weather, prices, or crop recommendations."

    # Pattern matching
    # 1. Weather Logic (English or Hindi keywords)
    if "weather" in user_message or "mausam" in user_message:
        city = None
        
        # Priority 1: Explicit "in/at/for [City]" pattern anywhere in sentence
        # Matches: "weather today in Delhi", "what is the weather for Mumbai", "weather at Pune"
        match_explicit = re.search(r'(?:in|at|for|of|like)\s+(\w+)', user_message)
        if match_explicit:
            possible_city = match_explicit.group(1)
            # Filter out common stopwords if they were accidentally captured
            if possible_city not in ['today', 'tomorrow', 'now', 'here', 'please', 'the']:
                city = possible_city

        # Priority 2: "Weather [City]" pattern (if no preposition found)
        # Matches: "Weather Delhi", "Weather Pune please"
        if not city:
            match_direct = re.search(r'weather\s+(\w+)', user_message)
            if match_direct:
                possible_city = match_direct.group(1)
                if possible_city not in ['in', 'at', 'for', 'of', 'like', 'is', 'was', 'today', 'tomorrow', 'now']:
                    city = possible_city

        # Priority 3: Fallback Hindi pattern
        if not city and "mausam" in user_message:
             match_hi = re.search(r'(\w+)\s+(?:ka|ke|me|mein)\s+mausam', user_message)
             if match_hi:
                 city = match_hi.group(1)

        if city:
            data = get_weather(city)
            if data and 'currentConditions' in data:
                temp = data['currentConditions']['temp']
                cond = data['currentConditions']['conditions']
                bot_reply = f"The weather in {city.capitalize()} is {temp} degrees Celsius with {cond.lower()}."
            else:
                bot_reply = f"Sorry, I couldn't fetch the weather for {city}. Please ensure the city name is correct."
        else:
            bot_reply = "I understood you want to know the weather, but I missed the city name. Please say 'Weather in [City Name]'."

    # 2. Greeting Logic (Strict Word Boundary)
    elif re.search(r'\b(hello|hi|namaste)\b', user_message):
        bot_reply = "Namaste! I am your Agri-Advisor. Ask me about weather, prices, or crop recommendations."
    
    elif "price" in user_message or "cost" in user_message or "bhav" in user_message:
        bot_reply = "You can check the daily Mandi rates in our 'Market Prices' section."
        
    elif "thank" in user_message:
        bot_reply = "You're welcome! Happy Farming."

    # Translate Reply back to Target Language
    if target_lang != 'en':
        try:
            bot_reply = GoogleTranslator(source='en', target=target_lang).translate(bot_reply)
        except Exception as e:
            print(f"Output Translation Error: {e}")

    return jsonify({'reply': bot_reply})