import streamlit as st
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd
# Initialize Nominatim API
geolocator = Nominatim(user_agent="MyApp")


location = geolocator.geocode("Rajasthan Chirasara")

print("The latitude of the location is: ", location.latitude)
print("The longitude of the location is: ", location.longitude)



df = pd.DataFrame(
    np.random.randn(10, 2) / [10, 10] + [location.latitude,location.longitude],
    columns=['lat', 'lon'])

st.dataframe(df)


st.map(df, use_container_width = True)

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [location.latitude,location.longitude],
    columns=['lat', 'lon'])

import pandas as pd


st.map(df, zoom=10)