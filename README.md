# Setup Guide for Jovius (in case he forgets)

To setup:
python -m venv openai-env
source openai-env/bin/activate
pip install openai python-dotenv pygame SpeechRecognition pyaudio
sudo apt-get install python3-distutils

Create .env file and inside put:
OPENAI_API_KEY=your_openai_api_key

Currently there is not DB. But DB can be added once feature is tested on Rasberry Pi 5 and is working fast.
May need to adjust some things so that it can run on linux right now it is working perfectly on windows.

This is why I need a Macbook...