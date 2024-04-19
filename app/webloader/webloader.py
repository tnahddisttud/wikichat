import urllib.request
from bs4 import BeautifulSoup
import re
import spacy

nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    text = re.sub(r'(\x1b\[([0-9;]+)m|\[\d+\])', '', text)
    text = re.sub(r'\n', ' ', text)
    return text


def extract_sentences(text: str) -> list[str]:
    doc = nlp(clean_text(text))
    return [sentence.text for sentence in doc.sents]


def get_wikipedia_text(url: str) -> list[str]:
    """
    Scrape the paragraph data from a wikipedia URL
    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser').find_all('p')
    text = ''.join([item.text for item in soup])
    return extract_sentences(text)
