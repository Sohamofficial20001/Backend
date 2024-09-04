# from flask import Flask, request, jsonify
# from flask_cors import CORS
# # from generate import generate_response, get_gemini_response, get_prompts
# import google.generativeai as genai
# import os

# app = Flask(__name__)
# CORS(app)



# def generate_response(question):
#     prompts , greet  = get_prompts()
#     genai.configure(api_key="AIzaSyA4wedlllm0xX9r7ERgbGQjQhM1Q3cIk6Y")
#     if question.lower() in ["hello", "hi", "who are you"]:
#         text = get_gemini_response(greet, question)
#     else:
#         text = get_gemini_response(prompts, question)
#     base_url = "http://slnxsaps4h15.marc.fr.ssg:50000/sap/opu/odata/sap/BILLOFMATERIALV2_SRV"
#     text = text.replace("base_url", base_url)
#     return text

# def get_prompts():

#     with open('prompt_service.txt', 'r') as file:
#         prompts = file.read().strip()
#         print(prompts)
#     with open('prompt_greeting.txt', 'r') as file_greet:
#         greet = file_greet.read().strip()
#         print(greet)
#     return prompts,greet


# def get_gemini_response(question,prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt,question])
#     print(response)
#     return response.text




# @app.route('/api/generate-response', methods=['POST'])
# def api_generate_response():
#     data = request.json
#     question = data.get('question')
#     response_text = generate_response(question)
#     print(response_text)
#     return jsonify({"response": response_text})


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import  get_data_from_query
from api import get_data_from_url

# from generate import generate_response, get_gemini_response, get_prompts
import google.generativeai as genai
app = Flask(__name__)
CORS(app)

prompt_set = False # Status to check if prompt file is selected or not
greeting_set = False # Status to check if greeting is shown or not
def generate_response(question, filename ):
    genai.configure(api_key="AIzaSyA4wedlllm0xX9r7ERgbGQjQhM1Q3cIk6Y")
    greeting_msg = url = base_url = query = ''
    if question.lower() in ["hello", "hi", "who are you"]:
        greeting_msg = get_gemini_response(question ,filename = 'prompt_greeting.txt')
    elif filename == "prompt_bom.txt":
        url = get_gemini_response(question ,filename = filename,)
        base_url = "http://slnxsaps4h15.marc.fr.ssg:50000/sap/opu/odata/sap/BILLOFMATERIALV2_SRV"
        url = url.replace("base_url", base_url)
    elif filename == "prompt_po.txt":
        url = get_gemini_response(question ,filename = filename,)
        base_url = "po_url"
        url = url.replace("base_url", base_url)
    elif filename == "prompt_query.txt":
        query  = get_gemini_response(question ,filename = filename)
    return greeting_msg ,url ,query

def get_prompts(file_name):
    # To set file name of the file  
    with open(file_name , 'r') as file:
        prompts = file.read().strip()
        # print(prompts)
    return prompts


def get_gemini_response(question,filename):
    # To set file name of the file
    prompts = get_prompts(file_name = filename)
    #generate gemini response
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompts,question])
    print(response.text)
    return response.text or ""


@app.route('/api/generate-response', methods=['POST'])
def api_generate_response():
    # columns = data = []
    data = request.json
    # print(data)
    question = data.get('question')
    filename = data.get('filename')
    columns = data = []
    response_greet , response_url ,response_query = generate_response(question, filename)
    if response_greet =="" and response_url != "":
        columns , data = get_data_from_url(response_url)
    elif response_greet =="" and response_query !="":
        columns , data = get_data_from_query(response_query)

    return jsonify({"greet": response_greet , "columns" : columns , "data" : data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)