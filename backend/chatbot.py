import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load book data
try:
    df = pd.read_csv("books_regression.csv")
except FileNotFoundError:
    df = None

# Enhanced questions and answers database
questions = [
    # General recommendations
    "recommend a book",
    "suggest a book",
    "what book should i read",
    "give me book recommendations",
    "can you recommend something",
    
    # Genre specific
    "i like fantasy books",
    "recommend fantasy novels",
    "fantasy book suggestions",
    "suggest self help books",
    "self improvement books",
    "i want to read romance",
    "romance book recommendations",
    "mystery thriller books",
    "science fiction recommendations",
    "educational books",
    "business books",
    
    # Book characteristics
    "short books",
    "long books",
    "easy books to read",
    "challenging books",
    "books for beginners",
    "advanced reading material",
    
    # Popular books
    "most popular books",
    "bestselling books",
    "highest rated books",
    "classic books",
    "famous books",
    
    # Authors
    "who is a good author",
    "famous authors",
    "best writers",
    "recommend an author",
    
    # Book series
    "book series recommendations",
    "trilogy suggestions",
    "series to read",
    
    # Reading advice
    "how to choose a book",
    "what makes a good book",
    "how to start reading",
    "reading tips",
    "improve reading habits",
    
    # System capabilities
    "help",
    "what can you do",
    "how does this work",
    "how do you recommend books",
    "what is this system",
    "features",
    
    # Specific book queries
    "tell me about harry potter",
    "what is the best fantasy series",
    "books like game of thrones",
    "similar to lord of the rings",
    
    # Rating queries
    "how do you rate books",
    "what is book rating",
    "rating system",
    
    # Difficulty levels
    "what are difficulty levels",
    "explain difficulty",
    "easy vs hard books",
    
    # Greeting
    "hello",
    "hi",
    "hey",
    "good morning",
    "greetings",
    
    # Thanks
    "thank you",
    "thanks",
    "appreciate it",
    
    # Goodbye
    "bye",
    "goodbye",
    "see you",
]

answers = [
    # General recommendations
    "I'd love to help! Tell me your preferred genre, approximate page count, and difficulty level, and I'll recommend the perfect book for you.",
    "Sure! Just let me know what genre interests you (Fantasy, Romance, Mystery, Science, Self-Help, or Education), and I'll suggest great books.",
    "To give you the best recommendation, please share: 1) Your favorite genre 2) Preferred book length 3) Reading difficulty level. Then click 'Analyze & Recommend'!",
    "I can recommend books based on your preferences! Use the form above to select genre, pages, and difficulty, then click the recommendation button.",
    "Absolutely! Just fill in your preferences above - choose a genre, set the page count, and select difficulty level for personalized recommendations.",
    
    # Genre specific
    "Fantasy books are magical! Popular titles include 'Harry Potter' series, 'Lord of the Rings', 'The Hobbit', 'A Song of Ice and Fire', and 'The Name of the Wind'. They transport you to incredible worlds!",
    "For fantasy lovers, I recommend classics like 'Harry Potter', 'The Chronicles of Narnia', epic tales like 'Lord of the Rings', or modern fantasy like 'The Stormlight Archive'.",
    "Great fantasy novels include: Harry Potter (magical school), Lord of the Rings (epic quest), Mistborn (unique magic system), and The Kingkiller Chronicle (beautiful prose).",
    "Excellent self-help books include 'Atomic Habits' by James Clear, 'The 7 Habits of Highly Effective People', 'How to Win Friends and Influence People', and 'Thinking, Fast and Slow'.",
    "For self-improvement, try: 'Atomic Habits' (habit building), 'Deep Work' (focus), 'The Power of Now' (mindfulness), 'Can't Hurt Me' (mental toughness).",
    "Romance readers love 'Pride and Prejudice', 'The Notebook', 'Me Before You', 'The Fault in Our Stars', and 'Beach Read'. These books will tug at your heartstrings!",
    "Popular romance novels: 'Pride and Prejudice' (classic), 'Red, White & Royal Blue' (contemporary), 'The Hating Game' (enemies to lovers), 'It Ends with Us' (emotional).",
    "Mystery thrillers to keep you on edge: 'Gone Girl', 'The Girl with the Dragon Tattoo', 'The Da Vinci Code', 'Big Little Lies', 'The Silent Patient'.",
    "Sci-Fi favorites include 'Dune', '1984', 'The Martian', 'Foundation', 'Ender's Game', and 'Ready Player One'. Perfect for fans of technology and future worlds!",
    "Educational books that enlighten: 'Sapiens' (human history), 'Educated' (memoir), 'Thinking, Fast and Slow' (psychology), 'A Brief History of Time' (physics).",
    "Business books: 'Good to Great', 'The Lean Startup', 'Zero to One', 'Start with Why', 'The Innovator's Dilemma' - great for entrepreneurs and professionals!",
    
    # Book characteristics
    "Short books under 250 pages: 'Animal Farm', 'The Old Man and the Sea', 'Of Mice and Men', 'The Great Gatsby', 'The Alchemist' - perfect for quick reads!",
    "Long books for deep immersion: 'War and Peace' (1200+ pages), 'Atlas Shrugged', 'The Stand', 'Infinite Jest', 'The Lord of the Rings trilogy'.",
    "Easy books for casual reading: 'The Alchemist', 'Who Moved My Cheese?', 'The Little Prince', 'Charlotte's Web', 'Diary of a Wimpy Kid'.",
    "Challenging reads: 'Ulysses', '100 Years of Solitude', 'Infinite Jest', 'Gravity's Rainbow', 'Crime and Punishment' - for experienced readers!",
    "Beginner-friendly books: 'The Giver', 'Holes', 'Wonder', 'Percy Jackson series', 'The Hunger Games' - easy to follow with engaging stories.",
    "Advanced literature: 'Moby Dick', 'The Brothers Karamazov', 'In Search of Lost Time', 'Finnegans Wake', 'The Sound and the Fury'.",
    
    # Popular books
    "Most popular books include: 'Harry Potter series', 'To Kill a Mockingbird', '1984', 'The Great Gatsby', 'The Lord of the Rings', 'Pride and Prejudice'.",
    "Bestsellers that everyone loves: 'Where the Crawdads Sing', 'Becoming by Michelle Obama', 'Educated', 'The Silent Patient', 'Atomic Habits'.",
    "Highest-rated books: 'To Kill a Mockingbird' (5/5), 'The Lord of the Rings' (4.9/5), 'Harry Potter' (4.8/5), '1984' (4.7/5), 'Pride and Prejudice' (4.6/5).",
    "Classic literature: 'Pride and Prejudice', 'Jane Eyre', 'Wuthering Heights', 'Great Expectations', 'The Count of Monte Cristo', 'Les Misérables'.",
    "Famous books everyone should read: 'To Kill a Mockingbird', '1984', 'The Catcher in the Rye', 'Lord of the Flies', 'Animal Farm', 'Brave New World'.",
    
    # Authors
    "Great authors include: J.K. Rowling (Fantasy), Stephen King (Horror/Thriller), Agatha Christie (Mystery), Jane Austen (Romance), Isaac Asimov (Sci-Fi).",
    "Famous authors: Ernest Hemingway, F. Scott Fitzgerald, Leo Tolstoy, Charles Dickens, Mark Twain, William Shakespeare, George Orwell.",
    "Best contemporary writers: Brandon Sanderson (Fantasy), Colleen Hoover (Romance), Dan Brown (Thriller), Yuval Noah Harari (Non-fiction), Malcolm Gladwell.",
    "I recommend authors based on genre! Fantasy: Brandon Sanderson, Patrick Rothfuss. Mystery: Agatha Christie, Dan Brown. Romance: Nicholas Sparks, Jane Austen.",
    
    # Book series
    "Amazing book series: 'Harry Potter' (7 books), 'Lord of the Rings' (3 books), 'The Hunger Games' (3 books), 'Divergent' (3 books), 'Percy Jackson' (5 books).",
    "Epic trilogies: 'His Dark Materials', 'The Hunger Games', 'Fifty Shades', 'Millennium series', 'The Lunar Chronicles', 'Red Rising'.",
    "Series worth reading: Harry Potter, Game of Thrones, Wheel of Time, Discworld, Foundation, The Expanse, The Witcher.",
    
    # Reading advice
    "Choose books based on: 1) Your interests (genre), 2) Available time (page count), 3) Reading experience (difficulty). Start with what excites you!",
    "A good book has: engaging characters, compelling plot, beautiful writing, emotional depth, and makes you think or feel. It should resonate with you personally.",
    "Start reading by: 1) Choose a genre you like, 2) Start with easier books, 3) Read 15-20 mins daily, 4) Don't force books you don't enjoy, 5) Join book communities!",
    "Reading tips: Set daily goals, create a reading space, avoid distractions, try different genres, discuss books with others, keep a reading journal.",
    "Improve reading habits: Read at the same time daily, start small (10 pages/day), always carry a book, join book clubs, set yearly goals, mix fiction and non-fiction.",
    
    # System capabilities
    "I can: 1) Recommend books based on genre/pages/difficulty, 2) Answer questions about books, 3) Explain genres and ratings, 4) Suggest reading strategies. Try asking me anything!",
    "I help you discover books! I use machine learning to predict book ratings and recommend titles based on your preferences. Just fill the form above and click 'Analyze & Recommend'!",
    "This is an AI-powered book recommendation system. Select your genre, preferred page count, and difficulty level, then I'll predict ratings and suggest books you'll love!",
    "I analyze your preferences using a Random Forest ML model trained on thousands of books. I consider genre, length, difficulty, and user ratings to give personalized recommendations.",
    "This system combines Machine Learning (for rating prediction) and Natural Language Processing (for chatbot interactions) to help you find your next great read!",
    "Features: 📚 ML-based recommendations, ⭐ Rating predictions, 💬 Interactive chatbot, 🎯 Personalized suggestions, 📊 Genre-specific insights, 🔍 Book discovery.",
    
    # Specific book queries
    "Harry Potter is a 7-book fantasy series about a young wizard. It's perfect for all ages, combines magic, friendship, and adventure. Rated 4.8/5 - highly recommended!",
    "The best fantasy series include: 'Lord of the Rings' (epic high fantasy), 'Harry Potter' (magical realism), 'Game of Thrones' (dark fantasy), 'Wheel of Time' (epic).",
    "Books like Game of Thrones: 'The Name of the Wind', 'The First Law trilogy', 'The Stormlight Archive', 'The Witcher series' - all feature complex characters and politics.",
    "Similar to LOTR: 'The Wheel of Time', 'The Sword of Shannara', 'The Chronicles of Narnia', 'Earthsea', 'The Silmarillion' - epic fantasy with rich world-building.",
    
    # Rating queries
    "I rate books on a 0-5 scale based on: genre popularity, user reviews, difficulty match, and reading satisfaction. Higher ratings mean better match for your preferences!",
    "Book ratings (0-5): 5=Masterpiece, 4-4.5=Excellent, 3.5-4=Very Good, 3=Good, 2.5-3=Average, <2.5=Below Average. I predict what rating YOU would give.",
    "My rating system uses machine learning to predict how much you'll enjoy a book based on genre preferences, reading level, and community ratings.",
    
    # Difficulty levels
    "Difficulty levels: 1=Easy (simple language, fast pacing), 2=Medium (moderate vocabulary), 3=Hard (complex themes), 4=Expert (dense prose), 5=Master (philosophical/literary).",
    "Easy books use simple language and clear plots. Hard books have complex themes, literary devices, philosophical depth, and require focus. Choose based on your experience!",
    "Easy (1-2): Young adult, light fiction. Medium (3): Most novels. Hard (4-5): Classic literature, philosophy, dense non-fiction. Match difficulty to your comfort level!",
    
    # Greeting
    "Hello! 👋 I'm your AI book advisor. I can recommend books, answer questions about literature, and help you find your next great read. How can I help?",
    "Hi there! 📚 Welcome to the Smart Book Advisor. Ask me about books, genres, authors, or use the form above for personalized recommendations!",
    "Hey! 🎉 Ready to discover amazing books? Tell me what you're interested in, or use the recommendation tool above!",
    "Good morning! ☀️ What kind of books are you in the mood for today? I can help you find the perfect read!",
    "Greetings, book lover! 📖 I'm here to help you discover your next favorite book. What interests you?",
    
    # Thanks
    "You're welcome! 😊 Happy reading! Feel free to ask me anything else about books.",
    "My pleasure! 📚 Enjoy your reading journey. Come back anytime you need more recommendations!",
    "Glad I could help! 🌟 Don't hesitate to ask if you need more book suggestions!",
    
    # Goodbye
    "Goodbye! 👋 Happy reading! Come back when you need more book recommendations!",
    "See you later! 📚 Enjoy your books and come back soon for more suggestions!",
    "Farewell! 🌟 May your reading adventures be amazing. Visit again anytime!",
]

# Initialize vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
X = vectorizer.fit_transform(questions)


def chatbot_response(message):
    """Enhanced chatbot with book data integration"""
    if not message or len(message.strip()) == 0:
        return "Please ask me something about books! 📚"
    
    message_lower = message.lower().strip()
    
    # Check for specific book queries in database
    if df is not None and any(word in message_lower for word in ['books in', 'titles in', 'list', 'show me']):
        genre_match = None
        for word in ['fantasy', 'selfhelp', 'self help', 'education', 'mystery', 'romance', 'science']:
            if word.replace(' ', '') in message_lower.replace(' ', ''):
                genre_match = word.replace(' ', '')
                if genre_match == 'selfhelp':
                    genre_match = 'SelfHelp'
                else:
                    genre_match = genre_match.capitalize()
                break
        
        if genre_match and genre_match in df['genre'].values:
            books = df[df['genre'] == genre_match].nlargest(5, 'user_rating')['title'].tolist()
            if books:
                return f"Top {genre_match} books:\n" + "\n".join([f"📖 {book}" for book in books])
    
    # Use TF-IDF similarity for general queries
    try:
        message_vec = vectorizer.transform([message_lower])
        similarity = cosine_similarity(message_vec, X)
        idx = similarity.argmax()
        confidence = similarity[0][idx]
        
        # If confidence is too low, give a generic helpful response
        if confidence < 0.1:
            return "I'm not sure I understood that. Try asking about:\n• Book recommendations\n• Specific genres (Fantasy, Romance, Mystery, etc.)\n• Authors and series\n• Reading tips\n• How this system works"
        
        return answers[idx]
    except Exception as e:
        return "I can help you find books! Ask me about genres, recommendations, or use the form above for personalized suggestions."


def get_genre_info(genre):
    """Get information about a specific genre"""
    genre_info = {
        'Fantasy': '🧙‍♂️ Fantasy: Magical worlds, mythical creatures, epic quests. Perfect for escapism and imagination!',
        'SelfHelp': '💡 Self-Help: Personal development, productivity, mindfulness. Great for self-improvement!',
        'Education': '🎓 Education: Learning, science, history, academics. Expand your knowledge!',
        'Mystery': '🔍 Mystery: Crime solving, suspense, plot twists. Keep you guessing until the end!',
        'Romance': '💖 Romance: Love stories, relationships, emotions. Perfect for heartwarming reads!',
        'Science': '🔬 Science: Scientific discoveries, technology, research. Fascinating facts and theories!'
    }
    return genre_info.get(genre, 'Genre information not available.')
