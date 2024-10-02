from openai import OpenAI  # Ensure openai==1.2.0 is installed

# Initialize the OpenAI client
client = OpenAI(
    api_key="Your API KEY",  # Use environment variables for API keys in production!
    base_url="https://api.upstage.ai/v1/solar"
)

try:
    # Create a chat completion request with streaming response
    stream = client.chat.completions.create(
        model="solar-pro",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hi, how are you?"
            }
        ],
        stream=True,  # Enable streaming
    )

    # Print the streamed response chunks
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            print(delta, end="")

except Exception as e:
    print(f"An error occurred: {e}")