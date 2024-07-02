import re
import openai
import os
import logging

logger = logging.getLogger("SplitGPTService")

class SplitGPTService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = openai.api_key

        # Define TEMPLATE
        self.QA_TEMPLATE_GPTSPLIT = """
        Evaluate the question to determine if it needs to be split into multiple distinct questions. If it doesn't need to be split, provide it as one question.

        If the question does not need to be split, provide the single question as follows:
        Split question 1: [original_question]

        However, if the question can be divided into multiple distinct questions, format the response as:
        Split question 1: [first split question]
        Split question 2: [second split question]

        If there are additional splits, continue the enumeration:
        Split question 1: [first split question]
        Split question 2: [second split question]
        Split question 3: [third split question]

        Provide your response according to the examples above based on your judgment.

        Original question: {original_question}
        """

    def split(self, model, question):
        messages = [
            {"role": "system", "content": "You are an AI assistant designed to split questions into multiple distinct questions based on your judgement."},
            {"role": "user", "content": self.QA_TEMPLATE_GPTSPLIT.format(original_question=question)}
        ]

        # Log the parameters
        logger.debug("Model: %s", model)
        logger.debug("Question: %s", question)

        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=3000,
            temperature=0.7
        )

        response_message = response.choices[0].message.content
        return self.post_process_response(response_message)

    def post_process_response(self, response: str) -> str:
        split_matches = [match for match in re.finditer(
            r"Split question \d+:\s*(.*?)(?=(Split question \d+:|$|\n))", response, re.S
        )]

        split_questions = [match.group(1).strip() for match in split_matches]

        if split_questions:
            return "\n".join(f"Split question {i + 1}: {q}" for i, q in enumerate(split_questions))
        else:
            raise ValueError(f"Unexpected response format: {response}")
