# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

#Load in our fitted models:
TOPICmodel = joblib.load("QTOPICmodel.joblib")

#Now take the user's input and produce a prediction:
def app():
    
    st.title("Question Topic Prediction")
    
    st.markdown('Enter values in the fields below. This app will provide a prediction for what question topic may be more likely to be asked by farmers when experiencing these conditions. Default values are averages taken from the training dataset. The more fields you can fill, the better the prediction.')

    st.markdown("Note: weather data used in training the model were monthly averages, except for precipitation which (in the model creator's best educated guess) is a monthly total. Daily values can be entered for all fields; this app will automatically assume a 30-day month and will scale your precipitation input behind the scenes.")
    
    LowTemp = st.number_input('Low temp (C):',min_value=0.0,max_value=100.0,value=19.9052)
    HighTemp = st.number_input('High temp (C):',min_value=0.0,max_value=100.0,value=29.1939)
    RelativeHumidity = st.number_input('Relative Humidity (percent):',min_value=0.0,max_value=100.0,value=65.9956)
    Precipitation = st.number_input('Precipitation (mm):',min_value=0.0,max_value=10000.0,value=3.27921)
    


    text_input = pd.DataFrame({
                               'avg_max_temp':[HighTemp],
                               'precipitation':[Precipitation*30], #Assuming 30 day month
                               'relative_humidity':[RelativeHumidity],
                               'avg_min_temp': [LowTemp]
                               })

    
    predicted = TOPICmodel.predict(text_input)

    st.markdown('Predicted topic: :blue[{top}]'.format(top=predicted))
# 
if __name__ == '__main__':
    app()