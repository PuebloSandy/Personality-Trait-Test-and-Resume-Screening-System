from csv import DictWriter
from datetime import date
import csv, os
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path

def per(userid):
    csv_file = csv.reader(open('./website/dataset/result-data.csv','r'))
    for row in csv_file:
        if userid==row[51]:
            row_data = row[0]
            Extraversion = 20 + int(row[21]) - int(row[22])  + int(row[23]) - int(row[24]) + int(row[25]) - int(row[26]) + int(row[27]) - int(row[28]) + int(row[29]) - int(row[30])
            Agreaableness = 14 - int(row[1]) + int(row[2]) - int(row[3]) + int(row[4]) - int(row[5]) + int(row[6]) - int(row[7]) + int(row[8]) + int(row[9]) + int(row[10])
            Conscienciouness = 14 + int(row[11]) - int(row[12])  + int(row[13]) - int(row[14]) + int(row[15]) - int(row[16]) + int(row[17]) - int(row[18]) + int(row[19]) + int(row[20])
            Neuroticism = 38 - int(row[31]) + int(row[32])  - int(row[33]) + int(row[34]) - int(row[35]) - int(row[36]) - int(row[37]) - int(row[38]) - int(row[39]) - int(row[40])
            Openness = 8 + int(row[41]) - int(row[42]) + int(row[43]) - int(row[44]) + int(row[45]) - int(row[46]) + int(row[47]) + int(row[48]) + int(row[49]) + int(row[50])

    return Extraversion,Agreaableness,Conscienciouness,Neuroticism,Openness,row_data