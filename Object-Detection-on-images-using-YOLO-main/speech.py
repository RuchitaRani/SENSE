import speech_recognition as sr
import pyttsx3
import subprocess
import keyboard


def execute_command(command):
    if "navigation" in command:
        subprocess.Popen(['python', 'x-c.py'])
    elif "help" in command:
        subprocess.Popen(['python', 'sos.py'])
    elif "close" in command:
        print("Closing the program...")
        exit()


recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def main():
    print("Press and hold the specified key to activate speech recognition...")
    while True:
        
        keyboard.wait('ctrl')

    
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)

            
            execute_command(text)
            speak("Command executed.")

        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            speak("Sorry, I'm having trouble accessing the speech recognition service.")


if __name__ == "__main__":
    main()
