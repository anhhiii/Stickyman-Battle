import pygame
import os
import json
import xml.etree.ElementTree as ET

class BattleBase:
    def __init__(self, screen, level_name):
        self.screen = screen
        self.running = True
        self.level_name = level_name

        self.tile_size = 16  # mỗi ô vuông là 16x16
        self.tile_layers = []
        self.object_layers = []

        self.load_level(level_name)
        self.load_tiles()

    def load_level(self, level_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        path = os.path.join(project_root, "levels", f"{level_name}.tmj")

        with open(path, "r") as f:
            data = json.load(f)

        self.tile_width = data.get('tilewidth', 16)
        self.tile_height = data.get('tileheight', 16)
        self.map_width = data['width']
        self.map_height = data['height']
        self.tilesets_info = data['tilesets']

        for layer in data['layers']:
            if layer['type'] == 'tilelayer':
                self.tile_layers.append(layer['data'])
            elif layer['type'] == 'objectgroup':
                self.object_layers.append(layer['objects'])

    def load_tiles(self):
        self.tiles = {}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        for tileset in self.tilesets_info:
            firstgid = tileset['firstgid']
            tsx_path = os.path.join(project_root, tileset['source'].replace("../", ""))

            tree = ET.parse(tsx_path)
            root = tree.getroot()

            image_elem = root.find('image')
            img_source = image_elem.get('source')

            if img_source.startswith("assets/"):
                img_full_path = os.path.join(project_root, img_source)
            else:
                img_full_path = os.path.join(os.path.dirname(tsx_path), img_source)

            img_full_path = os.path.normpath(img_full_path)

            if not os.path.isfile(img_full_path):
                raise FileNotFoundError(f"Không tìm thấy ảnh tileset: {img_full_path}")

            img_width = int(image_elem.get('width'))
            img_height = int(image_elem.get('height'))

            tilewidth = int(root.get('tilewidth'))
            tileheight = int(root.get('tileheight'))

            image = pygame.image.load(img_full_path).convert_alpha()

            tiles_x = img_width // tilewidth
            tiles_y = img_height // tileheight

            id_offset = 0
            for y in range(tiles_y):
                for x in range(tiles_x):
                    tile = pygame.Surface((tilewidth, tileheight), pygame.SRCALPHA)
                    tile.blit(image, (0, 0), (x * tilewidth, y * tileheight, tilewidth, tileheight))
                    self.tiles[firstgid + id_offset] = tile
                    id_offset += 1


    def draw(self):
        for layer in self.tile_layers:
            for idx, tile in enumerate(layer):
                tile = int(tile)
                if tile > 0:
                    col_idx = idx % self.map_width
                    row_idx = idx // self.map_width
                    img = self.tiles.get(tile)
                    if img:
                        self.screen.blit(img, (col_idx * self.tile_width, row_idx * self.tile_height))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"

            self.draw()
            pygame.display.flip()
            clock.tick(60)
