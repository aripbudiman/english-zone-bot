import requests

# url = "https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions.json"

# response = requests.get(url)
# data = response.json()

# for question_id, q in data.items():
#     print("ID:", question_id)
#     print("Question:", q["question"])
#     print("Options:", q["options"])
#     print("Correct index:", q["correct"])
#     print("-" * 60)

url = (
    "https://english-zone-2c406-default-rtdb.asia-southeast1.firebasedatabase.app/questions.json"
    "?limitToFirst=2"
)

res = requests.get(url)
print(res.json())
