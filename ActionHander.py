import os
import sys
import webbrowser
import subprocess
import threading
import datetime
from typing import Any
import pyttsx3
import requests
from intent_detector import IntentDetector

# ── Config ────────────────────────────────────────────────────────────────────
WEATHER_API_KEY = "92e22d0140e1b5b1d05e0b20f8abb6a8"   # get a free key at openweathermap.org
WEATHER_CITY    = "New York"        # change to your city
HUGGINGFACE_API_KEY = "YOUR_HF_API_KEY_HERE"  # Get free key at huggingface.co
# ─────────────────────────────────────────────────────────────────────────────

# Voice engine (ATLAS speaks back)
engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

# Optional: Set voice (macOS/Linux specific)
try:
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
except:
    pass

def speak(text: str, text_only: bool = False):
    """Make ATLAS speak a response."""
    print(f"ATLAS: {text}")
    if not text_only:
        try:
            # On macOS, use system 'say' command for more reliable audio
            if sys.platform == "darwin":
                subprocess.run(["say", text], check=False, timeout=30)
            else:
                # Otherwise use pyttsx3
                engine.say(text)
                engine.runAndWait()
        except Exception as e:
            print(f"[Audio note: {e}]")
            # Continue without audio - text is still printed


# ── Music controls ────────────────────────────────────────────────────────────
# These use keyboard shortcuts — works with Spotify, YouTube, VLC etc.
# On Windows uses pyautogui; swap for applescript on Mac if needed.

def _press_media_key(key: str):
    try:
        import pyautogui
        pyautogui.press(key)
    except ImportError:
        speak("Install pyautogui to control media. Run: pip install pyautogui")

def handle_play(command: str):
    _press_media_key("playpause")
    speak("Playing music, sir.")

def handle_pause(command: str):
    _press_media_key("playpause")
    speak("Music paused.")

def handle_resume(command: str):
    _press_media_key("playpause")
    speak("Resuming playback.")

def handle_stop(command: str):
    _press_media_key("stop")
    speak("Stopping playback.")

def handle_next(command: str):
    _press_media_key("nexttrack")
    speak("Skipping to next track.")

def handle_previous(command: str):
    _press_media_key("prevtrack")
    speak("Going back to previous track.")

def handle_volume_up(command: str):
    _press_media_key("volumeup")
    speak("Volume up.")

def handle_volume_down(command: str):
    _press_media_key("volumedown")
    speak("Volume down.")

def handle_mute(command: str):
    _press_media_key("volumemute")
    speak("Muted.")

def handle_unmute(command: str):
    _press_media_key("volumemute")
    speak("Unmuted.")


# ── Search & knowledge ────────────────────────────────────────────────────────

def handle_search(command: str):
    # Strip common filler phrases to get the actual query
    query = command.lower()
    for phrase in ["search for", "look up", "google", "find me", "search", "look"]:
        query = query.replace(phrase, "").strip()
    
    if not query:
        speak("What would you like me to search for?")
        return

    try:
        # Use Wikipedia API for search
        headers = {'User-Agent': 'ATLAS-Agent/1.0'}
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={query}"
        response = requests.get(url, timeout=5, headers=headers).json()
        results = response.get("query", {}).get("search", [])
        
        if results:
            # Get the first result
            title = results[0]["title"]
            snippet = results[0]["snippet"].replace("<span class='searchmatch'>", "").replace("</span>", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
            response_text = f"Found {title}. {snippet}"
            speak(response_text)
        else:
            speak(f"I didn't find any results for {query}.")
    except Exception as e:
        speak(f"I couldn't search for that. Please check your connection.")

def handle_define(command: str):
    # Extract the word being defined
    query = command.lower()
    for phrase in ["what does", "mean", "define", "definition of", "meaning of", "what is the meaning of", "explain what"]:
        query = query.replace(phrase, "").strip()

    word = query.strip()
    if not word:
        speak("Which word would you like me to define?")
        return

    try:
        # Use Wikipedia API for definitions
        headers = {'User-Agent': 'ATLAS-Agent/1.0'}
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={word}&prop=extracts&exintro=true&explaintext=true"
        response = requests.get(url, timeout=5, headers=headers).json()
        pages = response.get("query", {}).get("pages", {})
        
        if pages:
            page_id = list(pages.keys())[0]
            page = pages[page_id]
            if "extract" in page:
                extract = page["extract"][:300]  # First 300 characters
                speak(f"Definition of {word}: {extract}")
            else:
                speak(f"I couldn't find a definition for {word}.")
        else:
            speak(f"I couldn't find a definition for {word}.")
    except Exception as e:
        speak(f"I couldn't look up the definition. Please check your connection.")


# ── Weather ───────────────────────────────────────────────────────────────────

def handle_weather(command: str):
    if WEATHER_API_KEY == "92e22d0140e1b5b1d05e0b20f8abb6a8":
        speak("Weather API key not set. Get a free key at openweathermap.org and add it to the config.")
        return

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric"
        )
        data = requests.get(url, timeout=5).json()
        desc  = data["weather"][0]["description"]
        temp  = round(data["main"]["temp"])
        feels = round(data["main"]["feels_like"])
        speak(
            f"Currently {desc} in {WEATHER_CITY}. "
            f"Temperature is {temp} degrees, feels like {feels}."
        )
    except Exception:
        speak("I couldn't reach the weather service. Check your connection or API key.")


# ── Time & date ───────────────────────────────────────────────────────────────

def handle_time(command: str):
    now  = datetime.datetime.now()
    time = now.strftime("%I:%M %p")
    date = now.strftime("%A, %B %d %Y")
    if "date" in command or "day" in command:
        speak(f"Today is {date}. sir")
    else:
        speak(f"The time is {time}.")


# ── Timers ────────────────────────────────────────────────────────────────────

def handle_timer(command: str):
    import re
    numbers = re.findall(r"\d+", command)

    if not numbers:
        speak("How long should I set the timer for?")
        return

    seconds = int(numbers[0])
    unit    = "second"

    if "minute" in command:
        seconds *= 60
        unit = "minute"
    elif "hour" in command:
        seconds *= 3600
        unit = "hour"

    amount = int(numbers[0])
    speak(f"Timer set for {amount} {unit}{'s' if amount != 1 else ''}. Go.")

    def _ring():
        import time
        time.sleep(seconds)
        speak(f"Time's up! Your {amount} {unit} timer is done.")

    threading.Thread(target=_ring, daemon=True).start()


# ── Reminders ─────────────────────────────────────────────────────────────────

# Simple in-memory reminders list (swap for a JSON file to persist)
reminders: list[str] = []

def handle_reminder(command: str):
    task = command.lower()
    for phrase in ["remind me to", "remind me", "don't let me forget", "set a reminder for", "add a reminder", "schedule a reminder"]:
        task = task.replace(phrase, "").strip()

    if not task:
        speak("What would you like me to remind you about?")
        return

    reminders.append(task)
    speak(f"Got it. I'll remind you to {task}.")
    print(f"[Reminders] {reminders}")


# ── Security ──────────────────────────────────────────────────────────────────
# Placeholders — wire these up to your smart home API (e.g. Home Assistant)

def handle_arm(command: str):
    speak("Security system armed. Stay safe, sir.")
    # TODO: call your smart home API here

def handle_disarm(command: str):
    speak("Security system disarmed. Welcome home.")
    # TODO: call your smart home API here

def handle_lock(command: str):
    speak("Doors locked.")
    # TODO: call your smart home API here

def handle_unlock(command: str):
    speak("Doors unlocked.")
    # TODO: call your smart home API here


# ── App control ───────────────────────────────────────────────────────────────

# Map spoken app names to actual executables / URLs
APP_MAP = {
    "chrome":    "chrome",
    "browser":   "chrome",
    "spotify":   "spotify",
    "settings":  "ms-settings:",         # Windows settings
    "notepad":   "notepad",
    "calculator":"calc",
    "files":     "explorer",
    "terminal":  "cmd",
}

def _extract_app(command: str) -> str:
    command = command.lower()
    for name in APP_MAP:
        if name in command:
            return name
    return ""

def handle_open(command: str):
    app_name = _extract_app(command)
    if not app_name:
        speak("Which application should I open?")
        return
    target = APP_MAP[app_name]
    try:
        # macOS compatible version
        if sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", target])
        elif sys.platform == "win32":  # Windows
            os.startfile(target)
        else:  # Linux
            subprocess.Popen([target])
        speak(f"Opening {app_name}.")
    except Exception:
        speak(f"I couldn't open {app_name}. Make sure it's installed.")

def handle_close(command: str):
    app_name = _extract_app(command)
    if not app_name:
        speak("Which application should I close?")
        return
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.call(["pkill", "-f", app_name])
        else:  # Windows
            subprocess.call(["taskkill", "/f", "/im", f"{APP_MAP[app_name]}.exe"])
        speak(f"Closing {app_name}.")
    except Exception:
        speak(f"I couldn't close {app_name}.")


# ── Personality ───────────────────────────────────────────────────────────────

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my AI to stop acting like a flamingo. It had to put its foot down.",
    "Why did the neural network break up with the dataset? Too many issues with its training.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "Why do Java developers wear glasses? Because they don't C sharp.",
]

import random

def handle_greet(command: str):
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning. All systems online. What can I do for you?")
    elif hour < 18:
        speak("Good afternoon. ATLAS is ready. What do you need?")
    else:
        speak("Good evening. Ready when you are, sir.")

def handle_goodbye(command: str):
    speak("Goodbye. ATLAS going offline. Stay sharp.")
    sys.exit(0)

def handle_joke(command: str):
    speak(random.choice(JOKES))

def handle_news(command: str):
    webbrowser.open("https://news.google.com")
    speak("Opening Google News for you.")

def handle_help(command: str):
    speak(
        "I can help with music, volume, weather, time, timers, reminders, "
        "web search, definitions, security, opening and closing apps, "
        "and general conversation. Just say the word."
    )


# ── AI Chatbot ────────────────────────────────────────────────────────────────

def _get_chatbot_response(command: str) -> str:
    """Generate a response using Hugging Face AI API."""
    if HUGGINGFACE_API_KEY == "YOUR_HF_API_KEY_HERE":
        return None  # API key not set
    
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {
            "inputs": {
                "text": command,
                "past_user_inputs": [],
                "generated_responses": []
            }
        }
        
        url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # Extract the generated text from the response
            if "generated_text" in result:
                return result["generated_text"]
        return None
    except Exception as e:
        print(f"Chatbot error: {e}")
        return None


def handle_unknown(command: str):
    """Handle unknown intents by using AI chatbot."""
    # Try to get AI response
    ai_response = _get_chatbot_response(command)
    
    if ai_response:
        # Limit response length to avoid overly long speeches (max 200 chars)
        response_text = ai_response[:200]
        speak(response_text)
    else:
        # Fallback if API is not configured or fails
        speak("I didn't catch that. Could you rephrase it?")


# ── Intent → handler map ──────────────────────────────────────────────────────

INTENT_MAP: dict[str, Any] = {
    "play":         handle_play,
    "pause":        handle_pause,
    "resume":       handle_resume,
    "stop":         handle_stop,
    "next":         handle_next,
    "previous":     handle_previous,
    "volume_up":    handle_volume_up,
    "volume_down":  handle_volume_down,
    "mute":         handle_mute,
    "unmute":       handle_unmute,
    "search":       handle_search,
    "define":       handle_define,
    "weather":      handle_weather,
    "time":         handle_time,
    "timer":        handle_timer,
    "reminder":     handle_reminder,
    "arm":          handle_arm,
    "disarm":       handle_disarm,
    "lock":         handle_lock,
    "unlock":       handle_unlock,
    "open":         handle_open,
    "close":        handle_close,
    "greet":        handle_greet,
    "goodbye":      handle_goodbye,
    "joke":         handle_joke,
    "news":         handle_news,
    "help":         handle_help,
    "unknown":      handle_unknown,
}

def handle(intent: str, command: str):
    """Route an intent to the correct handler function."""
    handler = INTENT_MAP.get(intent, handle_unknown)
    handler(command)


# ── Main loop ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    detector = IntentDetector()
    speak("ATLAS online. How can I help you?")

    while True:
        try:
            command = input("You: ").strip()
            if not command:
                continue

            intent, confidence = detector.detect_intent(command)
            print(f"[Intent: {intent} | Confidence: {confidence:.2f}]")
            handle(intent, command)

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye.")
            break
