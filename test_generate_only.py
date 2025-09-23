from transformers import pipeline, set_seed

# Initialize generator
generator = pipeline("text-generation", model="gpt2")
set_seed(42)

# Get inputs
bpm = input("Enter your BPM (heart rate): ")
weight = input("Enter your weight (kg): ")
age = input("Enter your age (years): ")

# Controlled prompt
prompt = (
    "Here is an example:\n"
    "My bpm is 80, weight is 70, age is 25. Based on that, give me 3 healthy lunch ideas:\n"
    "1. Grilled salmon with brown rice and steamed broccoli\n"
    "2. Turkey and avocado wrap with spinach\n"
    "3. Chickpea salad with olive oil and lemon\n\n"
    f"Now you answer for this one: My bpm is {bpm}, weight is {weight}, age is {age}. Based on that, give me 3 healthy lunch ideas:\n"
)


# Generate response
output = generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)

# Extract just the suggestions
raw_text = output[0]["generated_text"]
suggestions = raw_text.split(":")[-1].strip().split("\n")
meals = [line.strip() for line in suggestions if line.strip().startswith(("1", "2", "3"))]

# Display result
print("\n Assistant Suggestion:")
for meal in meals[:3]:
    print(meal)
