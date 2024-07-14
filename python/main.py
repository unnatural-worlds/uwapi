from inspect import getmembers

import uw

STEAM_PATH = "/data/games/steamapps/common/Unnatural Worlds/bin"


def tick_callback_closure(game):
    def tick_callback(stepping):
        print(game.tick())

    return tick_callback


if __name__ == '__main__':
    game = uw.Game(steam_path=STEAM_PATH)
    game.log("Hello from the example bot!")
    game.log("this is a mistake", severity=uw.Severity.Error)
    game.set_player_name("tivvit")
    game.set_player_color(255, 255, 255)
    # game.connect_lobby_id(123)
    print(game.connection_state_enum())
    print(game.map_state_enum())
    print(game.tick())
    game.set_update_callback(tick_callback_closure(game))

    # uw_path = STEAM_PATH
    #
    # os.chdir(uw_path)
    # # if os.getcwd() != uw_path:
    # #     print("we have to go deeper")
    # #     subprocess.call(["python3", os.path.realpath(__file__)], cwd=uw_path)
    #
    # ffi = FFI()
    #
    # bots = open("/home/tivvit/git/uwapi/python/bots.h", "r").read()
    # ffi.cdef(bots)
    #
    # uw = ffi.dlopen("/data/games/steamapps/common/Unnatural Worlds/bin/libunnatural-uwapi-hard.so")

    # uw.uwInitialize(uw.UW_VERSION)
    # uw.uwLog(uw.UwSeverityEnum_Info, c_str("Hello from the example bot"))
    # uw.uwSetPlayerName(c_str("tivvit"))

    # player = ffi.new("UwMyPlayer *", {})
    # print(uw.uwMyPlayer(player))
    # print(getmembers(player))
    # print(player.playerEntityId)
