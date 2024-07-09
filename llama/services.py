import spacy
from django.db.models import Q
from langchain_community.llms import Ollama
from langchain import PromptTemplate, LLMChain
from transformers import pipeline
import logging
from llama.models import Company


class ChatbotService:
    def __init__(self):
        self.llm = Ollama(model="llama3-chatqa:8b")
        nlp = spacy.load("en_core_web_lg")
        self.intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def get_company_data(self):
        return list(Company.objects.filter(
            Q(potential_business_details__isnull=False) |
            Q(name__isnull=False) |
            Q(description__isnull=False) |
            Q(product_types__isnull=False) |
            Q(supplier_category__isnull=False)
        ).values(
            'id', 'name', 'description',
            'product_types', 'supplier_category'
        ))

    def extract_intent(self, question):
        candidate_labels = ["greeting", "farewell", "inquiry", "unknown"]
        result = self.intent_classifier(question, candidate_labels)
        intent = result["labels"][0]  # The top intent
        return intent

    def extract_company_name(self, question):
        question_words = ['what', 'which', 'how', 'where', 'when', 'who', 'why', 'is that', 'could', 'can']
        words = question.split()
        company_name = []
        for word in words:
            if word.lower() in question_words:
                break
            company_name.append(word)
        return ' '.join(company_name)

    def find_company_data(self, company_name, company_data):
        for company in company_data:
            if company_name.lower() in company['name'].lower():
                return company
        return None

    def ollama_answer(self, question, company_data, intent):
        try:
            # Extract company name from the question
            company_name = self.extract_company_name(question)

            # Find the specific company data
            specific_company_data = self.find_company_data(company_name, company_data)

            if not specific_company_data:
                return None, None

            template = """
            Company Name: {company_name}
            Company Description: {company_description}
            Product Types: {product_types}
            Supplier Category: {supplier_category}

            Question: {question}

            Based solely on the above company information, provide a concise answer to the question.
            Focus only on the information given about the company's products, manufacturing, or services.
            If the specific information is not mentioned, state that it's not provided.

            Answer:
            """

            prompt = PromptTemplate(template=template,
                                    input_variables=["company_name", "company_description", "product_types",
                                                     "supplier_category", "question"])
            chain = LLMChain(llm=self.llm, prompt=prompt)

            response = chain.run(
                company_name=specific_company_data['name'],
                company_description=specific_company_data['description'],
                product_types=specific_company_data['product_types'],
                supplier_category=specific_company_data['supplier_category'],
                question=question
            )

            # Clean up the response
            answer = response.strip()
            if answer.startswith("Answer:"):
                answer = answer[7:].strip()

            context = f"Information based on {company_name}'s company data."

            return answer, context

        except Exception as e:
            logging.error(f"Error using Ollama: {str(e)}")
            return None, None

    def answer_question(self, question):
        intent = self.extract_intent(question)
        company_data = self.get_company_data()
        return self.ollama_answer(question, company_data, intent)
