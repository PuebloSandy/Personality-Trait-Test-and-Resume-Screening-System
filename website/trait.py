from csv import DictWriter
from datetime import date
import csv, os
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path

def trait(userid,date_taken,timeStarted):
    csv_file = csv.reader(open('./website/dataset/result-data.csv','r'))
    for row in csv_file:
        if userid==row[51] and date_taken==row[52] and timeStarted==row[53]:
            row_userid = row[0] #user row number
            rows = row #user data
            row_num = int(row_userid) + 1 #user adding 1 to row
            row_get = row_num - 40 #minus the row of the user to get the nCluster 
            
            #Applicant data process on formula
            Ext = 20 + int(row[21]) - int(row[22])  + int(row[23]) - int(row[24]) + int(row[25]) - int(row[26]) + int(row[27]) - int(row[28]) + int(row[29]) - int(row[30])
            Agr = 14 - int(row[1]) + int(row[2]) - int(row[3]) + int(row[4]) - int(row[5]) + int(row[6]) - int(row[7]) + int(row[8]) + int(row[9]) + int(row[10])
            Cons = 14 + int(row[11]) - int(row[12]) + int(row[13]) - int(row[14]) + int(row[15]) - int(row[16]) + int(row[17]) - int(row[18]) + int(row[19]) + int(row[20])
            Neu = 38 - int(row[31]) + int(row[32])  - int(row[33]) + int(row[34]) - int(row[35]) - int(row[36]) - int(row[37]) - int(row[38]) - int(row[39]) - int(row[40])
            Open = 8 + int(row[41]) - int(row[42]) + int(row[43]) - int(row[44]) + int(row[45]) - int(row[46]) + int(row[47]) + int(row[48]) + int(row[49]) + int(row[50])

            df = pd.read_csv('./website/dataset/result-data.csv')
            columns = df.columns
            for column in columns:
                print(column)

            X = df[row_get:row_num][df.columns[1:50]]
            pd.set_option("display.max_columns",None)
            X = X.fillna(0)

            kmeans = MiniBatchKMeans(n_clusters=10, random_state=0, batch_size=100, max_iter=100).fit(X)
            len(kmeans.cluster_centers_)

            one = kmeans.cluster_centers_[0]
            two = kmeans.cluster_centers_[0]
            three = kmeans.cluster_centers_[0]
            four = kmeans.cluster_centers_[0]
            five = kmeans.cluster_centers_[0]
            six = kmeans.cluster_centers_[0]
            seven = kmeans.cluster_centers_[0]
            eight = kmeans.cluster_centers_[0]
            nine = kmeans.cluster_centers_[0]
            ten = kmeans.cluster_centers_[0]

            one_scores = {}
            one_scores['agreeableness_score'] = 14 - one[0] + one[1] - one[2] + one[3] - one[4] - one[5] + one[6] - one[7] + one[8] + one[9]
            one_scores['conscientiousness_score'] = 14 + one[0] - one[1] + one[2] - one[3] + one[4] - one[5] + one[6] - one[7] + one[8] + one[9]
            one_scores['extraversion_score'] = 20 + one[0] + one[1] + one[2] - one[3] + one[4] - one[5] + one[6] + one[7] + one[8] - one[9]
            one_scores['neuroticism_score'] = 38 - one[0] - one[1] + one[2] - one[3] + one[4] + one[5] + one[6] - one[7] + one[8] + one[9]
            one_scores['openness_score'] = 8 + one[0] - one[1] + one[2] - one[3] + one[4] - one[5] + one[6] - one[7] + one[8] + one[9]

            #Aggre = {}
            #Consc = {}
            #Extra = {}
            #Neuro = {}
            #Open = {}
            #Aggre['agreeableness_score'] = -one_scores['agreeableness_score'] + two_scores['agreeableness_score'] - three_scores['agreeableness_score'] + four_scores['agreeableness_score'] - five_scores['agreeableness_score'] - six_scores['agreeableness_score']  + seven_scores['agreeableness_score'] - eight_scores['agreeableness_score'] + nine_scores['agreeableness_score'] + ten_scores['agreeableness_score']
            #Consc['conscientiousness_score'] = one_scores['conscientiousness_score'] - two_scores['conscientiousness_score'] + three_scores['conscientiousness_score'] - four_scores['conscientiousness_score'] + five_scores['conscientiousness_score'] - six_scores['conscientiousness_score'] + seven_scores['conscientiousness_score'] - eight_scores['conscientiousness_score'] + nine_scores['conscientiousness_score'] + ten_scores['conscientiousness_score']
            #Extra['extraversion_score'] = one_scores['extraversion_score'] + two_scores['extraversion_score'] + three_scores['extraversion_score'] - four_scores['extraversion_score'] + five_scores['extraversion_score'] - six_scores['extraversion_score'] + seven_scores['extraversion_score'] + eight_scores['extraversion_score'] + nine_scores['extraversion_score'] - ten_scores['extraversion_score']
            #Neuro['neuroticism_score'] = one_scores['neuroticism_score'] - two_scores['neuroticism_score'] + three_scores['neuroticism_score'] - four_scores['neuroticism_score'] + five_scores['neuroticism_score'] - six_scores['neuroticism_score'] + seven_scores['neuroticism_score'] - eight_scores['neuroticism_score'] + nine_scores['neuroticism_score'] + ten_scores['neuroticism_score']
            #Open['openness_score'] = one_scores['openness_score'] - two_scores['openness_score'] + three_scores['openness_score'] - four_scores['openness_score'] + five_scores['openness_score'] - six_scores['openness_score'] + seven_scores['openness_score']  + eight_scores['openness_score'] + nine_scores['openness_score'] + ten_scores['openness_score'] 

            #Agreeableness = Aggre
            #Conscienciouness = Consc
            #Extraversion = Extra
            #Neuroticism = Neuro
            #Openness = Open
            #print(Agreeableness, Conscienciouness, Extraversion, Neuroticism, Openness)

            all_types = {'one': one,'two': two,'three': three,'four': four,'five': five,'six': six,'seven': seven,'eight': eight,'nine': nine,'ten': ten}
            all_types_scores = {}

            for name, personality_type in all_types.items():
                personality_trait = {}
                personality_trait['agreeableness_score'] = 14 - personality_type[0] + personality_type[1] - personality_type[2] + personality_type[3] - personality_type[4] - personality_type[5] + personality_type[6] - personality_type[7] + personality_type[8] + personality_type[9]
                personality_trait['conscientiousness_score'] = 14 + personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] - personality_type[5] + personality_type[6] - personality_type[7] + personality_type[8] + personality_type[9]
                personality_trait['extraversion_score'] = 20 + personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] - personality_type[5] + personality_type[6] + personality_type[7] + personality_type[8] - personality_type[9]
                personality_trait['neuroticism_score'] = 38 - personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] + personality_type[5] + personality_type[6] + personality_type[7] + personality_type[8] + personality_type[9]
                personality_trait['openness_score'] = 8 + personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] - personality_type[5] + personality_type[6] + personality_type[7] + personality_type[8] + personality_type[9]

                all_types_scores[name] = personality_trait

                all_extroversion = []
                all_neuroticism = []
                all_agreeableness = []
                all_conscientiousness = []
                all_openness = []

            for personality_type, personality_trait in all_types_scores.items():
                all_agreeableness = personality_trait['agreeableness_score']
                all_conscientiousness = personality_trait['conscientiousness_score']
                all_extroversion = personality_trait['extraversion_score']
                all_neuroticism = personality_trait['neuroticism_score']
                all_openness = personality_trait['openness_score']

            Agreeableness = all_agreeableness
            Conscientiousness = all_conscientiousness
            Extraversion = all_extroversion
            Neuroticism = all_neuroticism
            Openness = all_openness
            
    #return rows,Agreeableness,Conscientiousness,Extraversion,Neuroticism,Openness
    return rows,Agr,Cons,Ext,Neu,Open