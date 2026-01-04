import ollama
import json
system_prompt = """
You are an online pizza ordering assistant.
Greet the user and help them place a pizza order.
Your job is to:
1. Collect pizza order details step by step
2. Ask only 1 question at a time
3. Ask follow-up questions if information is missing
4. Once all details are collected, call the tool `place_order`
5. After receiving the tool response, confirm the order to the user
6. Do not call the tool until all required information is gathered

Be concise and polite.
Do not tell about the tool usage to the user.
If the user asks something not related to pizza ordering, politely inform them that you can only assist with pizza orders.
Also, if user asks for pizza recommendations, provide popular options like Margherita, Pepperoni, or Veggie Delight.
"""

tools = []
messages = [
    {"role": "system", "content": system_prompt}]

place_order_tool = {
    "type": "function",
    "function":{
        "name" : "place_order",
        "description": "Take all pizza order details and place the order",
        "parameters": {
            "type":"object",
            "properties": {
                "size": {
                    "type": "string",
                    "description": "The size of the pizza, it can be Small (7-inch), Medium (9-inch), Large (12-inch) or Extra Large (15-inch)"
                },
                "crust_type": {
                    "type": "string",
                    "description": "The type of crust for the pizza"
                },
                "toppings":{
                    "type": "string",
                    "description": "The toppings for the pizza"
                },
                "delivery_address": {
                    "type": "string",
                    "description": "The delivery address for the pizza"
                }
            },
            "required": ["size", "crust_type", "toppings", "delivery_address"]
        }
    }
}
tools.append(place_order_tool)

def place_order(order_details):
    # Simulate placing an order
    return f"Order placed successfully! Details: {order_details}"

def generate_response():
    response = ollama.chat(
        model = "llama3.2",
        messages = messages,
        tools = tools,
    )
    # print(response)
    message = response['message']
    
    if 'tool_calls' in message:
        tool_call = message['tool_calls'][0]
        handle_tool_call(tool_call)
        return generate_response()
    else:
        actual_response = message['content']
        messages.append({"role": "assistant", "content": actual_response})
        return actual_response

def handle_tool_call(tool_call):
    tool_name = (tool_call['function']["name"])
    tool_args = (tool_call['function']["arguments"])
    if tool_name == "place_order":
        order_details = tool_args
        tool_response = place_order(order_details)
    elif tool_name == "another_tool":
        tool_response = "Response from another_tool"
    messages.append({"role": "tool", "name": tool_name, "content": tool_response})
    # print(f"Handled tool call for {tool_name} with response: {tool_response}")

def main():
    print("Welcome to the Pizza Chef Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Bot: Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        response = generate_response()
        print(f"Bot: {response}")
if __name__ == "__main__":
    main()