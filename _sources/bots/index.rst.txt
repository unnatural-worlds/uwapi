Bots
====
Guide on writing custom AI/bots for Unnatural Worlds.

Bots act as a client connected to the game server (locally or over internet).
The server generally makes no assumption on whether a connection is a bot or a regular player.
Specifically, bots cannot cheat - no more than a regular player could.

Bots can be used for games against the built-in AI, against human players, or play on ladders dedicated for bots.

It is also possible to write a client program for managing a game server.
Eg. for automated tournaments.
It can manage players, and start the game when ready.
Finally it can save the results of the match.

.. toctree::
	:maxdepth: 1

	setup
	setupPython
	programOverview
	programSafety
	performance
	troubleshooting
