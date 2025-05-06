Program Overview
================
High-level look at basic bot program.

Environment Variables
---------------------
Some variables that may alter the behavior of your bot program.

- ``UNNATURAL_ROOT`` - path to the ``bin`` folder that contains the shared library.
- ``UNNATURAL_CONNECT_LOBBY`` - id of Steam lobby to connect to.
- ``UNNATURAL_CONNECT_ADDR`` - IP address or domain name to connect to.
- ``UNNATURAL_CONNECT_PORT`` - port of the game server to connect to.

Program Lifecycle
-----------------
At start, you are in full control of the program.

Initialization
^^^^^^^^^^^^^^

- You need to change current working directory to the ``bin`` directory in the game installation.
  Without it, the game will be unable to load maps and assets, even if it might load the shared library.

.. warning::
	Do *not* change current working directory once configured.

- Next you load the shared library.

.. tab-set::

   .. tab-item:: Python
      :sync: python

      TODO

   .. tab-item:: C#
      :sync: csharp

      The library is automatically loaded when you first access the global ``Game`` object.
      This happens inside the ``Bot`` constructor.

- Setup all your callbacks now.
  You may also set some parameters for the connection.

Connect
^^^^^^^
There are multiple ways to connect to a server.
The usual approach is to first try reconnecting, in case the game has crashed previously.
Second, you connect to an existing server using the parameters provided in the environment variables, if any.
Third, you spin up your own server.

Alternatively, you may implement your own logic to determine how to connect to a server.

No matter the method, the game will now take control over the program.
Your program is blocked until the network connection closes.
All your further actions will happen inside callbacks only.

Game Loop
^^^^^^^^^
All your registered callbacks are now called, when appropriate.
Notably, the ``Update`` callback is periodically called, no matter the game state.
This is where you keep track of the state of the game, and perform any of your actions.

.. warning::
	The ``Update`` callback, and some other, may be called before the game has actually started (eg. in ``Session``), or when the map is not yet ``Loaded``.
	Be mindful of what operations are valid in these circumstances.

You may prematurely close the connection with the ``Disconnect`` function.
This will do a graceful closing of the connection, that is, you will get some additional callbacks called.
After that the connect function will return.

Finalization
^^^^^^^^^^^^
When the connection function returns, the network connection has already been closed, and you take back control over the program.
You may do any cleanup operations, for example you may save some statistics from the game.
Ultimately, you should unload the shared library, and exit the program.

It may be tempting to just loop and connect again to next server, however this is strongly discouraged.
