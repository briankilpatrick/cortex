# chatbot/core.py

# Import json for structured chat logging
import json

# Import the function to send prompts to Ollama
from chatbot.ollama_client import query_ollama, check_ollama_health

# Import input helper
from chatbot.input_utils import input_with_timeout

# Import logging helpers
from chatbot.logging_utils import get_system_logger
from chatbot.logging_utils import get_chat_logger

# Import session handling
from chatbot.session import start_session, end_session

# Import configuration
from chatbot.config import TIMEOUT_SECONDS


# Main function to run the chatbot
def run_chatbot():
    # Set up logging
    system_logger = get_system_logger()
    chat_logger = get_chat_logger()

    # Fail fast if Ollama is not reachable
    if not check_ollama_health():
        print("Error: Cannot connect to Ollama at http://localhost:11434.")
        print("Make sure Ollama is running ('ollama serve') and try again.")
        system_logger.error("ERR003: Ollama health check failed on startup")
        return

    # Start a new audit session
    session_id, start_time = start_session()

    print("Cortex Chatbot ready! Type 'exit' or 'quit' to stop.")

    conversation_history = []  # stores all messages in this session
    """
    This gives the chatbot memory and user context and is stored only for
    the current session. We should use caution and be aware it will load
    the entire history of previous questions and responses every time we
    interact with the bot. This could grow large and slow down the responses,
    but the responses should be better.
    """

    exit_reason = "normal"

    try:
        # Main loop: keep chatting until user exits or timeout
        while True:
            # Ask the user for input, with a timeout
            # TODO consider implementing a character limit on questions to save memory - future work
            user_input = input_with_timeout("How can I help you: ", TIMEOUT_SECONDS)

            # If no input was received within TIMEOUT seconds, exit
            if user_input is None:
                exit_reason = "timeout"
                print(f"\nNo input detected for {TIMEOUT_SECONDS} seconds. Goodbye!")
                break

            # Make the exit command easier to detect
            cleaned_user_input = user_input.strip().lower()

            # Check if the user wants to quit
            if cleaned_user_input in {"exit", "quit"}:
                # Print exit message with website link
                print("More information can be found online at www.cortex.com \nGoodbye!")
                break

            # Save the user's message in conversation history
            conversation_history.append({"role": "user", "content": user_input})
            chat_logger.info(json.dumps({"session_id": session_id, "role": "user", "content": user_input}))

            # Build the full conversation prompt for the AI
            combined_prompt = ""
            for msg in conversation_history:
                # Capitalize role ("User" or "Bot") and include the message
                combined_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

            # Send the combined prompt to Ollama and get the AI's response
            try:
                bot_response = query_ollama(combined_prompt)
            except Exception:
                exit_reason = "error"
                bot_response = "[Error communicating with AI]"
                system_logger.exception("ERR001: Ollama API request failed")

            # Print the AI's response
            print(f"Cortex: {bot_response}\n")

            # Save the AI's response in conversation history
            conversation_history.append({"role": "bot", "content": bot_response})
            chat_logger.info(json.dumps({"session_id": session_id, "role": "bot", "content": bot_response}))

    except Exception:
        # Log unexpected errors to system log
        exit_reason = "error"
        system_logger.exception("ERR002: Unexpected error in chatbot loop")

    finally:
        # End the audit session whether normal exit, timeout, or error
        end_session(session_id, start_time, reason=exit_reason)
