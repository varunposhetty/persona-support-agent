def create_handoff(persona, query, sources):

    summary = {
        "persona": persona,
        "issue": query,
        "documents_used": sources,
        "recommendation": "Escalate to human support agent."
    }

    return summary


if __name__ == "__main__":

    handoff = create_handoff(
        "Frustrated User",
        "Unable to reset password",
        ["password_reset.txt"]
    )

    print(handoff)