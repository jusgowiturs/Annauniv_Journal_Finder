#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import spacy
from multiprocessing import Pool
#import en_core_web_sm
import en_core_web_md
nlp=en_core_web_md.load(disable=["parser", "tagger", "ner"])
#nlp=spacy.load('en_core_web_sm',disable=["parser", "tagger", "ner"])

import numpy as np



Table = pd.read_json('List_of_Journals_Vectors.json')
#Table = pd.read_csv('List_of_Journals_Vectors.csv')


Abstract = "This article proposes a support diminution design method for layered manufacturing of manifold surface based on variable orientation tracking (VOT). We aim at reducing the external support or upholders to a minimum with maximum possibility theoretically to save material and diminish material stripping effect (MSE), thereby improving the bilateral surface precision either exterior or interior. The cosmic gravity effect criterion is first used to extract surface need support from manifold surface with various materials by considering the balance force involving material characteristics and inclination angle. In the light of this criterion theory, varying the substrate normal orientation (SNO), namely workbench, for each layer in printing coordinate system, may break the balance between gravity and its equilibrium force. Therefore, the optimal SNO can be rigorously calculated using mathematical harmonic analysis among the continuous domain. To serve for the multidegree of freedom (DOF) on account of SNO, a reconfigurable VOT robot with six-axis DOF is developed for 3D printing (3DP). The matched servo controller is successfully implemented to accurate tracking of both orientation and Cartesian coordinates, using forward kinematic chains as well as reverse kinematic tracking"



X = nlp(Abstract)
#X.vector.shape




def Similarity(X):
    Y = nlp(Abstract).vector
    return np.dot(X,Y)/(np.linalg.norm(X) * np.linalg.norm(Y))




Table["Vec"] = Table["Vector"].apply(NUMPYArray)



Table.Vec.shape

























def NUMPYArray(X):
    return np.array(X)




Sim = Table.Vector.apply(Similarity)




Sim



#np.vectorize(Similarity)(Table.Vector,X.vector)







Column = Table.columns




Sorted_List = list(Sim.sort_values(ascending=False).index)[0:10]



New_Table = Table[Table.index.isin(Sorted_List)]
New_Table = New_Table.drop(["Sl.No","Vector","ISSN"],axis =1)

New_Table

