from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import Literal, Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# Define extraction model for extracting information
class EmailExtractionOutput(BaseModel):
    company_name: Optional[str] = None
    job_position: Optional[str] = None
    rejection_reason: Optional[str] = None


@CrewBase
class EextractionEmailCrew:
    """Email Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="o3-mini")


    @agent
    def information_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config["information_extractor"], 
            llm=self.llm,
        )
    @task
    def information_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["information_extraction_task"],
            output_pydantic=EmailExtractionOutput 
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