def get_bot_response(message):
    message = message.lower().strip()
    with open("responses.txt", "r", encoding="utf-8") as file:
        responses = [line.strip().split("::", 1) for line in file if "::" in line]

    user_inputs = [r[0].lower() for r in responses]
    bot_replies = [r[1] for r in responses]

    message_embedding = model.encode(message, convert_to_tensor=True)
    input_embeddings = model.encode(user_inputs, convert_to_tensor=True)

    similarities = util.cos_sim(message_embedding, input_embeddings)[0]
    best_match_idx = similarities.argmax().item()
    best_score = similarities[best_match_idx].item()

    if best_score > 0.6:  # you can fine-tune this threshold
        return bot_replies[best_match_idx]

    return "Sorry, I didn't understand that. Please ask a valid HR-related query."
