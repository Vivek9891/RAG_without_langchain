import uuid
from datetime import datetime
from typing import Dict, List
import os
from dotenv import load_dotenv
from openai import OpenAI
from semantic import semantic_search, get_context_with_sources
from gemini import LLM

# Initialize OpenAI client
load_dotenv()
client = OpenAI(api_key = os.getenv("OPEN_API_KEY"))



class History:
    def __init__(self):
        # In-memory conversation store
        self.conversations: Dict[str, List[dict]] = {}
        self.llm = LLM()


    def create_session(self) -> str:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        self.conversations[session_id] = []
        return session_id

    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to conversation history"""
        self.conversations[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_conversation_history(self, session_id: str,max_messages:int = None):
        """Get conversation history for a session"""
        
        if session_id not in self.conversations:
            return []

        histroy = self.conversations[session_id]

        if max_messages:
            histroy = histroy[-max_messages:]

        return histroy

    def format_history_for_prompt(self,session_id: str, max_messages: int = 5):
        """Format conversation history for inclusion in prompts"""
        history = self.get_conversation_history(session_id, max_messages)
        formatted_history = ""

        for msg in history:
            role = "Human" if msg["role"] == "user" else "Assistant"
            formatted_history += f"{role}: {msg['content']}\n\n"

        return formatted_history.strip()


    def contextualize_query(self, query: str, conversation_history:str, client: OpenAI):
        """
        Convert follow-up questions into standalone queries using Gemini
        """
        contextualize_prompt = """Given a chat history and the latest user question 
    which might reference context in the chat history, formulate a standalone 
    question which can be understood without the chat history. Do NOT answer 
    the question, just reformulate it if needed and otherwise return it as is."""

        try:
            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": contextualize_prompt},
                    {"role": "user", "content": f"Chat history:\n{conversation_history}\n\nQuestion:\n{query}"}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error contextualizing query: {str(e)}")
            return query  # Fallback to original query
        
    def conversational_rag_query(self,
    collection,
    query: str,
    session_id: str,
    n_chunks: int = 3
    ):
        """Perform RAG query with conversation history"""
        # Get conversation history
        conversation_history = self.format_history_for_prompt(session_id)

        # Handle follo up questions
        query = self.contextualize_query(query, conversation_history, client)
        print("Contextualized Query:", query)

        # Get relevant chunks
        context, sources = get_context_with_sources(
            semantic_search(collection, query, n_chunks)
        )
        print("Context:", context)
        print("Sources:", sources)


        response = self.llm.generate_response(context=context,conversation_history=conversation_history,query=query)

        # Add to conversation history
        self.add_message(session_id, "user", query)
        self.add_message(session_id, "assistant", response)

        return response, sources
            
