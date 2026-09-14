[![Build Status](https://circleci.com/gh/OpenDrift/opendrift.svg?style=svg)](https://app.circleci.com/pipelines/github/OpenDrift/opendrift)
[![Coverage Status](https://coveralls.io/repos/github/OpenDrift/opendrift/badge.svg?branch=master)](https://coveralls.io/github/OpenDrift/opendrift?branch=master)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.582321.svg)](https://doi.org/10.5281/zenodo.582321)
[![Slack](https://img.shields.io/badge/slack-opendrift-yellow.svg)](https://join.slack.com/t/opendrift-dev/shared_invite/zt-ozansc5h-AzMOOS9jOs~3CBihRR37Lw)
[![PyPI version](https://badge.fury.io/py/opendrift.svg)](https://badge.fury.io/py/opendrift)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/opendrift/badges/version.svg)](https://anaconda.org/conda-forge/opendrift)

> **PASCAL fork.** This is a fork of OpenDrift used by
> [`pascal_modular`](https://github.com/PASCAL-model/pascal_modular) for
> advection coupling, and installed alongside it by
> [`pascal_run`](https://github.com/PASCAL-model/pascal_run). It carries
> one deliberate change on top of upstream: `basemodel`'s `run()` used to
> run a simulation to completion in a single call, with its per-timestep
> loop body inlined directly inside that method. That loop body is now
> its own public method, `run_1step()`, which `run()` itself just calls
> in a loop - letting PASCAL's coupler advance the particle tracker by
> exactly one model timestep at a time (in lockstep with the IBM's own
> per-timestep update), instead of handing control to OpenDrift for an
> entire run. Everything else below is unmodified upstream OpenDrift.

opendrift
=========

![Image](https://github.com/opendrift/opendrift/blob/master/docs/opendrift_logo.png)

OpenDrift is a software for modeling the trajectories and fate of objects or substances drifting in the ocean, or even in the atmosphere.

![OpenDrift animation](https://dl.dropboxusercontent.com/s/u9apyh7ci1mdowg/opendrift.gif?dl=0)

[Documentation and installation instructions can be found here](https://opendrift.github.io/install.html).

Development
===========

We have a [slack-organization open for anyone to join](https://join.slack.com/t/opendrift-dev/shared_invite/zt-ozansc5h-AzMOOS9jOs~3CBihRR37Lw).
