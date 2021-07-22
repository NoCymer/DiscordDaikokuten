from pygelbooru import Gelbooru
import datetime
import asyncio
import async_timeout

MAX_ITERATION = 50


async def get_hentai(subject):
    start_time = datetime.datetime.now()
    deadline_time = start_time + datetime.timedelta(seconds=30)
    gelbooru = Gelbooru()
    result = "None"
    try:
        async with async_timeout.timeout(3.0):
            result = await gelbooru.random_post(tags=subject)
            if result == "":
                result = await gelbooru.random_post(tags=subject)
            print(result)
            if result is None:
                return "None"        
    except asyncio.TimeoutError:
        pass
    iteration = 1
    try:
        while result.rating == "s" and iteration <= MAX_ITERATION and datetime.datetime.now() <= deadline_time:
            iteration += 1
            last_result = result
            print(f"iteration : {iteration}")
            try:
                async with async_timeout.timeout(3.0):
                    result = await gelbooru.random_post(tags=subject)
            except asyncio.TimeoutError:
                result = last_result        
                continue
            print(result.rating)
            print(result)
            print('executed passing to next loop')
        if result.rating == "s":
            return "None"
        elif iteration >= MAX_ITERATION:
            return "None"     
    except AttributeError:
        return "None"
    return str(result)