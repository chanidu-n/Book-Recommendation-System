def chatbot_response(message):
    message = message.lower()

    if "recommend" in message:
        return "Tell me your favorite genre, number of pages, and difficulty."

    elif "fantasy" in message:
        return "Fantasy books are exciting! Harry Potter is a great choice."

    elif "help" in message:
        return "I can recommend books and predict how much you will like them."

    else:
        return "I'm your book assistant. Ask me for recommendations or help."
