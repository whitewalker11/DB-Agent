from google.adk import Agent
from .prompt import instruction
from .tools.visual_tools import plot_histogram,plot_time_series

visual_agent = Agent(
    name="visual_agent",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[plot_histogram,plot_time_series]
)
