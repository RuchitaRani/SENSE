import speech_recognition as sr
import subprocess

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def execute_object_recognition():
    """Function to execute object recognition script"""
    # Replace 'your_object_recognition_script.py' with the actual script name
    subprocess.call(["python", "your_object_recognition_script.py"])

def listen_and_process():
    """Function to listen to the speech input and process it"""
    with sr.Microphone() as source:
        print("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)

        # Perform actions based on recognized speech
        if "hello" in text:
            speak("Hello! How can I assist you today?")
        elif "how are you" in text:
            speak("I'm fine, thank you!")
        elif "goodbye" in text:
            speak("Goodbye! Have a great day!")
        elif "exploration" in text:
            speak("Initiating object recognition...")
            execute_object_recognition()
        else:
            speak("I'm sorry, I didn't understand that.")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    while True:
        listen_and_process()
