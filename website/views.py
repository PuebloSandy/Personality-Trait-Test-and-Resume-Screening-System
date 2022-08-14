from csv import DictWriter
from pickle import FALSE
from tkinter import Label
from django.shortcuts import render
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

import PyPDF2
import textract
import re
import string
import matplotlib.pyplot as plt

views = Blueprint('views',__name__)

# Homepage/Landing Page 
@views.route('/', methods=['GET','POST'])
def home():
    company = Company.query.first()
    try:
        if company == None or company == 0:
            coms = company
            com_slots = 0
        else:
            coms = company
            com_slots = company.available_slot
            #for row in company:
                #if row == 0:
                    #av_slots = '0'
                #else:  
                    #av_slots = row.available_slot
    except:
        return render_template("/index.html", user=current_user, coms=coms)

    return render_template("/index.html", user=current_user, coms=coms, slot=com_slots)

# Create Resume
@views.route('/create_resume_file', methods=['GET','POST'])
def resume_create_file():

    return render_template("/create-resume-form.html", user=current_user)

# Convert Resume Page
@views.route('/convert_resume_file_page', methods=['GET','POST'])
def resume_convert_file_page():

    return render_template("/convert-resume-form.html", user=current_user)

import urllib.request
from website import create_app
app = create_app()
# upload page
UPLOAD_FILE = "website/static/resume-file/pdf-file/"
app.config['UPLOAD_FILE'] = UPLOAD_FILE
ALLOWED_EXTENSIONS = set(['docx','pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Convert Resume
@views.route('/convert_resume_file', methods=['GET','POST'])
def resume_convert_file():
    if request.method == 'POST':
        files = request.files.get('resume')
        #working_dir = os.getcwd()
        #wdFormatPdf = 17
        #file=comtypes.client.CreateObject("Word.Application",pythoncom.CoInitialize())
        #doc = file.Documents.Open(files)
        #outfile = file.replace('docx','pdf')
        applicant_file = secure_filename(files.filename)
        loc = "./static/resume-file/pdf-file/"+applicant_file
        files.save(Path(__file__).parent / loc)
        flash('Successfully Save!', category='success')

        #app_resume_pdf = os.path.abspath(working_dir+'/website/static/resume-file/pdf-file/'+str(files))
        #files.SaveAs(app_resume_pdf,FileFormat=wdFormatPdf)
        #files.Close()
        #files.Quit()
        #flash("Successfully convert your Resume to PDF File", category='success')
        #msg = 'New record created successfully'
    #return jsonify(msg)
    return render_template("/convert-resume-form.html")

# Logout 
@views.route('/logout', methods=['GET','POST'])
def logout():
    session.pop("user", None)
    flash('Successfully Logout!', category='success')
    return redirect("/")

# Login Modal
@views.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if username == '' and password == '':
            flash('Please input your username and password!!', category='error')
            return redirect("/")
        elif username == '':
            flash('Please input your username!!', category='error')
            return redirect("/")
        elif password == '':
            flash('Please input your password!!', category='error')
            return redirect("/")
        elif user:
            session["user"] = user.id
            try:
                if check_password_hash(user.password, password):
                    if user.user_type == 'Admin':
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=True)
                        return redirect('admin-homepage')
                    else:
                        userid = user.id
                        check_trait = Trait.query.filter_by(user_id=userid).first()
                        try:
                            row_id_trait = check_trait.id
                            check_traitFinal = TraitFinal.query.filter_by(user_id=userid).first()
                            check_resume = ResumeFinal.query.filter_by(user_id=userid).first()
                            try:
                                row_id_trait_final = check_traitFinal.id
                                row_id_resume_final = check_resume.id
                                flash('Logged in successfully!', category='success')
                                login_user(user, remember=True)
                                return redirect('user-homepage')
                            except:          
                                flash('Logged in successfully!', category='success')
                                login_user(user, remember=True)
                                return redirect('/user-survey-form-confirm')
                        except:
                            flash('Logged in successfully..', category='success')
                            login_user(user, remember=True)
                            return redirect('user-homepage')
                else:
                    flash('incorrect password!', category='error')
            except:
                flash('User Doesn\'nt Exist!!', category='error')
        else:
            flash('User does\'nt Exist!!' , category='error')
            return redirect("/")

    return render_template("/index.html") 

import urllib.request
from website import create_app
app = create_app()
# upload page
UPLOAD_FOLDER = "website/static/images/profile-pictures/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
# Register
@views.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        usertype = "User"
        firstname = request.form.get('firstname')
        middleIni = request.form.get('middle')
        lastname = request.form.get('lastname')
        prefix = request.form.get('prefix')
        files = request.files.get('resume')
        #working_dir = os.getcwd()
        #wdFormatPdf = 17
        #file=comtypes.client.CreateObject("Word.Application",pythoncom.CoInitialize())
        #doc = file.Documents.Open(files)
        #outfile = file.replace('docx','pdf')

        #Applicant Resume information
        #PICTURE = request.files.get('picture')
        #PERSONALSTATEMENT = request.form.get('personal_statement')
        city = request.form.get('city')
        address = request.form.get('address')
        ADDRESS = address.capitalize()+", "+city.capitalize()
        #NATIONALITY = request.form.get('nationality')
        GENDER = request.form.get('gender')
        AGE = request.form.get('age')
        BIRTHDAY = request.form.get('birthday')
        MOBILE = request.form.get('mobile')
        #LANGUAGE = request.form.get('language')
        GMAIL = request.form.get('gmail')
        #FACEBOOK = request.form.get('facebook')
        #COLLEGE = request.form.get('college')
        #VOCATIONAL = request.form.get('vocational')
        #SHS = request.form.get('shs')
        #HS = request.form.get('hs')
        #PRIMARY = request.form.get('primary')
        #EXPERIENCE = request.form.get('experience')
        #SKILLS = request.form.get('skills')
        #REFERENCE = request.form.get('reference')
        
        #working_dir = os.getcwd()

        #if PICTURE and allowed_file(PICTURE.filename):
            #filename = secure_filename(PICTURE.filename)
            #mimetype = PICTURE.mimetype
            #PICTURE.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #root = Tk()
            #root.title("Personality")
            #root.geometry("800x500")
            #root.iconbitmap('./website/static/images/personality-icon.png')

            #loc_app = "./website/static/images/profile-pictures/"+filename
            #pic_of_ap = Image.open(loc_app)
            #resizing the image
            #size = width, height = pic_of_ap.size
            #new = pic_of_ap.resize((150,100)).save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #else:
            #flash('Oops, something went wrong in updatinng your data.. Please check the format of the image. Allowed image types are: png, jpg, jpeg, gif', category='error')
            #return redirect('/register')

        #if prefix == '' or prefix == 0 or prefix == 'None' or prefix == 'NONE':
            #FULLNAME = firstname.capitalize()+" "+middleIni.capitalize()+". "+lastname.capitalize()
            #Save_docx = lastname.capitalize()+","+firstname.capitalize()+middleIni.capitalize()
        #else:
            #FULLNAME = firstname.capitalize()+" "+middleIni.capitalize()+". "+lastname.capitalize()+","+prefix
            #Save_docx = lastname.capitalize()+","+prefix+","+firstname.capitalize()+middleIni.capitalize()

        company_id = Company.query.all()
        try:
            for row in company_id:
                comid = row.id
        except:
            comid = 0

        if len(username) < 2:
            flash('Username must be higher 2 characters.', category='error')
            return redirect("/register")
        elif len(password1) < 8:
            flash('Password must be higher 2 characters.', category='error')
            return redirect("/register")
        else:
            #document_path = Path(__file__).parent / "./static/resume-file/resume-xample.docx"
            #doc = DocxTemplate(document_path)
            #applicant save to docx file
            #file_name = Save_docx+"-Resume"
            #applicant_file = "%s.docx" % file_name
            #save_docx = "./static/resume-file/docx-file/"+applicant_file
            #img_to_get = "./website/static/images/profile-pictures/"+filename
            #file_to_save_img = Path(__file__).parent / img_to_get

            #context = {"PICTURE": InlineImage(doc, img_to_get),"FULLNAME": FULLNAME, "PERSONALSTATEMENT": PERSONALSTATEMENT.capitalize(), "ADDRESS": ADDRESS, "NATIONALITY": NATIONALITY.capitalize(), "GENDER": GENDER.capitalize(), "AGE": AGE,"BIRTHDAY": BIRTHDAY.capitalize(),"MOBILE": MOBILE,"LANGUAGE": LANGUAGE.capitalize(),"GMAIL": GMAIL,"FACEBOOK": FACEBOOK,"COLLEGE": COLLEGE.capitalize(),"VOCABULARY": VOCATIONAL.capitalize(),"SHS": SHS.capitalize(),"HS": HS.capitalize(),"PRIMARY": PRIMARY.capitalize(),"EXPERIENCE": EXPERIENCE.capitalize(),"SKILLS": SKILLS.capitalize(),"REFERENCE":REFERENCE.capitalize()}
            applicant_file = secure_filename(files.filename)
            loc = "./static/resume-file/pdf-file/"+applicant_file
            #files.save(Path(__file__).parent / loc)
            #flash('Successfully Save!', category='success')
            try:
                #doc.render(context)
                #doc.save(Path(__file__).parent / save_docx)
                files.save(Path(__file__).parent / loc)
            
                new_user = User(username=username, user_type=usertype, first_name=firstname.capitalize(), middle_name=middleIni.capitalize(), last_name=lastname.capitalize(), prefix=prefix, file=applicant_file, password=generate_password_hash(password1, method='sha256'), email=GMAIL, address=ADDRESS, age=AGE, gender=GENDER.capitalize(), birthday=BIRTHDAY, phone_number=MOBILE, company_id=comid)
                db.session.add(new_user)
                #db.session.commit()

                com_slot = Company.query.all()
                if com_slot == 0:
                    none = none
                else:
                    for get in com_slot:
                        com_id = get.id
                        com_avail = get.available_slot
                        company_id = Company.query.get(com_id)
                        usercount = 1
                        company_id.available_slot = int(com_avail) - int(usercount)
                        try:
                            db.session.commit()
                        except:
                            none = none

                #login_user(user, remember=True)
                flash('Successfully Created the Account!', category='succes')
                return redirect("/")
            except:
                flash('There is a Problem Creating your account the Account.. Please check your input data!!', category='error')
                return redirect("/register")

    return render_template("/register.html", user=current_user)


@views.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(username=username).first()
        try:
            if username != user.username:
                flash('Username doesn\'t exist!!!', category='error')
            elif len(password2) < 8:
                flash("Password so short!!", category='error')
                return redirect('/forgot-password')
            else:
                if check_password_hash(user.password, password1):
                    user.password = generate_password_hash(password2, method='sha256')
                    db.session.commit()
                    flash("Successfully Update your Password!!!", category='success')
                else:
                    flash('Incorrect Password!!!', category='error')
        except:
            flash('Username doesn\'t exist!!!', category='error')

    return render_template("/forgot-password.html")

# Admin Homepage 
@views.route('/admin-homepage', methods=['GET','POST'])
def admin_home():
    if "user" in session:
        user = session["user"]
        try:
            return render_template("/users/Admin/admin-homepage.html", user=user)
        except:
            flash("User Does\'nt Exist!!", category='error')
            return render_template("/users/Admin/admin-homepage.html", user=user)
    else:
        return redirect('/')

# Admin Company 
@views.route('/admin-company', methods=['GET','POST'])
def admin_company():
    if "user" in session:
        user = session["user"]
        try:
            row_com = Company.query.count()
            company = Company.query.all()
            if company == 0:
                com = 0
            else:
                com = company
            return render_template("/users/Admin/admin-company.html",user=user, com=com, row=row_com)
        except:
            flash("User Does\'nt Exist!!", category='error')
            return render_template("/users/Admin/admin-company.html",user=user, com=com, row=row_com)
    else:
        return redirect('/')

# Admin Add Company 
@views.route('/add-company', methods=['GET','POST'])
def admin_add_company():
    if "user" in session:
        user = session["user"]
        try:
            if request.method == 'POST':
                company_name = request.form.get('company_name')
                company_slot = request.form.get('company_slot')
                company_avail_slot = company_slot
                new_company = Company(company_name=company_name, slots=company_slot, available_slot=company_avail_slot)
                try:
                    db.session.add(new_company)
                    db.session.commit()
                    flash('Successfully Created Company Slot!', category='success')
                    return redirect('/admin-company')
                except: 
                    flash("There was a problem creating the Company Slot!!", category='error')
            return redirect("/admin-company")
        except:
            flash("User Does\'nt Exist!!", category='error')
            return redirect("/admin-company")
    else:
        return redirect('/')

# Admin Update Company 
@views.route('/update_company', methods=['GET','POST'])
def update_company():
    if "user" in session:
        user = session["user"]
        try:
            if request.method == 'POST':
                #company_id = request.form.get('company_id')
                company_id = Company.query.get(request.form.get('id'))
                try:
                    avail = company_id.available_slot
                    slot = company_id.slots
                    req_slot = request.form['company_slot']
                    
                    company_id.company_name = request.form['company_name']
                    company_id.slots = request.form['company_slot']
                    
                    if req_slot > slot:
                        add_slot = int(req_slot) - int(slot)
                        company_id.available_slot = int(avail) + int(add_slot)
                    elif req_slot < slot:
                        add_slot = int(slot) - int(req_slot)
                        company_id.available_slot = int(avail) - int(add_slot)
                    else:
                        company_id.available_slot = int(avail)

                    db.session.commit()
                    flash("Successfully Update Company Slot!", category='success')
                    return redirect("/admin-company")
                except:
                    flash("There was a problem updating the Company Slot!!", category='error')
            return redirect("admin-company")
        except:
            flash("User Does\'nt Exist!!", category='error')
            return redirect("admin-company")
    else:
        return redirect('/')

# Admin Delete Company 
@views.route('/delete_company', methods=['GET','POST'])
def delete_company():
    if "user" in session:
        user = session["user"]
        try:
            if request.method == 'POST':
                #company_id = request.form.get('company_id')
                company_id = Company.query.get(request.form.get('id'))
                #new_company = Company(id=company_id)
                try:
                    db.session.delete(company_id)
                    db.session.commit()
                    flash("Successfully Delete Company Slot!", category='success')
                    return redirect('/admin-company')
                except:
                    flash("There was a problem deleting the Company Slot!!", category='error')
                return redirect("/admin-company")
        except:
            flash("User Does\'nt Exist!!", category='error')
            return redirect("/admin-company")
    else:
        return redirect('/')

# Admin Term Area
@views.route('/admin-term', methods=['GET','POST'])
def admin_term():
    if "user" in session:
        user = session["user"]
        term = Term.query.all()
        if term == 0:
            ter = 0
        else:
            ter = term
        return render_template("/users/Admin/admin-terms.html",user=user, ter=ter)
    else:
        return redirect('/')

# Admin Add Term 
@views.route('/add-term', methods=['GET','POST'])
def admin_add_term():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            term_name = request.form.get('term_name')
            term_under = request.form.get('term_under')
            new_term = Term(term_name=term_name, term_under=term_under)
            try:
                db.session.add(new_term)
                db.session.commit()
                flash('Successfully Created Term Area!!!', category='success')
                return redirect('/admin-term')
            except: 
                flash("There was a problem creating the Term Area!!!", category='error')
        return redirect("/admin-term")
    else:
        return redirect('/')

# Admin Delete All Term Area 
@views.route('/delete_all_term', methods=['GET','POST'])
def delete_all_term():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            #company_id = request.form.get('company_id')
            company = Company.query.all()
            try:
                db.session.delete(company.id)
                db.session.commit()
                flash("Successfully Delete All Term Area!!!", category='success')
                return redirect('/admin-term')
            except:
                flash("There was a problem deleting all the Term Area!!!", category='error')
        return redirect("/admin-term")
    else:
        return redirect('/')

# Admin Update Term Area 
@views.route('/update_term', methods=['GET','POST'])
def update_term():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            #company_id = request.form.get('company_id')
            term_id = Term.query.get(request.form.get('id'))
            try:            
                term_id.term_name = request.form['term_name']
                term_id.term_under = request.form['term_under']

                db.session.commit()
                flash("Successfully Update Term Area!!!", category='success')
                return redirect("/admin-term")
            except:
                flash("There was a problem updating the Term Area!!!", category='error')
        return redirect("admin-term")
    else:
        return redirect('/')

# Admin Delete Term Area 
@views.route('/delete_term', methods=['GET','POST'])
def delete_term():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            #company_id = request.form.get('company_id')
            term_id = Term.query.get(request.form.get('id'))
            #new_company = Company(id=company_id)
            try:
                db.session.delete(term_id)
                db.session.commit()
                flash("Successfully Delete Term Area!!!", category='success')
                return redirect('/admin-term')
            except:
                flash("There was a problem deleting the Term Area!!!", category='error')
        return redirect("/admin-term")
    else:
        return redirect('/')

# Admin User Account 
@views.route('/admin_users_account', methods=['GET','POST'])
def admin_users():
    if "user" in session:
        userid = session["user"]
        try:
            user = User.query.filter_by(user_type='User').all()
            return render_template("/users/Admin/admin-users.html",user=userid, query=user)
        except:
            flash("User Does\'nt Exist!!", category='error')
            return render_template("/users/Admin/admin-users.html",user=userid, query=user)
    else:
        return redirect('/')

@views.route('/admin_delete_user', methods=['GET','POST'])
def admin_delete_user():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            user_id = request.form.get('userid')
            #get the user get company id 
            user_comid = User.query.filter_by(id=user_id).first()
            comid = user_comid.company_id
            # get the row of the company id of user
            com_row = Company.query.filter_by(id=comid).first()
            row_com_id = com_row.id
            row_com_av_slot = int(com_row.available_slot) + 1
            #get the user row in the trait save data
            get = Trait.query.filter_by(user_id=user_id).first()
            row_trait_id = get.id
            #get the user row in the traitfinal save data
            f = TraitFinal.query.filter_by(user_id=user_id).first()
            row_traitfinal_id = f.id
            #get the user row in the resume save data
            r = ResumeFinal.query.filter_by(user_id=user_id).first()
            row_resu_id = r.id

            userid = User.query.get(request.form.get('userid'))
            trait_id = Trait.query.get(row_trait_id)
            trait_final_id = TraitFinal.query.get(row_traitfinal_id)
            resume_id = ResumeFinal.query.get(row_resu_id)
            com_id_row = Company.query.get(row_com_id)
            try:
                com_id_row.available_slot = row_com_av_slot
                db.session.delete(userid)
                db.session.delete(trait_id)
                db.session.delete(trait_final_id)
                db.session.delete(resume_id)
                db.session.commit()
                flash("Successfully Delete User !!", category='success')
                return redirect('/admin_users_account')
            except:
                flash("There was a problem deleting the User!!", category='error')
        return redirect('admin_users_account')
    else:
        return redirect('/')

# Admin User Results 
@views.route('/admin_users_results', methods=['GET','POST'])
def admin_user_results():
    if "user" in session:
        user = session["user"]
        check_user = User.query.filter_by(user_type='User').all()
        try:    
            if request.method == 'POST':
                userid = request.form.get('userid')
                user_file = User.query.filter_by(id=userid).first()
                get = TraitFinal.query.filter_by(user_id=userid).first()
                on = ResumeFinal.query.filter_by(user_id=userid).first()
                try:
                    working_dir = os.getcwd()
                    applicant_pdf_file = user_file.file
                    #app_resume_pdf = os.path.abspath(working_dir+'./static/resume-file/pdf-file/'+applicant_pdf_file)
                    app_resume_pdf = '../../../static/resume-file/pdf-file/'+applicant_pdf_file

                    agreeable = get.agreeableness
                    consci = get.conscientiousness
                    extro = get.extroversion
                    nuero = get.neuroticism
                    opn = get.openness

                    qua = on.quality
                    ope = on.operations
                    su = on.supplychain
                    proj = on.project
                    da = on.data
                    ca = on.healthcare  
                    
                    #return render_template("/users/Admin/admin-users-results.html", user=current_user, agr=agreeable, cons=consci, ext=extro, nue=nuero, openn=opn, q=qua, op=ope, sup=su, pro=proj, d=da, c=ca, file=app_resume_pdf)
                except:
                    flash("There is no data Result for this Applicant yet!!", category='error')
                    return redirect("/admin_users_results")

            if check_user == 0 or check_user == []:
                check = 0
                fullname = 0
                return render_template("/users/Admin/admin-users-results.html",user=user, list=check, user_full=fullname)
            else:
                check = check_user
                for lists in check_user:
                    user_id = lists.id
                    first = lists.first_name
                    middle = lists.middle_name
                    last = lists.last_name
                    prefix = lists.prefix
                    if prefix == '' or prefix == 0 or prefix == 'None' or prefix == 'none' or prefix == 'NOne' or prefix == 'NONe' or prefix == 'NONE':
                        fullname = last+","+first+""+middle+"."
                    else:
                        fullname = last+","+prefix+","+first+""+middle+"."

                    Final_trait = TraitFinal.query.filter_by(user_id=user_id).all()
                    Final_resume = ResumeFinal.query.filter_by(user_id=user_id).all()

                return render_template("/users/Admin/admin-users-results.html",user=current_user, list=check, user_full=fullname, agr=agreeable, cons=consci, ext=extro, nue=nuero, openn=opn, q=qua, op=ope, sup=su, pro=proj, d=da, c=ca, file=app_resume_pdf)
        except:
            fullname = 0
        
        return render_template("/users/Admin/admin-users-results.html",user=current_user, list=check)
    else:
        return redirect('/')

# Admin User Results Search
@views.route('/admin_users_results_search', methods=['GET','POST'])
def admin_users_results_search():
    if "user" in session:
        user = session["user"]
        
    else:
        return redirect('/')

# User Homepage 
@views.route('/user-homepage', methods=['GET','POST'])
def user_home():
    if "user" in session:
        userid = session["user"]
        user = current_user.id
        term_area = Term.query.count()
        userid = User.query.filter_by(id=user).first()
        result_data = Trait.query.filter_by(user_id=user).first()
        try:
            user_id = userid
            firstname = userid.first_name
            middle = userid.middle_name
            lastname = userid.last_name
            prefix = userid.prefix
            #if prefix == '' or prefix == 0 or prefix == 'none' or prefix == 'None' or prefix == 'NOne' or prefix == 'NONe' or prefix == 'NONE':
                #fullname = lastname+","+firstname+middle+"-Resume"
            #else:
                #fullname = lastname+","+prefix+","+firstname+middle+"-Resume"
            files = userid.file

            working_dir = os.getcwd()
            #applicant_file = fullname+".docx"
            #app_resume_docx = os.path.abspath(working_dir+'/website/resume-file/docx-file/'+applicant_file)
            applicant_pdf_file = files
            app_resume_pdf = os.path.abspath(working_dir+'/website/resume-file/pdf-file/'+applicant_pdf_file)

            #docx_files = os.path.isfile(working_dir+'/website/static/resume-file/docx-file/'+applicant_file)
            pdf_files = os.path.isfile(working_dir+'/website/static/resume-file/pdf-file/'+applicant_pdf_file)

            if pdf_files == True:
                file = pdf_files
                if term_area < 15:
                    terms = 0
                else:
                    terms = term_area
                return render_template("/users/User/user-homepage.html", user=current_user, check=file, result=result_data, term=terms)
            else:
                file = pdf_files
                return render_template("/users/User/user-homepage.html", user=current_user, check=file)
            
            #return render_template("/users/User/user-homepage.html", user=current_user, check=file)
        except:
            return render_template("/users/User/user-homepage.html", user=current_user)
    else:
        return redirect('/')

# Convert docx to pdf
@views.route('/upload_file', methods=['GET','POST'])
def upload_file(): 
    if "user" in session:
        user = session["user"]

        if request.method == 'POST':
            #userid = request.form.get('userid')
            files = request.files.get('resume')

            user_id = User.query.get(request.form.get('userid'))
            try:
                applicant_file = secure_filename(files.filename)
                loc = "./static/resume-file/pdf-file/"+applicant_file
                files.save(Path(__file__).parent / loc)

                user_id.file = applicant_file
                db.session.commit()
                flash("Successfully Upload your Resume File!!", category='success')
                return redirect("/user-homepage")
            except:
                flash("Unsuccessfully Upload your Resume File!!", category='success')
                return redirect("/user-homepage")

        #userid = User.query.filter_by(id=id).first()
        #user_id = userid
        #firstname = userid.first_name
        #middle = userid.middle_name
        #lastname = userid.last_name
        #prefix = userid.prefix
        #if prefix == '' or prefix == 0 or prefix == 'none' or prefix == 'None' or prefix == 'NOne' or prefix == 'NONe' or prefix == 'NONE':
            #fullname = lastname+","+firstname+middle+"-Resume"
        #else:
            #fullname = lastname+","+prefix+","+firstname+middle+"-Resume"

        #working_dir = os.getcwd()
        #applicant_file = fullname+".docx"
        #app_resume_docx = os.path.abspath(working_dir+'/website/static/resume-file/docx-file/'+applicant_file)
        #applicant_pdf_file = fullname+".pdf"
        #app_resume_pdf = os.path.abspath(working_dir+'/website/static/resume-file/pdf-file/'+applicant_pdf_file)
                                
        #if applicant_file == applicant_file:
            #if app_resume_pdf == applicant_pdf_file:
                #none = "none"
            #else:
                #app_resume_docx = os.path.abspath(working_dir+'/website/resume-file/docx-file/'+applicant_file)
                #wdFormatPdf = 17
                #file=comtypes.client.CreateObject("Word.Application",pythoncom.CoInitialize())
                #doc = file.Documents.Open(app_resume_docx)
                #outfile = applicant_file.replace('docx','pdf')
                #app_resume_pdf = os.path.abspath(working_dir+'/website/resume-file/pdf-file/'+outfile)
                #doc.SaveAs(app_resume_pdf,FileFormat=wdFormatPdf)
                #doc.Close()
                #file.Quit()
                #flash("Successfully convert your Resume to PDF File", category='success')

        return redirect("/user-homepage")
    else:
        return redirect('/')

#User Resume file in Open in Page
@views.route('/user_files_resume')
def user_resume():
    result_data = Trait.query.filter_by(user_id=current_user.id).first()
    name = User.query.filter_by(id=current_user.id).first()
    firstname = name.first_name
    lastname = name.last_name
    middlename = name.middle_name
    prefix = name.prefix
    pdf = name.file

    try:
        #term_id = quality.term_name
        #if prefix == '' or prefix == 0 or prefix == 'none' or prefix == 'None' or prefix == 'NOne' or prefix == 'NONe' or prefix == 'NONE':
            #fullname = lastname+","+firstname+middlename+"-Resume.pdf"
        #else:
            #fullname = lastname+","+prefix+","+firstname+middlename+"-Resume.pdf"

        file = "../../../static/resume-file/pdf-file/"+pdf
        return render_template("/users/User/user-resume-file.html",user=current_user,file=file, result=result_data)
    except:
        flash("Something Problem or Missing the File in the Folder!!", category='error')

    return render_template("/users/User/user-resume-file.html",user=current_user,file=file, result=result_data)

# User Resume File Open in Browser
@views.route('/user_file_resume/<int:id>')
def user_file_resume(id):
    if "user" in session:
        userid = session["user"]

        user = User.query.filter_by(id=id).first()
        firstname = user.first_name
        middleIni = user.middle_name
        lastname = user.last_name
        prefix = user.prefix

        if prefix == '' or prefix == 0 or prefix == 'None' or prefix == 'NONE':
            file_name = lastname+","+firstname+middleIni+"-Resume"
        else:
            file_name = lastname+","+prefix+","+firstname+middleIni+"-Resume"

        try:
            applicant_pdf_file = "./resume-file/pdf-file/"+file_name+".pdf"
            pdf_file = Path(__file__).parent / applicant_pdf_file
            open_file = webbrowser.open_new_tab(pdf_file)
            flash('Takes a while to open your PDF File. Please wait to open your PDF File in the browser!!', category='success')
            return redirect("/user-homepage")
        except:
            flash('There is something wrong with your PDF File!!', category='error')
            return redirect("/user-homepage")
        #return render_template("/users/User/user-homepage.html", user=current_user)
    else:
        return redirect('/')

# User Survey Test Form 
@views.route('/user_test_form', methods=['GET','POST'])
def user_test_form():
    if "user" in session:
        userid = session["user"]
        trait = Trait.query.filter_by(user_id=userid).first()
        row_traitfinal = TraitFinal.query.filter_by(user_id=userid).first()
        row_resumefinal = ResumeFinal.query.filter_by(user_id=userid).first()
        try:
            traits = trait
            traitfinal = row_traitfinal
            resumefinal = row_resumefinal
            date = trait.date
            started = trait.time_started
            ended = trait.time_ended
            company_id = trait.company_id
            return render_template("/users/User/user-test-form.html", user=userid, row=traits, traitfinal=traitfinal, resumefinal=resumefinal, dates=date ,start=started, end=ended, result=trait)
        except:
            traits = 0
            traitfinal = 0
            resumefinal = 0
            date = 0
            started = 0
            ended = 0
            company_id = 0
            return render_template("/users/User/user-test-form.html", user=current_user, row=traits, traitfinal=traitfinal, resumefinal=resumefinal, dates=date ,start=started, end=ended, result=trait)
    else:
        return redirect('/')

# User Survey Test Form Enter 
@views.route('/user_test_form_enter/<int:id>', methods=['GET','POST'])
def user_test_form_enter(id):
    if "user" in session:
        user = session["user"]

        if request.method == 'POST':
            today = date.today()
            t = time.localtime()
            userid = request.form.get('userid')
            agr1 = 0
            dates = today.strftime("%d/%m/%Y")
            current_start_time = time.strftime("%H:%M:%S", t)
            current_end_time = 0

            comid = User.query.filter_by(id=id).first()
            company_id = comid.company_id

            save_trait = Trait(agr1=agr1, date=dates, time_started=current_start_time ,time_ended=current_end_time ,user_id=userid, company_id=company_id)
            try:
                db.session.add(save_trait)
                db.session.commit()
                return redirect('/user_survey_form')
            except:
                return redirect('/user_test_form')

        return render_template("/users/User/user-test-form.html", user=current_user)
    else:
        return redirect('/')

# User Survey Test Form Restart 
@views.route('/user_test_form_restart', methods=['GET','POST'])
def user_test_form_restart():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            userid = request.form.get('userid')
            rowuserid = Trait.query.get(request.form.get('row_id'))
            row_traitfinal_id = TraitFinal.query.get(request.form.get('traitfinal_id'))
            row_resumefinal_id = ResumeFinal.query.get(request.form.get('resusmefinal_id'))
            try:
                db.session.delete(rowuserid)
                db.session.delete(row_traitfinal_id)
                db.session.delete(row_resumefinal_id)
                db.session.commit()
                flash("Successfully Restart your Survey!!", category='success')
                return redirect('/user_test_form')
            except:
                flash("Could\'nt Restart your Survey.. Something may Wrong!!", category='error')
                return redirect('/user_test_form')

        return render_template("/users/User/user-test-form.html", user=current_user)
    else:
        return redirect('/')

# User Survey Test Form Restart 
@views.route('/user_survey_form_restart', methods=['GET','POST'])
def user_survey_form_restart():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            userid = request.form.get('userid')
            rowtraitid = Trait.query.get(request.form.get('traitid'))
            try:
                db.session.delete(rowtraitid)
                db.session.commit()
                flash("Successfully Restart your Survey!!", category='success')
                return redirect('/user_test_form')
            except:
                flash("Could\'nt Restart your Survey.. Something may Wrong!!", category='error')
                return redirect('/user_test_form')

        return render_template("/users/User/user-test-form.html", user=current_user)
    else:
        return redirect('/')

# User Survey Form 
@views.route('/user_survey_form', methods=['GET','POST'])
def user_survey_form():
    if "user" in session:
        user = session["user"]
        trait = Trait.query.filter_by(user_id=user).first()
        if request.method == 'POST':
            today = date.today()
            t = time.localtime()
            user_id = request.form.get('userid')
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

            DATE_TAKEN = today.strftime("%d/%m/%Y")
            #current_start_time = time.strftime("%H:%M:%S", t)
            current_end_time = time.strftime("%H:%M:%S", t)
            userid = Trait.query.filter_by(user_id=user_id).first()
            traitID = userid.id
            row_ID = Trait.query.get(traitID)
            user_info = Trait.query.filter_by(user_id=user_id).first()
            user_start_time = user_info.time_started
            
            try:  
                row_ID.agr1 = AGR1
                row_ID.time_ended = current_end_time
                db.session.commit()

                csv_row = csv.reader(open('./website/dataset/result-data.csv','r'))
                num_rows = len(list(csv_row))
                sr_no = int(num_rows)
                # list of column names 
                field_names = ['sr_no','AGR1','AGR2','AGR3','AGR4','AGR5','AGR6','AGR7','AGR8','AGR9','AGR10','CSN1','CSN2','CSN3','CSN4','CSN5','CSN6','CSN7','CSN8','CSN9','CSN10','EXT1','EXT2','EXT3','EXT4','EXT5','EXT6','EXT7','EXT8','EXT9','EXT10','NEU1','NEU2','NEU3','NEU4','NEU5','NEU6','NEU7','NEU8','NEU9','NEU10','OPN1','OPN2','OPN3','OPN4','OPN5','OPN6','OPN7','OPN8','OPN9','OPN10','USERID','DATE_TAKEN','START_TIME','END_TIME']

                # Dictionary
                dict= {'sr_no':sr_no,'AGR1':AGR1,'AGR2':AGR2,'AGR3':AGR3,'AGR4':AGR4,'AGR5':AGR5,'AGR6':AGR6,'AGR7':AGR7,'AGR8':AGR8,'AGR9':AGR9,'AGR10':AGR10,'CSN1':CSN1,'CSN2':CSN2,'CSN3':CSN3,'CSN4':CSN4,'CSN5':CSN5,'CSN6':CSN6,'CSN7':CSN7,'CSN8':CSN8,'CSN9':CSN9,'CSN10':CSN10,'EXT1':EXT1,'EXT2':EXT2,'EXT3':EXT3,'EXT4':EXT4,'EXT5':EXT5,'EXT6':EXT6,'EXT7':EXT7,'EXT8':EXT8,'EXT9':EXT9,'EXT10':EXT10,'NEU1':EST1,'NEU2':EST2,'NEU3':EST3,'NEU4':EST4,'NEU5':EST5,'NEU6':EST6,'NEU7':EST7,'NEU8':EST8,'NEU9':EST9,'NEU10':EST10,'OPN1':OPN1,'OPN2':OPN2,'OPN3':OPN3,'OPN4':OPN4,'OPN5':OPN5,'OPN6':OPN6,'OPN7':OPN7,'OPN8':OPN8,'OPN9':OPN9,'OPN10':OPN10,'USERID':user_id,'DATE_TAKEN':DATE_TAKEN,'START_TIME':user_start_time,'END_TIME':current_end_time}

                with open('./website/dataset/result-data.csv','a',newline='') as f_object:
                    dictwriter_object = DictWriter(f_object, fieldnames=field_names)
                    dictwriter_object.writerow(dict)
                    f_object.close()
                    return redirect('/user-survey-form-confirm')
            except:
                flash('Something wrong with the data you answer.. Please contact the personel incharge!!', category='error')
        #else:
            #return redirect("/")
        return render_template("/users/User/user-survey-form.html", user=current_user, trait=trait)
    else:
        return redirect('/')

# User Survey Form Confirm
@views.route('/user-survey-form-confirm', methods=['GET','POST'])
def user_survey_form_confirm():
    if "user" in session:
        user = session["user"]
        if request.method == 'POST':
            userid = request.form.get('userid')
            user_info = User.query.filter_by(id=userid).first()
            t = Trait.query.filter_by(user_id=userid).first()
            dateTaken = t.date
            timeStarted = t.time_started
            #resume algorithm model
            firstname = user_info.first_name
            middleIni = user_info.middle_name
            lastname = user_info.last_name
            company_id = user_info.company_id
            prefix = user_info.prefix
            pdf = user_info.file

            if prefix == '' or prefix == 0 or prefix == 'None' or prefix == 'none' or prefix == 'NOne' or prefix == 'NONe' or prefix == 'NONE':
                file_name = lastname+","+firstname+middleIni+"-Resume"
            else:
                file_name = lastname+","+prefix+","+firstname+middleIni+"-Resume"
            #resume model
            applicant_pdf_file = "./static/resume-file/pdf-file/"+pdf
            pdf_file = Path(__file__).parent / applicant_pdf_file

            user_file = userfile(pdf_file)
            Quality = user_file[0]
            Operations = user_file[1]
            Supplychain = user_file[2]
            Project = user_file[3]
            Data = user_file[4]
            Healthcare = user_file[5]

            #personality survey model
            user_trait = trait(userid,dateTaken,timeStarted)
            rows = user_trait[0]
            Agreeableness = round(user_trait[1])
            Conscientiousness = round(user_trait[2])
            Extraversion = round(user_trait[3])
            Neuroticism = round(user_trait[4])
            Openness = round(user_trait[5])

            save_final_trait = TraitFinal(agreeableness=Agreeableness,conscientiousness=Conscientiousness,extroversion=Extraversion,neuroticism=Neuroticism,openness=Openness,user_id=userid,company_id=company_id)
            save_resume_score = ResumeFinal(quality=Quality,operations=Operations,supplychain=Supplychain,project=Project,data=Data,healthcare=Healthcare,user_id=userid,company_id=company_id)
            try:
                #try:
                db.session.add(save_final_trait)
                db.session.add(save_resume_score)
                db.session.commit()
                flash('Successfully Save the data!!!', category='success')
                return redirect('/user_result_meaning')
                #except:
                #    flash('Could\'nt Save your data. Please contact the personel incharge', category='error')
                #    return render_template("/users/User/user-survey-form-confirm.html", user=current_user)
            except:
                flash('Something Might wrong.. Please contact personel incharge!!', category='error')
                return render_template("/users/User/user-survey-form-confirm.html",user=current_user)
            #return redirect('/user-result-meaning')
        return render_template("/users/User/user-survey-form-confirm.html", user=current_user)
    else:
        return redirect('/')
    
# User Trait Meaning
@views.route('/user_result_meaning', methods=['GET','POST'])
def user_result_meaning():
    if "user" in session:
        userid = session["user"]
        return render_template("/users/User/user-result-meaning.html", user=current_user)
    else:
        return redirect('/')