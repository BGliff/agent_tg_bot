import aiohttp

from agent.chains import analyze


async def get_summary_by_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return await analyze(html)
