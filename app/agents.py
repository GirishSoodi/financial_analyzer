import os
from dotenv import load_dotenv
from crewai import Agent, LLM

from app.tools import read_data_tool, investment_tool, risk_tool

load_dotenv()

# ✅ NVIDIA GLM-4.7 LLM

llm = LLM(
    model="meta/llama3-8b-instruct",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0.3
)
# ✅ Financial Analyst
financial_analyst = Agent(
    role="Senior Financial Analyst",

    goal=(
        "Thoroughly analyze the uploaded financial document and extract key financial metrics "
        "such as revenue, net income, operating margins, cash flow, debt levels, and growth trends. "
        "Provide structured financial insights based strictly on the information present in the document. "
        "Highlight performance improvements, areas of concern, and significant changes compared to prior periods "
        "if mentioned."
    ),

    backstory=(
        "You are a Chartered Financial Analyst (CFA) with extensive experience analyzing "
        "corporate earnings reports, quarterly filings, and investor presentations. "
        "You specialize in financial statement analysis, ratio interpretation, and performance benchmarking. "
        "You prioritize accuracy, clarity, and evidence-based conclusions, avoiding speculation "
        "beyond the document content."
    ),

    verbose=True,
    memory=False,

    # ✅ FIXED
    tools=[read_data_tool],

    llm=llm,
    allow_delegation=False,
    respect_context_window=True,
    max_iter=2,
    max_execution_time=60,
)

# ✅ Verifier
verifier = Agent(
    role="Financial Document Verifier",

    goal=(
        "Assess whether the uploaded document qualifies as a financial report, "
        "such as an earnings release, quarterly report, annual report, or investor update. "
        "Summarize the type of document, its reporting period, and the primary financial topics covered."
    ),

    backstory=(
        "You are a financial compliance and reporting specialist with experience reviewing "
        "corporate filings and investor communications. You carefully evaluate document structure, "
        "terminology, and financial disclosures to determine authenticity and classification."
    ),

    verbose=True,
    memory=False,

    # ✅ FIXED
    tools=[read_data_tool],

    llm=llm,
    allow_delegation=False,
    respect_context_window=True,
    max_iter=2,
    max_execution_time=60,
)

# ✅ Investment Advisor
investment_advisor = Agent(
    role="Investment Advisor",

    goal=(
        "Based on the financial analysis provided, develop balanced and realistic investment "
        "considerations. Discuss potential opportunities and risks while considering financial performance, "
        "industry context, and overall stability. Avoid exaggerated return expectations and ensure "
        "recommendations are aligned with prudent investment principles."
    ),

    backstory=(
        "You are a licensed investment advisor with expertise in equity analysis, "
        "portfolio strategy, and long-term capital allocation. You focus on risk-adjusted returns "
        "and sustainable investment decisions rather than speculative strategies."
    ),

    verbose=True,
    memory=False,

    # ✅ FIXED
    tools=[investment_tool],

    llm=llm,
    allow_delegation=False,
    respect_context_window=True,
    max_iter=1,
    max_execution_time=60,
)

# ✅ Risk Assessor
risk_assessor = Agent(
    role="Risk Assessment Specialist",

    goal=(
        "Analyze financial document risks using tool output and produce structured risk report. "
        "You MUST use the read_data_tool and MUST produce FINAL structured risk report. "
        "You MUST NOT stop after tool execution."
    ),

    backstory=(
        "You are an expert financial risk analyst specializing in corporate financial risk, "
        "liquidity analysis, operational risk, and market risk assessment."
    ),

    verbose=True,
    memory=False,

    # ✅ FIXED
    tools=[read_data_tool, risk_tool],

    llm=llm,
    allow_delegation=False,
    respect_context_window=True,
    max_iter=2,
    max_execution_time=60,
)