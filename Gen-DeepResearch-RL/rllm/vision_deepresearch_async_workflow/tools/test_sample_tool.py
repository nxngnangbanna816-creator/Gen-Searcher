from __future__ import annotations

import asyncio

from vision_deepresearch_async_workflow.tools.sample_tool import SampleTool


async def _run() -> None:
    tool = SampleTool()

    result_plain = await tool.call(message="hello world")
    assert "word_count: 2" in result_plain
    assert "char_count: 11" in result_plain

    result_upper = await tool.call(message="hello world", uppercase=True)
    assert "message: HELLO WORLD" in result_upper


if __name__ == "__main__":
    asyncio.run(_run())
    print("sample_tool test passed")
