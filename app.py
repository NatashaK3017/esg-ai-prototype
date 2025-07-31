import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Import API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function to load mock Excel data
@st.cache_data
def load_excel(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Load your mock data (update the path if needed)
emissions_df = load_excel("mock_esg_data.xlsx", sheet_name="Emissions")

# Dummy ESG documents text
sustainability_policy_text = """Our company is committed to reducing emissions across operations and engaging suppliers to improve Scope 3 performance..."""
board_charter_text = """The board oversees all governance matters including ethical conduct, risk management, and corporate transparency..."""

st.title("ESG Reporting Prototype")

# Show the emissions data
st.header("Emissions Data")
st.dataframe(emissions_df)

# Show dummy documents
st.header("Sustainability Policy")
st.write(sustainability_policy_text)

st.header("Board Charter")
st.write(board_charter_text)

# Text input for prompt to AI
prompt_input = st.text_area("Enter your question or prompt about ESG reporting:")

if st.button("Generate AI Response"):
    if not prompt_input.strip():
        st.warning("Please enter a prompt.")
    else:
        # Compose the full prompt for the AI, combining dummy docs + user input
        full_prompt = (
            f"Sustainability Policy:\n{sustainability_policy_text}\n\n"
            f"Board Charter:\n{board_charter_text}\n\n"
            f"Emissions Data Summary:\n{emissions_df.describe().to_string()}\n\n"
            f"User Question: {prompt_input}\n"
            f"Answer the question based on the above ESG data and documents."
        )

        # Call OpenAI's chat completion
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.3,
            )
            answer = response.choices[0].message.content
            st.subheader("AI Response")
            st.write(answer)

        except Exception as e:
            st.error(f"Error calling OpenAI API: {e}")
