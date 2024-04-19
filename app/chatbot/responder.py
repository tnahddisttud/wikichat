import json
from pathlib import Path
import numpy as np
import os

path = Path(__file__).parent.parent.absolute() / 'resources' / 'intents.json'

with open(os.path.normpath(path), 'r') as file:
    intents = json.load(file)


def get_response(intent):
    """
        Matches intent from tag in intents.json file and chooses a random response.
    """
    for intent_data in intents['intents']:
        if intent_data['tag'] == intent:
            responses = intent_data['responses']
            return np.random.choice(responses)
