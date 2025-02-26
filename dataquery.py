import streamlit as st
import openai
import pandas as pd
from openai import OpenAI
from config import openai_api_key

client=OpenAI(api_key=openai_api_key)

# Streamlit app
st.title("Excel Question Answering with GPT")

# File uploader for Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load the Excel file into a Pandas DataFrame
        df = pd.read_excel(uploaded_file)

        # Display a sample of the data (optional)
        if st.checkbox("Show sample data"):
            st.dataframe(df.head())

        question = st.text_area("Enter your question about the Excel data:", height=100)

        if st.button("Submit"):
            if not question:
                st.warning("Please enter a question.")
            else:
                # 1. Excel Data Description for GPT
                data_description = f"Excel Data:\n{df.head(100).to_string()}\n\nColumn Names: {', '.join(df.columns)}"
                print("I have reached data description")

                # 2. GPT Prompt Engineering (for chat models)
                messages = [
                    {"role": "system", "content": f"""
                        You are a helpful assistant that answers questions about data in an Excel file.
                        Use the provided data description to understand the data and answer the question.
                                  Data Description:
                        {data_description}
                    """},
                    {"role": "user", "content": question}
                ]

                # 3. GPT API Call (using chat/completions)
                try:
                    print("I have reached the OpenAI call")
                    # response = openai.Completion.create(
                    #     model="gpt-3.5-turbo",
                    #     messages=messages,
                    #     max_tokens=200,
                    #     n=1,
                    #     stop=None,
                    #     temperature=0.0,
                    # )
                    chat_completion = client.chat.completions.create(  # Add the.create() call
                        messages=messages,
                        model="gpt-4o",
                    )
                    gpt_answer = chat_completion.choices[0].message.content  # Access the message content
                    st.write(gpt_answer)


                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    except Exception as e:
        st.error(f"Error processing the Excel file: {e}")