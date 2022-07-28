from flask import Flask, render_template, request, send_file
from geopy.geocoders import ArcGIS
import pandas
import datetime

app = Flask(__name__)

@app.route('/')
def first_():
    return render_template('geofirst.html')

@app.route('/success', methods=['POST'])
def success():
    global filename
    if request.method == 'POST':
        f = request.files['file']
        try:
            nom = ArcGIS()
            df = pandas.read_csv(f)
            df['coordinates'] = df['Address'].apply(nom.geocode)
            df['Latitude'] = df['Coordinates'].apply(lambda x: x.latitude if x != None else None)
            df['Longitude'] = df['Coordinates'].apply(lambda x: x.longitude if x != None else None)
            df = df.drop('coordinates', 1)
            filename = datetime.datetime.now().strftime('uploads/%Y-%m-%d-%H-%M-%S-%f'+'.csv')
            df.to_csv(filename, index=None)
            return render_template('geofirst.html', text=df.to_html(), btn='download.html')
        except Exception as e:
            return render_template('geofirst.html', text=str(e))

@app.route('/download')
def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
