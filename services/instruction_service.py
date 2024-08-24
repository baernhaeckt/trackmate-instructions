from typing import AsyncIterable

from openai import OpenAI, ChatCompletion

import config
from models.input_model import InputModel


class InstructionService:
    def __init__(self):
        self.client = OpenAI(
            api_key=config.settings.OPENAI_API_KEY
        )

    def _execute_chat_completion(self, start: InputModel, end: InputModel, stream: bool) -> ChatCompletion:
        prompt = (f"this ist the startpoint\n latitude: {start.latitude}, longitude: {start.longitude}, altitude: {start.altitude}\n\n"
                  f"this is the endpoint\n latitude: {end.latitude}, longitude: {end.longitude}, altitude: {end.altitude}")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an expert assistant for blind people who can use lat and long coordinates to"
                                    "instruct a blind person in which direction to walk. Use right, left and straight instead"
                                    "of the cardinal points. Indicate how many meters and steps there are. The instructions"
                                    "must be helpful and detailed for blind people, don't use any lat and long values in the output."
                                    "Always answer in German."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            },
            stream=stream
        )

        return response

    def generate_text(self, start: InputModel, end: InputModel) -> AsyncIterable[str]:
        openai_response = self._execute_chat_completion(start, end, True)
        for chunk in openai_response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def generate_audio(self, start: InputModel, end: InputModel) -> AsyncIterable[bytes]:
        openai_response = self._execute_chat_completion(start, end, False)

        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=openai_response.choices[0].message.content,
        ) as response:
            if response.status_code == 200:
                for chunk in response.iter_bytes(chunk_size=2048):
                    yield chunk
