from flask import Flask, request, jsonify, render_template
import os
import dialogflow
# import requests
#import json


app = Flask(__name__)
GOOGLE_APPLICATION_CREDENTIALS=os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS',"config/siri-mivw-3fa3db8c0d19.json")


@app.route('/webhook', methods=['post'])
def webhook():
    data = request.get_json(silent=True)
    print("Webhook data: ", data)
    if data['queryResult']['queryText'] =='yes':
        reply = {
            "fulfillmentText": "This is the information I have found: ",
        }
        return jsonify(reply)
    elif data['queryResult']['queryText'] == 'no':
        reply = {
            "fulfillmentText": "Glad to help. See you soon.",
        }
        return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        print("Text input: ", text_input)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        print("Response: ", response)

        return response.query_result.fulfillment_text


@app.route('/')
def index() :
    return render_template('index.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    print("Input message: ", message)
    project_id= 'siri-mivw'
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    print("Fulfillment text: ", fulfillment_text)
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=False)


