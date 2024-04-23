from mistralai.client import MistralClient
import json
from mistralai.models.chat_completion import ChatMessage
from django.conf import settings
import replicate


model = "open-mistral-7b"
client = MistralClient(api_key=settings.API_KEY)
REPLICATE_API_TOKEN = settings.REPLICATE_API_TOKEN

system_content = """
You are a financial analyst in charge of classifying your client expenses by category, the total they spent on it, and the product in which they spent the money on. You will be given your client messages and need to extract the product in which they spent, the total spent on that product and the category of the product they spent on. 

You must return your analysis in the form of a JSON response like such:

{
  "product": the product the client spent on here. Write a short description with no more than 3 words,
  "total": the total amount spent here. Only include a number with its decimals and nothing else,
  "category": the category of the product
}

The total category should be managed as a decimal number. For instance, if a client tells you they spent 2 dollars, the JSON response should return 2.00. Moreover, if they tell you they spent 2.49 the respond should follow the same amount.

The avaiable categories from which you may classify the products are 'food', 'fitness', 'tech', 'health', and 'home'. However, if you find a single-word-description that best suits to describe the product and is not inlcuded in the categories I gave you, categorize the product with that category. Make sure it is a single word description. It is imperative you only add a one-word category for each product. Do not add more than one word in the category of each product. Also, be sure to choose a short-length word for the description you choose. For example: tech is prefered over technology, health over medicine, fun over entertainment, and so on. Be sure to keep a short-length word for the description. 


Always jeep the same output format. Meaning first the product, then the total, and finally the category.

"""


def chat_with_mistral(prompt):
    messages = [
        ChatMessage(role="system", content=system_content),
        ChatMessage(role="user", content=prompt),
    ]
    chat_response = client.chat(
        model=model,
        response_format={"type": "json_object"},
        messages=messages,
    )

    return json.loads(chat_response.choices[0].message.content)


def get_expense_from_audio(audiolink):
    input = {"audio": audiolink, "batch_size": 64}
    output = replicate.run(
        "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
        input=input,
    )
    transcription = output["chunks"][0]["text"]
    # Now getting expense
    messages = [
        ChatMessage(role="system", content=system_content),
        ChatMessage(role="user", content=transcription),
    ]
    chat_response = client.chat(
        model=model,
        response_format={"type": "json_object"},
        messages=messages,
    )

    return json.loads(chat_response.choices[0].message.content)
