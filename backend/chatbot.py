from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


questions = [
"recommend a book",
"i like fantasy books",
"suggest self help books",
"help",
"what can you do",
"how does this system work"
]


answers = [
"Tell me your genre, pages, and difficulty to recommend a book.",
"Fantasy books like Harry Potter are popular.",
"Self-help books like Atomic Habits are highly rated.",
"I can recommend books using machine learning.",
"I predict book ratings using ML and help via chatbot.",
"This system uses RandomForest ML and NLP chatbot."
]


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)




def chatbot_response(message):
    message_vec = vectorizer.transform([message])
    similarity = cosine_similarity(message_vec, X)
    idx = similarity.argmax()
    return answers[idx]
