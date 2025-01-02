import asyncio

import fastapi_poe as fp
from llm_backends.utils import IntervalTimer


class PoeService:
    def __init__(self, api_key, bot_name="Claude-3.5-Sonnet"):
        self.bot_name = bot_name
        self.api_key = api_key
        self.timer = IntervalTimer(15)

    def get_completion(self, question):
        """
        Synchronously retrieves bot responses using asyncio.run().

        Args:
            messages: A list of ProtocolMessage objects.

        Returns:
            A responses in str
        """
        messages = [fp.ProtocolMessage(role="user", content=question)]

        async def _get_response_async(api_key, messages):
            """
            Asynchronous helper function to gather responses.
            """
            responses = []
            async for partial in fp.get_bot_response(
                messages=messages, bot_name=self.bot_name, api_key=api_key
            ):
                responses.append(partial.text)
            str_resp = "".join(responses)
            return str_resp

        return asyncio.run(_get_response_async(self.api_key, messages))
