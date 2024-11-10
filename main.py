import json
import os
from industry_research_agent import IndustryResearchAgent
from use_case_generation_agent import RAGAgent
from resource_asset_agent import ResourceAssetAgent
from proposal import ProposalAgent

def main():
    # Define company and industry names
    company_name = "APPLE INC"
    industry_name = "Retail"
    
    # Define Serper and Groq API keys separately
    serper_api_key = "f1f9fcf2086065048536fb6d26b9b797051e9a46"  # Replace with your actual Serper API key
    groq_api_key = "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"  # Replace with your actual Groq API key

    # Set API keys as environment variables
    os.environ["SERPER_API_KEY"] = serper_api_key
    os.environ["GROQ_API_KEY"] = groq_api_key

    try:
        # Step 1: Run Industry & Company Research Agent with Serper API key
        industry_research_agent = IndustryResearchAgent(company_name, industry_name, os.getenv("SERPER_API_KEY"))
        industry_research_results = industry_research_agent.run()
        
        # Validate and process data
        industry_data = industry_research_results.get("industry_data")
        company_data = industry_research_results.get("company_data")
        
        print("Industry Data:", type(industry_data), industry_data)
        print("Company Data:", type(company_data), company_data)
        
        # Convert non-string data types if necessary
        if not isinstance(industry_data, str):
            print("Industry data is not a string! Converting to string...")
            industry_data = json.dumps(industry_data) if isinstance(industry_data, dict) else str(industry_data)
        
        if not isinstance(company_data, str):
            print("Company data is not a string! Converting to string...")
            company_data = json.dumps(company_data) if isinstance(company_data, dict) else str(company_data)
        
        # Step 2: Run Use Case Generation Agent (assumes no API key needed)
        use_case_agent = RAGAgent(industry_data, company_data)
        use_cases = use_case_agent.generate_use_cases()
        
        if use_cases is None:
            raise Exception("Failed to generate use cases")
        
        # Step 3: Run Resource Asset Collection Agent with Groq API key
        resource_agent = ResourceAssetAgent(use_cases, os.getenv("GROQ_API_KEY"))
        datasets = resource_agent.run()
        
        # Step 4: Run Proposal Agent
        proposal_agent = ProposalAgent(industry_data, company_data, use_cases, datasets)
        final_proposal = proposal_agent.run()
        
        # Output the Final Proposal
        print("\nFinal Proposal:\n")
        print(final_proposal)
        
    except Exception as e:
        print(f"Error in pipeline execution: {str(e)}")

if __name__ == "__main__":
    main()