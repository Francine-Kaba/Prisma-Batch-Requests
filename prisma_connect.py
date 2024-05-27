import asyncio
from prisma import Prisma

MAX_RETRIES = 2
RETRY_DELAY = 3


async def connect_to_prisma(prisma: Prisma) -> bool:
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            if prisma.is_connected():
                await prisma.disconnect()
            await prisma.connect()
            return True
        except Exception:
            retry_count += 1
            await asyncio.sleep(RETRY_DELAY)
    return False
