def generate_reply(system_prompt: str, user_message: str):
    """
    Temporary AI function.
    Later this will call OpenAI.
    """

    return (
        f"{system_prompt}\n\n"
        f"User asked: {user_message}\n\n"
        f"(This is a temporary AI response.)"
    )