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
   :target: https://github.com/Midnighter/metanetx-sdk/blob/stable/.github/CODE_OF_CONDUCT.md
   :alt: Code of Conduct

.. image:: https://github.com/Midnighter/metanetx-sdk/workflows/CI-CD/badge.svg
   :target: https://github.com/Midnighter/metanetx-sdk/workflows/CI-CD
   :alt: GitHub Actions

.. image:: https://codecov.io/gh/Midnighter/metanetx-sdk/branch/stable/graph/badge.svg
   :target: https://codecov.io/gh/Midnighter/metanetx-sdk
   :alt: Codecov

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code Style Black

.. summary-start

Parse and process information from `MetaNetX <https://metanetx.org>`_ for
`MIRIAM <http://co.mbine.org/standards/miriam>`_ compatibility using the
`Identifiers.org <http://identifiers.org/>`_ namespaces.

Install
=======

It's as simple as:

.. code-block:: console

    pip install metanetx-sdk

Usage
=====

The authoritative source on how to use the various commands is always accessible via
the commands' help.

.. code-block:: console

    mnx-sdk -h

Normally you would start by loading the files from the MetaNetX FTP server

.. code-block:: console

    mnx-sdk pull ./data

and then transforming each data table.

.. code-block:: console

    mnx-sdk etl chem-prop ./data/chem_prop.tsv.gz ./data/transformed_chem_prop.tsv.gz

You can also directly use the functions from the ``metanetx_sdk.api`` module.

Copyright
=========

* Copyright © 2019-2020, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0 
  <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. summary-end
