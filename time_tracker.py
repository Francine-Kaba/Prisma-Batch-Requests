import asyncio
from datetime import datetime
from time import time
from prisma import Prisma

from prisma_connect import connect_to_prisma

prisma = Prisma()

################################# Time Tracker and timesheet separated ################################


async def test_time_tracker():
    start1 = time()
    if await connect_to_prisma(prisma):
        start2 = time()
        await prisma.time_tracker.find_many(
            include={
                    'teamsheet': True
                    }
        )
        start3 = time()
        count = await prisma.time_tracker.count()
        print("Time Tracker Query 1:", seconds_to_microseconds(start2 - start1), "seconds")
        print("Time Tracker Query 2:", seconds_to_microseconds(start3 - start2), "seconds")
        # print("Time Tracker Query 3", start3)
        print("Time Tracker Count", count)



################################ Merged time tracker and timesheet ################################


async def test_time_log():
    start1 = time()
    if await connect_to_prisma(prisma):
        start2 = time()
        await prisma.time_logs.find_many()
        start3 = time()
        count = await prisma.time_logs.count()
        print("Time Log Query 1:", seconds_to_microseconds(start2 - start1), "seconds")
        print("Time Log Query 2:", seconds_to_microseconds(start3 - start2), "seconds")
        # print("Time Log Query 3", start3)
        print("Time Log Count", count)


def seconds_to_microseconds(seconds):
    return seconds * 1_000_000



if __name__ == '__main__':
    asyncio.run(test_time_log())
    asyncio.run(test_time_tracker())