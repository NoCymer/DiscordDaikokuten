from pygelbooru import Gelbooru


async def get_hentai(subject):
    gelbooru = Gelbooru()
    print(subject)
    results = await gelbooru.random_post(tags=[subject])
    return str(results)
