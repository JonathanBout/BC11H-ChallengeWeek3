from game import config
from os import listdir
import re


class MapManager:
    def __init__(self) -> None:
        self.map_regex = re.compile(r"^map-.*\.txt$")
        self.waypoint_regex = re.compile(r"<\s*(\d+)\s*,\s*(\d+)\s*>")
        self.load_maps()

    def load_maps(self):
        self.loaded_maps: list[MapConfig] = []
        for file in listdir(config.MAP_DIRECTORY):
            if not self.map_regex.match(file):
                continue

            with open(config.MAP_DIRECTORY + "/" + file, "r") as reader:
                parsed_map = self.__parse_map(
                    reader.read().replace("\r\n", "\n").replace("\r", "\n")
                )
                self.loaded_maps.append(parsed_map)

    def __parse_map(self, map_config: str):
        """
        Parses a map from a string. Structure should be as follows:\n
        [map name]\n
        [map description]\n
        [map background file]\n
        [map music file]\n
        [render scale X x render scale Y]\n
        [collider scale X x collider scale Y]\n
        [<waypoint 1 X, waypoint 1 Y> <waypoint 2 X, waypoint 2 Y> ...]
        """
        lines = map_config.split("\n")
        map_name = lines[0].strip()
        map_description = lines[1].strip()
        map_background_file = lines[2].strip()
        map_music_file = lines[3].strip()
        map_render_scale = self.__scale_from_str(lines[4])
        map_collider_scale = self.__scale_from_str(lines[5])

        map_waypoints_str = " ".join(lines[6:]).split(" ")
        map_waypoints: list[tuple[int, int]] = []
        for waypoint in map_waypoints_str:
            if matches := self.waypoint_regex.match(waypoint):
                map_waypoints.append((int(matches.group(1)), int(matches.group(2))))
            else:
                print("Invalid waypoint:", waypoint)

        return MapConfig(
            map_name,
            map_description,
            map_waypoints,
            map_background_file,
            map_music_file,
            map_render_scale,
            map_collider_scale,
        )

    def __scale_from_str(self, scale_str: str):
        x, y = scale_str.lower().split("x")
        return float(x.strip()), float(y.strip())


class MapConfig:
    def __init__(
        self,
        name: str,
        description: str,
        waypoints: list[tuple[int, int]],
        background_image: str,
        music_file: str,
        render_scale: tuple[float, float],
        collider_scale: tuple[float, float],
    ):
        self.name = name
        self.description = description
        self.waypoints = waypoints
        self.background_image = background_image
        self.music_file = music_file
        self.render_scale = render_scale
        self.collider_scale = collider_scale
