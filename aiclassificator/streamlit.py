import streamlit as st
import openai
import os
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Ensure API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not configured. Use an environment variable 'OPENAI_API_KEY'.")

# Load the trained model
model_dir = os.path.abspath("aiclassificator/trained_unifiedqa_model")
if not os.path.exists(model_dir):
    raise FileNotFoundError(f"The trained model is not found at {model_dir}.")

tokenizer = T5Tokenizer.from_pretrained(model_dir)
model = T5ForConditionalGeneration.from_pretrained(model_dir)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predict(question, context):
    input_text = f"question: {question} context: {context}"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)

    output = model.generate(input_ids)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

def extend_response_with_openai(base_answer):
    try:
        messages = [
            {"role": "system", "content": "You are an IT expert specialized in incident resolution. Respond in a structured format."},
            {"role": "user", "content": (
                f"In no more than 200 characters, for the IT incident '{base_answer}', respond in the following structured format:\n\n"
                "<span>[brief description of the issue]</span>.\n\n"
                "**One common cause is:** <span>[explain a likely root cause]</span>.\n\n"
                "**Incident assigned to:** <span>[assign this incident to a support team]</span>."
            )}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        
        extended_answer = response["choices"][0]["message"]["content"]
        return extended_answer
    
    except openai.error.OpenAIError as e:
        st.error(f"Error using OpenAI GPT: {str(e)}")
        return "Error: Unable to generate extended response."

st.title("AI Incident Classifier")
st.write("This app classifies IT incidents and provides structured recommendations.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = ""  

st.markdown(
    """
    <style>
    .chat-area {
        background-color: #1e1e1e;
        color: white;
        font-family: "Courier New", monospace;
        padding: 10px;
        border-radius: 10px;
        height: 400px;
        overflow-y: auto;
        scroll-behavior: smooth;
    }
    </style>
    <script>
    const chatArea = document.getElementsByClassName('chat-area')[0];
    if (chatArea) {
        chatArea.scrollTop = chatArea.scrollHeight;
    }
    </script>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="chat-area" id="chat-area">
        {st.session_state["chat_history"]}
    </div>
    """,
    unsafe_allow_html=True,
)

user_message = st.text_input("Type your message:", "")
col1, col2 = st.columns([18, 2])

with col2:
    send_button = st.button("Send") 

if send_button:
    if user_message.strip():
        with st.spinner("Generating response..."):
            try:
                base_answer = predict("What is the reported error?", user_message)
                ai_response = extend_response_with_openai(base_answer)

                user_formatted = f"<div style='text-align: right;'><b>You:</b> {user_message}</div>"
                ai_formatted = f"<div style='text-align: left;'><b>AI:<br> {ai_response}</b></div>"

                st.session_state["chat_history"] += f"{user_formatted}<br>{ai_formatted}<br>"

                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            
        #    My computer is overheating and the fan sounds strange
        #    My headset microphone is not capturing my voice