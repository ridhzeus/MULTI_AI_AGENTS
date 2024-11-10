import requests

class ResourceAssetAgent:
    def __init__(self, use_cases: list):
        """
        Initializes the agent with the proposed use cases.
        
        Args:
            use_cases (list): List of proposed use cases for which datasets are needed.
        """
        self.use_cases = use_cases

    def search_datasets(self):
        """
        Searches for relevant datasets for each use case on GitHub only.
        
        Returns:
            list: A list of dictionaries containing datasets for each use case.
        """
        datasets = []
        for use_case in self.use_cases:
            case_datasets = {
                "use_case": use_case,
                "datasets": self.search_github(use_case)
            }
            datasets.append(case_datasets)
        
        return datasets

    def search_github(self, use_case: str):
        """
        Searches for repositories or datasets on GitHub using a keyword based on the use case.
        
        Args:
            use_case (str): The use case to search for.
        
        Returns:
            list: List of datasets from GitHub.
        """
        github_api_url = f"https://api.github.com/search/repositories?q={use_case}+dataset"
        response = requests.get(github_api_url)
        
        if response.status_code == 200:
            data = response.json()
            return [
                {"title": repo["name"], "url": repo["html_url"]}
                for repo in data.get("items", [])
            ]
        else:
            print(f"Error: Failed to fetch GitHub data for {use_case}, Status Code: {response.status_code}")
            return []

    def run(self):
        """
        Runs the agent, searches for datasets based on the use cases, and saves the results to a markdown file.
        
        Returns:
            list: The datasets found for each use case.
        """
        datasets = self.search_datasets()
        
        # Save the results to a markdown file
        with open("assets.md", "w") as file:
            for entry in datasets:
                file.write(f"## {entry['use_case']}\n")
                if entry["datasets"]:
                    for dataset in entry["datasets"]:
                        file.write(f"- [{dataset['title']}]({dataset['url']})\n")
                else:
                    file.write("- No datasets found\n")
        
        return datasets

if __name__ == "__main__":
    # Example use cases based on your industry research
    use_cases = [
        "automated customer support",
        "predictive maintenance",
        "fraud detection",
        "sentiment analysis",
        "supply chain optimization"
    ]
    
    agent = ResourceAssetAgent(use_cases)
    datasets = agent.run()

    # Optionally, print the datasets found
    for dataset in datasets:
        print(f"\nUse Case: {dataset['use_case']}")
        for ds in dataset['datasets']:
            print(f"- {ds['title']}: {ds['url']}")