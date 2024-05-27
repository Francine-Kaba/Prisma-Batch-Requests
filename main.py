import asyncio
from datetime import datetime
from time import time
from prisma import Prisma

from prisma_connect import connect_to_prisma

prisma = Prisma()
userId = 1

######################## Client ########################


async def main():
    start = datetime.now()
    async with Prisma() as client:
        for i in range(10000):
            start2 = datetime.now()
            await client.audit_log.create(
                data={
                    'timestamp': datetime.now(),
                    'userId': i,
                    'action': str(i),
                    'details': str(i)
                }
            )
        start3 = datetime.now()

    print("Mutation Start 1", start)
    print("Mutation Start 2", start2)
    print("Mutation Start 3", start3)


async def main_queries():
    async with Prisma() as client:
        start = datetime.now()
        await client.audit_log.find_many()
    start2 = datetime.now()

    print("Query Start 1", start)
    print("Query Start 1", start2)

#################### Backend Batcher ####################


async def batcher():
    start = datetime.now()
    async with Prisma() as client:
        async with client.batch_() as batcher:
            for i in range(20):
                start2 = datetime.now()
                batcher.audit_log.create(
                    data={
                        'timestamp': datetime.now(),
                        'userId': i,
                        'action': str(i),
                        'details': str(i)
                    }
                )
        start3 = datetime.now()

    print("Batcher Mutations Start 1", start)
    print("Batcher Mutations Start 2", start2)
    print("Batcher Mutations Start 3", start3)


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
    start1 = datetime.now()
    if await connect_to_prisma(prisma):
        start2 = datetime.now()
        for i in range(10000):
            await prisma.audit_log.create_many(
                data={
                    'timestamp': datetime.now(),
                    'userId': i,
                    'action': str(i),
                    'details': str(i)
                }
            )
        start3 = datetime.now()
        print("Test Mutation 1", start1)
        print("Test Mutation 2", start2)
        print("Test Mutation 3", start3)


async def test_queries():
    start1 = datetime.now()
    if await connect_to_prisma(prisma):
        start2 = datetime.now()
        await prisma.audit_log.find_many()
        start3 = datetime.now()
        print("Query 1", start1)
        print("Query 2", start2)
        print("Query 3", start3)


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(main_queries())
    asyncio.run(batcher())
    # asyncio.run(batcher_queries())
    asyncio.run(test())
    # asyncio.run(test_queries())
