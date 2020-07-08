import tkinter as tk
from tkinter import *
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import tkinter.font as font
import smtplib
import request
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishme():
	hour=int(datetime.datetime.now().hour)
	if hour>=6 and hour<12:
		speak("GOOD MORNING")
	elif hour>=12 and hour<20:
		speak("GOOD EVENING")
	elif hour>=20 and hour<=24:
		speak("GOOD NIGHT")

	speak("hello how may i help you")

def takeinputcommand():
	r=sr.Recognizer();
	with sr.Microphone() as source:
		r.pause_threshold=1
		r.energy_threshold=10000
		audio=r.listen(source)
	try:
		query1=r.recognize_google(audio,language='en-in')

	except Exception as e:
		return "None"
	return query1

def simple_get(url):
    try:
        with closing(get(url,stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        speak("sorry for inconvienience please try again later")
        return None



def is_good_response(resp):
    content_type=resp.headers['Content-Type'].lower()
    return (resp.status_code==200 and content_type is not None and content_type.find('html')>-1)

def assistant_call():
	while True:
		query=takeinputcommand().lower()
		if "alexa" in query:
			wishme()
			query1=takeinputcommand().lower();
			if 'tell' in query1 and 'me' in query1 and 'about' in query1:
				speak("searching wikipedia....")
				query1=query1.replace("tell me about","")
				results=wikipedia.summary(query1,sentences=2)
				speak('According to wikipedia')
				speak(results)
				print("vikhyat")
				break
			elif 'open youtube' in query1:
				webbrowser.open_new('youtube.com')
				break
			elif 'open google' in query1:
				webbrowser.open('www.google.com')
				break
			elif 'news' in query1:
				res=simple_get('https://timesofindia.indiatimes.com/home/headlines')
				speak('Recent news')
				html=BeautifulSoup(res,'html.parser')
				content=html.find_all("span",{"class":"w_tle"})
				for a in content:
					speak(a.text)

				break;
			elif 'exit' in query1:
				speak("thank you")
				break
		elif 'exit' in query:
			break
		else:
			continue

def helpbox():
	m=tk.Tk(className='help')
	m.geometry("650x100")
	T = Text(m, height=6, width=150) 
	T.pack()
	T.insert(INSERT,'to activate it say jarvis')
	T.insert(INSERT, 'Task\t\t\t\t\t\t\tCommand\n')
	T.insert(INSERT,'To open youtube\t\t\t\t\t\t\tOpen Youtube\n') 
	T.insert(INSERT,'To open google\t\t\t\t\t\t\tOpen google\n') 
	T.insert(INSERT,'want to know about something\t\t\t\t\t\t\ttell me about ...\n') 
	T.insert(INSERT,'to listen news\t\t\t\t\t\t\ttodays news \n') 
	T.insert(INSERT,'To exit\t\t\t\t\t\t\texit\n') 
	# S = tk.Scrollbar(root)



m=tk.Tk(className="Assistant")
m.configure(background='black')
myFont = font.Font(family='Helvetica', size=15, weight='bold')

button=tk.Button(m,text='listen',width=12,height=2,bg='white',command=assistant_call,font=myFont)
button.place(anchor="center")
button.pack(pady=(150,10))
# background_image=tk.PhotoImage(file="C:\\Users\\Vikhyat\\Desktop\\python\\nlp\\bk.gif")
# background_label = tk.Label(m, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
m.geometry("600x400")

button1=tk.Button(m,text='help',width=12,height=2,bg='white',command=helpbox,font=myFont)
button1.place(anchor="center")
button1.pack()



m.mainloop()
