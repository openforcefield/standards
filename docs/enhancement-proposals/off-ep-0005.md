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

## Usage and Impact

## Backward compatibility

## Detailed description

## Alternatives

## Discussion

- Toolkit [#1084](https://github.com/openforcefield/openff-toolkit/issues/1084)
- Standards [#29](https://github.com/openforcefield/standards/issues/29)

## Copyright

This template is based upon the
[OFF-EP template](https://openforcefield.github.io/standards/enhancement-proposals/off-ep-template/).

This document is explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
