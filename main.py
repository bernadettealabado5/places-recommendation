import streamlit as st
import openai
import asyncio

# Setup the OpenAI client using an asynchronous client with the secret API key
openai.api_key = st.secrets["API_key"]

async def generate_response(messages):
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=messages
    )
    return response['choices'][0]['message']['content']

async def fetch_response(messages, session_key):
    response = await generate_response(messages)
    st.session_state[session_key] = response

def main():
    st.title("RoamRanger")
    st.subheader("RoamRanger is a user-friendly web application designed to help users discover ideal vacation spots based on their preferences. By guiding users through a multi-level prompting process, RoamRanger leverages the power of OpenAI's GPT-4 API to generate personalized recommendations and detailed information about various vacation destinations.")
    st.text("Bernadette E. Alabado\n"
            "BSCS 3-B AI\n"
            "West Visayas State University")

    # Initialize session state variables if they don't exist
    if 'level' not in st.session_state:
        st.session_state.level = 1
        st.session_state.prompt = []
    if 'more_examples' not in st.session_state:
        st.session_state.more_examples = 0

    if st.session_state.level == 1:
        type_of_vacation = st.text_input("What type of vacation place are you looking for? (e.g., beach, mountain, city, etc.)")
        if st.button("Submit", key="level1"):
            st.session_state.prompt.append({"role": "user", "content": type_of_vacation})
            st.session_state.level += 1
            st.experimental_rerun()

    if st.session_state.level >= 2:
        examples_question = f"Can you suggest some specific names of {st.session_state.prompt[0]['content']} vacation places?"
        if 'examples' not in st.session_state or st.session_state.more_examples > 0:
            if st.session_state.more_examples > 0:
                examples_question = f"Can you suggest more specific names of {st.session_state.prompt[0]['content']} vacation places?"
                st.session_state.more_examples = 0
            st.session_state.prompt.append({"role": "user", "content": examples_question})
            asyncio.run(fetch_response(st.session_state.prompt, 'examples'))
            st.experimental_rerun()

        if 'examples' in st.session_state:
            st.write("Here are some examples:")
            st.write(st.session_state.examples)
            if st.button("Get More Examples", key="more_examples"):
                st.session_state.more_examples += 1
                st.experimental_rerun()

            if st.session_state.level == 2:
                if st.button("Next", key="level2"):
                    st.session_state.level += 1
                    st.experimental_rerun()

    if st.session_state.level >= 3:
        place_choice = st.text_input("Enter the name of the vacation place you are interested in from the examples above:")
        if place_choice and st.session_state.level == 3:
            st.session_state.prompt.append({"role": "user", "content": place_choice})
            if st.button("Submit", key="level3"):
                st.session_state.level += 1
                st.experimental_rerun()

    if st.session_state.level >= 4:
        detailed_question = f"What are the age restrictions, cultural norms, entrance fees, and activities available at {st.session_state.prompt[2]['content']}? Also, provide some travel tips for visitors."
        if 'detailed_info' not in st.session_state:
            st.session_state.prompt.append({"role": "user", "content": detailed_question})
            asyncio.run(fetch_response(st.session_state.prompt, 'detailed_info'))
            st.experimental_rerun()

        if 'detailed_info' in st.session_state:
            st.write(f"Details for {st.session_state.prompt[2]['content']}:")
            st.write(st.session_state.detailed_info)

            # Optional: Display images from a URL
            image_url = f"https://example.com/images/{st.session_state.prompt[2]['content'].replace(' ', '_').lower()}.jpg"  # Placeholder URL
            st.image(image_url, caption=f"Scenic view of {st.session_state.prompt[2]['content']}")

    if st.session_state.level > 4:
        st.write("Thank you for using RoamRanger!")

if __name__ == "__main__":
    main()
