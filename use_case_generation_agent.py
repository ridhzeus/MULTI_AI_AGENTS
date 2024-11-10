import os
# Set these environment variables before importing transformers
os.environ["TRANSFORMERS_FRAMEWORK"] = "pt"  # Tell transformers to use PyTorch only
os.environ["USE_TORCH"] = "TRUE"
os.environ["USE_TF"] = "FALSE"

from typing import List, Dict, Any
import numpy as np
from datetime import datetime
import json
import torch
from transformers import AutoTokenizer, AutoModel, AutoConfig
import warnings
warnings.filterwarnings('ignore')  # Suppress warning messages
from sklearn.metrics.pairwise import cosine_similarity

# Document Store Class to load, save, and manage documents
class DocumentStore:
    def __init__(self, storage_path: str = "document_store.json"):
        self.storage_path = storage_path
        self.documents = self._load_documents()
        
    def _load_documents(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_documents(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.documents, f)
            
    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        doc = {
            'id': len(self.documents),
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        self.documents.append(doc)
        self.save_documents()
        return doc['id']
    
    def get_document(self, doc_id: int) -> Dict[str, Any]:
        return next((doc for doc in self.documents if doc['id'] == doc_id), None)

# Simple Embedding Class for text encoding using BERT-based model
class SimpleEmbedding:
    def __init__(self):
        config = AutoConfig.from_pretrained('bert-base-uncased', trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', config=config)
        self.model = AutoModel.from_pretrained('bert-base-uncased', config=config)
        self.model.eval()  # Set to evaluation mode
        
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def encode(self, text: str) -> np.ndarray:
        encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        normalized_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
        return normalized_embeddings.numpy()

# Vector Store to store and search document embeddings
class VectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.embeddings = []
        self.doc_ids = []
        
    def add_embedding(self, doc_id: int, text: str):
        embedding = self.embedding_model.encode(text)
        self.embeddings.append(embedding.squeeze())
        self.doc_ids.append(doc_id)
        
    def search(self, query: str, top_k: int = 3) -> List[tuple]:
        query_embedding = self.embedding_model.encode(query)
        doc_embeddings = np.array(self.embeddings)
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
        top_k_indices = similarities.argsort()[-top_k:][::-1]
        return [(self.doc_ids[idx], similarities[idx]) for idx in top_k_indices]

# RAG Agent for generating use cases based on industry and company data
class RAGAgent:
    def __init__(self, industry_data: str, company_data: str):
        self.industry_data = industry_data
        self.company_data = company_data
        
        # Initialize components
        self.document_store = DocumentStore()
        self.embedding_model = SimpleEmbedding()
        self.vector_store = VectorStore(self.embedding_model)
        
        # Initialize knowledge base
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self):
        # Add initial documents to the document store
        industry_doc_id = self.document_store.add_document(self.industry_data, {'type': 'industry_data'})
        company_doc_id = self.document_store.add_document(self.company_data, {'type': 'company_data'})
        
        # Generate embeddings for the documents
        self.vector_store.add_embedding(industry_doc_id, self.industry_data)
        self.vector_store.add_embedding(company_doc_id, self.company_data)
        
    def add_knowledge(self, content: str, metadata: Dict[str, Any] = None):
        doc_id = self.document_store.add_document(content, metadata)
        self.vector_store.add_embedding(doc_id, content)
        
    def generate_use_cases(self) -> str:
        try:
            # Retrieve relevant context for use case generation
            query = "AI/ML use cases for improving customer satisfaction and operations"
            relevant_docs = self.vector_store.search(query)
            
            # Build context from relevant documents
            context = "\n\n".join([
                self.document_store.get_document(doc_id)['content']
                for doc_id, _ in relevant_docs
            ])
            
            # Create a prompt for use case generation
            prompt = f"""Based on the following context and data, propose specific AI/ML use cases for improving customer satisfaction and operations:

Context:
{context}

Please provide detailed use cases that leverage AI/ML technologies to address specific business needs and opportunities."""
            
            # Generate use cases using a language model (Groq model assumed)
            from groq import Groq
            self.client = Groq()
            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            if hasattr(completion, 'choices') and len(completion.choices) > 0:
                use_cases = completion.choices[0].message.content
                
                # Store the generated use cases
                self.add_knowledge(use_cases, {'type': 'generated_use_cases', 'timestamp': datetime.now().isoformat()})
                
                return use_cases
            else:
                print("Error: No choices found in the response")
                return None
                
        except Exception as e:
            print(f"Error generating use cases: {str(e)}")
            return None

# Main function for running the agent
def main():
    # Example data: Industry trends and Apple's use of AI
    industry_data = """
    The technology industry is seeing rapid advancements in AI, automation, and machine learning.
    Key trends include:
    - Natural Language Processing improvements
    - Computer Vision applications
    - Predictive Analytics
    - Automated Customer Service
    """
    
    company_data = """
    Apple Inc. is using AI to enhance its products and services:
    - Siri virtual assistant
    - Photos app with object recognition
    - Predictive text and autocorrect
    - App Store recommendations
    """
    
    try:
        # Create an instance of RAGAgent with industry and company data
        agent = RAGAgent(industry_data, company_data)
        
        # Add additional knowledge (e.g., customer feedback)
        additional_knowledge = """
        Recent customer feedback indicates:
        - Users want more personalized experiences
        - Faster response times needed
        - Better product recommendations requested
        - Technical support improvements needed
        """
        agent.add_knowledge(additional_knowledge, {'type': 'customer_feedback'})
        
        # Generate use cases based on the context
        use_cases = agent.generate_use_cases()
        
        if use_cases:
            print("\nGenerated Use Cases:")
            print("-" * 50)
            print(use_cases)
        else:
            print("Failed to generate use cases.")
            
    except Exception as e:
        print(f"Error running the agent: {str(e)}")

if __name__ == "__main__":
    main()