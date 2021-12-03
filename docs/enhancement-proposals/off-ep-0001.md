# OFF-EP 1 — Clarify that constraint distances override equilibrium bond distances

**Status:** Proposed

**Authors:** Matt Thompson, matt.thompson@openforcefield.org

**Stakeholders:** David Mobley, John Chodera, Jeffrey Wagner, Simon Boothroyd

**Acceptance criteria:** Unanimity

**Created:** 2021-11-23

**Discussion:** [Issue #5](https://github.com/openforcefield/standards/issues/5)

**Implementation:** [PR #21](https://github.com/openforcefield/standards/pull/21)

## Abstract

This OFF-EP improves the documentation of the constraints section.

## Motivation and Scope

Most sections of the SMIRNOFF specification can be applied independently of others, but the
`<Constraints>` section depends on the `<Bonds>` section in many implementations. Specifically, a
pair of atoms can be subject to a harmonic bond potential via a `<Bond>` parameter and also be
constrained via a constraint specified by a `<Constraint>` parameter. This leads to two edge cases
that are not explicitly described in the specification.

The first case is in which each section specifies a distance parameter, which are likely not
numerically identical, and it is not clear which should be applied. The current implementation in
the OpenFF Toolkit uses the distance specified in the `<Constraint>` record.

The second case is in which a `<Constraint>` record does not specify the distance, in which case the
`length` value of a corresponding bond parameter is used. The current implementation in the OpenFF
Toolkit uses the distance specified in the `<Bond>` record.

These each could be minor points of confusion for anybody re-implementing the SMIRNOFF spec. At
worst, these ambiguities could cause behavior differences between implementations.

## Usage and Impact

There should be no impact on existing implementations as the only current implementation we are
aware of already follows the behavior described by these changes.

## Backward compatibility

This proposal does not change the behavior; it only makes explicit what is currently implicit in the
specification and what is the current behavior of the implementation in the OpenFF Toolkit.
Therefore, there should be no backwards compatibility issues.

## Detailed description

This OFF-EP adds the following clarifications to the `<Constraints>` section of the SMIRNOFF
specification:

```
If a constraint is applied across a bond between two atoms, then the length of that bond will be constrained to:

* the value of the `distance` attribute of the `<Constraint>` parameter _if one is specified_, *otherwise*
* the value of the `length` attribute of the `<Bond>` parameter that is matched by that bond

If the `<Constraint/>` parameter does not specify a distance and is applied to two atoms that either aren't bonded or which do not have an associated `<Bond/>` parameter, an exception should be raised.
```

## Discussion

- [Issue #5](https://github.com/openforcefield/standards/issues/5)

## Copyright

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
