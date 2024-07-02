import re
import openai
import os
import openai
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
import logging

logger = logging.getLogger("SplitLlamaService")


class SplitLlamaService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = openai.api_key

        # Define TEMPLATE
        self.QA_TEMPLATE_LLAMASPLIT = """
        <|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an AI assistant designed to split questions into multiple distinct questions based on your judgement.<|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        Focus on the question and decide to split the question or not. Split it into multiple distinct questions as necessary. Provide your response in the format:

        Split question 1:

        or

        Split question 1:
        Split question 2:

        or 

        Split question 1:
        Split question 2:
        Split question 3:

        as your judgement.

        Original question: {original_question}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """

    def make_split_chain(self, model: str) -> RunnableSequence:
        split_template = ChatPromptTemplate.from_messages([
            ("system",
             "You are an AI assistant designed to split questions into multiple distinct questions based on your judgement."),
            ("human", "{original_question}")
        ])

        selected_model = ChatOpenAI(
            model=model,
            api_key=self.api_key
        )

        return RunnableSequence([
            lambda input: {"original_question": input['question']},
            split_template,
            selected_model,
            StrOutputParser(),
            lambda output: self.post_process_response(output),
        ])

    def post_process_response(self, response: str) -> str:
        split_matches = [match for match in re.finditer(
            r"Split question \d+:\s*(.*?)(?=(Split question \d+:|$|\n))", response, re.S
        )]

        split_questions = [match.group(1).strip() for match in split_matches]

        if split_questions:
            return "\n".join(f"Split question {i + 1}: {q}" for i, q in enumerate(split_questions))
        else:
            raise ValueError(f"Unexpected response format: {response}")