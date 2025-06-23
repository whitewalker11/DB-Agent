from google.adk import Agent
from .prompt import instruction
from .tools.analysis_tools import compute_statistics,compute_correlation

analysis_agent = Agent(
    name="analysis_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[compute_statistics, compute_correlation]
)

