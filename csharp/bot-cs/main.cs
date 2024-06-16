using System;
using System.Collections.Generic;
using System.Linq;

namespace Unnatural
{
    using PolicyEnum = Interop.UwForeignPolicyEnum;

    internal class Bot
    {
        readonly Random random = new Random();

        void Preparing(object sender, EventArgs e)
        {
            Console.WriteLine("preparing");
        }

        void Updating(object sender, EventArgs e)
        {
        }

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

        void Stepping(object sender, uint tick)
        {
            switch (tick % 10)
            {
                case 1:
                    AttackNearestEnemies();
                    break;
                case 5:
                    AssignRandomRecipes();
                    break;
            }
        }

        void Finished(object sender, EventArgs e)
        {
            Console.WriteLine("finished");
        }

        void Shooting(object sender, Interop.UwShootingData data)
        {
        }

        void Start()
        {
            Game.SetPlayerName("bot-cs");
            Game.SetStartGui(true);
            Console.WriteLine("starting");
            Game.ConnectNewServer();
            Console.WriteLine("done");
        }

        Bot()
        {
            Game.Preparing += Preparing;
            Game.Updating += Updating;
            Game.Stepping += Stepping;
            Game.Finished += Finished;
            Game.Shooting += Shooting;
        }

        static void Main(string[] args)
        {
            Bot bot = new Bot();
            bot.Start();
        }
    }
}
