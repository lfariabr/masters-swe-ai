# pages/TopicModeling.py

import streamlit as st
import pandas as pd
from resolvers.BERTopicModel import train_bertopic_model
from utils.preprocessing import classify_nps, calculate_nps
from utils.data_upload import data_upload
import time
import requests
import os
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def show_google_maps():
    """
    Main function for the Google Maps Page.
    Which will simply display 10 places and be plugged in google maps api to grab review data and throw it into our pipeline
    """
    st.title("📍 Google Maps")
    st.markdown("""
    Experiments with Google Maps API.
    """)

    if st.button("Run Google Maps"):
            with st.spinner("Fetching routes from Sydney Town Hall to Parramatta..."):
                # Use your actual API key
                api_key = GOOGLE_MAPS_API_KEY

                endpoint = "https://routes.googleapis.com/directions/v2:computeRoutes"
                headers = {
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": api_key,
                    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline"
                }

                body = {
                    "origin": {
                        "address": "Sydney Town Hall"
                    },
                    "destination": {
                        "address": "Parramatta, NSW"
                    },
                    "travelMode": "DRIVE"
                }

                response = requests.post(endpoint, headers=headers, json=body)

                if response.status_code == 200:
                    data = response.json()
                    route = data["routes"][0]
                    st.success("✅ Route fetched successfully!")
                    st.write(f"🛣️ Distance: {route['distanceMeters'] / 1000:.2f} km")
                    st.write(f"⏱️ Duration: {route['duration']}")
                else:
                    st.error(f"❌ Failed to fetch directions: {response.text}")

                    time.sleep(5)
                    st.success("Google Maps data fetched successfully!")
    else:
        st.info("""
        👆 **Select one of the available Stores and click Run Google Maps**        
        """)