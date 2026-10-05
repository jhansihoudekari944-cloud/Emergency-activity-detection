from streamlit_js_eval import get_geolocation

def get_live_location():

    location = get_geolocation()

    if location is None:
        return None

    lat = location["coords"]["latitude"]
    lon = location["coords"]["longitude"]

    return lat, lon