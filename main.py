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

    # Step 1: Get the type of vacation places the user is interested in
    type_of_vacation = st.text_input("What type of vacation place are you looking for? (e.g., beach, mountain, city, etc.)")
    
    # Step 2: Provide examples and further info based on user interest
    if type_of_vacation:
        examples_context = "Provide examples of vacation places suitable for enjoying a " + type_of_vacation + " environment."
        examples_question = f"Can you suggest some {type_of_vacation} vacation places?"
        if st.button("Get Examples", key="examples"):
            examples = await generate_response(examples_question, examples_context)
            st.write("Here are some examples:")
            st.write(examples)
        
        # Step 3: Gather more information about a specific place chosen by the user
        place_choice = st.text_input("Enter the name of the vacation place you are interested in from the examples above:")
        
        if place_choice:
            if st.button("Get Information", key="info"):
                details_context = f"Details about activities and photos for {place_choice}."
                details_question = f"Can you provide details and activities available at {place_choice}?"
                
                details = await generate_response(details_question, details_context)
                st.write(f"Details for {place_choice}:")
                st.write(details)
                
                # Optional: Display images from a URL
                image_url = f"https://example.com/images/{place_choice.replace(' ', '_').lower()}.jpg"  # Placeholder URL
                st.image(image_url, caption=f"Scenic view of {place_choice}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(app())
