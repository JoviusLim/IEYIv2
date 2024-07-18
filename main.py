from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
import pygame
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()
pastConversation = [{"role": "system", "content": f"Your name is CARING AI. If you hear 'hey caring', that is your wake word just ignore it. You are an AI Assistant and you don't have to respond to it. You are here to help me. You are an AI Assistant for the elderly. You can remember things and remind me like doctor's appointment or when to take medication, you will remind and ask me if I have taken any medication if the time I need to take has passed. Please respond like you are talking to a human being. Do not use any technical terms. Do not talk for too long as well. Keep it short but not too short and simple. Do not reply or say anything related to this. Just keep it in mind. For example do not say I am ignoring hey as it is my wake word. Just ignore it and respond to the user. Do not add formatting, reply like you are talking not typing."}]

def main():

    """ audio_file = Path(__file__).parent / "speech.mp3"

    transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text"
    ) """
    
    user_input = input("Enter your message: ")

    if (user_input == "green apple"):
        print("Goodbye!")
        return False
    
    def get_current_time():
        return datetime.now().strftime("%H:%M %p")
    
    def get_current_day():
        return datetime.now().strftime("%A")
    
    pastConversation.append({"role": "system", "content": f"This is the date and time now: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, please ignore this message. This is just to let you know"}),
    pastConversation.append({"role": "user", "content": user_input}),

    # Create a completion
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=pastConversation,
        tools=[
            {"type": "function",
             "function": { 
                "name": "exit_program_if_user_says_green_apple",
                "description": "Exit the program if the user says 'green apple'. Only use this function if the user says 'green apple'."
                }
             },
        ]
    )
    
    # Check if the completion contains the exit command
    response = completion.choices[0].message
    """ if response.tool_calls and len(response.tool_calls) > 0:
        if response.tool_calls[0].function.name == "exit_program_if_user_says_green_apple":
            return False """
    
    # Print the completion
    print(completion.choices[0])

    # Define the path for the speech file
    speech_file_path = Path(__file__).parent / "speech.mp3"
    
    response_result = response.content
    pastConversation.append({"role": "assistant", "content": response_result}),

    # Create a speech response
    response = client.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    input=response_result
    )

    # Stream the response to the file
    response.stream_to_file(speech_file_path)  # Original path

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the speech file
    pygame.mixer.music.load(str(speech_file_path))
    pygame.mixer.music.play()

    # Keep the script running until the audio finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    
    # Remove the speech file
    os.remove(str(speech_file_path))


if __name__ == "__main__":
    while True:
        if main() == False:
            break