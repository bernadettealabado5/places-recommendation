import streamlit as st
import requests

# Setup the Gemini API client using the provided API key
gemini_api_key = st.secrets["gemini_api_key"]

# Function to get place recommendations based on the type of vacation place
def get_place_recommendations(vacation_type):
    # Example: You might use a different place recommendation service or API here
    # This is just a placeholder for demonstration purposes
    response = requests.get(f"https://api.example.com/places?type={vacation_type}&api_key={gemini_api_key}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get details of a specific place
def get_place_details(place_name):
    # Example: You might use a different service or API here to get place details
    # This is just a placeholder for demonstration purposes
    response = requests.get(f"https://api.example.com/place/{place_name}?api_key={gemini_api_key}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def app():
    st.title("Vacation Place Recommender")

    # Step 1: Get the type of vacation places the user is interested in
    vacation_type = st.text_input("Enter the type of vacation place you want to visit (e.g., Beach, Historical, Mountain, City, etc.):")

    if st.button("Generate Recommendations"):
        if vacation_type:
            recommendations = get_place_recommendations(vacation_type.lower())
            if recommendations:
                st.write("Here are some recommendations for you:")
                for recommendation in recommendations[:20]:
                    st.write(recommendation)
                place_choice = st.text_input("Enter the name of the place you want more details about:")
                if place_choice:
                    details = get_place_details(place_choice)
                    if details:
                        st.write("Details for", place_choice)
                        st.write("Entrance Fee:", details.get("entrance_fee", "Not available"))
                        st.write("Precautions:", details.get("precautions", "Not available"))
                        st.write("What to Bring:", details.get("what_to_bring", "Not available"))
                        st.write("Description:", details.get("description", "Not available"))
                    else:
                        st.error("Failed to retrieve details for", place_choice)
            else:
                st.error("Failed to retrieve recommendations. Please try again later.")
        else:
            st.error("Please enter a valid vacation type.")

if __name__ == "__main__":
    app()
