import pydantic
import requests

logic = '''
class Response(pydantic.BaseModel):
    reason: str

resp_obj = Response.parse_obj(response.json())

'''

response = requests.post(
    url='https://restful-booker.herokuapp.com/auth'
)

# resp_obj = Response.parse_obj(response.json())
# resp_obj.reason

res = exec(logic)

print(resp_obj.reason)
