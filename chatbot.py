# chatbot.py
import nltk
from transformers import pipeline
from database import log_chat

# Download NLTK data (only once)
nltk.download('punkt')

# Load Transformer QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# FAQ database
faq_data = {
    "greeting": "Hello! How can I assist you today?",
    "hours": "Our support team is available 24/7 to assist you.",
    "contact": "You can reach us via email at support@example.com or call +91-1234567890.",
    "services": "We offer product guidance, order support, and issue resolution.",
    "pricing": "Pricing depends on services. Please visit our pricing page or contact support.",
    "location": "We operate globally with offices in India, USA, and the UK.",
    "refund": "You can request a refund within 7 days of purchase. Terms and conditions apply.",
    "track": "You can track your order using the tracking link sent to your email after dispatch."
}

# Combine all FAQ responses into one text block for Transformer QA
context = " ".join(faq_data.values())

def detect_intent(user_input):
    lowered = user_input.lower().strip()

    if any(kw in lowered for kw in ["hi", "hello", "hey", "how are you", "greetings"]):
        return "greeting"
    if any(kw in lowered for kw in ["track", "tracking", "order status"]):
        return "track"
    if any(kw in lowered for kw in ["hour", "time", "when", "working hours"]):
        return "hours"
    if any(kw in lowered for kw in ["price", "cost", "charge", "fee"]):
        return "pricing"
    if any(kw in lowered for kw in ["location", "office", "address"]):
        return "location"
    if any(kw in lowered for kw in ["refund", "return", "cancel"]):
        return "refund"
    if any(kw in lowered for kw in ["service", "support", "help"]):
        return "services"
    if any(kw in lowered for kw in ["email", "phone", "contact"]):
        return "contact"

    return None

def generate_response(user_input):
    intent = detect_intent(user_input)

    if intent:
        response = faq_data[intent]
    else:
        # Fallback to Transformer QA model
        result = qa_pipeline(question=user_input, context=context)
        answer = result['answer']
        score = result['score']

        if score > 0.5:
            response = answer
        else:
            response = "I'm sorry, I couldn't understand that. Please try rephrasing or contact support."

    # Log the conversation
    log_chat(user_input, response)
    return response
