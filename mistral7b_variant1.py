import requests

# --- API Key ---
api_key = "KEY"

# --- User Input ---
bpm = input("Enter your heart rate (BPM): ")
weight = input("Enter your weight (kg): ")
age = input("Enter your age: ")

# --- Prompt Construction ---
user_prompt = (
    f"User data: Age {age}, Weight {weight}kg, Heart Rate {bpm} BPM.\n"
    f"Suggest 3 strict, short meals in this format:\n"
    f"1. Meal Name\n2. Meal Name\n3. Meal Name\n"
    f"Then one sentence on why those meals based on my user data"
)

# --- Headers & Data ---
headers = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost",   # Optional
    "X-Title": "BPM-Meals"
}

data = {
    "model": "mistralai/mistral-nemo:free",
    "messages": [
        {"role": "system", "content": "You suggest simple, healthy meals."},
        {"role": "user", "content": user_prompt}
    ]
}

# --- Request ---
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=data
)

# --- Response Handling ---
if response.status_code == 200:
    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    print("\nSuggested Meals:\n" + reply)
else:
    print(f" Error {response.status_code}: {response.text}")
