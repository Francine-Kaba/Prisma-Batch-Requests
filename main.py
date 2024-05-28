import asyncio
from datetime import datetime
from time import time
from prisma import Prisma

from prisma_connect import connect_to_prisma
from time_tracker import seconds_to_microseconds

prisma = Prisma()
userId = 1

######################## Client ########################


async def main():
    start = time()
    async with Prisma() as client:
        for i in range(10000):
            start2 = time()
            await client.audit_log.create(
                data={
                    'timestamp': datetime.now(),
                    'userId': i,
                    'action': str(i),
                    'details': str(i)
                }
            )
        start3 = time()

    print("Mutation Client Start 1",time()-start)
    # print("Mutation Client Start 2", seconds_to_microseconds(start3-start2))
    # print("Mutation Start 3", start3)


async def main_queries():
    async with Prisma() as client:
        start = time()
        await client.audit_log.find_many()
    start2 = time()

    print("Query Client Start 1", time()-start)
    # print("Query Client Start 1", start2)

#################### Backend Batcher ####################


async def batcher():
    start = time()
    async with Prisma() as client:
        async with client.batch_() as batcher:
            for i in range(10000):
                start2 = time()
                batcher.audit_log.create(
                    data={
                        'timestamp': datetime.now(),
                        'userId': i,
                        'action': str(i),
                        'details': str(i)
                    }
                )
        start3 = datetime.now()

    print("Batcher Mutations Start 1", time()-start)
    # print("Batcher Mutations Start 2", seconds_to_microseconds(start3-start2))
    # print("Batcher Mutations Start 3", start3)


async def batcher_queries():
    async with Prisma() as client:
        async with client.batch_() as batcher:
            start = datetime.now()
            batcher.audit_log.find_many()
    start2 = datetime.now()

    print("Batcher Queries Start 1", start)
    print("Batcher Queries Start 1", start2)

######################## prisma connect ########################


async def test():
    start1 = time()
    if await connect_to_prisma(prisma):
        start2 = datetime.now()
        for i in range(10000):
            await prisma.audit_log.create(
                data={
                    'timestamp': datetime.now(),
                    'userId': i,
                    'action': str(i),
                    'details': str(i)
                }
            )
        start3 = datetime.now()
        print("Test Mutation 1", time()-start1)
        # print("Test Mutation 2", start2)
        # print("Test Mutation 3", start3)


async def test_queries():
    start1 = time()
    if await connect_to_prisma(prisma):
        start2 = datetime.now()
        await prisma.audit_log.find_many()
        start3 = datetime.now()
        print("Test Query 1", time()-start1)
        # print("Query 2", start2)
        # print("Query 3", start3)


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(main_queries())
    # asyncio.run(batcher())
    # asyncio.run(batcher_queries())
    asyncio.run(test())
    asyncio.run(test_queries())
