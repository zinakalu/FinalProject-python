import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key= os.getenv("ECONOMICAPI")

url = "https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={api_key}&file_type=json"

response = requests.get(url)
data = json.loads(response.text)

# Now data is a Python dictionary you can work with. For example:
# for observation in data['observations']:
#     print(observation['date'], observation['value'])


print(json.dumps(data, indent=4))

