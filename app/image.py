from PIL import Image

import app.DataBase.requests as rq

import json

filename_icon1 = 'app/static/textures/icons/icon_1.png'
filename_icon2 = 'app/static/textures/icons/icon_2.png'
filename_map = 'app/static/textures/maps/map_sea_kingdom.png'

with open("app/static/positions.json", "r", encoding="utf8") as pos:
    positions = json.load(pos)

async def generate_game_field(map_id, _key):

    scores, icons = await rq.get_icons_scores(_key)

    with Image.open(filename_icon1) as icon1:
        icon1.load()

    with Image.open(filename_icon2) as icon2:
        icon2.load()

    if map_id == 1:

        with Image.open(filename_map) as map:
            map.load()
            
        for i in range(0, len(scores)):
            if icons[i] == 0:
                position = positions["medieval"]["small"][f"{scores[i]}"].split(', ')
                map.paste(
                    icon1.resize((95, 95)), (int(position[0]), int(position[1])), mask=icon1.resize((95, 95))
                )
            if icons[i] == 1:
                position = positions["medieval"]["small"][f"{scores[i]}"].split(', ')
                map.paste(
                    icon2.resize((95, 95)), (int(position[0]), int(position[1])), mask=icon1.resize((95, 95))
                )
        
        map = map.resize((int(map.width / 1.7), int(map.height / 1.7)))

        map.save(f"app/temp/gf_{_key}.png")
        return f"app/temp/gf_{_key}.png"