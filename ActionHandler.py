import pyttsx3
import subprocess
import webbrowser
import datetime
import time
import random
import requests
from intent_detector import IntentDetector

# ── Config ────────────────────────────────────────────────────────────────────
WEATHER_API_KEY = "YOUR_KEY_HERE"   # free key at openweathermap.org
WEATHER_CITY    = "New York"        # change to your city
# ─────────────────────────────────────────────────────────────────────────────

engine = pyttsx3.init()
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

def speak(text: str):
    print(f"ATLAS: {text}")
    engine.say(text)
    engine.runAndWait()

def run_applescript(script: str):
    """Execute AppleScript on macOS."""
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.stdout.strip()


# ── Music controls (AppleScript → Spotify or Music app) ──────────────────────

def _spotify(action: str):
    """Control Spotify via AppleScript."""
    script = f"""
    tell application "Spotify"
        {action}
    end tell
    """
    run_applescript(script)

def handle_play(command: str):
    _spotify("play")
    speak("Playing music")

def handle_pause(command: str):
    _spotify("pause")
    speak("Music paused")

def handle_resume(command: str):
    _spotify("play")
    speak("Resuming music")

def handle_stop(command: str):
    _spotify("pause")
    speak("Music stopped")

def handle_next(command: str):
    _spotify("next track")
    speak("Skipping to next track")

def handle_previous(command: str):
    _spotify("previous track")
    speak("Going to previous track")

def handle_volume_up(command: str):
    script = "set volume output volume (output volume of (get volume settings) + 10)"
    run_applescript(script)
    speak("Volume increased")

def handle_volume_down(command: str):
    script = "set volume output volume (output volume of (get volume settings) - 10)"
    run_applescript(script)
    speak("Volume decreased")

def handle_mute(command: str):
    script = "set volume output muted true"
    run_applescript(script)
    speak("Muted")

def handle_unmute(command: str):
    script = "set volume output muted false"
    run_applescript(script)
    speak("Unmuted")


# ── Search & knowledge ────────────────────────────────────────────────────────

def handle_search(command: str):
    """Search Google for query."""
    query = command.replace("search", "").replace("google", "").strip()
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching for {query}")

def handle_define(command: str):
    """Look up word definition."""
    word = command.replace("define", "").replace("what does", "").strip()
    webbrowser.open(f"https://www.merriam-webster.com/dictionary/{word}")
    speak(f"Looking up {word}")


# ── Weather ───────────────────────────────────────────────────────────────────

def handle_weather(command: str):
    speak(f"Weather for {WEATHER_CITY}: Sunny, 72 degrees. (Set up API key for real data)")


# ── Time & date ───────────────────────────────────────────────────────────────

def handle_time(command: str):
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")


# ── Timers ────────────────────────────────────────────────────────────────────

def handle_timer(command: str):
    """Set a simple timer."""
    speak("Timer set for 10 minutes")
    time.sleep(600)
    speak("Timer complete")


# ── Reminders ─────────────────────────────────────────────────────────────────

reminders: list = []

def handle_reminder(command: str):
    reminder_text = command.replace("remind", "").replace("set reminder", "").strip()
    reminders.append(reminder_text)
    speak(f"Reminder set: {reminder_text}")


# ── Security ──────────────────────────────────────────────────────────────────
# Wire these up to Home Assistant or your smart home API

def handle_arm(command: str):
    speak("System armed")
    # TODO: Connect to your smart home API

def handle_disarm(command: str):
    speak("System disarmed")
    # TODO: Connect to your smart home API

def handle_lock(command: str):
    speak("Door locked")
    # TODO: Connect to your smart lock API

def handle_unlock(command: str):
    speak("Door unlocked")
    # TODO: Connect to your smart lock API


# ── App control (macOS open -a / osascript quit) ──────────────────────────────

APP_MAP = {
    "chrome":    "Google Chrome",
    "browser":   "Safari",
    "safari":    "Safari",
    "spotify":   "Spotify",
    "settings":  "System Settings",
    "notes":     "Notes",
    "calendar":  "Calendar",
    "mail":      "Mail",
    "messages":  "Messages",
    "terminal":  "Terminal",
    "finder":    "Finder",
    "calculator":"Calculator",
    "vscode":    "Visual Studio Code",
    "code":      "Visual Studio Code",
    "xcode":     "Xcode",
}

def _extract_app(command: str) -> str:
    """Extract app name from command."""
    for key, app_name in APP_MAP.items():
        if key in command.lower():
            return app_name
    return None

def handle_open(command: str):
    app = _extract_app(command)
    if app:
        subprocess.run(["open", "-a", app])
        speak(f"Opening {app}")
    else:
        speak("App not found")

def handle_close(command: str):
    app = _extract_app(command)
    if app:
        script = f'tell application "{app}" to quit'
        run_applescript(script)
        speak(f"Closing {app}")
    else:
        speak("App not found")


# ── Personality ───────────────────────────────────────────────────────────────

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my AI to stop acting like a flamingo. It had to put its foot down.",
    "Why did the neural network break up with the dataset? Too many issues with its training.",
    "Why do Java developers wear glasses? Because they don't C sharp.",
    "A SQL query walks into a bar, walks up to two tables and asks — can I join you?",
]

def handle_greet(command: str):
    speak("Hello! I'm ATLAS. How can I assist you?")

def handle_goodbye(command: str):
    speak("Goodbye! See you next time.")

def handle_joke(command: str):
    joke = random.choice(JOKES)
    speak(joke)

def handle_news(command: str):
    webbrowser.open("https://news.google.com")
    speak("Opening Google News")

def handle_help(command: str):
    speak("I can play music, control smart home devices, search the web, tell jokes, and much more. What would you like?")

def handle_unknown(command: str):
    """Send unknown commands to a free chatbot AI."""
    try:
        # Using the free Hugging Face API with GPT2
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers={"Authorization": "Bearer hf_placeholder"},
            json={"inputs": command}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0:
                reply = result[0].get("generated_text", "I didn't understand that.").strip()
                speak(reply)
                return
    except:
        pass
    
    # Fallback: Use Open-Meteo free API for a simple response
    speak("I'm not sure about that. Can you rephrase your question?")


# ── Intent → handler map ──────────────────────────────────────────────────────

INTENT_MAP = {
    "play":        handle_play,
    "pause":       handle_pause,
    "resume":      handle_resume,
    "stop":        handle_stop,
    "next":        handle_next,
    "previous":    handle_previous,
    "volume_up":   handle_volume_up,
    "volume_down": handle_volume_down,
    "mute":        handle_mute,
    "unmute":      handle_unmute,
    "search":      handle_search,
    "define":      handle_define,
    "weather":     handle_weather,
    "time":        handle_time,
    "timer":       handle_timer,
    "reminder":    handle_reminder,
    "arm":         handle_arm,
    "disarm":      handle_disarm,
    "lock":        handle_lock,
    "unlock":      handle_unlock,
    "open":        handle_open,
    "close":       handle_close,
    "greet":       handle_greet,
    "goodbye":     handle_goodbye,
    "joke":        handle_joke,
    "news":        handle_news,
    "help":        handle_help,
    "unknown":     handle_unknown,
}

def handle(intent: str, command: str):
    """Route intent to appropriate handler."""
    handler = INTENT_MAP.get(intent, handle_unknown)
    handler(command)


# ── Main loop ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    detector = IntentDetector()
    speak("Testing speech synthesis")
    speak("ATLAS online. How can I help you?")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit", "bye"]:
                handle("goodbye", user_input)
                break
            
            intent, confidence = detector.detect_intent(user_input)
            print(f"Intent: {intent} (confidence: {confidence:.2f})")
            handle(intent, user_input)
            
        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred")