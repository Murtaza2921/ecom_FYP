import openai

GROQ_API_KEY = ""

def generate_query(user_prompt):
    """Converts user input into a MongoDB query using Groq API."""
    system_prompt = """
    You are an AI assistant that converts natural language queries into MongoDB queries.
    The database contains products with fields: name, description, price, stock, category, and images.
    
    If the user asks for comparisons, generate a query that retrieves all mentioned products.
    """

def generate_query(user_prompt):
    client = openai.OpenAI()  # Use OpenAI client object

    response = client.chat.completions.create(
        model="gpt-4",  # Update this to your required model (or "gpt-3.5-turbo")
        messages=[{"role": "system", "content": "Generate MongoDB query based on user request."},
                  {"role": "user", "content": user_prompt}]
    )

    return response.choices[0].message.content.strip()
    
