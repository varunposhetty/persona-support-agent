def should_escalate(query, results):

    query = query.lower()

    escalation_words = [
        "billing",
        "legal",
        "refund",
        "lawsuit",
        "account hacked",
        "human agent"
    ]

    for word in escalation_words:
        if word in query:
            return True

    if len(results) == 0:
        return True

    return False


if __name__ == "__main__":

    query = input("User: ")

    if should_escalate(query, []):
        print("Escalation Required")
    else:
        print("No Escalation")