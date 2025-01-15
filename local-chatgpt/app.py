# Import necessary libraries.
# Chainlit helps us build the chat interface.
import chainlit as cl  
# Ollama lets us talk to the language model.
import ollama  

# This function runs when a new chat starts.
@cl.on_chat_start
async def start_chat():
    # Store the chat history in the user's session.
    # We start with a system message to guide the AI's behavior.
    cl.user_session.set(
        "interaction",
        [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ],
    )

    # Create an empty message to hold our greeting.
    msg = cl.Message(content="")

    # Define the greeting message.
    start_message = "Hello, I'm your 100% local alternative to ChatGPT running on Llama3.2-Vision. How can I help you today?"

    # Stream the greeting to the user, character by character.
    for token in start_message:
        await msg.stream_token(token)

    # Send the complete greeting message.
    await msg.send()

# This function defines a 'tool' that sends messages to the language model.
@cl.step(type="tool")
async def tool(input_message, image=None):

    # Get the chat history from the user's session.
    interaction = cl.user_session.get("interaction")

    # Add the user's message to the chat history.
    # If there's an image, include that too.
    if image:
        interaction.append({"role": "user",
                            "content": input_message,
                            "images": image})
    else:
        interaction.append({"role": "user",
                            "content": input_message})
    
    # Send the chat history to the language model and get a response.
    response = ollama.chat(model="llama3.2-vision",
                            messages=interaction) 
    
    # Add the model's response to the chat history.
    interaction.append({"role": "assistant",
                        "content": response.message.content})
    
    # Return the model's response.
    return response

# This function runs when the user sends a message.
@cl.on_message 
async def main(message: cl.Message):
    # Check if the message is the /clear command
    if message.content == "/clear":
        await clear_history()  # Call the clear_history function
    # Check if the message is the /show_history command
    elif message.content == "/show_history":
        await show_history()  # Call the show_history function

    else:
        # Check if the message has any images.
        images = [file for file in message.elements if "image" in file.mime]

        # If there are images, send them to the language model along with the message.
        if images:
            tool_res = await tool(message.content, [i.path for i in images])

        # If there are no images, just send the message.
        else:
            tool_res = await tool(message.content)

        # Create an empty message to hold the model's response.
        msg = cl.Message(content="")

        # Stream the model's response to the user, character by character.
        for token in tool_res.message.content:
            await msg.stream_token(token)

        # Send the complete response message.
        await msg.send()

async def clear_history():
    """
    Clear the chat history.
    """
    cl.user_session.set("interaction", [])
    await cl.Message(content="Chat history cleared!").send()

async def show_history():
    """
    Display the current chat history.
    """
    interaction = cl.user_session.get("interaction")
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in interaction])
    await cl.Message(content=f"Here's the chat history:\n{history_text}").send()
