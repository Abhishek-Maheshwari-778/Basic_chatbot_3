import spacy
import random
import data  
from collections import deque  

#
nlp = spacy.load('en_core_web_sm')


conversation_history = deque(maxlen=5)  
knowledge_storage = {} 
def preprocess_input_spacy(user_input):
    doc = nlp(user_input)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return tokens, entities

def detect_emotion(user_input):
    """Simple emotion detection based on keywords."""
    emotions = {
        'happy': ['happy', 'joy', 'excited', 'good'],
        'sad': ['sad', 'down', 'depressed', 'bad'],
        'angry': ['angry', 'mad', 'furious', 'annoyed']
    }
    for emotion, keywords in emotions.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            return emotion
    return None

def learn_new_info(user_input):
    """Detect if user wants to teach the bot something."""
    if "learn" in user_input.lower():
        return True
    return False

def store_knowledge(user_input):
    """Store new information provided by the user."""
    if 'that is' in user_input.lower() or 'this is' in user_input.lower():
        parts = user_input.split('is')
        if len(parts) > 1:
            key = parts[0].strip()
            value = parts[1].strip()
            knowledge_storage[key] = value
            return f"Got it! I'll remember that {key} is {value}."
    return "Could you clarify what you'd like me to remember?"

def get_response_spacy(user_input):
  
    responses = data.responses

   
    tokens, entities = preprocess_input_spacy(user_input)

    
    emotion = detect_emotion(user_input)
    if emotion and emotion in responses:
        return random.choice(responses[emotion])

    
    if learn_new_info(user_input):
        return "What would you like me to learn?"

   
    for token in tokens:
        if token in responses:
            return random.choice(responses[token])

    
    if entities:
        for entity in entities:
            if entity[1] == 'PERSON':
                return f"Nice to meet you, {entity[0]}!"
            elif entity[1] == 'ORG':
                return f"Oh, you mentioned {entity[0]}. What would you like to know about them?"
            elif entity[1] == 'GPE':
                return f"{entity[0]} is a great place! Have you been there?"
            elif entity[1] == 'DATE':
                return f"I see you mentioned a date: {entity[0]}. What's special about that?"

    
    if 'remember' in conversation_history:
        return store_knowledge(user_input)

   
    if conversation_history.count(user_input.lower()) > 1:
        return "You seem to be asking this again. Is something unclear?"

   
    if 'help' in conversation_history:
        return random.choice(["I noticed you asked for help earlier. How can I assist?", "Still need help with something?"])

    return random.choice([
        "I'm not sure I understand. Could you clarify?",
        "Tell me more about that.",
        "That's interesting!"
    ])

def chatbot_spacy():
    print("Welcome! You can start chatting with me (type 'exit' to quit).")
    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye! Have a great day.")
            break
        
       
        conversation_history.append(user_input.lower())
        
        
        if learn_new_info(user_input):
            conversation_history.append('remember')

       
        response = get_response_spacy(user_input)
        
        print("Chatbot:", response)

if __name__ == "__main__":
    chatbot_spacy()
