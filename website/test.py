import csv,os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from .models import Term
from . import db
import PyPDF2
import textract
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inline

pdf = 'Pueblo Sandy G. - Epic 3 - CV.pdf'

def userfile(pdf):
    # Open pdf file
    #pdf = 'Pueblo Sandy G. - Epic 3 - CV.pdf'
    resume_input = open(pdf,'rb')
    # Read file
    pdfReader = PyPDF2.PdfFileReader(resume_input)
    # Get total number of pages
    num_pages = pdfReader.numPages
    # Initialize a count for the number of pages
    count = 0
    # Initialize a text empty etring variable
    text = ""
    # Extract text from every page on the file
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()

        # Convert all strings to lowercase
    text = text.lower()
    # Remove numbers
    text = re.sub(r'\d+','',text)
    # Remove punctuation
    text = text.translate(str.maketrans('','',string.punctuation))

    quality = Term.query.filter_by(term_under="Quality/Six_Sigma").first()
    operation = Term.query.filter_by(term_under="Operations_management").first()
    supply = Term.query.filter_by(term_under="Supply_chain").first()
    project = Term.query.filter_by(term_under="Project management").first()
    data = Term.query.filter_by(term_under="Data_analytics").first()
    health = Term.query.filter_by(term_under="Healthcare").first()

    # Create dictionary with industrial and system engineering key terms by area
    terms = {'Quality/Six Sigma':[quality],      
        'Operations management':[operation],
        'Supply chain':[supply],
        'Project management':[supply],
        'Data analytics':[data],
        'Healthcare':[health]}

    # Initializie score counters for each area
    quality = 0
    operations = 0
    supplychain = 0
    project = 0
    data = 0
    healthcare = 0
    # Create an empty list where the scores will be stored
    scores = []
    # Obtain the scores for each area
    for area in terms.keys():     
        if area == 'Quality/Six Sigma':
            for word in terms[area]:
                if word in text:
                    quality +=1
            scores.append(quality)      
        elif area == 'Operations management':
            for word in terms[area]:
                if word in text:
                    operations +=1
            scores.append(operations)       
        elif area == 'Supply chain':
            for word in terms[area]:
                if word in text:
                    supplychain +=1
            scores.append(supplychain)       
        elif area == 'Project management':
            for word in terms[area]:
                if word in text:
                    project +=1
            scores.append(project)     
        elif area == 'Data analytics':
            for word in terms[area]:
                if word in text:
                    data +=1
            scores.append(data)       
        else:
            for word in terms[area]:
                if word in text:
                    healthcare +=1
            scores.append(healthcare)

    # Create a data frame with the scores summary
    #summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
    #summary

    # Create pie chart visualization
    #pie = plt.figure(figsize=(10,10))
    #plt.pie(summary['score'], labels=summary.index, explode = (0.1,0,0,0,0,0), autopct='%1.0f%%',shadow=True,startangle=90)
    #plt.title('Industrial Engineering Candidate - Resume Decomposition by Areas')
    #plt.axis('equal')
    #plt.show()

    # Save pie chart as a .png file
    #pie.savefig('resume_screening_results.png')

    return quality,operations,supplychain,project,data,healthcare

app = userfile()

if __name__== "__main__":
    app.run(debug=True)