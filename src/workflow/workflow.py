from langgraph.graph import StateGraph,END,MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from src.agent.Travel_Planer import TravelPlanner
from src.tools.tools import tools
from src.exception import CustomException
from src.logger import logging


class Workflow:
    def __init__(self):
        self.planer = TravelPlanner()

    def create_workflow(self):
        workflow = StateGraph(MessagesState)

        workflow.add_node('trip_palnner',self.planer.plan)
        workflow.add_node('tool_node',ToolNode(tools))

        workflow.set_entry_point('trip_palnner')

        workflow.add_conditional_edges(
            'trip_palnner',
            tools_condition,
            {
                'tools':'tool_node',
                END:END
            }
        )

        workflow.add_edge('tool_node','trip_palnner')

        app = workflow.compile()

        return app