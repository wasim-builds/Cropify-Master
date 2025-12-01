from flask import Blueprint, request, jsonify

chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/chat-api', methods=['POST'])
def chat_api():
    user_message = request.json.get('message', '').lower()
    
    # Simple Rule-Based Logic (You can expand this!)
    if "hello" in user_message or "hi" in user_message:
        bot_reply = "Namaste! How can I help you with your crops today?"
    elif "weather" in user_message:
        bot_reply = "You can check the latest weather forecast in our 'Weather' section."
    elif "price" in user_message or "cost" in user_message:
        bot_reply = "Market prices change daily. Please check the 'Shop' for seed and fertilizer prices."
    elif "disease" in user_message:
        bot_reply = "If your crop has a disease, please upload a photo in the 'Crop Disease' section."
    elif "soil" in user_message:
        bot_reply = "Soil health is vital! Use our recommendation tool to find the best crop for your soil."
    else:
        bot_reply = "I am still learning. Please try asking about weather, crops, or diseases."

    return jsonify({'reply': bot_reply})