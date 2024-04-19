import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk.tokenize import word_tokenize
import nltk
from pathlib import Path

model_path = Path(__file__).parent.parent.absolute() / 'resources' / 'chatbot_model.pth'
intents_path = Path(__file__).parent.parent.absolute() / 'resources' / 'intents.json'


class IntentClassifier:
    """
        IntentClassifier class for training and using a neural network model for intent classification.
    """
    def __init__(self, intents_file_path=intents_path, model_save_path=model_path):
        self.intents_file_path = intents_file_path
        self.model_save_path = model_save_path
        self.intents = None
        self.all_words = None
        self.tags = None
        self.xy = None
        self.X_train = None
        self.y_train = None
        self.input_size = None
        self.output_size = None
        self.model = None
        self.load_intents()
        self.preprocess_data()
        self.create_model()

    def load_intents(self):
        """
            Loads intent data from the JSON file.
        """
        nltk.download('punkt')
        with open(self.intents_file_path, 'r') as file:
            self.intents = json.load(file)

    def preprocess_data(self):
        """
        Preprocesses intent data by tokenizing patterns and creating input-output pairs.
        """
        all_words = []
        tags = []
        xy = []
        for intent in self.intents['intents']:
            tag = intent['tag']
            tags.append(tag)
            for pattern in intent['patterns']:
                words = word_tokenize(pattern.lower())
                all_words.extend(words)
                xy.append((words, tag))

        self.all_words = sorted(set(all_words))
        self.tags = tags
        self.xy = xy

        X_train = []
        y_train = []
        for (pattern_words, tag) in self.xy:
            bag = [1 if word in pattern_words else 0 for word in self.all_words]
            X_train.append(bag)
            y_train.append(tags.index(tag))

        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)
        self.input_size = len(self.all_words)
        self.output_size = len(tags)

    def create_model(self, hidden_size=8):
        self.model = NeuralNet(self.input_size, hidden_size, self.output_size)

    def train(self, learning_rate=0.001, num_epochs=1000, batch_size=8):
        dataset = IntentDataset(self.X_train, self.y_train)
        train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)

        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                outputs = self.model(words)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

        torch.save(self.model.state_dict(), self.model_save_path)

    def predict_intent(self, sentence):
        self.model.load_state_dict(torch.load(self.model_save_path))
        self.model.eval()
        with torch.no_grad():
            sentence_words = word_tokenize(sentence.lower())
            X = [1 if word in sentence_words else 0 for word in self.all_words]
            X = torch.tensor(X, dtype=torch.float32)
            output = self.model(X)
            predicted_tag = self.tags[torch.argmax(output).item()]
            return predicted_tag


class IntentDataset(Dataset):
    """
    Dataset class for intent classification data.
    """
    def __init__(self, X_data, y_data):
        self.n_samples = len(X_data)
        self.X_data = torch.tensor(X_data, dtype=torch.float32)
        self.y_data = torch.tensor(y_data, dtype=torch.long)

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


class NeuralNet(nn.Module):
    """
        Neural network model for intent classification.
        This neural network consists of an input layer, a hidden layer, and an output layer.
        The input layer size is determined by the number of unique words in the input data.
        The hidden layer size is a parameter that can be adjusted during model creation.
        The output layer size is determined by the number of unique intent tags in the data.
    """
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
