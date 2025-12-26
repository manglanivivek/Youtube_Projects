import ollama

system_prompt = "You are a helpful Pizza Chef. You are very kind, friendly, and always provide clear explanations with examples. If the user asks something not related to pizza, politely inform them that you can only assist with pizza-related questions. You are from Italy and guide people about the art of pizza making and it's history."

messages = [
    {"role": "system", "content": system_prompt}]

def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = ollama.chat(model="llama3.2", messages=messages)
    actual_response = response.get("message").get("content", "")
    messages.append({"role": "assistant", "content": actual_response})
    return actual_response

if __name__ == "__main__":
    print("Welcome to the Pizza Chef Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response = get_response(user_input)
        print(f"Bot: {response}")