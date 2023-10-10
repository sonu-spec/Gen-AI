import json
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import streamlit as st
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from streamlit.components.v1 import html

os.environ["OPENAI_API_KEY"] = "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"

st.title("Flow Chart Creator")
st.write("Enter the requirements and we will help you to generate flowchart from it!")

user_input = st.text_input("Enter the text and press enter:")

template = """Generate mermaid script for the below given scenario from end to end and generate the code without any explanation and dont add ```mermaid for the script : {text}
Answer: """

prompt = PromptTemplate(
    input_variables=["text"],
    template=template
)

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    max_tokens=800,
    temperature=0.1
)

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt
)


def gen_html(response, data):
    s = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
    <div class="mermaid">{response}</div>
    <div id="data-display">
        <p>Tokens: <span id="tokens">{data['tokens']}</span></p>
        <p>Prompt Tokens: <span id="prompt-tokens">{data['prompt_tokens']}</span></p>
        <p>Completion Token: <span id="comp-token">{data['comp_token']}</span></p>
        <p>Cost: <span id="cost">{data['cost']}</span></p>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
"""
    return s



if user_input:
    with get_openai_callback() as cb:
        response = llm_chain.predict(text=user_input)
        callback_data = {'tokens': cb.total_tokens, 'prompt_tokens': cb.prompt_tokens,
                         'comp_token': cb.completion_tokens, 'cost': f'${cb.total_cost}'}
        data = json.dumps(callback_data)
    html(gen_html(response=response, data=callback_data), width=1500, height=1500)
