from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import pandas as pd
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
columns = []

class UploadFileForm(FlaskForm):
   file = FileField("file")
   submit = SubmitField("Upload File")

@app.route("/", methods = ['GET', 'POST'])

@app.route("/index", methods = ['GET', 'POST'])
def index():
   dir_name = "static/files"
   file_names = os.listdir(dir_name)
   for file in file_names: 
      if file.endswith(".csv"):
         os.remove(os.path.join(dir_name, file))
      
   form = UploadFileForm()
   if form.validate_on_submit():
        file = form.file.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return render_template('success.html'), {"Refresh": "3; url=secondpage"}
   return render_template('index.html', form=form)

@app.route("/secondpage", methods = ['GET', 'POST'])
def secondpage():
   dir_name = "static/files"
   file_names = os.listdir(dir_name)
   for file in file_names: 
      if file.endswith(".csv"):
         csv_path = os.path.join(dir_name, file)
         df = pd.read_csv(csv_path)
   columns = []
   column_names = list(df.columns)
   for c in column_names:
      columns.append(c)
   return render_template('secondpage.html', columns=columns)

@app.route("/output", methods = ['GET', 'POST'])
def output():
   dir_name = "static/files"
   file_names = os.listdir(dir_name)
   for file in file_names: 
      if file.endswith(".csv"):
         csv_path = os.path.join(dir_name, file)
         df = pd.read_csv(csv_path)
   var = request.form.get("ctech")
   sorted_list = df.sort_values(by=var, ascending=True)

   table = sorted_list.to_html()
   html_table = open("templates/output.html", "w")
   html_table.write("{% extends 'layout.html' %}")
   html_table.write("{% block body %}")
   html_table.write(table)
   html_table.write("{% endblock %}")
   html_table.close()
   return render_template('output.html')

@app.route("/demopage", methods = ['GET', 'POST'])
def demopage():
   return render_template('demopage.html')
   
if __name__ == '__main__':
   app.run(debug = True)
