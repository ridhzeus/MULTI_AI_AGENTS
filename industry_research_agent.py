import requests
import json

class IndustryResearchAgent:
    def __init__(self, company_name, industry_name, api_key):
        self.company_name = company_name
        self.industry_name = industry_name
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"

    def fetch_industry_data(self):
        # Searching for industry trends related to AI
        query = f"{self.industry_name} AI trends"
        return self.perform_search(query)

    def fetch_company_data(self):
        # Searching for company's AI initiatives
        query = f"{self.company_name} AI initiatives"
        return self.perform_search(query)

    def fetch_market_size(self):
        # Fetching information about the market size and growth forecast
        query = f"{self.industry_name} market size and growth forecast"
        return self.perform_search(query)

    def fetch_competitive_landscape(self):
        # Fetching details about the competitive landscape in the industry
        query = f"{self.industry_name} competitive landscape"
        return self.perform_search(query)

    def fetch_technology_trends(self):
        # Fetching the latest technology trends in the industry
        query = f"{self.industry_name} latest technology trends"
        return self.perform_search(query)

    def fetch_financial_performance(self):
        # Fetching recent financial performance data of the company
        query = f"{self.company_name} financial performance"
        return self.perform_search(query)

    def fetch_customer_sentiment(self):
        # Fetching customer reviews and sentiments about the company
        query = f"{self.company_name} customer reviews and sentiment"
        return self.perform_search(query)

    def fetch_regulatory_updates(self):
        # Fetching regulatory changes relevant to the industry
        query = f"{self.industry_name} regulatory changes"
        return self.perform_search(query)

    def fetch_esg_initiatives(self):
        # Fetching the company's environmental, social, and governance initiatives
        query = f"{self.company_name} ESG initiatives"
        return self.perform_search(query)

    def perform_search(self, query):
        # Prepare the payload and headers
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            # Make the POST request to the Serper API
            response = requests.post(self.base_url, headers=headers, data=payload)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()  # Parse the JSON response
            return data  # Return the JSON data
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")  # Handle HTTP errors
            return None
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle other exceptions
            return None

    def run(self):
        # Collecting data from all fetch functions
        industry_data = self.fetch_industry_data()
        company_data = self.fetch_company_data()
        market_size = self.fetch_market_size()
        competitive_landscape = self.fetch_competitive_landscape()
        technology_trends = self.fetch_technology_trends()
        financial_performance = self.fetch_financial_performance()
        customer_sentiment = self.fetch_customer_sentiment()
        regulatory_updates = self.fetch_regulatory_updates()
        esg_initiatives = self.fetch_esg_initiatives()
        
        # Return a combined result
        return {
            "industry_data": industry_data,
            "company_data": company_data,
            "market_size": market_size,
            "competitive_landscape": competitive_landscape,
            "technology_trends": technology_trends,
            "financial_performance": financial_performance,
            "customer_sentiment": customer_sentiment,
            "regulatory_updates": regulatory_updates,
            "esg_initiatives": esg_initiatives
        }

# Example usage
if __name__ == "__main__":
    # Replace with your actual API key
    api_key = 'f1f9fcf2086065048536fb6d26b9b797051e9a46'
    
    # Create an instance of the IndustryResearchAgent
    agent = IndustryResearchAgent(company_name="Apple Inc", industry_name="Technology", api_key=api_key)
    
    # Run the agent and print the results
    results = agent.run()
    print(json.dumps(results, indent=2))  # Pretty-print the combined results