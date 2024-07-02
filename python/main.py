import os
from cffi import FFI
from inspect import getmembers

import uw

STEAM_PATH = "/data/games/steamapps/common/Unnatural Worlds/bin"


if __name__ == '__main__':
    game = uw.Game(steam_path=STEAM_PATH)
    game.log("Hello from the example bot!")
    game.set_player_name("tivvit")

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
