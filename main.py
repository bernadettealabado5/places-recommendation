import streamlit as st
import openai
from openai import AsyncOpenAI
import requests  # For fetching images from URLs

# Setup the OpenAI client using an asynchronous client with the secret API key
client = AsyncOpenAI(api_key=st.secrets["API_key"])

async def generate_response(question, context):
    model = "gpt-4-0125-preview"
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question},
            {"role": "system", "content": context}
        ]
    )
    return completion.choices[0].message.content

async def app():
    st.title("Vacation Place Recommender")
    st.text("Group 1 Intelligent Systems Final Project\n"
            "Bernadette E. Alabado\n"
            "Samantha V. Bangcaya\n"
            "Yllennor Anne V. Carbonell\n"
            "Asie Jay E. Fondales\n"
            "Almera J. Valladolid\n"
            "BSCS 3-B AI\n"
            "West Visayas State University")

    # Step 1: Get the type of vacation places the user is interested in
    type_of_vacation = st.text_input("What type of vacation place are you looking for? (e.g., beach, mountain, city, etc.)")

    # Button to handle fetching more examples
    more_examples_state = st.session_state.get('more_examples', 0)  # Tracks the number of times more examples were requested

    # Step 2: Provide examples and further info based on user interest
    if type_of_vacation:
        examples_context = f"Provide {more_examples_state+1} set(s) of examples of vacation places suitable for enjoying a {type_of_vacation} environment."
        examples_question = f"Can you suggest some specific names of {type_of_vacation} vacation places? More examples."
        if st.button("Get Examples", key="examples") or more_examples_state:
            examples = await generate_response(examples_question, examples_context)
            st.write("Here are some examples:")
            st.write(examples)

        # Button to get more examples
        if st.button("More Examples"):
            more_examples_state += 1
            st.session_state['more_examples'] = more_examples_state  # Update session state
        
        # Step 3: Gather more information about a specific place chosen by the user
        place_choice = st.text_input("Enter the name of the vacation place you are interested in from the examples above:")
        
        if place_choice:
            if st.button("Get Detailed Information", key="detailed_info"):
                detailed_context = f"Comprehensive information about {place_choice}, including age restrictions, cultural norms, potential expenses like entrance fees, and activities available."
                detailed_question = f"What are the age restrictions, cultural norms, entrance fees, and activities available at {place_choice}?"
                
                detailed_info = await generate_response(detailed_question, detailed_context)
                st.write(f"Details for {place_choice}:")
                st.write(detailed_info)
                
                # Optional: Display images from a URL
                image_url = f"https://example.com/images/{place_choice.replace(' ', '_').lower()}.jpg"  # Placeholder URL
                st.image(image_url, caption=f"Scenic view of {place_choice}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
