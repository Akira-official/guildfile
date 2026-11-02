"""
src/agent/ai_client.py
High-speed LLM inference engine supporting Groq and OpenAI models with multimodal vision.
"""

import os
import difflib
from openai import OpenAI
from typing import List, Dict, Any, Optional
from ..utils.logger import setup_logger

logger = setup_logger("HelixCore.AIClient")


class AIClient:
    """Handles text generation and multimodal vision requests with deduplication guards."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = "https://api.groq.com/openai/v1" if os.getenv("GROQ_API_KEY") else None

        if not self.api_key:
            logger.warning("[!] No GROQ_API_KEY or OPENAI_API_KEY found in environment.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key, base_url=base_url)

        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        self.vision_model = os.getenv("GROQ_VISION_MODEL", "qwen-2.5-32b")

    def generate_chat_reply(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.85
    ) -> Optional[str]:
        """Generates a contextual response and deduplicates against recent turns."""
        if not self.client:
            return "bro configure the GROQ_API_KEY first 💀"

        payload = [{"role": "system", "content": system_prompt}]
        for m in messages[-8:]:
            payload.append(m)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=payload,
                temperature=temperature,
                max_tokens=150,
                presence_penalty=0.6,
                frequency_penalty=0.8
            )
            raw = response.choices[0].message.content.strip()
            return self.clean_reply(raw, messages)
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return None

    def clean_reply(self, reply: str, history: List[Dict[str, str]]) -> str:
        """Strips quotes and deduplicates response against recent history."""
        cleaned = reply.strip('"\'')
        # Check similarity against the last assistant message
        recent_bot_replies = [m["content"] for m in history if m["role"] == "assistant"]
        if recent_bot_replies:
            last = recent_bot_replies[-1]
            similarity = difflib.SequenceMatcher(None, cleaned.lower(), last.lower()).ratio()
            if similarity > 0.65:
                logger.info(f"Deduplicator triggered (similarity {similarity:.2f}). Modifying reply.")
                cleaned = f"wait, {cleaned}"
        return cleaned

    def analyze_image_and_roast(self, image_url: str, caption: str = "") -> Optional[str]:
        """Analyzes an attached image or meme using multimodal vision."""
        if not self.client:
            return None

        prompt = (
            "You are Helix on Discord. A friend just uploaded this image. "
            "Inspect what's in the image and roast it or react with hilarious Discord slang (under 15 words)."
        )
        if caption:
            prompt += f" They captioned it: '{caption}'"

        try:
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                max_tokens=80,
                temperature=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Vision analysis failed: {e}")
            return "who told you to upload this blurfest 💀"

