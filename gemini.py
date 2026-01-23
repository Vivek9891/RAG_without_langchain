import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))

class LLM:

    def get_prompt(self,context: str, conversation_history:str,query: str):
        """Generate a prompt combining context, history, and query"""
        prompt = f"""
            You are a helpful AI assistant.

            Use the provided document context to answer the user's question.

            Rules:
            - The question may contain spelling mistakes or grammatical errors.
            - Try to understand the user's intent, not just exact words.
            - If the answer is mostly present in the context (about 70–80% relevance),
            answer using the available information.
            - You may rephrase or infer missing details if they logically follow
            from the context.
            - Do NOT add outside knowledge.
            - If the question is clearly unrelated to the context, respond with:
            "I don't know. This question is outside the provided context."

            Context from documents:
            ----------------------
            {context}

            Conversation history:
            ---------------------
            {conversation_history}

            User question:
            --------------
            {query}

            Answer clearly and concisely:
        """

        return prompt


    def generate_response(self,
        context: str,
        conversation_history:str,
        query: str
    ):
        """Generate a response using Gemini with conversation history"""

        # Build prompt (same logic as before)
        prompt = self.get_prompt(context,conversation_history, query)

        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # or gpt-3.5-turbo for lower cost
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,  # Lower temperature for more focused responses
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
        
    

        
    
