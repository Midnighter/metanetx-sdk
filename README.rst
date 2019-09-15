============
MetaNetX SDK
============

.. image:: https://img.shields.io/pypi/v/metanetx-sdk.svg
   :target: https://pypi.org/project/metanetx-sdk/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/metanetx-sdk.svg
   :target: https://pypi.org/project/metanetx-sdk/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/metanetx-sdk.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg
   :target: https://github.com/Midnighter/metanetx-sdk/blob/master/.github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://img.shields.io/travis/Midnighter/metanetx-sdk/master.svg?label=Travis%20CI
   :target: https://travis-ci.org/Midnighter/metanetx-sdk
   :alt: Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/Midnighter/metanetx-sdk?branch=master&svg=true
   :target: https://ci.appveyor.com/project/Midnighter/metanetx-sdk
   :alt: AppVeyor

.. image:: https://codecov.io/gh/Midnighter/metanetx-sdk/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/metanetx-sdk
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

Parse and process information from `MetaNetX <https://metanetx.org>`_ for
`MIRIAM <http://co.mbine.org/standards/miriam>`_ compatibility using the
`Identifiers.org <http://identifiers.org/>`_ registries.

Usage
=====

The easiest way to access the processed data is through `quilt <https://quiltdata.com/>`_
loading the data package ``midnighter/metanetx``.

If you want to go the hard way, you can do so by first `installing <#Install>`_ the
package and then using the ``metanetx`` command line program.

.. code-block:: console

    metanetx update -h

    metanetx process -h

Install
=======

It's as simple as:

.. code-block:: console

    pip install metanetx-sdk

Copyright
=========

* Copyright (c) 2019, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0 
  <https://www.apache.org/licenses/LICENSE-2.0>`_.
