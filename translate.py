from dotenv import load_dotenv
from google.cloud import translate_v2 as gtranslate
import os

load_dotenv()
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
translate_client = gtranslate.Client.from_service_account_json("/Users/zinakalu/Downloads/carbide-legend-394922-212775f295fd.json")



def translate_text(text, target):
    result = translate_client.translate(text, target)
    translated_text = result['translatedText']
    return translated_text


# print(translate_text("hello", "ig"))