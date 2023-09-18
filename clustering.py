# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:21:21 2023

@author: SemanurSancar
"""

import joblib
from sklearn.preprocessing import StandardScaler
import pandas as pd
from typing import Tuple


def kmeans_clustering(ave_gen_table_selected_coor: pd.DataFrame) -> Tuple[int]:
    kmeans = joblib.load('kmeans_model_100.pkl')
    # İstediğiniz iki sütunu seçin
    
    ave_gen_table_selected_coor_for_clustering = pd.concat([ave_gen_table_selected_coor["Average Generation [kWh]"], ave_gen_table_selected_coor["Standard Dev."]])
    ave_gen_table_selected_coor_for_clustering = pd.DataFrame(ave_gen_table_selected_coor_for_clustering).T
    
    
    data = ave_gen_table_selected_coor_for_clustering
    
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    # KMeans modeli ile kümeye aidiyeti tahmin etme
    kmeans_labels_generation = kmeans.predict(data_scaled)
    
    cluster = kmeans_labels_generation[0]
    
    return cluster