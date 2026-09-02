from uwapi import *


class Extractor:
    is_configured: bool = False

    def __init__(self):
        uw_events.on_update(self.on_update)

    def extract(self):
        if uw_game.map_state() != MapState.Loaded:
            return

        uw_game.log_info("extracting")

        types = {}
        for proto_id, prototype in uw_prototypes._all.items():
            if prototype.type not in types:
                types[prototype.type] = {}
            types[prototype.type][proto_id] = prototype

        output = ""
        for type, mapping in types.items():
            output += f"## {type.name}\n"
            for id, prototype in sorted(mapping.items(), key=lambda x: x[1].full_name):
                output += f"{id} {prototype.full_name}\n"
            output += f"\n\n"

        with open("prototypes.md", "w") as f:
            f.write(output)

        uw_game.log_info("extraction done")

        uw_game.disconnect()

    def configure(self):
        if (
            self.is_configured
            or uw_game.game_state() != GameState.Session
            or not uw_world.is_admin()
        ):
            return
        self.is_configured = True
        uw_admin.set_map_selection("extra/arena.uwmap")

    def on_update(self, stepping: bool):
        self.configure()
        self.extract()

    def run(self):
        uw_game.connect_new_server(0, "", "--uwapi 2")


if __name__ == "__main__":
    with UwapiLibrary():
        Extractor().run()
