# OFF-EP 0004 — Handlers specify their dependence on other handlers

**Status:** Proposed

**Authors:** Matt Thompson

**Stakeholders:** David Mobley, John Chodera, Jeffrey Wagner, Simon Boothroyd

**Acceptance criteria:** <Unanimity>

**Created:** 2021-12-01

**Discussion:** [Issue #2](https://github.com/openforcefield/standards/issues/2)

**Implementation:** [PR #24](https://github.com/openforcefield/standards/pull/24)

## Abstract

This OFF-EP requires that handlers state which other handlers they depend on, if any.

## Motivation and Scope

There are some cases in which it is not clear which parameter section(s) in a SMIRNOFF force field
depend on each other. For example, it is natural to define a TIP3P force field with a
`<LibraryCharges>` section but neglect to add an `<Electrostatics>` section. This leads to
difficulties and strange behaviors in implementation. For example, there is no way to know what
cutoff method and distance should be used when the `<Electrostatics>` section is missing. This
ambiguity could be resolved by requiring that, if a force field defines any charge methods, it must
have a `<Electrostatics>` section. This sort of approach should be applied generally to all
handlers; developers implementing this SMIRNOFF specification may intuit these relationships over
time, but a better solution would be clarifying them in the specification itself.

This appears to only be an issue when handlers **require** information from other handlers. There
are some cases in which one section **could** use information from another but does not **require**
it. For example, a `<Bonds>` section does not **require** to information from other sections,
but `<LibraryCharges>` does (`<Electrostatics>`, see above). A `<Constraints>` section that does not
define the distances of constrained bonds will **require** a corresponding `<Bonds>` section, but it
is also possible to define a `<Constraints>` section that does fully define all constraint distances
and does not require a `<Bonds>` section.


## Usage and Impact

This proposal adds requirements to the specification that, in some cases, may require changes to
existing SMIRNOFF implementations. These changes should be improvements in the sense that
relationships between handlers will be clarified, but some changes may be breaking in the sense that
behavior could change.

For example, continuing with the case of TIP3P water from above, a SMIRNOFF implementation after
this proposal should raise an exception if there is a `<LibraryCharges>` section present but no
`<Electrostatics>` sectoin present, since the form depends on the latter. This raised exception
would be a breaking change, though it is easy to argue this is an improvement.

## Backward compatibility

For cases in which required sections are currently missing, this proposal will break backwards
compatibility by requiring that an exception should be raised. There should be no backwards
incompatibilities with optional handler interdependence.

Each changed section (`<Constraints>`, `<LibraryCharges>`, `<ChargeIncrementModel>`) had its version
bumped to 0.4 to reflect this change. Up-converting from version 0.3 should be straightforward,
assuming that the changes made explicit here were already present implicitly.


## Detailed description

This OFF-EP proposes that each parameter handler section

* states which other sections **must** be present ("other required sections") and 
* states which other sections it **may** interact with ("other optional sections").

If, after loading all setions from a file or other data source, a section that must be present
according to some other section is missing, an exception should be raised.

Parameter handlers do not interact with other handlers not listed in either section.

This OFF-EP adds the following information to the introduction of the `Parameter sections` section
of the SMIRNOFF specification:

```
For cases in which a parameter handler depends on another, each handler specifies which other
handlers must be present if information from another handler is required and also states which other
handlers it may optionally interact with.
```

and also updates some existing sections to clarify handler interedependence according to the current
implementation. `<Constraints>` added `<Bonds>` as an optional section and `<LibraryCharges>`
and `<ChargeIncrementModel>` each added `<Electrostatics>` as a required sections. Each was bumped
to version 0.4.

## Discussion

- [Issue #2](https://github.com/openforcefield/standards/issues/2)
- [Toolkit issue #716](https://github.com/openforcefield/openff-toolkit/issues/716) describing the TIP3P case
- [Review of Toolkit PR #833](https://github.com/openforcefield/openff-toolkit/pull/833#issuecomment-816336358) describing the more fundamental issue


## Copyright

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
