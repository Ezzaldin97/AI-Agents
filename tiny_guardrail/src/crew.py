from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tools.custom_tool import PIIRemovalTool, BadWordsRemovalTool
from crewai_tools import FileReadTool, DirectoryReadTool
import os

@CrewBase
class TinyGuardrail():
	"""TinyGuardrail crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def guardrail(self) -> Agent:
		return Agent(
			config=self.agents_config['guardrail'],
			llm=LLM(
				model=f"{os.getenv('REMOTE_PROVIDER')}/{os.getenv('HF_MODEL')}", 
				api_key=os.getenv('HF_TOKEN')
			),
			verbose=True
		)

	@task
	def guard_task(self) -> Task:
		return Task(
			config=self.tasks_config['guard_task'],
			tools=[
				DirectoryReadTool(), FileReadTool(),
				PIIRemovalTool(), BadWordsRemovalTool()
			]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TinyGuardrail crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
