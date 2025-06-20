Setup Python
============
Instructions to install Python:

.. tab-set::
   :sync-group: platform

   .. tab-item:: Windows
      :sync: windows

      Install latest stable version of python from: https://www.python.org/downloads/windows/.
      Make sure to add it to system path.

      .. code-block:: bash

         # update pip
         python -m pip install --upgrade pip

   .. tab-item:: Linux
      :sync: linux

      .. code-block:: bash

         # install python
         sudo apt update
         sudo apt install python3-dev python3-pip

Also install dependencies:

.. code-block:: bash

   # install cffi
   pip install cffi

