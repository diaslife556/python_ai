import psycopg2
from transformers import pipeline, set_seed
import datetime

# --- GPT-2 Setup ---
generator = pipeline("text-generation", model="gpt2")
set_seed(42)

# --- PostgreSQL Connection Setup ---
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="3307"
)
cursor = conn.cursor()

# --- User Input ---
name = input("Enter your name: ")
bpm = int(input("Enter your BPM (heart rate): "))
weight = int(input("Enter your weight (kg): "))
age = int(input("Enter your age (years): "))

# --- Insert user ---
cursor.execute("INSERT INTO users (name, age, weight, bpm) VALUES (%s, %s, %s, %s) RETURNING id",
               (name, age, weight, bpm))
user_id = cursor.fetchone()[0]
conn.commit()

# --- GPT Prompt ---
prompt = (
    "Example:\n"
    "My bpm is 80, weight is 70, age is 25.\n"
    "Healthy lunch ideas:\n"
    "1. Grilled salmon with brown rice and steamed broccoli\n"
    "2. Turkey and avocado wrap with spinach\n"
    "3. Chickpea salad with olive oil and lemon\n\n"
    "Now generate new ideas.\n"
    f"My bpm is {bpm}, weight is {weight}, age is {age}.\n"
    "Healthy lunch ideas:\n"
)

# --- Generate GPT-2 Response ---
output = generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.8)[0]["generated_text"]

# --- Parse Only 3 Meals ---
lines = output.split("Healthy lunch ideas:")[-1].strip().split("\n")
meals = [line.strip() for line in lines if line.strip().startswith(("1", "2", "3"))][:3]
response = "\n".join(meals)

# --- Store Prompt & Response ---
cursor.execute("INSERT INTO meal_prompts (user_id, prompt_text, gpt_response) VALUES (%s, %s, %s)",
               (user_id, prompt, response))
conn.commit()

# --- Output to User ---
print("\n Assistant Suggestion:")
for meal in meals:
    print(meal)

# --- Clean up ---
cursor.close()
conn.close()

