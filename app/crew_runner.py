from crewai import Crew, Process

from app.agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)

from app.task import (
    verification,
    analyze_financial_document,
    investment_analysis,
    risk_assessment
)


def run_crew(query, file_path):

    financial_crew = Crew(
        agents=[
            verifier,
            financial_analyst,
            investment_advisor,
            risk_assessor
        ],
        tasks=[
            verification,
            analyze_financial_document,
            investment_analysis,
            risk_assessment
        ],
        process=Process.sequential,
        verbose=False,
        memory=False,
        full_output=True
    )

    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "file_path": file_path
        }
    )

    outputs = []

    if hasattr(result, "tasks_output"):

        for task_output in result.tasks_output:

            if hasattr(task_output, "raw"):
                outputs.append(str(task_output.raw))

    return "\n\n=====================\n\n".join(outputs)