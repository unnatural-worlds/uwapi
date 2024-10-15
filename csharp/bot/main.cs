using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.IO;

namespace Unnatural
{
    internal class Bot
    {
        readonly Random random = new Random();
        uint step = 0; // save some cpu cycles by splitting work over multiple steps

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
                    Entity enemy = enemyUnits.OrderByDescending(x => Map.DistanceEstimate(own.Pos, x.Pos)).First();
                    Commands.Order(own.Id, Commands.FightToEntity(enemy.Id));
                }
            }
        }

        void AssignRandomRecipes()
        {
            foreach (Entity own in World.Entities().Values.Where(x => x.Own && x.Unit.HasValue))
            {
                List<uint> recipes = own.ProtoUnit.recipes;
                if (recipes?.Count > 0)
                {
                    var recipe = recipes[random.Next(recipes.Count)];
                    Commands.SetRecipe(own.Id, recipe);
                }
            }
        }

        void Updating(object sender, bool stepping)
        {
            if (!stepping)
                return;
            switch (step++ % 10) // save some cpu cycles by splitting work over multiple steps
            {
                case 1:
                    AttackNearestEnemies();
                    break;
                case 5:
                    AssignRandomRecipes();
                    break;
            }
        }

        void Start()
        {
            Game.LogInfo("bot-cs start");
            Game.SetPlayerName("bot-cs");
            if (!Game.TryReconnect())
            {
                Game.SetConnectStartGui(true);
                string lobby = Environment.GetEnvironmentVariable("UNNATURAL_CONNECT_LOBBY");
                string addr = Environment.GetEnvironmentVariable("UNNATURAL_CONNECT_ADDR");
                string port = Environment.GetEnvironmentVariable("UNNATURAL_CONNECT_PORT");
                if (lobby != null)
                    Game.ConnectLobbyId(ulong.Parse(lobby));
                else if (addr != null && port != null)
                    Game.ConnectDirect(addr, ushort.Parse(port));
                else
                    Game.ConnectNewServer();
            }
            Game.LogInfo("bot-cs done");
        }

        Bot()
        {
            Game.Updating += Updating;
        }

        static int Main(string[] args)
        {
            string root = Environment.GetEnvironmentVariable("UNNATURAL_ROOT");
            if (root == null)
            {
                string cwd = Directory.GetCurrentDirectory();
                if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows) && Directory.GetFiles(cwd, Interop.LibName + ".dll").Length > 0)
                    root = cwd;
                else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux) && Directory.GetFiles(cwd, "lib" + Interop.LibName + ".so").Length > 0)
                    root = cwd;
            }
            if (root == null)
            {
                if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                    root = "C:/Program Files (x86)/Steam/steamapps/common/Unnatural Worlds/bin";
                else
                    root = Environment.GetEnvironmentVariable("HOME") + "/.steam/steam/steamapps/common/Unnatural Worlds/bin";
            }
            Console.WriteLine("looking for uw library in: " + root);
            Directory.SetCurrentDirectory(root);

            Bot bot = new Bot();
            bot.Start();
            return 0;
        }
    }
}
