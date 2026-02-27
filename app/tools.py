from crewai.tools import BaseTool
from pypdf import PdfReader
from pydantic import BaseModel, Field
from typing import Type
import os
import re
import hashlib


# =====================================================
# SCHEMA: Financial Document Input
# =====================================================

class FinancialDocumentInput(BaseModel):
    file_path: str = Field(..., description="Absolute path to financial PDF document")


# =====================================================
# TOOL 1: READ FINANCIAL DOCUMENT TOOL
# =====================================================

class FinancialDocumentTool(BaseTool):

    name: str = "read_data_tool"

    description: str = (
        "Extracts and cleans financial data from PDF. "
        "Returns structured content with checksum. "
        "Use ONLY once per document."
    )

    args_schema: Type[BaseModel] = FinancialDocumentInput

    cache: bool = False
    max_usage_count: int = 3

    def _run(self, file_path: str) -> str:

        try:

            if not file_path:
                return "ERROR: file_path missing"

            if not os.path.exists(file_path):
                return f"ERROR: File not found: {file_path}"

            reader = PdfReader(file_path)

            text_parts = []

            for page in reader.pages:

                text = page.extract_text()

                if text:

                    # Clean text
                    text = text.replace("\x00", "")

                    text = re.sub(r"\n{3,}", "\n\n", text)

                    text = re.sub(r"[^\x00-\x7F]+", " ", text)

                    text_parts.append(text.strip())

            if not text_parts:
                return "ERROR: No readable content"

            full_text = "\n".join(text_parts)

            # Hard safety limit for glm-5 cloud
            cleaned_text = full_text[:10000]

            checksum = hashlib.md5(cleaned_text.encode()).hexdigest()

            return (
                "FINANCIAL_DOCUMENT_CONTENT_START\n\n"
                f"{cleaned_text}\n\n"
                "FINANCIAL_DOCUMENT_CONTENT_END\n\n"
                f"DOCUMENT_CHECKSUM:{checksum}"
            )

        except Exception as e:

            return f"ERROR reading PDF: {str(e)}"


# =====================================================
# SCHEMA: Investment Tool Input
# =====================================================

class InvestmentInput(BaseModel):
    data: str = Field(..., description="Financial document content")


# =====================================================
# TOOL 2: INVESTMENT ANALYSIS TOOL
# =====================================================

class InvestmentTool(BaseTool):

    name: str = "investment_analysis_tool"

    description: str = (
        "Analyzes financial data and identifies investment indicators "
        "including profitability, growth, and financial strength."
    )

    args_schema: Type[BaseModel] = InvestmentInput

    cache: bool = False
    max_usage_count: int = 3

    def _run(self, data: str) -> str:

        try:

            if not data:
              return "Investment Insight:\n- No financial data provided"

            data_lower = data.lower()

# accept both checksum content and summaries
            valid = (
              "revenue" in data_lower or
              "income" in data_lower or
              "cash" in data_lower or
              "margin" in data_lower or
              "growth" in data_lower 
             )

            if not valid:
               return "Investment Insight:\n- Insufficient financial indicators"
            text = data.lower()

            insights = []

            if "revenue" in text:
                insights.append("Revenue trends identified")

            if "net income" in text:
                insights.append("Profitability indicators present")

            if "cash flow" in text:
                insights.append("Positive operating cash flow indicators")

            if "free cash flow" in text:
                insights.append("Free cash flow metrics identified")

            if "growth" in text:
                insights.append("Business growth indicators present")

            if "decline" in text or "decrease" in text:
                insights.append("Negative financial performance indicators")

            if "margin" in text:
                insights.append("Profit margin data available")

            if not insights:
                insights.append("No major investment indicators detected")

            checksum = hashlib.md5(text[:3000].encode()).hexdigest()

            return (
                "Investment Insight:\n"
                + "\n".join(f"- {i}" for i in insights)
                + f"\nCHECKSUM:{checksum}"
            )

        except Exception as e:

            return f"Investment tool error: {str(e)}"


# =====================================================
# SCHEMA: Risk Tool Input
# =====================================================

class RiskInput(BaseModel):
    data: str = Field(..., description="Financial document content")


# =====================================================
# TOOL 3: RISK ASSESSMENT TOOL
# =====================================================

class RiskTool(BaseTool):

    name: str = "risk_assessment_tool"

    description: str = (
        "Analyzes financial content to identify liquidity, operational, "
        "financial, and market risks."
    )

    args_schema: Type[BaseModel] = RiskInput

    cache: bool = False
    max_usage_count: int = 3

    def _run(self, data: str) -> str:

        try:

            if not data:
               return "Risk Overview:\n- No financial data provided"

            data_lower = data.lower()

            valid = (
              "revenue" in data_lower or
              "income" in data_lower or
              "cash" in data_lower or
              "risk" in data_lower or
              "decline" in data_lower
             )

            if not valid:
              return "Risk Overview:\n- Insufficient risk indicators"

            text = data.lower()

            risks = []

            if "decline" in text or "decrease" in text:
                risks.append("Revenue or profitability decline risk")

            if "cash flow" in text:
                risks.append("Cash flow fluctuation risk")

            if "debt" in text or "liabilities" in text:
                risks.append("Debt exposure risk")

            if "uncertain" in text or "uncertainty" in text:
                risks.append("Macroeconomic uncertainty risk")

            if "tariff" in text:
                risks.append("Trade and tariff risk")

            if "operating margin" in text:
                risks.append("Operating margin compression risk")

            if not risks:
                risks.append("No major financial risks detected")

            checksum = hashlib.md5(text[:3000].encode()).hexdigest()

            return (
                "Risk Overview:\n"
                + "\n".join(f"- {r}" for r in risks)
                + f"\nCHECKSUM:{checksum}"
            )

        except Exception as e:

            return f"Risk tool error: {str(e)}"


# =====================================================
# TOOL INSTANCES
# =====================================================

read_data_tool = FinancialDocumentTool()

investment_tool = InvestmentTool()

risk_tool = RiskTool()