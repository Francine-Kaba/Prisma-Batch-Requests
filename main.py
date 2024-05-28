import asyncio
from datetime import datetime
from time import time
from prisma import Prisma

from prisma_connect import batch_operations, connect_to_prisma
from time_tracker import seconds_to_microseconds

prisma = Prisma()
userId = 1

######################## Client ########################


async def main():
    start = time()
    async with Prisma() as client:
        for i in range(10000):
            await client.audit_log.create(
                data={
                    'timestamp': datetime.now(),
                    'userId': i,
                    'action': str(i),
                    'details': str(i)
                }
            )

    print("Mutation Client Start 1", time()-start)


async def main_queries():
    async with Prisma() as client:
        start = time()
        await client.audit_log.find_many()

    print("Query Client Start 1", time()-start)

#################### Backend Batcher ####################


async def batcher():
    start = time()
    async with Prisma() as client:
        async with client.batch_() as batcher:
            for i in range(10000):
                batcher.audit_log.create(
                    data={
                        'timestamp': datetime.now(),
                        'userId': i,
                        'action': str(i),
                        'details': str(i)
                    }
                )

    print("Batcher Mutations Start 1", time()-start)

#################### Backend Batcher with retries ####################
async def batcher_function():
    start = time()
    if await connect_to_prisma(prisma):
        for i in range(10000):
            data = [{
                'timestamp': datetime.now(),
                'userId': i,
                'action': str(i),
                'details': str(i)
            }]
            print(type(data))
            batch_success = await batch_operations(prisma, data)    
            if batch_success:
                print("Batch create operations completed successfully.")
            else:
                print("Batch create operations failed.")  
        print("Batcher Mutations Start 1", time()-start)


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
        for i in range(10000):
            await prisma.audit_log.create(
                data={
                    'timestamp': datetime.now(),
                    'userId': i,
                    'action': str(i),
                    'details': str(i)
                }
            )
        print("Test Mutation 1", time()-start1)


async def test_queries():
    start1 = time()
    if await connect_to_prisma(prisma):
        await prisma.audit_log.find_many()
        print("Test Query 1", time()-start1)


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(main_queries())
    # asyncio.run(batcher())
    asyncio.run(batcher_function())
    # asyncio.run(batcher_queries())
    # asyncio.run(test())
    # asyncio.run(test_queries())
