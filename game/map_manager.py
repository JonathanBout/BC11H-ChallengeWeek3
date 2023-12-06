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
                parsed_map = self.__parse_map(reader.read())
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
        lines = map_config.splitlines()
        lines = [line for line in [
            line.split("#")[0].strip()
            for line in lines
            if not line.strip().startswith("#")
        ] if len(line) > 0]

        map_name = lines[0]
        map_description = lines[1]
        map_background_file = lines[2]
        map_music_file = lines[3]
        map_render_scale = self.__scale_from_str(lines[4])
        map_collider_scale = self.__scale_from_str(lines[5])
        map_starting_points = self.__coords_from_str(lines[6])
        map_waypoints = self.__coords_from_str(" ".join(lines[7:]))

        return MapConfig(
            map_name,
            map_description,
            map_starting_points,
            map_waypoints,
            map_background_file,
            map_music_file,
            map_render_scale,
            map_collider_scale,
        )

    def __scale_from_str(self, scale_str: str):
        x, y = scale_str.lower().split("x")
        return float(x.strip()), float(y.strip())

    def __coords_from_str(self, points_str: str):
        points: list[tuple[int, int]] = []
        points_list_str = points_str.split(" ")
        for waypoint in points_list_str:
            if matches := self.waypoint_regex.match(waypoint):
                points.append((int(matches.group(1)), int(matches.group(2))))
            else:
                print("Invalid waypoint:", waypoint)
        return points


class MapConfig:
    def __init__(
        self,
        name: str,
        description: str,
        starting_points: list[tuple[int, int]],
        waypoints: list[tuple[int, int]],
        background_image: str,
        music_file: str,
        render_scale: tuple[float, float],
        collider_scale: tuple[float, float],
    ):
        self.name = name
        self.description = description
        self.starting_points = starting_points
        self.waypoints = waypoints
        self.background_image = background_image
        self.music_file = music_file
        self.render_scale = render_scale
        self.collider_scale = collider_scale
