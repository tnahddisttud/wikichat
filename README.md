# 🤖 WikiChat: Your Friendly Information Retrieval Chatbot!

Welcome to WikiChat, your personal gateway to conversing with Wikipedia articles using Natural Language Processing (NLP).

WikiChat is designed with 10 distinct intents, allowing you to engage in meaningful conversations : `greeting`,`goodbye`,`age`,`name`,`help`,`weather`,`joke`,`thanks`, `news`, and `wikipedia`.


![wikichat](https://github.com/tnahddisttud/wikichat/assets/37979764/5fe87dd1-35f9-4831-8952-1dec80b4d520)

---

### Getting Started:

To set up WikiChat locally, follow these simple steps:

#### Requirements:
- Ensure you have Python installed (version >= 3.11)
- Install [Poetry](https://python-poetry.org/docs/) for dependency management

#### Setup Instructions:

1. **Create a Virtual Environment**:
   ```shell
   poetry shell
   ```

2. **Install Dependencies**:
   ```shell
   poetry install
   ```
   Additionally, you may also need to run: `python -m spacy download en_core_web_sm`.


3. **Start the Backend Server**:
   ```shell
   uvicorn main:app --reload
   ```

4. **Launch the Frontend UI**:
   - Navigate to the frontend directory in a new terminal session.
   - Start the Streamlit application:
   ```shell
   streamlit run chat_ui.py
   ```

5. **Access WikiChat**:
   - Open your preferred web browser.
   - Enter `http://localhost:8501` in the address bar.
   - Click on the "Create" button to create the database.
   
![wikichat_create_db](https://github.com/tnahddisttud/wikichat/assets/37979764/ac99ed63-0211-41b2-b1ba-b6c55c17b82b)


Now you're all set to chat with WikiChat!

---

### Troubleshooting:

You may encounter some issues during index creation with chromadb due to Sqlite3. [Chroma requires SQLite > 3.35](https://docs.trychroma.com/troubleshooting#sqlite), if you encounter issues with having too low of a SQLite version please try the following:

- Install pysqlite3-binary, `pip install pysqlite3-binary` and then override the default sqlite3 library before running Chroma by following the steps mentioned [here](https://gist.github.com/defulmere/8b9695e415a44271061cc8e272f3c300?permalink_comment_id=4650539#gistcomment-4650539).


### References:

- [Using spaCy in Your Chatbot for Natural Language Processing](https://cobusgreyling.medium.com/using-spacy-in-your-chatbot-for-natural-language-processing-8fa14c26bb51)
- [How To Create an Intelligent Chatbot in Python Using the spaCy NLP Library](https://www.digitalocean.com/community/tutorials/how-to-create-an-intelligent-chatbot-in-python-using-the-spacy-nlp-library)
- [Step-by-Step Guide to Create a Customized Chatbot Using spaCy Python NLP Library](https://community.intersystems.com/post/step-step-guide-create-customized-chatbot-using-spacy-python-nlp-library)
- [Chroma Documentation: Getting Started](https://docs.trychroma.com/getting-started)
- [Streamlit Tutorials: Building Conversational Apps](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
