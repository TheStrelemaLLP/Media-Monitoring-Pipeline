from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from config import Config

class StrelemaLLM:
    def __init__(self, model=Config.LLM_MODEL, temperature=Config.TEMPERATURE):
        self.model = model
        self.temperature = temperature
        self.llm = self._initialize_llm()
        self.parser = StrOutputParser()

    def _initialize_llm(self):
        if self.model.startswith("gpt"):
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                openai_api_key=Config.OPENAI_API_KEY
            )
        elif self.model.startswith("gemini"):
            return ChatGoogleGenerativeAI(
                model=self.model,
                temperature=self.temperature,
                google_api_key=Config.GOOGLE_API_KEY
            )
        elif self.model.startswith("claude"):
            return ChatAnthropic(
                model=self.model,
                temperature=self.temperature,
                anthropic_api_key=Config.ANTHROPIC_API_KEY
            )
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def invoke(self, prompt):
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else response

    def parse(self, response):
        return self.parser.parse(response).strip()
