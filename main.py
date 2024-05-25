import streamlit as st
import openai
import asyncio

# Setup the OpenAI client using an asynchronous client with the secret API key
client = AsyncOpenAI(api_key=st.secrets["API_key"])

async def generate_response(messages):
    response = await openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=messages
    )
    return response['choices'][0]['message']['content']

def main():
    st.title("Roam Ranger")
    st.subheader("Roam Ranger is a user-friendly web application designed to help users discover ideal vacation spots based on their preferences. By guiding users through a multi-level prompting process, RoamRanger leverages the power of OpenAI's GPT-3 API to generate personalized recommendations and detailed information about various vacation destinations.")
    st.text("Bernadette E. Alabado\n"
            "BSCS 3-B AI\n"
            "West Visayas State University")

    # Multi-Level Prompting
    if 'level' not in st.session_state:
        st.session_state.level = 1
        st.session_state.prompt = []

    st.write(f"Level {st.session_state.level} Prompt")

    if st.session_state.level == 1:
        type_of_vacation = st.text_input("What type of vacation place are you looking for? (e.g., beach, mountain, city, etc.)")
        if st.button("Submit", key="level1"):
            st.session_state.prompt.append({"role": "user", "content": type_of_vacation})
            st.session_state.level += 1

    elif st.session_state.level == 2:
        examples_question = f"Can you suggest some specific names of {st.session_state.prompt[0]['content']} vacation places?"
        st.session_state.prompt.append({"role": "user", "content": examples_question})

        if st.button("Get Examples", key="examples"):
            examples = asyncio.run(generate_response(st.session_state.prompt))
            st.write("Here are some examples:")
            st.write(examples)
            st.session_state.level += 1

    elif st.session_state.level == 3:
        place_choice = st.text_input("Enter the name of the vacation place you are interested in from the examples above:")
        if st.button("Submit", key="level3"):
            st.session_state.prompt.append({"role": "user", "content": place_choice})
            st.session_state.level += 1

    elif st.session_state.level == 4:
        detailed_question = f"What are the age restrictions, cultural norms, entrance fees, and activities available at {st.session_state.prompt[2]['content']}?"
        st.session_state.prompt.append({"role": "user", "content": detailed_question})

        if st.button("Get Detailed Information", key="detailed_info"):
            detailed_info = asyncio.run(generate_response(st.session_state.prompt))
            st.write(f"Details for {st.session_state.prompt[2]['content']}:")
            st.write(detailed_info)

            # Optional: Display images from a URL
            image_url = f"https://example.com/images/{st.session_state.prompt[2]['content'].replace(' ', '_').lower()}.jpg"  # Placeholder URL
            st.image(image_url, caption=f"Scenic view of {st.session_state.prompt[2]['content']}")

    if st.session_state.level > 4:
        st.write("Thank you for using the Creative Text Generator!")

if __name__ == "__main__":
    main()
