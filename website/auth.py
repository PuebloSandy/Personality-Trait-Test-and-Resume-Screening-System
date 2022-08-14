from csv import DictWriter
from pickle import FALSE
from tkinter import Label
#from unicodedata import category
#from django.shortcuts import render
from flask import Flask, Blueprint,app, request, render_template, flash, redirect, jsonify, url_for, session
from sqlalchemy.sql import func
from .models import User
from .models import Company
from .models import Term
from .models import Trait
from .models import TraitFinal
from .models import ResumeFinal
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from werkzeug.utils import redirect, secure_filename
import csv, os, pandoc, pypandoc, pythoncom, comtypes.client, webbrowser, time, win32com.client
from .resume import userfile
from .trait import trait
#from pypandoc.pandoc_download import download_pandoc
import pandas as pd
import numpy as np
#import aspose.words as aw
#from sklearn.cluster import MiniBatchKMeans
from pathlib import Path
from docxtpl import DocxTemplate, InlineImage
from tkinter import *
from PIL import Image, ImageTk

auth = Blueprint('auth',__name__)

# Homepage/Landing Page 
@auth.route('/', methods=['GET','POST'])
def home():
    return render_template("/index.html")

# Login Page 
@auth.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) < 2 and len(password) < 2:
            flash('Username and Password must be higher 2 characters.', category='error')
        else:
            flash('Successfully Login', category='succes')
        return redirect("/user-homepage")
        
    return render_template("/index.html")

# Register
@auth.route('/register', methods=['GET','POST'])
def register():
    return render_template("/register.html")

# User Homepage 
@auth.route('/user-homepage', methods=['GET','POST'])
def user_home():
    return render_template("/users/User/user-homepage.html")

# User Survey Test Form 
@auth.route('/user-test-form', methods=['GET','POST'])
def user_test_form():
    if request.method == 'POST':
        return redirect('/user-survey-form')

    return render_template("/users/User/user-test-form.html")

# User Survey Form 
@auth.route('/user-survey-form', methods=['GET','POST'])
def user_survey_form():
    if request.method == 'POST':
        userid = 2
        EXT1=request.form.get('EXT1')
        AGR1=request.form.get('AGR1')
        CSN1=request.form.get('CSN1')
        EST1=request.form.get('EST1')
        OPN1=request.form.get('OPN1')
        EXT2=request.form.get('EXT2')
        AGR2=request.form.get('AGR2')
        CSN2=request.form.get('CSN2')
        EST2=request.form.get('EST2')
        OPN2=request.form.get('OPN2')
        EXT3=request.form.get('EXT3')
        AGR3=request.form.get('AGR3')
        CSN3=request.form.get('CSN3')
        EST3=request.form.get('EST3')
        OPN3=request.form.get('OPN3')
        EXT4=request.form.get('EXT4')
        AGR4=request.form.get('AGR4')
        CSN4=request.form.get('CSN4')
        EST4=request.form.get('EST4')
        OPN4=request.form.get('OPN4')
        EXT5=request.form.get('EXT5')
        AGR5=request.form.get('AGR5')
        CSN5=request.form.get('CSN5')
        EST5=request.form.get('EST5')
        OPN5=request.form.get('OPN5')
        EXT6=request.form.get('EXT6')
        AGR6=request.form.get('AGR6')
        CSN6=request.form.get('CSN6')
        EST6=request.form.get('EST6')
        OPN6=request.form.get('OPN6')
        EXT7=request.form.get('EXT7')
        AGR7=request.form.get('AGR7')
        CSN7=request.form.get('CSN7')
        EST7=request.form.get('EST7')
        OPN7=request.form.get('OPN7')
        EXT8=request.form.get('EXT8')
        AGR8=request.form.get('AGR8')
        CSN8=request.form.get('CSN8')
        EST8=request.form.get('EST8')
        OPN8=request.form.get('OPN8')
        EXT9=request.form.get('EXT9')
        AGR9=request.form.get('AGR9')
        CSN9=request.form.get('CSN9')
        EST9=request.form.get('EST9')
        OPN9=request.form.get('OPN9')
        EXT10=request.form.get('EXT10')
        AGR10=request.form.get('AGR10')
        CSN10=request.form.get('CSN10')
        EST10=request.form.get('EST10')
        OPN10=request.form.get('OPN10')

        # list of column names 
        field_names = ['AGR1','AGR2','AGR3','AGR4','AGR5','AGR6','AGR7','AGR8','AGR9','AGR10','CSN1','CSN2','CSN3','CSN4','CSN5','CSN6','CSN7','CSN8','CSN9','CSN10','EXT1','EXT2','EXT3','EXT4','EXT5','EXT6','EXT7','EXT8','EXT9','EXT10','NEU1','NEU2','NEU3','NEU4','NEU5','NEU6','NEU7','NEU8','NEU9','NEU10','OPN1','OPN2','OPN3','OPN4','OPN5','OPN6','OPN7','OPN8','OPN9','OPN10','USERID']

        # Dictionary
        dict= {'AGR1':AGR1,'AGR2':AGR2,'AGR3':AGR3,'AGR4':AGR4,'AGR5':AGR5,'AGR6':AGR6,'AGR7':AGR7,'AGR8':AGR8,'AGR9':AGR9,'AGR10':AGR10,'CSN1':CSN1,'CSN2':CSN2,'CSN3':CSN3,'CSN4':CSN4,'CSN5':CSN5,'CSN6':CSN6,'CSN7':CSN7,'CSN8':CSN8,'CSN9':CSN9,'CSN10':CSN10,'EXT1':EXT1,'EXT2':EXT2,'EXT3':EXT3,'EXT4':EXT4,'EXT5':EXT5,'EXT6':EXT6,'EXT7':EXT7,'EXT8':EXT8,'EXT9':EXT9,'EXT10':EXT10,'NEU1':EST1,'NEU2':EST2,'NEU3':EST3,'NEU4':EST4,'NEU5':EST5,'NEU6':EST6,'NEU7':EST7,'NEU8':EST8,'NEU9':EST9,'NEU10':EST10,'OPN1':OPN1,'OPN2':OPN2,'OPN3':OPN3,'OPN4':OPN4,'OPN5':OPN5,'OPN6':OPN6,'OPN7':OPN7,'OPN8':OPN8,'OPN9':OPN9,'OPN10':OPN10,'USERID':userid}

        with open('./website/dataset/traits-result.csv','a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(dict)
            f_object.close()
            return redirect('/user-survey-form-confirm')

    return render_template("/users/User/user-survey-form.html")

# User Survey Form Confirm
@auth.route('/user-survery-form-confirm', methods=['GET','POST'])
def user_survey_form_confirm():
    if request.method == 'POST':
        userid = request.form.get('userid')

        csv_file = csv.reader(open('./website/dataset/result-data.csv','r'))

        for row in csv_file:
            if userid==row[51]:
                print(row)
                return redirect("/users/User/user-survey-form-confirm.html", rowdata=row)
        #return redirect('/user-result-meaning')
    
    return render_template("/users/User/user-survey-form-confirm.html")

# User Trait Meaning
@auth.route('/user-result-meaning', methods=['GET','POST'])
def user_result_meaning():
    return render_template("/users/User/user-result-meaning.html")