import os
from chat.persona import SYSTEM_PROMPT
from groq import AsyncGroq
from message.model import MessageTab

class ChatAgent:

    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        self.client = AsyncGroq(api_key=api_key) if api_key else None

    async def get_response(self, user_message: str, history: list[MessageTab] | None = None) -> str:
        if not self.client:
            return "The professor requires proper credentials to operate. Please configure GROQ_API_KEY."
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in history or []:
            role = "user" if msg.role.upper() == "USER" else "assistant"
            messages.append({
                "role": role,
                "content": msg.content,
            })

        messages.append({"role": "user", "content": user_message})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""

agent = ChatAgent()

async def get_response(user_message: str, history: list[MessageTab] | None = None) -> str:
    return await agent.get_response(user_message, history)