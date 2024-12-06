import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.title("Attendance Tracker")
st.subheader("Today's Attendance")

ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
hour = int(timestamp[:2])
if hour >= 11 and hour < 13:
    # If so, set the subject to "AI"
    subject = "AI"
# Otherwise, check if the current time is between 1:00pm and 3:00pm
elif hour >= 13 and hour < 15:
    # If so, set the subject to "DSE6"
    subject = "DSE6"
# If neither condition is met, set the subject to None
else:
    subject = None

df = pd.read_csv("C:/Users/VINAY SAHAL/PycharmProjects/FaceRecognition/Atttendance" + date + ".csv")

st.dataframe(df.style.highlight_max(axis=0))
