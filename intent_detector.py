
from typing import Dict, Tuple, List
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
            ("play my music", "play"),
            ("start playing", "play"),
            ("play song", "play"),
            ("play the playlist", "play"),
            ("play", "play"),
            ("pause the song", "pause"),
            ("pause it", "pause"),
            ("stop the music", "pause"),
            ("pause", "pause"),
            ("next track", "next"),
            ("skip", "next"),
            ("play next", "next"),
            ("next", "next"),
            ("go back", "previous"),
            ("previous song", "previous"),
            ("last track", "previous"),
            ("previous", "previous"),
            ("search for song", "search"),
            ("google something", "search"),
            ("find information", "search"),
            ("search", "search"),
            ("what can you do", "help"),
            ("help me", "help"),
            ("show commands", "help"),
            ("help", "help"),
            ("stop playing", "stop"),
            ("stop", "stop"),
            ("resume the music", "resume"),
            ("continue playing", "resume"),
            ("resume", "resume"),
            ("mute audio", "mute"),
            ("turn off sound", "mute"),
            ("mute", "mute"),
            ("unmute", "unmute"),
            ("turn on sound", "unmute"),
            ("unmute", "unmute"),
            ("arm security", "arm"),
            ("activate alarm", "arm"),
            ("arm", "arm"),
            ("disarm system", "disarm"),
            ("deactivate alarm", "disarm"),
            ("disarm", "disarm"),
            ("lock the door", "lock"),
            ("secure the door", "lock"),
            ("lock", "lock"),
            ("unlock door", "unlock"),
            ("open the door", "unlock"),
            ("unlock", "unlock"),
            ("define word", "define"),
            ("what does mean", "define"),
            ("explain term", "define"),
            ("define", "define"),
            ("open chrome", "open"),
            ("launch browser", "open"),
            ("open", "open"),
            ("close app", "close"),
            ("quit application", "close"),
            ("close", "close"),
            ("volume up", "volume_up"),
            ("increase volume", "volume_up"),
            ("volume down", "volume_down"),
            ("decrease volume", "volume_down"),
            ("weather today", "weather"),
            ("how's the weather", "weather"),
            ("weather", "weather"),
            ("what time is it", "time"),
            ("current time", "time"),
            ("time", "time"),
            ("set timer", "timer"),
            ("start timer", "timer"),
            ("timer", "timer"),
            ("tell joke", "joke"),
            ("make me laugh", "joke"),
            ("joke", "joke"),
            ("news", "news"),
            ("latest news", "news"),
            ("hello atlas", "greet"),
            ("hi", "greet"),
            ("hello", "greet"),
            ("goodbye", "goodbye"),
            ("bye", "goodbye"),
            ("set reminder", "reminder"),
            ("remind me", "reminder"),
            ("reminder", "reminder"),
        ]
        self.train_model()

    def train_model(self):
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

        if confidence < 0.05:
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