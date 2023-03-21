import streamlit as st

from geopy.geocoders import Nominatim

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, r2_score

def Clean(L):
    New_L = []
    
    for i in L:
        if type(i) == int or type(i) == float:
            New_L.append(i)
            
    return New_L




def DepthCal(Df):
    AveragePre = sum( Clean(list(Df['WL PREMONSOON']))) / len(Df['WL PREMONSOON'])
    AveragePos = sum( Clean(list(Df['WL POSTMONSOON']))) / len(Df['WL POSTMONSOON'])
    AverageFlu = sum( Clean(list(Df['FLUCTUATION']))) / len(Df['FLUCTUATION'])
     
    Total = AverageFlu+AveragePos+AveragePre
    
    return Total

def AllCal(Df):
    ListVillage = list(Df.Village.unique())
    
    FinalList = []
    
    for i in ListVillage:
        newDf = Df.loc[Df['Village'] == i]
        # print(newDf)
        FinalList.append((i, DepthCal(newDf)))
    
    max_tuple = max(FinalList, key=lambda tup: tup[1])
    
    return max_tuple


data = pd.read_excel('total_water.xlsx')

st.sidebar.title('Developer\'s Contact')
st.sidebar.markdown('[![Chethan-Reddy]'
                '(https://img.shields.io/badge/Author-Py%20Decoders-brightgreen)]'
                '(https://www.linkedin.com/in/chethan-reddy-0201791ba/)') 

st.sidebar.success("IT Day Rajasthan Hackathon")

st.sidebar.image("borewell-drilling-process.jpg")

st.sidebar.caption("""1. The Bore Well Location Predictor for Villages of Rajasthan is a tool that 
holds great importance for the rural communities of Rajasthan. As water scarcity is a major issue 
in the state, this tool provides valuable information for the villagers to locate the best spots for 
digging bore wells.

2. By using this tool, villagers can identify areas with a higher probability of 
finding water, which can save them time and resources in their search for a reliable water source. 
This can also help them avoid digging dry wells or wells that yield insufficient water, which can be 
a significant economic burden for them.

3. Moreover, the tool can also be used to promote sustainable water usage by encouraging 
villagers to dig bore wells in areas that are likely to replenish quickly. This can help in conserving 
water and preventing depletion of groundwater resources.""")

st.title("Bore Well Location Predictor for Villages of Rajasthan")

st.image("Average-depth-to-water-level-map-of-the-western-Rajasthan-source-NRAA-2014.png")

with st.form("my_form"):
   st.subheader("Selec the Given Details")

   District = st.selectbox("Select the district" , list(data.District.unique()))
   Block = st.selectbox("Select the block of the district" , list(data.Block.unique()))
  

   submitted = st.form_submit_button("Predict the Location")

   if submitted == True:
      myData =  data.loc[data['District'] == District]
      myData = myData.loc[myData['Block'] == Block]

      Ans = AllCal(myData)

      st.write(f"The best village to increate the bore Wells is {Ans[0]} with a score of {Ans[1]}")

      geolocator = Nominatim(user_agent="MyApp")
      location = geolocator.geocode(f"Rajasthan {Ans[0]}")

      st.write("The latitude of the Village is: ", location.latitude)
      st.write("The longitude of the Village is: ", location.longitude)


      df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [location.latitude,location.longitude],
            columns=['lat', 'lon'])
      
      st.map(df, zoom=10)

      st.subheader("To Locations where you can insert the borewell!!!")
      st.dataframe(df)





