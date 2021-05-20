from pygelbooru import Gelbooru
import datetime

max_iteration = 50


async def get_hentai(subject):
    start_time = datetime.datetime.now()
    deadline_time = start_time + datetime.timedelta(seconds=60)
    gelbooru = Gelbooru()
    result = await gelbooru.random_post(tags=subject)
    iteration = 1
    while result.rating == "s" and iteration <= max_iteration and datetime.datetime.now() <= deadline_time:
        iteration += 1
        result = await gelbooru.random_post(tags=[subject])
    if iteration >= 10:
        return "No NSFW image have been found"
    return str(result)

