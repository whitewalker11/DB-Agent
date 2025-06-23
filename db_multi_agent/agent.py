from google.adk.agents import LlmAgent
from .prompt import router_instruction

# Import sub-agents
from .sub_agents.analysis_agent.agent import analysis_agent
from .sub_agents.query_agent.agent import query_agent
from .sub_agents.schema_agent.agent import schema_agent
from .sub_agents.visual_agent.agent import visual_agent

# Initialize the router agent with child agents
root_agent = LlmAgent(
    name="db_muti_agent",
    model="gemini-2.0-flash",
    description=router_instruction,
    sub_agents=[
        query_agent,
        schema_agent,
        analysis_agent,
        visual_agent
    ]
)

# Optional: function to retrieve agent
def create_agent():
    return root_agent
