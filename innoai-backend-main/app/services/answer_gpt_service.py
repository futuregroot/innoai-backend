import os
import json
import openai
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("AnswerGPTService")

class AnswerGPTService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.QA_TEMPLATE_GPTANSWER = (
            "You are an expert researcher. Use the following pieces of context to answer the question at the end:\n"
            "If the answer involves multiple items, provide the information in a list format using bullets ( • ):\n"
            "- Information on multiple items: • Item 1 • Item 2 • Item 3\n"
            "If the answer describes a process or steps, outline the steps clearly and sequentially with numbers:\n"
            "- Information on the process: 1. 2. 3.\n"
            "If the answer requires a comparison, create a comparison chart with line:\n"
            "- Comparative information:\n"
            "| Item | Feature 1 | Feature 2 | Feature 3 |\n"
            "|------|------------|------------|------------|\n"
            "| Item 1 | Feature 1 details | Feature 2 details | Feature 3 details |\n"
            "| Item 2 | Feature 1 details | Feature 2 details | Feature 3 details |\n"
            "| Item 3 | Feature 1 details | Feature 2 details | Feature 3 details |\n"
            "For any other type of answer, provide a clear and concise response in paragraph form.\n"
            "<context>\n{context}\n</context>\n"
            "<chat_history>\n{chat_history}\n</chat_history>\n"
            "Question: {question}\n"
            "Helpful answer in markdown:"
        )

    def answer(self, model, question, chat_history, context, chatroom_service, chatroom_id):
        history_messages = []
        if chat_history:
            history = json.loads(chat_history)
            for entry in history:
                history_messages.append({"role": entry["role"], "content": entry["content"]})

        messages = [
            {"role": "system", "content": "You are an expert researcher."}
        ] + history_messages + [
            {"role": "user", "content": self.QA_TEMPLATE_GPTANSWER.format(context=context, chat_history=chat_history, question=question)}
        ]

        logger.debug("Model: %s", model)
        logger.debug("Question: %s", question)
        logger.debug("Chat History: %s", chat_history)
        logger.debug("Context: %s", context)

        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=3000,
            temperature=0.1
        )

        response_message = response.choices[0].message.content
        chatbot_message = response_message

        # Update the chatroom with the new messages
        chatroom_service.update_chatroom_message(chatroom_id, question, chatbot_message)

        return response_message

def format_search_results(results):
    context = f"Document ID: {results['id']}\nMetadata: {results['metadata']}\nContent: {results['document']}"
    return context
