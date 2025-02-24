from PIL import Image

def generate_game_field(map_id, queue, scores, icons):

    filename_icon1 = 'app/static/textures/icons/icon_1.png'
    filename_icon2 = 'app/static/textures/icons/icon_2.png'

    with Image.open(filename_icon1) as icon1:
        icon1.load()

    with Image.open(filename_icon2) as icon2:
        icon2.load()

    if map_id == 1:

        filename_map = 'app/static/textures/maps/map_sea_kingdom.png'

        with Image.open(filename_map) as map:
            map.load()
            
        map.paste(
            icon1.resize((95, 95)), (1563, 1710), mask=icon1.resize((95, 95))
        )
        #map.paste(
        #    icon2, (1570, 1720)
        #)
        map.show()

generate_game_field(1, None, None, None)