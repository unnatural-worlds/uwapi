using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace Unnatural
{
    internal class Bot
    {
        readonly Random random = new Random();
        bool isConfigured = false;
        uint workStep = 0; // save some cpu cycles by splitting work over multiple steps

        void AttackNearestEnemies()
        {
            var ownUnits = World.Entities().Values.Where(x => x.Own && x.ProtoUnit?.dps > 0);
            if (ownUnits.Count() == 0)
                return;
            var enemyUnits = World.Entities().Values.Where(x => x.Enemy && x.Unit.HasValue);
            if (enemyUnits.Count() == 0)
                return;
            foreach (Entity own in ownUnits)
            {
                if (Commands.Orders(own.Id).Length == 0)
                {
                    Entity enemy = enemyUnits.OrderBy(x => Map.DistanceEstimate(own.Pos, x.Pos)).First();
                    Commands.Order(own.Id, Commands.FightToEntity(enemy.Id));
                }
            }
        }

        void AssignRandomRecipes()
        {
            foreach (Entity own in World.Entities().Values.Where(x => x.Own && x.Unit.HasValue))
            {
                if (own.Recipe.HasValue)
                    continue;
                List<uint> recipes = own.ProtoUnit.recipes;
                if (recipes?.Count > 0)
                {
                    var recipe = recipes[random.Next(recipes.Count)];
                    Commands.SetRecipe(own.Id, recipe);
                }
            }
        }

        void Configure()
        {
            // auto start the game if available
            if (isConfigured && Game.GameState() == Interop.UwGameStateEnum.Session && World.IsAdmin())
            {
                Thread.Sleep(3000); // give the observer enough time to connect
                Admin.StartGame();
                return;
            }
            // is configuring possible?
            if (isConfigured || Game.GameState() != Interop.UwGameStateEnum.Session || World.MyPlayerId() == 0)
                return;
            isConfigured = true;
            Game.LogInfo("configuration start");
            Game.SetPlayerName("bot-cs");
            Game.PlayerJoinForce(0); // create new force
            Game.SetForceColor(1f, 0f, 0f);
            // Game.SetForceRace(RACE_ID); // todo
            if (World.IsAdmin())
            {
                // Admin.SetMapSelection("planets/tetrahedron.uwmap");
                Admin.SetMapSelection("special/risk.uwmap");
                Admin.AddAi();
                Admin.SetAutomaticSuggestedCameraFocus(true);
            }
            Game.LogInfo("configuration done");
        }

        void Updating(object sender, bool stepping)
        {
            Configure();
            if (!stepping)
                return;
            switch (workStep++ % 10) // save some cpu cycles by splitting work over multiple steps
            {
                case 1:
                    AttackNearestEnemies();
                    break;
                case 5:
                    AssignRandomRecipes();
                    break;
            }
        }

        void Run()
        {
            Game.LogInfo("bot-cs start");
            if (!Game.TryReconnect())
            {
                Game.SetConnectStartGui(true, "--observer 2");
                if (!Game.ConnectEnvironment())
                {
                    // automatically select map and start the game from here in the code
                    if (false)
                        Game.ConnectNewServer(0, "", "--allowUwApiAdmin 1");
                    else
                        Game.ConnectNewServer();
                }
            }
            Game.LogInfo("bot-cs done");
        }

        Bot()
        {
            Events.Updating += Updating;
        }

        static int Main(string[] args)
        {
            LibraryHelpers.SetCurrentDirectory();
            Bot bot = new Bot();
            bot.Run();
            return 0;
        }
    }
}
