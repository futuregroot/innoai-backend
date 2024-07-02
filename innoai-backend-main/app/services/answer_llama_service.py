import os
import openai
import logging
import openai
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_core.vectorstores import VectorStoreRetriever

logger = logging.getLogger("AnswerLlamaService")

class AnswerLlamaService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = openai.api_key

        # Define TEMPLATE
        self.QA_TEMPLATE_LLAMAANSWER = """
        Provide a concise and direct answer referring to the context:
        <context>
          {context}
        </context>
        Question: {question}
        """

    def make_chat_chain(self, retriever: VectorStoreRetriever) -> RunnableSequence:
        answer_template = ChatPromptTemplate.from_template(self.QA_TEMPLATE_LLAMAANSWER)

        selected_model = ChatOpenAI(
            model="llama",
            api_key=self.api_key
        )

        return RunnableSequence([
            lambda input: {
                'context': self.combine_documents_fn(retriever.get_relevant_documents(input['question'])),
                'question': input['question'],
                'chat_history': input['chat_history']
            },
            answer_template,
            selected_model,
            StrOutputParser(),
        ])

    def combine_documents_fn(self, docs: [Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)