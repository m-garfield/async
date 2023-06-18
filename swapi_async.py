import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from models import Base, Session, SwapiPeople, engine

MAX_CHUNK_SIZE = 10


async def get_people(people_id):
    url = f"https://swapi.dev/api/people/{people_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def insert_to_db(people_json_list):
    async with Session() as session:
        for data in people_json_list:
            swapi_people = SwapiPeople(
                id=data["url"].split("/")[-2],
                birth_year=data["birth_year"],
                eye_color=data["eye_color"],
                films=", ".join([film.split("/")[-2] for film in data["films"]]),
                gender=data["gender"],
                hair_color=data["hair_color"],
                height=data["height"],
                homeworld=data["homeworld"].split("/")[-2],
                mass=data["mass"],
                name=data["name"],
                skin_color=data["skin_color"],
                species=", ".join([specie.split("/")[-2] for specie in data["species"]]),
                starships=", ".join([starship.split("/")[-2] for starship in data["starships"]]),
                vehicles=", ".join([vehicle.split("/")[-2] for vehicle in data["vehicles"]])
            )
            session.add(swapi_people)
        await session.commit()

async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    for ids_chunk in chunked(range(1, 91), MAX_CHUNK_SIZE):
        get_people_coros = [get_people(people_id) for people_id in ids_chunk]
        people_json_list = await asyncio.gather(*get_people_coros)
        asyncio.create_task(insert_to_db(people_json_list))
    current_task = asyncio.current_task()
    tasks_sets = asyncio.all_tasks()
    tasks_sets.remove(current_task)
    await asyncio.gather(*tasks_sets)
    await engine.dispose()

if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
