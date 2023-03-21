import streamlit as st

from geopy.geocoders import Nominatim

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, r2_score

data = pd.read_excel('total_water.xlsx')

# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")

location = geolocator.geocode("Rajasthan")

print("The latitude of the location is: ", location.latitude)
print("The longitude of the location is: ", location.longitude)

st.sidebar.title('Developer\'s Contact')
st.sidebar.markdown('[![Chethan-Reddy]'
                '(https://img.shields.io/badge/Author-Py%20Decoders-brightgreen)]'
                '(https://www.linkedin.com/in/chethan-reddy-0201791ba/)') 

st.sidebar.success("IT Day Rajasthan Hackathon")

st.sidebar.image("Water_clear.jpeg")

st.sidebar.caption("""Overall, the forecasting tool for water levels in Rajasthan 
can provide crucial information to the government that can help in better water resource management 
and planning, leading to sustainable development in the state.""")



import streamlit as st
import pandas as pd
import numpy as np

st.title("Forecasting Tool for water levels in Rajasthan")

st.write("""This tool is a forecasting model that provides information on water
 levels in Rajasthan based on inputs such as district, block, village, and well type. 
 It provides three outputs, namely water level pre-monsoon, water level post-monsoon, and fluctuation. 
 The tool aims to assist in water resource management and planning by providing 
timely and accurate information on water availability in specific areas.""")

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [location.latitude,location.longitude],
    columns=['lat', 'lon'])

import pandas as pd


st.map(df, zoom=10)

submitted = None


with st.form("my_form"):
   st.subheader("Selec the Given Details")

   District = st.selectbox("Select the district" , list(data.District.unique()))
   Block = st.selectbox("Select the block of the district" , list(data.Block.unique()))
   Village = st.selectbox("Select the village of the block" , list(data.Village.unique()))
   WellType = st.radio("Selec the well Type",list(data['Well Type'].unique()))

   # Every form must have a submit button.
   submitted = st.form_submit_button("Predict")

   if submitted == True:
        location = geolocator.geocode(f"Rajasthan {Village}")

        st.write("The latitude of the Village is: ", location.latitude)
        st.write("The longitude of the Village is: ", location.longitude)


        print("Yes")
        myData = data.loc[data['District'] == District]
        myData = myData.loc[myData['Block'] == Block]
        myData = myData.loc[myData['Village'] == Village]
        myData = myData.loc[myData['Well Type'] == WellType]
        myData = myData.sort_values(by=['Year'])

        x = list(np.array(myData['Year']))
        y1 = list(np.array(myData['WL PREMONSOON']))

        print(x,y1)

        mymodel1 = np.poly1d(np.polyfit(x, y1, 3))

        myline = [2020,2021, 2022, 2023, 2024]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=myData['Year'], y=myData['WL PREMONSOON'],   mode='lines+markers' , name='Water Level Presmonsoon Acctual'))
        y_pred1 = list(mymodel1(myline))
        y_pred1[0] = list(myData['WL PREMONSOON'])[len(myData['WL PREMONSOON']) - 1]
        fig.add_trace(go.Scatter(x=myline, y=y_pred1,   mode='lines+markers', name="Water Level PremonsoonPredicted"))
        fig.update_layout(width=800, height=550, xaxis_title='Year',
            yaxis_title='Level Indicator')
        

        x = list(np.array(myData['Year']))
        y2 = list(np.array(myData['WL POSTMONSOON']))

        print(x,y2)

        mymodel2 = np.poly1d(np.polyfit(x, y2, 3))

        myline = [2020,2021, 2022, 2023, 2024]

        fig.add_trace(go.Scatter(x=myData['Year'], y=myData['WL POSTMONSOON'],   mode='lines+markers' , name='Water Level Postmonsoon Acctual'))
        y_pred2 = list(mymodel2(myline))
        y_pred2[0] = list(myData['WL POSTMONSOON'])[len(myData['WL POSTMONSOON']) - 1]
        fig.add_trace(go.Scatter(x=myline, y=y_pred2,   mode='lines+markers', name="Water Level Postmonsoon Predicted"))
        fig.update_layout(width=800, height=550, xaxis_title='Year',
            yaxis_title='Level Indicator') 
        
        x = list(np.array(myData['Year']))
        y3 = list(np.array(myData['FLUCTUATION']))

        print(x,y3)

        mymodel3 = np.poly1d(np.polyfit(x, y3, 3))

        myline = [2020,2021, 2022, 2023, 2024]

        fig.add_trace(go.Scatter(x=myData['Year'], y=myData['FLUCTUATION'],   mode='lines+markers' , name='FLUCTUATION Acctual'))
        y_pred3 = list(mymodel3(myline))
        y_pred3[0] = list(myData['FLUCTUATION'])[len(myData['FLUCTUATION']) - 1]
        fig.add_trace(go.Scatter(x=myline, y=y_pred3,   mode='lines+markers', name="FLUCTUATION Predicted"))
        fig.update_layout(width=800, height=550, xaxis_title='Year',
            yaxis_title='Level Indicator') 


        
        
if submitted == True:
    st.write(fig)
