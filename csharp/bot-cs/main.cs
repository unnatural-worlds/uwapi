using System;
using System.Collections.Generic;
using System.Linq;

namespace Unnatural
{
    using PolicyEnum = Interop.UwForeignPolicyEnum;

    internal class Bot
    {
        readonly Random random = new Random();
        uint step = 0;

        void AttackNearestEnemies()
        {
            var ownUnits = World.Entities().Values.Where(x => Entity.Own(x) && Entity.Has(x, "Unit") && Prototypes.Unit(x.Proto.proto)?.dps > 0);
            if (ownUnits.Count() == 0)
                return;

            var enemyUnits = World.Entities().Values.Where(x => Entity.Policy(x) == PolicyEnum.Enemy && Entity.Has(x, "Unit"));
            if (enemyUnits.Count() == 0)
                return;

            foreach (dynamic own in ownUnits)
            {
                uint id = own.Id;
                uint pos = own.Position.position;
                if (Commands.Orders(id).Length == 0)
                {
                    dynamic enemy = enemyUnits.OrderByDescending(x => Map.DistanceEstimate(pos, x.Position.position)).First();
                    Commands.Order(id, Commands.FightToEntity(enemy.Id));
                }
            }
        }

        void AssignRandomRecipes()
        {
            foreach (dynamic own in World.Entities().Values.Where(x => Entity.Own(x) && Entity.Has(x, "Unit")))
            {
                List<uint> recipes = Prototypes.Unit((uint)own.Proto.proto).recipes;
                if (recipes?.Count > 0)
                {
                    var recipe = recipes[random.Next(recipes.Count)];
                    Commands.CommandSetRecipe((uint)own.Id, recipe);
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
            Game.SetPlayerName("bot-cs");
            Console.WriteLine("starting");
            if (!Game.TryReconnect())
            {
                Game.SetStartGui(true);
                if (!Game.ConnectFindLan())
                    Game.ConnectNewServer();
            }
            Console.WriteLine("done");
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
                Console.Error.WriteLine("Environment variable UNNATURAL_ROOT must be set.");
                Console.Error.WriteLine("Eg. <steam path>/steamapps/common/Unnatural Worlds/bin.");
                return 1;
            }
            System.IO.Directory.SetCurrentDirectory(root);

            Bot bot = new Bot();
            bot.Start();
            return 0;
        }
    }
}
