from flask import Blueprint, request, jsonify

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/chat-api', methods=['POST'])
def chat_api():
    import re
    from datetime import datetime, timedelta
    from Apps.crop import get_weather 
    from deep_translator import GoogleTranslator

    data = request.json
    user_message = data.get('message', '').lower()
    lang = data.get('language', 'en-US') 
    
    target_lang = lang.split('-')[0] if '-' in lang else lang

    # Translate input
    try:
        if target_lang != 'en':
            translated_text = GoogleTranslator(source='auto', target='en').translate(user_message).lower()
            if translated_text:
                user_message = translated_text
            print(f"DEBUG: Input: {data.get('message')} | Translated: {user_message}")
    except Exception as e:
        print(f"Translation Error: {e}")

    bot_reply = "I am still learning. Please try asking about weather, prices, or crop recommendations."

    # --- NLU LOGIC ---
    
    # 1. Weather & Forecast Logic
    if "weather" in user_message or "mausam" in user_message or "forecast" in user_message:
        city = None
        target_day_index = 0 # Default: Today
        day_name = "today"

        # Time Logic: Detect "tomorrow", "day after"
        if "tomorrow" in user_message:
            target_day_index = 1
            day_name = "tomorrow"
        elif "next week" in user_message:
            target_day_index = 7 # Just a sample point in future
            day_name = "next week"
        
        # City Extraction Logic (Improved)
        # Priority 1: Explicit "in [City]"
        match_explicit = re.search(r'(?:in|at|for|of|like)\s+(\w+)', user_message)
        if match_explicit:
            possible_city = match_explicit.group(1)
            if possible_city not in ['today', 'tomorrow', 'now', 'here', 'please', 'the']:
                city = possible_city
        
        # Priority 2: Direct "Weather [City]"
        if not city:
            match_direct = re.search(r'weather\s+(\w+)', user_message)
            if match_direct:
                possible_city = match_direct.group(1)
                if possible_city not in ['in', 'at', 'today', 'tomorrow']:
                    city = possible_city

        # Priority 3: Fallback Hindi
        if not city and "mausam" in user_message:
             match_hi = re.search(r'(\w+)\s+(?:ka|ke|me|mein)\s+mausam', user_message)
             if match_hi:
                 city = match_hi.group(1)

        if city:
            data = get_weather(city)
            if data and 'days' in data:
                # Ensure index is within range (usually 15 days data)
                if target_day_index >= len(data['days']):
                    target_day_index = len(data['days']) - 1 # cap at max
                
                forecast = data['days'][target_day_index]
                temp = forecast['temp']
                cond = forecast['conditions']
                date = forecast['datetime']
                
                bot_reply = f"The weather in {city.capitalize()} for {day_name} ({date}) is {temp}°C with {cond.lower()}."
            else:
                bot_reply = f"Sorry, I couldn't fetch the forecast for {city}."
        else:
            bot_reply = "Please tell me the city name, for example: 'Weather in Mumbai tomorrow'."

    # 2. Greeting Logic
    elif re.search(r'\b(hello|hi|namaste)\b', user_message):
        bot_reply = "Namaste! I am your Agri-Advisor. Ask me about weather, prices, or crop recommendations."
    
    # 3. Market Price Logic
    elif "price" in user_message or "cost" in user_message or "bhav" in user_message or "rate" in user_message:
        bot_reply = "You can check the daily Mandi rates in our 'Market Prices' section."
        
    # 4. Smart Seasonal Crop Advice
    elif any(word in user_message for word in ["crop", "grow", "plant", "season", "sowing", "suggest", "best"]):
        current_month = datetime.now().month
        
        # Extended Logic:
        # If user provided a city (e.g. "Best crop for Delhi"), we could fetch weather. 
        # For now, we use general seasonal + hypothetical weather logic for robustness.
        
        advice = ""
        season = ""
        
        # Rabi (Winter)
        if current_month >= 10 or current_month <= 3:
            season = "Rabi (Winter)"
            intro = "Since it is Winter (Rabi season):"
            advice = "Wheat and Mustard are excellent choices. If you have irrigation, Chickpea yields well. For vegetables, Potato and Spinach are best suited for the cool nights."
            
        # Zaid (Summer)
        elif 4 <= current_month <= 6:
            season = "Zaid (Summer)"
            intro = "Since it is Summer (Zaid season):"
            advice = "Watermelon, Musk Melon, and Cucumber are profitable short-duration crops. Ensure you have sufficient water supply. Bitter Gourd is also pest-resistant in this season."
            
        # Kharif (Monsoon)
        else:
            season = "Kharif (Monsoon)"
            intro = "Since it is Monsoon (Kharif season):"
            advice = "Rice (Paddy) is the primary crop if rainfall is good. For areas with less rain, Maize and Soybean are safer bets. Cotton is high-value but requires pest management."

        bot_reply = f"{intro} {advice} \n(Tip: Valid for temperature 15-25°C. Check local soil health too!)"

    elif "thank" in user_message:
        bot_reply = "You're welcome! Happy Farming."

    # Translate Reply back
    if target_lang != 'en':
        try:
            bot_reply = GoogleTranslator(source='en', target=target_lang).translate(bot_reply)
        except Exception as e:
            print(f"Output Translation Error: {e}")

    return jsonify({'reply': bot_reply})