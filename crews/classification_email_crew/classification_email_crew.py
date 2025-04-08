from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import Literal, Optional
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from litellm import completion
from dotenv import load_dotenv
load_dotenv()



# Define classification model for categorization
class EmailClassificationOutput(BaseModel):
    category: Literal["Application_Received", "Rejection", "Interview_Invitation", "Irrelevant"]


@CrewBase
class ClassificationEmailCrew:
    """Email Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="o3-mini")

    @agent
    def categorizer(self) -> Agent:
        return Agent(
            config=self.agents_config["categorizer"],
            llm=self.llm,
        )

    @task
    def categorization_task(self) -> Task:
        return Task(
            config=self.tasks_config["categorization_task"],
            output_pydantic=EmailClassificationOutput
        )

    @crew
    def crew(self) -> Crew:
        """Creates the  Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

