from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from werkzeug.utils import secure_filename
from Models import QueryModel
from extensions import db
import requests
from utils import *
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
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}/today?unitGroup=metric&include=days&key={}&contentType=json"
    WEATHER_URL = url.format(city, API_KEY)
    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        result = response.json()
        for res in result['days']:
            if res['icon'] == 'clear-day': res['icon_url'] = 'https://www.visualcrossing.com/img/clear-day.c5680783.svg'
            if res['icon'] == 'partly-cloudy-day': res['icon_url'] = 'https://www.visualcrossing.com/img/partly-cloudy-day.3f13edae.svg'
            if res['icon'] == 'cloudy': res['icon_url'] = 'https://www.visualcrossing.com/img/cloudy.61f1f7c3.svg'
            if res['icon'] == 'rain': res['icon_url'] = 'https://www.visualcrossing.com/img/rain.36d72e24.svg'
            if res['icon'] == 'showers-day': res['icon_url'] = 'https://www.visualcrossing.com/img/showers-day.2f888a31.svg'
            if res['icon'] == 'showers-night': res['icon_url'] = 'https://www.visualcrossing.com/img/showers-night.b7f6058d.svg'
            if res['icon'] == 'thunder-showers-day': res['icon_url'] = 'https://www.visualcrossing.com/img/thunder-showers-day.90053223.svg'
            if res['icon'] == 'thunder-rain': res['icon_url'] = 'https://www.visualcrossing.com/img/thunder-rain.c575e6f7.svg'
        return result