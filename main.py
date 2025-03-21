from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_openai import ChatOpenAI  # ✅ Use the correct OpenAI model
from dotenv import load_dotenv
import os
import streamlit as st
import tempfile

def main():
    load_dotenv()

    # Load the OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEY is not set. Please check your .env file.")
        return

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")

    if csv_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            tmp_file.write(csv_file.getvalue())
            tmp_file_path = tmp_file.name

        # ✅ Use ChatOpenAI instead of OpenAI
        llm = ChatOpenAI(openai_api_key=api_key, temperature=0)

        # ✅ Allow dangerous code execution explicitly
        try:
            agent = create_csv_agent(llm, tmp_file_path, verbose=True, allow_dangerous_code=True)
        except Exception as e:
            st.error(f"❌ Failed to create agent: {e}")
            return

        user_question = st.text_input("Ask a question about your CSV: ")

        if user_question.strip():
            with st.spinner(text="Processing... ⏳"):
                try:
                    response = agent.run(user_question)
                    st.write(response)
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
