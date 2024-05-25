import streamlit as st
import openai
from openai import AsyncOpenAI
import asyncio

# Setup the OpenAI client using an asynchronous client with the secret API key
client = AsyncOpenAI(api_key=st.secrets["API_key"])

# Function to generate response from OpenAI API
async def generate_response(messages):
    completion = await client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return completion.choices[0].message.content

# Function to fetch response and store it in session state
async def fetch_response(messages, session_key):
    response = await generate_response(messages)
    st.session_state[session_key] = response

# Main function to run the Streamlit app
def main():
    st.title("RoamRanger")
    st.subheader("RoamRanger is a user-friendly web application designed to help users discover ideal vacation spots based on their preferences. By guiding users through a multi-level prompting process, RoamRanger leverages the power of OpenAI's GPT-3 API to generate personalized recommendations and detailed information about various vacation destinations.")
    st.text("Bernadette E. Alabado\n"
            "BSCS 3-B AI\n"
            "West Visayas State University")

    # Initialize session state variables if they don't exist
    if 'level' not in st.session_state:
        st.session_state.level = 1
        st.session_state.prompt = []

    # Level 1: Ask the user for the type of vacation place
    if st.session_state.level == 1:
        type_of_vacation = st.text_input("What type of vacation place are you looking for? (e.g., beach, mountain, city, etc.)")
        if st.button("Submit", key="level1"):
            st.session_state.prompt.append({"role": "user", "content": type_of_vacation})
            st.session_state.level += 1

    # Level 2: Ask the API for the specific names of vacation places
    if st.session_state.level >= 2:
        examples_question = f"Can you suggest some specific names of {st.session_state.prompt[0]['content']} vacation places?"
        if 'examples' not in st.session_state:
            st.session_state.prompt.append({"role": "user", "content": examples_question})
            asyncio.run(fetch_response(st.session_state.prompt, 'examples'))

        # Display the examples fetched from the API
        if 'examples' in st.session_state:
            st.write("Here are the TOP 10 recommended places:")
            st.write(st.session_state.examples)

            # Provide a button to proceed to the next step
            if st.session_state.level == 2:
                if st.button("Next", key="level2"):
                    st.session_state.level += 1

    # Level 3: Ask the user to choose a specific vacation place from the examples
    if st.session_state.level >= 3:
        place_choice = st.text_input("Enter the name of the vacation place you are interested in from the examples above:")
        if place_choice and st.session_state.level == 3:
            st.session_state.prompt.append({"role": "user", "content": place_choice})
            if st.button("Submit", key="level3"):
                st.session_state.level += 1

    # Level 4: Ask the API for detailed information about the chosen place
    if st.session_state.level >= 4:
        detailed_question = f"What are the age restrictions, cultural norms, entrance fees, and activities available at {st.session_state.prompt[2]['content']}? Also, provide some travel tips for visitors."
        if 'detailed_info' not in st.session_state:
            st.session_state.prompt.append({"role": "user", "content": detailed_question})
            asyncio.run(fetch_response(st.session_state.prompt, 'detailed_info'))

        # Display the detailed information fetched from the API
        if 'detailed_info' in st.session_state:
            st.write(f"Details for {st.session_state.prompt[2]['content']}:")
            st.write(st.session_state.detailed_info)

            # Optional: Display images from a URL
            image_url = f"https://example.com/images/{st.session_state.prompt[2]['content'].replace(' ', '_').lower()}.jpg"  # Placeholder URL
            st.image(image_url, caption=f"Scenic view of {st.session_state.prompt[2]['content']}")

            # Provide a button to start over the process
            if st.button("Start Over"):
                st.session_state.level = 1
                st.session_state.prompt = []
                st.experimental_rerun()

            # Display a thank you message
            st.write("Thank you for using RoamRanger!")

if __name__ == "__main__":
    main()
