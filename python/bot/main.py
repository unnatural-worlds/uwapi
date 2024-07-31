import uw

STEAM_PATH = "/data/games/steamapps/common/Unnatural Worlds/bin"


class Bot:
    def __init__(self, game):
        self.game = game
        self.step = 0

        # register update callback
        self.game.add_update_callback(self.tick_callback_closure())

    def start(self):
        print("starting")
        if not self.game.try_reconnect():
            self.game.set_start_gui(True)
            if not self.game.set_connect_find_lan():
                self.game.connect_new_server()
        print("done")

    def attack_nearest_enemies(self):
        pass
        # var ownUnits = World.Entities().Values.Where(x => Entity.Own(x) && Entity.Has(x, "Unit") && Prototypes.Unit(x.Proto.proto)?.dps > 0);
        #             if (ownUnits.Count() == 0)
        #                 return;
        #
        #             var enemyUnits = World.Entities().Values.Where(x => Entity.Policy(x) == PolicyEnum.Enemy && Entity.Has(x, "Unit"));
        #             if (enemyUnits.Count() == 0)
        #                 return;
        #
        #             foreach (dynamic own in ownUnits)
        #             {
        #                 uint id = own.Id;
        #                 uint pos = own.Position.position;
        #                 if (Commands.Orders(id).Length == 0)
        #                 {
        #                     dynamic enemy = enemyUnits.OrderByDescending(x => Map.DistanceEstimate(pos, x.Position.position)).First();
        #                     Commands.Order(id, Commands.FightToEntity(enemy.Id));
        #                 }
        #             }

    def assign_random_recipes(self):
        pass

    #             foreach (dynamic own in World.Entities().Values.Where(x => Entity.Own(x) && Entity.Has(x, "Unit")))
    #             {
    #                 List<uint> recipes = Prototypes.Unit((uint)own.Proto.proto).recipes;
    #                 if (recipes?.Count > 0)
    #                 {
    #                     var recipe = recipes[random.Next(recipes.Count)];
    #                     Commands.CommandSetRecipe((uint)own.Id, recipe);
    #                 }
    #             }

    def tick_callback_closure(self):
        def tick_callback(stepping):
            if not stepping:
                return
            self.step += 1
            print(self.game.tick())
            print(self.step)
            if self.step % 10 == 1:
                self.attack_nearest_enemies()

            if self.step % 10 == 5:
                self.assign_random_recipes()

        return tick_callback


if __name__ == '__main__':
    game = uw.Game(steam_path=STEAM_PATH)
    game.log("Hello from the example bot!")
    game.log("this is a mistake", severity=uw.Severity.Error)
    game.set_player_name("tivvit")
    game.set_player_color(1, 1, 1)
    # game.connect_lobby_id(123)
    print(game.connection_state_enum())
    print(game.map_state_enum())
    print(game.tick())

    bot = Bot(game)
    bot.start()

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
