import os
from chat.persona import SYSTEM_PROMPT
from groq import AsyncGroq

class ChatAgent:

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        self.client = AsyncGroq(api_key=api_key) if api_key else None

    async def get_response(self, user_message: str) -> str:
        if not self.client:
            return "The professor requires proper credentials to operate. Please configure GROQ_API_KEY."
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""

agent = ChatAgent()

async def get_response(user_message: str) -> str:
    return await agent.get_response(user_message)