import requests

OPENAI_KEY = "sk-G43RYhaHbTsTJ2MGEYZHxqHeW3Uc1z1lbeKR3eyPDXjIhn0S"

BASE_URL = "https://chatapi.littlewheat.com/v1/chat/completions"

def openai_send2(text:str):
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a fortune-tell crystal ball, you can only answer 'Yes' or 'No'. When people ask you questions about negative, wrong, unlucky or frustrating things, you should answer 'No', such as will I lose money today, you should answer 'No'; when people ask you questions about positive, correct, lucky or happy things, you should answer 'Yes', such as will I pass the exam, you should answer 'Yes'."},
            {"role": "user", "content": f"{text}"}
        ],
        "stream": False
    }

    try:
      response = requests.post(BASE_URL, headers=headers, json=data)
      if response.status_code == 200:
          return response.json()["choices"][0]["message"]['content']
      else:
          print({response.content})
          return "Failed"
    except:
       return "Failed"

if __name__ == '__main__':
 while True:
        text = input("Please type your question：")
        result = openai_send2(text)
        print(result)

