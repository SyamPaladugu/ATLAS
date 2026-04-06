from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class IntentDetector:
    def __init__(self) -> None:
        self.model: Pipeline = Pipeline([])
        self.intents = [
            'play', 'pause', 'next', 'previous', 'search', 'help',
            'unknown', 'stop', 'resume', 'mute', 'unmute', 'disarm',
            'arm', 'lock', 'unlock', 'define', 'open', 'close',
            'volume_up', 'volume_down', 'weather', 'time', 'reminder',
            'joke', 'news', 'greet', 'goodbye', 'timer'
        ]
        self.training_data = [
            # --- play ---
            ("play my favorite song", "play"),
            ("start playing music", "play"),
            ("begin the track", "play"),
            ("play some music", "play"),
            ("put on a song", "play"),
            ("play something", "play"),
            ("play hip hop", "play"),
            ("play jazz music", "play"),
            ("play the next song", "play"),
            ("I want to listen to music", "play"),
            ("start the music", "play"),
            ("play atlas playlist", "play"),

            # --- pause ---
            ("pause the music", "pause"),
            ("pause this", "pause"),
            ("hold on", "pause"),
            ("pause please", "pause"),
            ("can you pause that", "pause"),
            ("wait pause it", "pause"),
            ("pause the song", "pause"),
            ("pause playback", "pause"),
            ("pause it", "pause"),
            ("just pause", "pause"),
            ("pause for a moment", "pause"),
            ("temporarily pause", "pause"),

            # --- resume ---
            ("resume playback", "resume"),
            ("resume the music", "resume"),
            ("continue playing", "resume"),
            ("unpause", "resume"),
            ("keep playing", "resume"),
            ("resume", "resume"),
            ("continue the song", "resume"),
            ("start again", "resume"),
            ("resume please", "resume"),
            ("go back to playing", "resume"),
            ("continue from where we left", "resume"),
            ("play again", "resume"),

            # --- stop ---
            ("stop playing", "stop"),
            ("stop the music", "stop"),
            ("turn off music", "stop"),
            ("stop everything", "stop"),
            ("halt", "stop"),
            ("stop now", "stop"),
            ("cut the music", "stop"),
            ("silence", "stop"),

            # --- next ---
            ("skip to next", "next"),
            ("go forward", "next"),
            ("play next track", "next"),
            ("next song", "next"),
            ("skip this", "next"),
            ("skip song", "next"),
            ("next please", "next"),
            ("I don't like this song", "next"),
            ("skip ahead", "next"),
            ("change the song", "next"),

            # --- previous ---
            ("go back", "previous"),
            ("previous song", "previous"),
            ("rewind", "previous"),
            ("last track", "previous"),
            ("go to previous", "previous"),
            ("play that again", "previous"),
            ("back to the last song", "previous"),
            ("previous track please", "previous"),

            # --- volume up ---
            ("volume up", "volume_up"),
            ("turn it up", "volume_up"),
            ("louder please", "volume_up"),
            ("increase the volume", "volume_up"),
            ("can you make it louder", "volume_up"),
            ("raise the volume", "volume_up"),
            ("make it louder", "volume_up"),
            ("turn up the volume", "volume_up"),
            ("crank it up", "volume_up"),
            ("amp it up", "volume_up"),
            ("increase volume", "volume_up"),
            ("louder", "volume_up"),
            ("make volume louder", "volume_up"),
            ("pump up the volume", "volume_up"),
            ("boost volume", "volume_up"),
            ("up the volume", "volume_up"),

            # --- volume down ---
            ("volume down", "volume_down"),
            ("turn it down", "volume_down"),
            ("quieter please", "volume_down"),
            ("decrease the volume", "volume_down"),
            ("lower the volume", "volume_down"),
            ("make it quieter", "volume_down"),
            ("turn down the volume", "volume_down"),
            ("not so loud", "volume_down"),

            # --- mute ---
            ("mute", "mute"),
            ("mute the sound", "mute"),
            ("go silent", "mute"),
            ("mute please", "mute"),
            ("be quiet", "mute"),
            ("shut up", "mute"),
            ("silence the audio", "mute"),
            ("turn off the sound", "mute"),

            # --- unmute ---
            ("unmute", "unmute"),
            ("unmute please", "unmute"),
            ("turn the sound back on", "unmute"),
            ("I can hear you now", "unmute"),
            ("restore audio", "unmute"),

            # --- search ---
            ("search for pytorch tutorials", "search"),
            ("look up the weather", "search"),
            ("google iron man", "search"),
            ("can you find information about", "search"),
            ("search the web for", "search"),
            ("look it up", "search"),
            ("find me information on", "search"),
            ("search for recipes", "search"),
            ("browse for news", "search"),
            ("ask google", "search"),
            ("search that", "search"),
            ("search online", "search"),
            ("look for", "search"),
            ("find me", "search"),
            ("web search", "search"),
            ("look up information", "search"),

            # --- define ---
            ("what does this word mean", "define"),
            ("whats the meaning of this word", "define"),
            ("define algorithm", "define"),
            ("what is the definition of", "define"),
            ("explain what this means", "define"),
            ("what does ephemeral mean", "define"),
            ("give me the definition of", "define"),
            ("define the term", "define"),
            ("what is the meaning of", "define"),
            ("define that", "define"),
            ("explain this term", "define"),
            ("what is that called", "define"),
            ("definition please", "define"),
            ("explain the meaning", "define"),

            # --- weather ---
            ("what is the weather today", "weather"),
            ("is it going to rain", "weather"),
            ("whats the weather like", "weather"),
            ("tell me the forecast", "weather"),
            ("should I bring an umbrella", "weather"),
            ("how hot is it outside", "weather"),
            ("weather forecast for tomorrow", "weather"),
            ("is it sunny today", "weather"),
            ("what temperature is it", "weather"),
            ("how cold is it", "weather"),
            ("weather please", "weather"),
            ("what's the weather condition", "weather"),
            ("will it rain", "weather"),
            ("check the weather", "weather"),
            ("weather for today", "weather"),

            # --- time ---
            ("what time is it", "time"),
            ("tell me the time", "time"),
            ("what is the date today", "time"),
            ("what day is it", "time"),
            ("current time please", "time"),
            ("whats todays date", "time"),
            ("what year is it", "time"),
            ("current date", "time"),
            ("what's the time now", "time"),
            ("tell me today's date", "time"),
            ("current time", "time"),
            ("time please", "time"),
            ("what time", "time"),

            # --- timer ---
            ("set a timer for 5 minutes", "timer"),
            ("start a 10 minute timer", "timer"),
            ("timer for 30 seconds", "timer"),
            ("remind me in 5 minutes", "timer"),
            ("set a countdown", "timer"),
            ("start the countdown", "timer"),
            ("give me a 2 minute timer", "timer"),
            ("timers", "timer"),
            ("set timer", "timer"),
            ("start timer", "timer"),
            ("timer please", "timer"),
            ("run a timer", "timer"),
            ("count down 1 minute", "timer"),

            # --- reminder ---
            ("remind me to call mum", "reminder"),
            ("set a reminder for tomorrow", "reminder"),
            ("don't let me forget my meeting", "reminder"),
            ("add a reminder", "reminder"),
            ("remind me at 3pm", "reminder"),
            ("schedule a reminder", "reminder"),
            ("remind me to take my medicine", "reminder"),
            ("reminder please", "reminder"),
            ("remember to", "reminder"),
            ("set a reminder", "reminder"),
            ("reminders", "reminder"),
            ("remind me", "reminder"),
            ("don't forget", "reminder"),

            # --- arm ---
            ("arm the system", "arm"),
            ("activate security", "arm"),
            ("enable the alarm", "arm"),
            ("arm the alarm", "arm"),
            ("turn on the security system", "arm"),
            ("set the alarm", "arm"),
            ("secure the house", "arm"),
            ("arm please", "arm"),
            ("activate the alarm", "arm"),
            ("security on", "arm"),
            ("arm security", "arm"),
            ("enable security", "arm"),

            # --- disarm ---
            ("disarm the system", "disarm"),
            ("deactivate security", "disarm"),
            ("disable the alarm", "disarm"),
            ("disarm the alarm", "disarm"),
            ("turn off the security system", "disarm"),
            ("I'm home disarm", "disarm"),
            ("disarm please", "disarm"),
            ("disable security", "disarm"),
            ("security off", "disarm"),
            ("deactivate alarm", "disarm"),
            ("turn off alarm", "disarm"),

            # --- lock ---
            ("lock the door", "lock"),
            ("lock up", "lock"),
            ("secure the door", "lock"),
            ("lock the house", "lock"),
            ("lock everything", "lock"),

            # --- unlock ---
            ("unlock the door", "unlock"),
            ("open the lock", "unlock"),
            ("let me in", "unlock"),
            ("unlock the house", "unlock"),
            ("unlock please", "unlock"),

            # --- open ---
            ("open the app", "open"),
            ("open the application", "open"),
            ("open chrome", "open"),
            ("launch the browser", "open"),
            ("open spotify", "open"),
            ("open settings", "open"),
            ("start the application", "open"),
            ("launch the app", "open"),
            ("open that", "open"),

            # --- close ---
            ("close the app", "close"),
            ("close the application", "close"),
            ("close this window", "close"),
            ("shut down the app", "close"),
            ("close chrome", "close"),
            ("exit the application", "close"),
            ("close that", "close"),
            ("quit the app", "close"),

            # --- greet ---
            ("hello atlas", "greet"),
            ("hey atlas", "greet"),
            ("hi there", "greet"),
            ("good morning atlas", "greet"),
            ("good evening", "greet"),
            ("what's up", "greet"),
            ("yo atlas", "greet"),
            ("howdy", "greet"),
            ("hello", "greet"),
            ("hey", "greet"),
            ("hi", "greet"),
            ("good morning", "greet"),
            ("good afternoon", "greet"),
            ("greetings atlas", "greet"),
            ("good to see you", "greet"),

            # --- goodbye ---
            ("goodbye atlas", "goodbye"),
            ("see you later", "goodbye"),
            ("bye", "goodbye"),
            ("shut down atlas", "goodbye"),
            ("exit", "goodbye"),
            ("goodnight atlas", "goodbye"),
            ("that's all for now", "goodbye"),
            ("I'm done", "goodbye"),
            ("goodbye", "goodbye"),
            ("bye bye", "goodbye"),
            ("farewell", "goodbye"),
            ("catch you later", "goodbye"),
            ("see you soon", "goodbye"),
            ("talk later", "goodbye"),

            # --- joke ---
            ("tell me a joke", "joke"),
            ("say something funny", "joke"),
            ("make me laugh", "joke"),
            ("got any jokes", "joke"),
            ("tell me something funny", "joke"),
            ("make a joke", "joke"),
            ("funny joke please", "joke"),
            ("jokes please", "joke"),
            ("something funny", "joke"),

            # --- news ---
            ("what's in the news", "news"),
            ("give me the latest news", "news"),
            ("any news today", "news"),
            ("what's happening in the world", "news"),
            ("catch me up on the news", "news"),
            ("news headlines", "news"),
            ("news please", "news"),
            ("what's new", "news"),
            ("latest news", "news"),

            # --- help ---
            ("help me", "help"),
            ("what can you do", "help"),
            ("what can you help with", "help"),
            ("show me your commands", "help"),
            ("what are your features", "help"),
            ("how do I use you", "help"),
            ("what do you support", "help"),
            ("give me a list of commands", "help"),
            ("I need help", "help"),
            ("help please", "help"),
            ("what are you capable of", "help"),
            ("how can you help", "help"),
        ]
        self.train_model()
    
    def train_model(self) -> None:
        """Train ML model on predefined training data."""
        commands, labels = zip(*self.training_data)
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                lowercase=True, 
                stop_words='english',
                ngram_range=(1, 2),
                max_features=1000,
                min_df=1,
                max_df=0.9
            )),
            ('clf', MultinomialNB(alpha=0.5))
        ])
        
        self.model.fit(commands, labels)
    
    def detect_intent(self, command: str) -> Tuple[str, float]:
        """
        Detect intent from voice command using ML.
        
        Args:
            command: Voice command string
            
        Returns:
            Tuple of (intent, confidence)
        """
        command_lower = command.lower().strip()
        
        if not command_lower:
            return ('unknown', 0.0)
        
        intent = str(self.model.predict([command_lower])[0])
        confidence_scores = self.model.predict_proba([command_lower])[0]
        confidence = float(max(confidence_scores))

        if confidence < 0.12:
            return ('unknown', confidence)
        
        return (intent, confidence)


if __name__ == "__main__":
    detector = IntentDetector()
    
    test_commands = [
        "play my favorite song",
        "pause the music",
        "volume up please",
        "skip to next track",
        "what can you help with",
        "arm the system",
        "disarm the system",
        "close the application",
        "open the application",
        "what does this word mean",
        "what is the weather today",
        "set a timer for 10 minutes",
        "tell me a joke",
        "what time is it",
        "hello atlas",
        "goodbye atlas",
        "unknown command xyz",
    ]
    
    print(f"{'Command':<40} {'Intent':<15} {'Confidence'}")
    print("-" * 70)
    for cmd in test_commands:
        intent, confidence = detector.detect_intent(cmd)
        print(f"{cmd:<40} {intent:<15} {confidence:.2f}")