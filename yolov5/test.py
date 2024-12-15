import requests

HOST = 'http://127.0.0.1:8000/'
headers = {'Authorization': 'JWT 6f006c05c3862d11b170ed7362d1aa3d4fdbbd47', 'Accept': 'application/json'}
data = {
    'title': "Test Title",
    'text': "Test Text",
    'created_date': "2024-12-15T02:16:15.272207+09:00",
    'author': 1,
    'helmet_status': "all_wearing"
}
file = {'image': open('test.png', 'rb')}

response = requests.post(HOST + '/api_root/Post/', data=data, files=file, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
