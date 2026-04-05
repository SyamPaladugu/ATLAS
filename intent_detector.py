import re
from typing import Dict, Tuple, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

class IntentDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.intents = [
            'play', 'pause','next', 'previous', 'search', 'help', 'unknown','stop','resume','mute','disarm','arm','lock','unlock','define','open'
            'close'          ]
        self.training_data = [
            ("play my favorite song", "play"),
            ("start playing music", "play"),
            ("begin the track", "play"),
            ("resume playback", "play"),
            ("pause the music", "pause"),
            ("stop playing", "pause"),
            ("skip to next", "next"),
            ("go forward", "next"),
            ("play next track", "next"),
            ("go back", "previous"),
            ("previous song", "previous"),
            ("rewind", "previous"),
            ("ask google ", "search"),
            ("what does this mean", "search"),
            ("what does this word mean", "define"),
            ("whats the meaning of this word", "define "),
            ("help me", "help"),
            ("what can you do", "help"),
            ("what can you help with", "help"),
            ("arm the system", "arm"),
            ("disarm the system", "disarm"),
            ("Close app please", "close"),
            ("Close the application", "close"),
            ("open app", "open"),
            ("open the application", "open"),
        ]
        self.train_model()
    
    def train_model(self):
        """Train ML model on predefined training data."""
        commands, labels = zip(*self.training_data)
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
            ('clf', MultinomialNB())
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
        
        intent = self.model.predict([command_lower])[0]
        confidence_scores = self.model.predict_proba([command_lower])[0]
        confidence = float(max(confidence_scores))
        
        return (intent, confidence)

# Example usage
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
        "Close the application",
        "open the application",
        "what does this word mean",
        "whats the meaning of this word",
        "unknown command"
    ]
    
    for cmd in test_commands:
        intent, confidence = detector.detect_intent(cmd)
        print(f"Command: '{cmd}' -> Intent: {intent} (Confidence: {confidence:.2f})")