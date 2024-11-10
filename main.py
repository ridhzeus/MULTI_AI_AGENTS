import json
import os
from dotenv import load_dotenv
from industry_research_agent import IndustryResearchAgent
from use_case_generation_agent import RAGAgent
from resource_asset_agent import ResourceAssetAgent
from proposal import ProposalAgent

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Define company and industry names
    company_name = "APPLE INC"
    industry_name = "Technology and Consumer Electronics"
    
    try:
        # Step 1: Run Industry & Company Research Agent using Serper API key
        print("\nStep 1: Running Industry Research")
        print("=" * 50)
        industry_research_agent = IndustryResearchAgent(
            company_name, 
            industry_name, 
            os.getenv("SERPER_API_KEY")
        )
        industry_research_results = industry_research_agent.run()
        
        # Validate and process data
        industry_data = industry_research_results.get("industry_data")
        company_data = industry_research_results.get("company_data")
        
        print("Industry Data:", type(industry_data), industry_data)
        print("Company Data:", type(company_data), company_data)
        
        # Convert non-string data types if necessary
        if not isinstance(industry_data, str):
            print("Converting industry data to string format...")
            industry_data = json.dumps(industry_data) if isinstance(industry_data, dict) else str(industry_data)
            
        if not isinstance(company_data, str):
            print("Converting company data to string format...")
            company_data = json.dumps(company_data) if isinstance(company_data, dict) else str(company_data)
        
        # Step 2: Generate Use Cases using GROQ API key
        print("\nStep 2: Generating Use Cases")
        print("=" * 50)
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise Exception("GROQ API key not found in environment variables")
            
        use_case_agent = RAGAgent(industry_data, company_data, api_key=groq_api_key)
        use_cases = use_case_agent.generate_use_cases()
        
        if use_cases is None:
            raise Exception("Use case generation failed")
        
        print(f"Generated {len(use_cases)} use cases")
        
        # Step 3: Collect Resources using GitHub API key
        print("\nStep 3: Collecting Resources")
        print("=" * 50)
        github_api_key = os.getenv("GITHUB_API_KEY")
        if not github_api_key:
            raise Exception("GitHub API key not found in environment variables")
            
        resource_agent = ResourceAssetAgent(use_cases, github_api_key)
        datasets = resource_agent.run()
        
        print(f"Collected {len(datasets)} datasets")
        
        # Step 4: Generate Final Proposal
        print("\nStep 4: Generating Final Proposal")
        print("=" * 50)
        proposal_agent = ProposalAgent(industry_data, company_data, use_cases, datasets)
        final_proposal = proposal_agent.run()
        
        # Create output directory if it doesn't exist
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Save the final proposal
        proposal_path = os.path.join(output_dir, "Apple_AI_ML_Proposal.md")
        with open(proposal_path, "w", encoding='utf-8') as f:
            f.write(final_proposal)
        
        print(f"\nFinal proposal saved to: {proposal_path}")
        print("\nProposal Preview:\n")
        print(final_proposal[:500] + "...\n")
        
    except Exception as e:
        print(f"\nError in pipeline execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
