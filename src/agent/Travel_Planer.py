from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langgraph.graph import MessagesState
import os
from dotenv import load_dotenv
from src.tools.tools import tools
from src.exception import CustomException
from src.logger import logging

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class TravelPlanner:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model='models/gemini-2.0-flash', api_key=GEMINI_API_KEY)
        self.llm_with_tools = self.llm.bind_tools(tools=tools)



    def plan(self,state: MessagesState) -> MessagesState:
    

        prompt = """You are an AI Travel Planner and Expense Manager. Your task is to assist users in planning trips to any city worldwide using reasoning and tools.
                    use the tools appropriate while answering
                    Give the detailed iternary for the provided duration which includes for each day:
                    - attractions and activities in places
                    - restaurants
                    - transportation
                    - hotel stays
                    - wheather forecast
                    to get data about hotels , restuarants,transportation at city and famous places use brave_search tool or wiki_tool"""


        # The planner function will now effectively leverage the tools based on the improved prompt
        response = self.llm_with_tools.invoke([prompt]+state['messages'])
        print(response)

        state['messages'] = [response]

        return {**state}