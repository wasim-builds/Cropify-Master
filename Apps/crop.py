from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from werkzeug.utils import secure_filename
from Models import QueryModel
from extensions import db
import requests
from utils import *
from Apps.icon_utils import get_icon_url
from fpdf import FPDF # Import PDF library

crop = Blueprint('crop', __name__)

@crop.route('/fertilizer', methods = ['GET', 'POST'])
def fertilizer():
    crops = crop_types()
    soils = soil_types()

    if request.method == 'POST':
        n = request.form.get('nitrogen')
        p = request.form.get('phosphorous')
        k = request.form.get('potassium')
        temp = request.form.get('temp')
        hum = request.form.get('humidity')
        mos = request.form.get('Moisture')
        crop_name = request.form.get('crop')
        soil = request.form.get('soil')

        result = predict_fertilizer(temp, hum, mos, soil, crop_name, n, p, k)

        # Save result in session to print later
        session['last_report'] = {
            'type': 'Fertilizer Recommendation',
            'inputs': {'Crop': crop_name, 'Soil': soil, 'Nitrogen': n, 'Phosphorus': p},
            'result': result
        }

        context = { 'crops': enumerate(crops), 'soils': enumerate(soils), 'result': result }
        return render_template("crop/fertilizer.html", **context)

    context = { 'crops': enumerate(crops), 'soils': enumerate(soils) }
    return render_template("crop/fertilizer.html", **context)


@crop.route('/crop', methods = ['GET', 'POST'])
def crop_recommendation():
    crops = crop_types()
    soils = soil_types()

    if request.method == 'POST':
        n = request.form.get('nitrogen')
        p = request.form.get('phosphorous')
        k = request.form.get('potassium')
        temp = request.form.get('temp')
        hum = request.form.get('humidity')
        rain = request.form.get('Moisture')
        ph = request.form.get('ph')
        soil = request.form.get('soil')

        result = predict_crop(n,p,k,temp,hum,ph, rain)

        # Save result in session for PDF
        session['last_report'] = {
            'type': 'Crop Recommendation',
            'inputs': {'Nitrogen': n, 'Phosphorus': p, 'Potassium': k, 'pH': ph, 'Rainfall': rain},
            'result': result
        }

        context = { 'crops': enumerate(crops), 'soils': enumerate(soils), 'result': result }
        return render_template("crop/crop.html", **context)

    context = { 'crops': enumerate(crops), 'soils': enumerate(soils) }
    return render_template("crop/crop.html", **context)

@crop.route('/download_report')
def download_report():
    if 'last_report' not in session:
        flash("No recent analysis found to download.", "warning")
        return redirect(url_for('crop.crop_recommendation'))
    
    data = session['last_report']
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Cropify - Smart Farming Report", ln=True, align='C')
    pdf.cell(200, 10, txt="------------------------------------------------", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=f"Report Type: {data['type']}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Input Parameters:", ln=True)
    for key, value in data['inputs'].items():
        pdf.cell(200, 10, txt=f" - {key}: {value}", ln=True)
        
    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=16)
    pdf.set_text_color(0, 128, 0) # Green color
    pdf.cell(200, 10, txt=f"Recommendation: {data['result']}", ln=True)
    
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=farming_report.pdf'
    return response

@crop.route('/crop-disease')
def crop_disease():
    return render_template("crop/crop-disease.html")

@crop.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city_name = request.form.get('city_name')
        result = get_weather(city_name)
        return render_template('crop/weather.html', result = result)
    return render_template("crop/weather.html")

@crop.route('/schemes')
def schemes():
    return render_template("crop/schemes.html")

@crop.route('/market')
@crop.route('/market')
def market():
    import datetime
    import random
    
    lang = request.args.get('lang', 'en')
    today = datetime.date.today().strftime("%d %B %Y")
    
    # Translation Dictionary
    TRANSLATIONS = {
        'hi': {
            'Wheat': 'गेहूँ', 'Rice': 'चावल', 'Maize': 'मक्का', 'Cotton': 'कपास',
            'Potato': 'आलू', 'Tomato': 'टमाटर', 'Onion': 'प्याज़', 'Soybean': 'सोयाबीन',
            'Sharbati': 'शरबती', 'Basmati 1121': 'बासमती 1121', 'Yellow Hybrid': 'पीला हाइब्रिड',
            'H-4': 'H-4', 'Jyoti': 'ज्योति', 'Hybrid': 'हाइब्रिड', 'Red Nashik': 'लाल नासिक', 'JS-335': 'JS-335',
            'Azadpur, Delhi': 'आजादपुर, दिल्ली', 'Karnal, Haryana': 'करनाल, हरियाणा',
            'Gulbarga, Karnataka': 'गुलबर्गा, कर्नाटक', 'Rajkot, Gujarat': 'राजकोट, गुजरात',
            'Agra, UP': 'आगरा, यूपी', 'Kolar, Karnataka': 'कोलार, कर्नाटक',
            'Lasalgaon, Maharashtra': 'लासलगाँव, महाराष्ट्र', 'Indore, MP': 'इंदौर, एमपी',
            'Daily Market Prices': 'दैनिक मंडी भाव', 'Crop': 'फसल', 'Variety': 'किस्म',
            'Market/Mandi': 'मंडी', 'Price': 'भाव (₹/ क्विंटल)', 'Change': 'बदलाव'
        },
        'ta': {
            'Wheat': 'கோதுமை', 'Rice': 'அரிசி', 'Maize': 'மக்காச்சோளம்', 'Cotton': 'பருத்தி',
            'Potato': 'உருளைக்கிழங்கு', 'Tomato': 'தக்காளி', 'Onion': 'வெங்காயம்', 'Soybean': 'சோயாபீன்',
            'Azadpur, Delhi': 'ஆசாத்பூர், டெல்லி', 'Karnal, Haryana': 'கர்னல், ஹரியானா',
            'Daily Market Prices': 'தினசரி சந்தை விலைகள்', 'Crop': 'பயிர்', 'Variety': 'வகை',
            'Market/Mandi': 'சந்தை', 'Price': 'விலை (₹)', 'Change': 'மாற்றம்'
        },
        'te': {
            'Wheat': 'గోధుమలు', 'Rice': 'బియ్యం', 'Maize': 'మొక్కజొన్న', 'Cotton': 'ప్రతి',
            'Potato': 'బంగాళాదుంప', 'Tomato': 'టమాటా', 'Onion': 'ఉల్లిపాయ', 'Soybean': 'సోయాబీన్',
            'Azadpur, Delhi': 'ఆజాద్‌పూర్, ఢిల్లీ', 'Karnal, Haryana': 'కర్నాల్, హర్యానా',
            'Daily Market Prices': 'రోజువారీ మార్కెట్ ధరలు', 'Crop': 'పంట', 'Variety': 'రకం', 
            'Market/Mandi': 'మార్కెట్', 'Price': 'ధర (₹)', 'Change': 'మార్పు'
        }
    }

    # Base Data (English)
    base_data = [
        {"crop": "Wheat", "variety": "Sharbati", "market": "Azadpur, Delhi", "base_price": 2250, "icon": "https://img.icons8.com/color/48/wheat.png"},
        {"crop": "Rice", "variety": "Basmati 1121", "market": "Karnal, Haryana", "base_price": 4100, "icon": "https://img.icons8.com/color/48/rice-bowl.png"},
        {"crop": "Maize", "variety": "Yellow Hybrid", "market": "Gulbarga, Karnataka", "base_price": 2050, "icon": "https://img.icons8.com/color/48/corn.png"},
        {"crop": "Cotton", "variety": "H-4", "market": "Rajkot, Gujarat", "base_price": 6300, "icon": "https://img.icons8.com/color/48/cotton.png"},
        {"crop": "Potato", "variety": "Jyoti", "market": "Agra, UP", "base_price": 850, "icon": "https://img.icons8.com/color/48/potato.png"},
        {"crop": "Tomato", "variety": "Hybrid", "market": "Kolar, Karnataka", "base_price": 1200, "icon": "https://img.icons8.com/color/48/tomato.png"},
        {"crop": "Onion", "variety": "Red Nashik", "market": "Lasalgaon, Maharashtra", "base_price": 1800, "icon": "https://img.icons8.com/color/48/onion.png"},
        {"crop": "Soybean", "variety": "JS-335", "market": "Indore, MP", "base_price": 4900, "icon": "https://img.icons8.com/color/48/soy.png"},
    ]
    
    market_data = []
    
    # Process Data: Randomize Price & Translate
    for item in base_data:
        # Randomize Price (+/- 5%)
        fluctuation = random.randint(-50, 100)
        current_price = item['base_price'] + fluctuation
        
        # Determine trend arrow
        trend = "▲" if fluctuation > 0 else "▼"
        trend_val = f"{trend} {abs(fluctuation)}"
        
        # Translation Lookup
        crop_name = item['crop']
        variety = item['variety']
        market_name = item['market']
        
        if lang in TRANSLATIONS:
            t = TRANSLATIONS[lang]
            crop_name = t.get(crop_name, crop_name)
            variety = t.get(variety, variety)
            market_name = t.get(market_name, market_name)

        market_data.append({
            "crop": crop_name,
            "variety": variety,
            "market": market_name,
            "price": f"{current_price:,}", # Format with commas
            "change": trend_val,
            "icon": item['icon']
        })
        
    labels = {
        'title': TRANSLATIONS.get(lang, {}).get('Daily Market Prices', 'Daily Market Prices'),
        'col_crop': TRANSLATIONS.get(lang, {}).get('Crop', 'Crop'),
        'col_variety': TRANSLATIONS.get(lang, {}).get('Variety', 'Variety'),
        'col_mandi': TRANSLATIONS.get(lang, {}).get('Market/Mandi', 'Market/Mandi'),
        'col_price': TRANSLATIONS.get(lang, {}).get('Price', 'Price (₹/Quintal)'),
        'col_change': TRANSLATIONS.get(lang, {}).get('Change', 'Change')
    }

    return render_template("crop/market.html", market_data=market_data, date=today, labels=labels, current_lang=lang)

@crop.route('/former-queries', methods=['GET', 'POST'])
def former_queries():
    if request.method == 'POST':
        title = request.form.get("title")
        file = request.files.get("file")
        filename = 'static/images/queries'+secure_filename(file.filename)
        file.save(filename)
        query = QueryModel(text=title, img_url=filename, userId=session['id'])
        db.session.add(query)
        db.session.commit()
        flash("Query raised successfully", "success")
        return redirect(url_for("crop.former_queries"))
    return render_template('crop/query.html')

def get_weather(city):
    API_KEY = '3MUNGGH2VYWHHDXSBBDN24WHL'
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}?unitGroup=metric&key={}&contentType=json"
    WEATHER_URL = url.format(city, API_KEY)
    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        result = response.json()
        # Process icons for days
        for day in result['days']:
            day['icon_url'] = get_icon_url(day['icon'])
        
        # Process icons for hours (for the first day at least)
        if 'hours' in result['days'][0]:
            for hour in result['days'][0]['hours']:
                hour['icon_url'] = get_icon_url(hour['icon'])
                
        return result