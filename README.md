# RoamRanger

Bernadette E. Alabado\n
BSCS 3-B AI\n
West Visayas Satte University

RoamRanger is a user-friendly web application designed to help users discover ideal vacation spots based on their preferences. By guiding users through a multi-level prompting process, RoamRanger leverages the power of OpenAI's GPT-3 API to generate personalized recommendations and detailed information about various vacation destinations.

## Introduction

RoamRanger helps users discover ideal vacation spots based on their preferences. Through a series of guided prompts, users can narrow down their vacation preferences, receive personalized recommendations, and get detailed information about various destinations. The application uses OpenAI's GPT-3 API to provide these recommendations and details.

## Project Setup

To set up this project, I began by writing the code on GitHub, using the Python programming language. After the coding was completed, I deployed the project on Streamlit, an open-source app framework. During the deployment process, I accessed the advanced settings within Streamlit to input the necessary API key, which is essential for utilizing the ChatGPT API successfully. This step ensured that the application could communicate with the ChatGPT service, enabling its functionality as intended. Make sure to have your python file to be deployed and its incorporating requirements.txt.

### Prerequisites

- Python 3.10.0
- Git
- Streamlit

## Functionalities

- **Vacation Type Selection:** Users can specify the type of vacation place they are looking for (e.g., beach, mountain, city).
- **Place Recommendations:** Based on the specified type, the application suggests specific vacation places.
- **Detailed Information:** Users can select a place from the recommendations to get detailed information about it, including age restrictions, cultural norms, entrance fees, activities, and travel tips.
- **Restart Option:** Users can start the process over at any time to explore different vacation options.

## Usage Instructions

1. **Run the application:**

    ```bash
    streamlit run main.py
    ```

2. **Interact with the application:** Open the URL provided by Streamlit in your browser and use the interface to interact with the application.

## Deployment Process

1. **Deploy to Streamlit Cloud:**

    - Navigate to [Streamlit Cloud](https://share.streamlit.io/).
    - Click on "New app" and connect your GitHub repository.
    - Choose the repository and branch (usually `main` or `master`).
    - Set the file path to `main.py`.
    - In the advanced settings, add your OpenAI API key under `Secrets`:

      ```toml
      [secrets]
      API_key = "your_openai_api_key_here"
      ```

2. **Launch The App:**

   Click "Deploy" and wait for the app to be deployed. You will be given a URL to access your Streamlit app.

## API Key Configuration

1. **Set API Key in Advanced Settings:**

    - Navigate to your deployed app on Streamlit Cloud.
    - Go to "Settings" and then "Advanced Settings".
    - Add your API key in the appropriate field.

    Alternatively, you can set the API key in your local environment:

    ```bash
    export API_KEY='your_openai_api_key'  # On Windows use `set API_KEY=your_openai_api_key`
    ```

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a pull request.
