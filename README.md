# 🧠 Heart2Heart — Emotion-Aware Journaling with NLP

Heart2Heart is a web-based journaling prototype that uses **Natural Language Processing (NLP)** to analyze emotions in journal entries. The system highlights emotional words in the user's writing and provides **reflective questions** based on the detected sentiment to encourage self-reflection and emotional awareness.

> **Note:** Heart2Heart is designed as a self-reflection tool and is **not intended for mental health diagnosis or self-diagnosis**.

---

## 🔧 Features

* **Emotion and sentiment analysis** using BERT.
* **Text highlighting** to identify positive and negative emotional words.
* **Reflective questions** generated based on the overall sentiment of a journal entry.
* **Journal history** to review previous entries and their analysis.
* **Mood Calendar** to track emotional patterns over time.
* Web-based prototype developed using **Streamlit**.

---

## 🧠 Methodology

* **Dataset:** 20,000 emotion-related text samples from Kaggle.
* **Preprocessing** of text data before model training.
* **BERT-based NLP model** for emotion/sentiment classification.
* **Training:** 3 epochs with a batch size of 16.
* **Evaluation:** Accuracy, Precision, Recall, and F1-score.
* **Deployment:** Integrated into a Streamlit web prototype.

The model uses emotion categories such as **sadness, fear, and happiness** to analyze the emotional content of journal entries.

---

## 💡 Project Goal

The project aims to make journaling more interactive by helping users recognize emotional patterns in their writing and reflect on their feelings through guided questions. The current prototype supports **English-language input** due to the dataset and model used.

---

## 🛠️ Technologies

* Python
* Natural Language Processing (NLP)
* BERT
* Streamlit
* Pandas
* NumPy
* Machine Learning / Deep Learning
