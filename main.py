import json
import logging
import requests
from twilio.twiml.messaging_response import MessagingResponse

class Request:
    def __init__(self, prompt, model="text-davinci-003", max_tokens=500):
    # , temperature=0, top_p=1, n=1, stream=False, logprobs=None, stop="\n"
    
        self.model = model
        self.prompt = prompt
        self.max_tokens = max_tokens
        # self.temperature = temperature
        # self.top_p = top_p
        # self.n = n
        # self.stream = stream
        # self.logprobs = logprobs
        # self.stop = stop

class Choice:
    def __init__(self, index, text, logprobs, finish_reason):
        self.index = index
        self.text = text
        self.logprobs = logprobs
        self.finish_reason = finish_reason

def whatsapp_webhook(request):

    twilio_response = MessagingResponse()
    msg = twilio_response.message()

    logging.info(f"Received request before get_json: {request}")
    request_data = request.values.get('Body', "")
    
    logging.info(f"Received request after get_json: {request_data}")
    req = Request(prompt=request_data)
    logging.info(f"Text request: {req}")

    var_dict = req.__dict__
    logging.info(f"__dict__ request: {var_dict}")
    data = json.dumps(var_dict)
    logging.info(f"data request: {data}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }

    resp = requests.post("https://api.openai.com/v1/completions", headers=headers, data=data)
    
    logging.info(f"resp from OpenAI: {resp}")

    logging.info(f"resp.content from OpenAI: {resp.content}")
    if resp.status_code != 200:
        logging.error(f"Failed to retrieve data. Here is a more verbose reason: {resp.reason}")
        msg.body(
            'Sorry we could not process your request. Erro 2xx'
        )

    resp_data = resp.json()
    logging.info(f"resp_data: {resp_data}")
    choices_data = resp_data["choices"]
    logging.info(f"Choices data: {choices_data}")
    if len(choices_data) == 0:
        logging.error("No choices returned by API")
        msg.body(
            'Sorry we could not process your request. choices_data==0'
        )

    text = choices_data[0]["text"]
    logging.info(f"Text: {text}")
    if text is None:
        logging.error("No text returned by API")
        msg.body(
            'Sorry we could not process your request. text is null'
        )

    msg.body(text.strip())
    return str(twilio_response)
