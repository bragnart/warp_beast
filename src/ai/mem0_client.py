# src/ai/mem0_client.py
from __future__ import annotations
import os
from mem0 import MemoryClient
from dotenv import load_dotenv


class Mem0aiClient:

    def __init__(self, project_id: str, user_id: str, agent_id: str, run_id: str):
        self.project_id = project_id
        self.user_id = user_id
        self.agent_id = agent_id
        self.run_id = run_id
        load_dotenv()
        api_key = os.environ.get("MEM0_API_KEY")
        self.client = MemoryClient(
            api_key=api_key,
            #project_id=self.project_id
        )

    def add_messages(self, user_msg: str, agent_msg: str, infer: bool = True):
        self.client.add(
            messages=[
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": agent_msg}
            ],
            infer = infer,
            user_id = self.user_id,
            agent_id = self.agent_id,
            run_id = self.run_id
        )

    def search_memories(self, query: str, limit: int = 5):
        raw_results = self.client.search(
            query=query,
            user_id=self.user_id,
            top_k=limit,
            filters={"agent_id": self.agent_id},
            threshold=0.4
        )
        return raw_results["results"]