import requests

url = "http://13.60.195.147:8000/ru/Review/"

# Вариант 1: Basic Auth (логин/пароль)
response = requests.get(url, auth=("user", "pass"))
print("Status:", response.status_code)
print("Response:", response.text)

# Вариант 2: Bearer Token (если нужен токен)
# response = requests.get(url, headers={"Authorization": "Bearer YOUR_TOKEN"})
# print("Status:", response.status_code)
# print("Response:", response.text)