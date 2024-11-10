class ProposalAgent:
    def __init__(self, use_cases_with_assets):
        """
        Initializes the proposal agent with the use cases and their corresponding datasets/assets.
        
        Args:
            use_cases_with_assets (list): A list of dictionaries with use case descriptions, resources, and references.
        """
        self.use_cases_with_assets = use_cases_with_assets

    def generate_proposal(self):
        """
        Generates the final proposal by listing down the top use cases along with resource links and references.
        
        Returns:
            str: The final proposal as a markdown-formatted string.
        """
        proposal_text = "# Final Proposal\n\n"
        proposal_text += "## Top Use Cases\n\n"
        
        for entry in self.use_cases_with_assets:
            use_case = entry['use_case']
            resources = entry.get('datasets', [])
            references = entry.get('references', [])

            proposal_text += f"### {use_case}\n\n"
            proposal_text += f"**Description**: This use case addresses {use_case.lower()} in alignment with the company's goals. "
            proposal_text += f"It aims to improve areas such as [mention relevant operational needs, e.g., customer experience, predictive maintenance].\n\n"
            proposal_text += "#### Resource Links:\n"
            
            if resources:
                for resource in resources:
                    proposal_text += f"- [{resource['title']}]({resource['url']})\n"
            else:
                proposal_text += "- No specific resources found\n"
                
            if references:
                proposal_text += "\n#### References:\n"
                for reference in references:
                    proposal_text += f"- {reference}\n"
            
            proposal_text += "\n---\n\n"
        
        return proposal_text

    def save_proposal(self, filename="Final_Proposal.md"):
        """
        Saves the generated proposal to a markdown file.
        
        Args:
            filename (str): The filename to save the proposal as.
        """
        proposal = self.generate_proposal()
        
        with open(filename, "w") as file:
            file.write(proposal)
        
        print(f"Proposal saved as {filename}")

if __name__ == "__main__":
    # Sample data structure for use cases, resources, and references
    use_cases_with_assets = [
        {
            "use_case": "Automated Customer Support",
            "datasets": [
                {"title": "Customer Support Conversations Dataset", "url": "https://github.com/example/customer-support"},
                {"title": "FAQ Data for Customer Service", "url": "https://huggingface.co/datasets/faq-customer-service"}
            ],
            "references": ["Suggested based on industry trend reports", "Customer service enhancement reports"]
        },
        {
            "use_case": "Predictive Maintenance",
            "datasets": [
                {"title": "Industrial Equipment Maintenance Logs", "url": "https://www.kaggle.com/datasets/equipment-maintenance"},
                {"title": "Predictive Maintenance Data", "url": "https://huggingface.co/datasets/maintenance"}
            ],
            "references": ["Industry benchmarks in predictive maintenance", "Maintenance data for operational efficiency"]
        },
        # Add other use cases as needed
    ]
    
    # Initialize the Proposal Agent and generate the final proposal
    agent = ProposalAgent(use_cases_with_assets)
    agent.save_proposal()