from langchain_openai import OpenAIEmbeddings
#from langchain_cohere import CohereEmbeddings
#import dspy


""" 
# Define a class-based signature
class GenerateAnswer(dspy.Signature):

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Chain different modules together to retrieve information from Wikipedia Abstracts 2017, then pass it as context for Chain of Thought to generate an answer
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
    
    def forward(self, question):
        context = self.retrieve(question).passages
        answer = self.generate_answer(context=context, question=question)
        return answer

 """






def vector_search(user_query, collection):
    """
    Perform a vector search in the MongoDB collection based on the user query.

    Args:
    user_query (str): The user's query string.
    collection (MongoCollection): The MongoDB collection to search.

    Returns:
    list: A list of matching documents.
    """
    model = OpenAIEmbeddings(model="text-embedding-3-large")
    #cohere_embeddings = CohereEmbeddings(model="embed-english-light-v3.0")

    # Generate embedding for the user query
    query_embedding = model.embed_query(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed."

# Define the vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "flow_embedding",
                "numCandidates": 150,  # Number of candidate matches to consider
                "limit": 4,  # Return top 4 matches
            }
        },
        {
            "$sort": {
                "updated_at": -1  # Sort by score in descending order
            }
        },
        {
        "$limit": 1  # Limit to only the last document
        },
        {
            "$project": {
                "_id": 0,  # Exclude the _id field
                "chart_flow_rate": 1,  # Include the plot field
                "transformers_off_count": 1,  # Include the title field
                "transformers_on_count": 1,  # Include the genres field
                "generators_off_count": 1,
                "generators_on_count": 1,
                "ele_off_count": 1,
                "ele_on_count": 1,
                "updated_at":1,
                "score": {"$meta": "vectorSearchScore"},  # Include the search score
            }
        },
    ]


    # Execute the search
    results = collection.aggregate(pipeline)
    return list(results)


