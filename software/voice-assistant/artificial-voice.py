################ Henri Lahousse ################
# artificial voice
# 05/31/2022

# libraries
import pyttsx3

# enter string of whatever you want it to say
def speak(inp):
    engine = pyttsx3.init()

    """RATE"""
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    engine.setProperty('rate', 160)  # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[1].id)  # index 0 = male, 1 = female

    engine.say(inp)
    engine.runAndWait()
    engine.stop()
