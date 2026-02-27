from crewai import Task
from app.agents import financial_analyst, verifier, investment_advisor, risk_assessor
from app.tools import read_data_tool


# ✅ 1. Document Verification Task
verification = Task(
    description=(
        "Use read_data_tool with "
        "file_path='{file_path}'.\n\n"

        "STRICT RULES:\n"
        "- NEVER copy document text\n"
        "- NEVER repeat raw text\n"
        "- ONLY summarize and analyze\n"
        "- OUTPUT structured report ONLY\n"
        "- DO NOT include document excerpts\n\n"

        "Answer query: '{query}'"
    ),
    expected_output=(
        "Document Verification Report:\n\n"
        "Company Name:\n"
        "Document Type:\n"
        "Reporting Period:\n"
        "Key Financial Sections:\n"
        "Summary:"
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False,
)


# ✅ 2. Financial Analysis Task (CRITICAL FIX APPLIED)
analyze_financial_document = Task(
    description=(
        "Step 1: Use read_data_tool with "
        "file_path='{file_path}'.\n\n"

        "Step 2: Analyze the extracted financial data.\n\n"

        "IMPORTANT RULES:\n"
        "- DO NOT return raw PDF text\n"
        "- DO NOT copy document content\n"
        "- USE extracted data to generate financial analysis\n"
        "- OUTPUT ONLY structured financial report\n\n"

        "Step 3: Analyze:\n"
        "- Revenue\n"
        "- Net income\n"
        "- Profit margins\n"
        "- Cash flow\n"
        "- Debt\n"
        "- Growth trends\n\n"

        "Step 4: Answer user query '{query}'.\n\n"

        "Step 5: Generate structured financial analysis report."
    ),
    expected_output=(
        "Financial Analysis Report:\n\n"

        "Revenue Analysis:\n"
        "- Explanation\n\n"

        "Profitability Analysis:\n"
        "- Explanation\n\n"

        "Cash Flow Analysis:\n"
        "- Explanation\n\n"

        "Debt Analysis:\n"
        "- Explanation\n\n"

        "Growth Trends:\n"
        "- Explanation\n\n"

        "Financial Strength:\n"
        "- Strong / Moderate / Weak\n\n"

        "Key Insights:\n"
        "- Insight 1\n"
        "- Insight 2\n"
        "- Insight 3\n"
        "- Insight 4\n"
        "- Insight 5"
    ),
    agent=financial_analyst,
    tools=[read_data_tool],
    context=[verification],
    async_execution=False,
)


# ✅ 3. Investment Recommendation Task
investment_analysis = Task(
    description=(
        "Step 1: Review financial analysis report.\n\n"

        "IMPORTANT RULES:\n"
        "- DO NOT repeat document text\n"
        "- USE financial analysis to generate recommendation\n\n"

        "Step 2: Identify strengths and risks.\n\n"

        "Step 3: Generate professional investment recommendation."
    ),
    expected_output=(
        "Investment Recommendation Report:\n\n"

        "Growth Outlook:\n"
        "- Explanation\n\n"

        "Risk Level:\n"
        "- Low / Medium / High\n\n"

        "Investor Suitability:\n"
        "- Conservative / Moderate / Aggressive\n\n"

        "Final Recommendation:\n"
        "- Buy / Hold / Caution\n"
        "- Explanation"
    ),
    agent=investment_advisor,
    tools=[],
    context=[analyze_financial_document],
    async_execution=False,
)


# ✅ 4. Risk Assessment Task
risk_assessment = Task(
    description=(
        "Step 1: Use read_data_tool with" 
        "file_path='{file_path}' to extract document text.\n\n"

        "Step 2: Carefully analyze the extracted financial content.\n\n"

        "CRITICAL INSTRUCTIONS:\n"
        "- You MUST use the tool output to perform risk analysis\n"
        "- You MUST generate a structured risk report\n"
        "- You MUST NOT return tool action\n"
        "- You MUST NOT return raw document text\n"
        "- You MUST produce FINAL structured report\n\n"

        "Step 3: Identify and analyze:\n"
        "- Liquidity risk\n"
        "- Debt risk\n"
        "- Operational risk\n"
        "- Market risk\n\n"

        "Step 4: Generate FINAL risk assessment report."
    ),

    expected_output=(
        "Risk Assessment Report:\n\n"

        "Liquidity Risk:\n"
        "- Explanation based on cash flow and liquidity\n\n"

        "Debt Risk:\n"
        "- Explanation based on debt and liabilities\n\n"

        "Operational Risk:\n"
        "- Explanation based on operations and production\n\n"

        "Market Risk:\n"
        "- Explanation based on revenue trends and competition\n\n"

        "Overall Risk Level:\n"
        "- Low / Medium / High\n\n"

        "Summary:\n"
        "- Final professional risk summary"
    ),

    agent=risk_assessor,
    tools=[],
    context=[analyze_financial_document],
    async_execution=False,
)