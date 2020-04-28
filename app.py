import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


DATA_URL = (
"C:/Users/Gowri/Desktop/streamlit_project/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
#Here I added that emoji by copy pasting from google here
st.markdown("This application is a Streamlit dashboard that can be used "
"to analyze motor vehicle collisions in NYC 🗽" )

#Decorate our function with st.cache since we dont want to redo this computation each time app is rerun
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']] )
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    #you cannot have any missing values in the latitude and longitude as that would just break the application
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace = True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)
original_data = data

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("No: of people injured in the collsions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a given time of day?")
#hour = st.selectbox("Hour to look at", range(0,24),1)
hour = st.slider("Hour to look at", 0,23)
#hour = st.sidebar.slider("Hour to look at", 0,23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour,(hour+1)% 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

#read documentation of pydeck further
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state = {
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time', 'latitude', 'longitude']],
        get_position=['longitude', 'latitude'],
        radius = 100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour+1)%24))
filtered = data[
    (data['date/time'].dt.hour>=hour) & (data['date/time'].dt.hour<(hour+1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height = 400)
st.write(fig)

#Selecting top 5 streets where people have been injured the most
st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people',['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
