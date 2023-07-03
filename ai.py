import sys
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import openpyxl
import subprocess
import pywhatkit
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init('sapi5')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello,Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")




class VoiceAssistantWindow(QMainWindow):
    def _init_(self):
        super()._init_()

        # Initialize the speech recognition and text-to-speech engines
        self.speech_recognizer = sr.Recognizer()
        self.speech_engine = pyttsx3.init()

        # Set up the GUI
        self.setWindowTitle('Voice Assistant')
        self.setWindowIcon(PyQt5.QtGui.QIcon(r'C:\Users\Parv Jain\Desktop\wallpaper\mic.png'))
        self.setGeometry(100, 100, 400, 400)

        # Add a button to start the voice recognition
        self.start_button = QPushButton('Start', self)
        self.start_button.setGeometry(10, 10, 50, 30)
        self.start_button.clicked.connect(self.start_voice_recognition)

        # Add a text box to display the recognized speech
        self.speech_textbox = QTextEdit(self)
        self.speech_textbox.setGeometry(10, 50, 380, 340)

        # Add a label to display the status of the voice recognition
        self.status_label = QLabel('Press the button to start voice recognition', self)
        self.status_label.setGeometry(70, 10, 300, 30)
        wishMe()

    def start_voice_recognition(self):
        # Change the status label
        self.status_label.setText('Listening...')

        # Start listening to the microphone
        with sr.Microphone() as source:
            audio = self.speech_recognizer.listen(source)

        # Try to recognize the speech
        try:
            recognized_text = self.speech_recognizer.recognize_google(audio)
            self.speech_textbox.append(recognized_text)
            self.status_label.setText('Recognized speech: ' + recognized_text)
        except sr.UnknownValueError:
            self.status_label.setText('Unable to recognize speech')
        except sr.RequestError as e:
            self.status_label.setText('Error: ' + str(e))
         
        query = recognized_text.lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")


        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'make a note' in query:
            statement = query.replace("make a note", "")
            note(statement)

        elif 'play' in query:
            song = query.replace('play', '')
            speak('playing' + song)
            pywhatkit.playonyt(song)

        elif 'email to shiv' in query:
            try:
                speak("What should I say?")
                content = recognized_text()
                to = "jainprv18@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry I am not able to send this email")

        # Speak the recognized text
        self.speech_engine.say(recognized_text)
        self.speech_engine.runAndWait()

if _name_ == '_main_':

        app = QApplication(sys.argv)
        window = VoiceAssistantWindow()
        window.show()
        sys.exit(app.exec_())