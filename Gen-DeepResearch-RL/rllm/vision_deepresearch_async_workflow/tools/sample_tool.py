from __future__ import annotations

from vision_deepresearch_async_workflow.tools.shared import DeepResearchTool


class SampleTool(DeepResearchTool):
    """Simple example tool for local testing and integration checks."""

    def __init__(self):
        super().__init__(
            name="sample_tool",
            description="Echoes a short message and returns basic text stats for smoke testing.",
            parameters={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "ข้อความที่ต้องการให้เครื่องมือประมวลผล",
                    },
                    "uppercase": {
                        "type": "boolean",
                        "description": "หากเป็น true จะคืนค่าเป็นตัวพิมพ์ใหญ่",
                        "default": False,
                    },
                },
                "required": ["message"],
            },
        )

    async def call(self, message: str, uppercase: bool = False) -> str:
        text = message.upper() if uppercase else message
        words = len([token for token in text.strip().split() if token])
        chars = len(text)
        return (
            "[sample_tool]\n"
            f"message: {text}\n"
            f"word_count: {words}\n"
            f"char_count: {chars}"
        )
