Program Safety
==============
Memory and threads guarantees of the api.

Memory
------

Memory ownership is never transferred across the api boundary.
Usually, any pointers returned from any of the *c* functions are valid until next call to the same function.
Therefore, most *c* functions are *not* reentrant.

The Python and C# wrappers functions always copy all necessary memory from the provided pointers into the native memory of the language.
Be careful if you use a *c* function directly.

Threads
-------

.. important::
	The api is strictly singlethreaded!

