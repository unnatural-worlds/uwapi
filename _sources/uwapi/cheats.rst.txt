Cheats
------
These may help you with testing your creations.
Type it in chat.
All commands start with slash `/`.

Game speed
==========
Set game speed, in percentages.
Valid values are from 10 % to 1000 %.

.. code-block::

	/gamespeed 100

Environment
===========
Set position and speed of sun.
Speed is between 0 and 10.
Offset is from 0 to 1.

.. code-block::

	/weatherspeed 1.0
	/weatheroffset 0.0

Fog of war
==========
Enable or disable fog of war.

.. code-block::

	/fogofwar on
	/fogofwar off

Spawning
========
Add units, buildings, or resources.

.. code-block::

	/spawn 20 metal
	/spawn 5 paladin
	/spawn 1 drill

AI
==
Controls behavior of all ai/bots players.

.. code-block::

	/ai difficulty 0.0
	/ai aggressive 0.0
	/ai stretching 0.0
	/ai expansive 0.0

+-------+------------+
| Value | Difficulty |
+=======+============+
|    -1 | Dormant    |
+-------+------------+
|     0 | Easy       |
+-------+------------+
|     1 | Medium     |
+-------+------------+
|     2 | Hard       |
+-------+------------+
|     3 | Extreme    |
+-------+------------+

+-------+-------------------+-------------------+-------------------+
| Value | Aggressive        | Stretching        | Expansive         |
+=======+===================+===================+===================+
|     0 | Defensive         | Army in one group | Just one base     |
+-------+-------------------+-------------------+-------------------+
|     1 | Sometimes attacks | Few groups        | Few expansions    |
+-------+-------------------+-------------------+-------------------+
|     2 | Always attacks    | Many small groups | Many expansions   |
+-------+-------------------+-------------------+-------------------+

Special value `nan` can also be used for these commands, to reset a value to its default.
