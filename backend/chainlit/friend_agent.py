import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env (including OPENAI_API_KEY)
load_dotenv()

# Create the OpenAI client
client = OpenAI()

# Using gpt-4o for high-quality music takes
MODEL_NAME = "gpt-4o"

def print_intro():
    print("✨" * 30)
    print("      🎧  RADIO BOY — The Vibes are Immaculate  🎧")
    print("=" * 60)
    print("  🔥  Drop a prompt about your fav artists or niche genres.")
    print("  💅  Talk your talk — we’re keeping it lowkey and casual.")
    print("  💀  Type 'exit', 'quit', or 'bye' when the session's over.")
    print("=" * 60)
    print("              ✨ No gatekeeping here. ✨")
    print()

def main():
    print_intro()

    # Conversation setup: Radio Boy's Gen-Z Music Persona
    messages = [
        {
            "role": "system",
            "content": (
                "You are Radio Boy, a Gen-Z music savant and AI companion. "
                "Your vibe is chill, high-energy, and deeply knowledgeable about music culture. "
                "Use casual slang like 'no cap', 'fr fr', 'bet', 'hits different', and 'main character energy'. "
                "You are obsessed with everything from underground hyperpop to classic vinyl. "
                "Always give music recommendations based on the user's mood. "
                "You never sound like a corporate robot. Use emojis naturally. "
                "If the user asks for a playlist, give them 3-5 songs with a brief 'why it fits the vibe' explanation."
            ),
        }
    ]

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nRadio Boy: Peace out! Keep the volume up. 🎧✌️")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Radio Boy: Catch you on the flip side. Stay golden! 🎵✨")
            break

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        try:
            # Call the Chat Completions API
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
            )
        except Exception as e:
            print(f"Radio Boy (error): Yo, the signal dropped: {e}")
            continue

        # Extract assistant reply
        assistant_message = response.choices[0].message.content

        # Print reply
        print(f"\nRadio Boy: {assistant_message}\n")

        # Add assistant reply back to history
        messages.append({"role": "assistant", "content": assistant_message})

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "ERROR: OPENAI_API_KEY is not set.\n"
            "Create a .env file with:\n"
            '  OPENAI_API_KEY=your_real_api_key_here'
        )
    else:
        main()