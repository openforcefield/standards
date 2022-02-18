# OFF-EP 0005 — Allow different electrostatics methods to be used on period and non-periodic systems

**Status:** Proposed

**Authors:** Matt Thompson

**Stakeholders:** Karmen Condic-Jurkic, Jeffrey Wagner, David Mobley, John Chodera

**Acceptance criteria:** Unanimity

**Created:** 2020-02-18

**Discussion:** [Issue #29](https://github.com/openforcefield/standards/issues/29)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## Abstract

This change allows for the `<Electrostatics>` tag to optionally specify that different methods
shouuld be used for periodic (i.e. condensed-phase) and non-periodic (i.e. gas phase) systems. This
in particular enables a force field to specify that PME should be used for periodic systems and no
cutoff should be used for non-periodic systems.

## Motivation and Scope

In version 0.3 of the `<Electrostatics>` tag, the default and most commonly-used electrostatics
method is PME (`method="PME")`. It is, however, not compatible with non-periodic systems, such as
gas-phase and/or single-molecule systems. In practice, force fields defined with PME are modified by
users in ways that make them compatible with non-periodic systems, such as the
[``NoCutoff``](http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html?highlight=nocutoff#coulomb-interaction-without-cutoff)
option provided by OpenMM's ``NonbondedForce``.

Given that is it not tractable to use (much less train) a force field that can only be applied to
periodic OR non-periodic systems, this OFF-EP proposes that the `<Electrostatics>` tag may specify
that different methods should be used for each kinda of systems.

This OFF-EP
* does not propose changes any detail of the `<vdW>` section
* does not alter the intended meaning of `method="PME"`

## Usage and Impact

## Backward compatibility

## Detailed description

TODO:
* Copy or reference diff of specification
* Decide if `method` should be removed / how to guess if `method` is specified but no others
* Decide on removing `method="Coulomb"`
  * Make sure there is wiggle room for engines that do not explicitly allow non-periodic simulation
    but do allow for direct electrostatics with box size >> moleclue size (possibly with cut-off
    electrostatics, but in a way that's effectively "no-cutoff")
* Discuss how to upscale 0.3 to 0.4

## Alternatives

## Discussion

- Toolkit [#1084](https://github.com/openforcefield/openff-toolkit/issues/1084)
- Standards [#29](https://github.com/openforcefield/standards/issues/29)

## Copyright

This template is based upon the
[OFF-EP template](https://openforcefield.github.io/standards/enhancement-proposals/off-ep-template/).

This document is explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
