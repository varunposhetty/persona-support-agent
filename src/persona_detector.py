def detect_persona(message):

    message = message.lower()

    technical_words = [
        "api", "logs", "authentication",
        "error", "configuration",
        "server", "debug"
    ]

    frustrated_words = [
        "angry", "frustrated",
        "nothing works",
        "urgent", "terrible",
        "issue", "hate"
    ]

    executive_words = [
        "business",
        "impact",
        "operations",
        "timeline",
        "resolution",
        "executive"
    ]

    for word in technical_words:
        if word in message:
            return "Technical Expert"

    for word in frustrated_words:
        if word in message:
            return "Frustrated User"

    for word in executive_words:
        if word in message:
            return "Business Executive"

    return "General User"


if __name__ == "__main__":

    query = input("User: ")

    persona = detect_persona(query)

    print("Detected Persona:", persona)