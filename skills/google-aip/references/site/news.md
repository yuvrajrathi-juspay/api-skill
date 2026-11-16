# News (AIP newsletter archive)

> Source: <https://google.aip.dev/news>

Want to keep up with the AIP system, and what we are working on? Welcome to the
**AIP newsletter**, a monthly publication covering new AIP guidance, and any
other developments useful to API producers.

> **Note (skill packaging):** The newsletter is a historical archive. The
> AIP documents themselves are authoritative; where a newsletter describes
> guidance that was later changed, follow the current AIP.

## March 2021: Auth and Field Masks

> Source: <https://google.aip.dev/news/2021-03>

Highlights:
- Reviewing: [AIP-149](../general/aip-0149-unset-field-values.md), [AIP-161](../general/aip-0161-field-masks.md), [AIP-211](../general/aip-0211-authorization-checks.md)
- Approval of AIPs discussed in the October 2020 newsletter.

Welcome to the seventh edition of the **AIP newsletter**, which is designed to
keep you up to date about the AIP program, and particular proposals making
their way through the system.

We have three new AIPs this month. As always, the AIP newsletter kicks off what
is effectively a "public comment" period: the AIP editors are happy with this
proposal, but we want to ensure that you are too. Assuming feedback is
sufficiently positive, we intend to formally approve these proposals on Friday,
March 26, 2021.

### AIPs under review

#### AIP-149: Unset field values

> In many messages, many fields are optional: the user is not required to
> provide them, or for output fields, the service might not populate the field.

[Unset field values][aip-149] refer to primitive fields where the service makes
a meaningful distinction between an empty value (such as `0` or `false`) and
not setting the value at all. While this is generally discouraged if an
alternative design is feasible, there are certainly occasions where this is the
best approach.

**Summary:** [AIP-149][] provides guidance around use of the `optional` keyword
for primitives.

We are aiming to approve AIP-149 on March 26. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/711).

[aip-149]: ../general/aip-0149-unset-field-values.md

#### AIP-161: Field masks

> Often, when updating resources, it is desirable to specify exactly which
> fields are being updated, so that the service can ignore the rest, even if
> the user sends new values.

[Field masks][aip-161] are the way that users are able to specify exactly which
fields to read or update. They are necessary to ensure that adding fields to
existing messages remains backwards-compatible.

While we have had an internal specification for field masks for some time, this
AIP publicizes the specification.

**Summary:** [AIP-161][] provides a public specification for field masks.

We are aiming to approve AIP-161 on March 26. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/718).

[aip-161]: ../general/aip-0161-field-masks.md

#### AIP-211: Authorization checks

> The majority of operations, whether reads or writes, require authorization:
> permission to do the thing the user is asking to do. Additionally, it is
> important to be careful how much information is provided to _unauthorized_
> users, since leaking information can be a security concern.

[Authorization checks][aip-211] discusses when in the logical process of a
request the authorization check ought to occur, and what error to send when an
auth check fails.

In particular, if an authorization check fails, regardless of whether the
resource exists, the service consistently returns `PERMISSION_DENIED` with an
error message that also indicates that the resource might not exist.

**Summary:** [AIP-211][] provides guidance about authorization checks: when to
perform them, and what error to send.

We are aiming to approve AIP-211 on March 26. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/719).

[aip-211]: ../general/aip-0211-authorization-checks.md

### Additional approvals

We also intend to approve the AIPs that were placed under review in the October
2020 newsletter. This includes [AIP-128][] ([#708][]), [AIP-148][] ([#710][]),
and [AIP-164][] ([#709][]). If you have feedback, please leave a comment in the
referenced pull requests.

[aip-128]: ../general/aip-0128-declarative-friendly-interfaces.md
[aip-148]: ../general/aip-0148-standard-fields.md
[aip-164]: ../general/aip-0164-soft-delete.md
[#708]: https://github.com/aip-dev/google.aip.dev/pull/708
[#709]: https://github.com/aip-dev/google.aip.dev/pull/709
[#710]: https://github.com/aip-dev/google.aip.dev/pull/710

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-144](../general/aip-0144-repeated-fields.md): Expand Add and Remove guidance.
  ([#648](https://github.com/aip-dev/google.aip.dev/pull/648))
- [AIP-154](../general/aip-0154-resource-freshness-validation.md): Etag failures should use `ABORTED`.
  ([#705](https://github.com/aip-dev/google.aip.dev/pull/705))
- [AIP-162](../general/aip-0162-resource-revisions.md): Forbid deleting the only remaining revision.
  ([#692](https://github.com/aip-dev/google.aip.dev/pull/692))
- [AIP-162](../general/aip-0162-resource-revisions.md): Restrict revision tags to lower-case.
  ([#707](https://github.com/aip-dev/google.aip.dev/pull/707))
- [AIP-165](../general/aip-0165-criteria-based-delete.md): Make implicit recommendations more explicit.
  ([#662](https://github.com/aip-dev/google.aip.dev/pull/662))
- [AIP-203](../general/aip-0203-field-behavior-documentation.md): Add `UNORDERED_LIST` to field behaviors.
  ([#671](https://github.com/aip-dev/google.aip.dev/pull/671))

## October 2020: Declarative-friendly APIs

> Source: <https://google.aip.dev/news/2020-10>

Highlights:
- Reviewing: [AIP-128](../general/aip-0128-declarative-friendly-interfaces.md), [AIP-148](../general/aip-0148-standard-fields.md), [AIP-164](../general/aip-0164-soft-delete.md)
- Declarative-friendly updates to existing AIPs.

Welcome to the sixth edition of the **AIP newsletter**, which is designed to
keep you up to date about the AIP program, and particular proposals making
their way through the system.

We have an exciting slate of AIPs entering review this cycle, all around the
theme of "declarative-friendly APIs". The linchpin here is AIP-128, which
introduces and explains the topic.

The idea behind declarative-friendly APIs addresses an important need: the
ability to integrate with popular, declarative tools, such as Kubernetes or
Terraform. These tools and others are used by numerous developers, and the
follow a straightforward paradigm: the user provides the tool with the desired
state, and the tool brings that state into fruition.

Integration with these tools is critical for cloud providers, but with the
number of services _and_ the number of tools continuously increasing, support
is difficult without a reliance on automation. Automation, in turn, requires
strong consistency.

While ordinarily AIPs stay in review for about a month, we intend for this
review cycle to be longer, to allow time for APIs to be released that follow
this guidance. Assuming the feedback is sufficiently positive, we will probably
be looking at formal approval around the end of the year.

### AIPs under review

#### AIP-128: Declarative-friendly interfaces

> Many services need to interact with common DevOps tools, particularly those
> that create and manage network-addressible resources (such as virtual
> machines, load balancers, database instances, and so on). These tools revolve
> around the principle of "configuration as code": the user specifies the
> complete intended landscape, and tooling is responsible for making whatever
> changes are necessary to achieve the user's specification.
>
> These tools are **declarative**: rather than specifying specific actions to
> take, they specify the desired _outcome_, with the actions being derived
> based on the differences between the current landscape and the intended one.

[Declarative-friendly interfaces][aip-128] describes patterns for making
interfaces that are friendly to automated tooling. The basic idea is that by
being more strict and consistent, it becomes possible to write tools that
"translate" the interface to a declarative form without having to know anything
about the specific API.

This reduces feature latency for users. Essentially, the adapter or plugin can
be automatically generated, and so an automated pipeline becomes possible: as
soon as the service launches new features, they become available in the
adapters also.

Because declarative-friendliness is a wide-ranging concept, impacting the
guidance in numerous other AIPs as well, it was difficult to determine how to
structure the information. Therefore, this AIP also has a robust "further
reading" section that points to declarative-friendly guidance in other AIPs.

**Summary:** [AIP-128][] provides an explanation of what it means for a service
to be declarative-friendly, and why a service might want to adopt these
patterns. It also indexes declarative-friendly guidance found in other AIPs.

[aip-128]: ../general/aip-0128-declarative-friendly-interfaces.md

#### AIP-148: Standard fields

> Certain concepts are common throughout any corpus of APIs. In these
> situations, it is useful to have a standard field name that is used
> consistently to communicate that concept.

[Standard fields][aip-148] is, in some ways, an overdue AIP. It describes
fields common throughout our corpus, such as `name`, `parent`, and
`create_time`, that were on the list of standard fields in the original API
style guide and did not get a full treatment in other AIPs. Common fields that
are covered in other AIPs are not discussed in this one. (As an example,
`language_code` is given extensive treatment in [AIP-143][], so not repeated
here.)

This takes on new importance with our focus on declarative-friendly APIs
because tools written to marshal between a declarative tool and the service can
see those tools and know what they mean.

**Summary:** [AIP-148][] describes common fields that are already in common use
throughout our API corpus. It also describes certain fields that are expected
on declarative-friendly resources.

[aip-143]: ../general/aip-0143-standardized-codes.md
[aip-148]: ../general/aip-0148-standard-fields.md

#### AIP-164: Soft delete

> There are several reasons why a client could desire soft delete and undelete
> functionality, but one over-arching reason stands out: recovery from
> mistakes. A service that supports undelete makes it possible for users to
> recover resources that were deleted by accident.

[Soft delete][aip-164] is increasingly critical for APIs that need to cater to
enterprise users, due to the need to be able to recover from mistakes without
data loss. While [AIP-135][] previously discussed soft delete, it was clear
that a more thorough treatment is necessary.

This AIP goes through the request patterns in more detail, and discusses topics
such as LROs and errata, that are relevant to soft delete and undelete.

**Summary:** [AIP-164][] expands the guidance on soft delete and undelete and
provides a more detailed look at both.

[aip-135]: ../general/aip-0135-standard-methods-delete.md
[aip-164]: ../general/aip-0164-soft-delete.md

### AIP sections under review

Because of the need to add declarative-friendly guidance into existing AIPs,
certain sections needed to be introduced into existing, approved AIPs in a
reviewing state. These are all in use for declarative-friendly guidance and
would be approved alongside AIP-128:

- AIP-134: [Create or update](../general/aip-0134-standard-methods-update.md#create-or-update)
- AIP-135: [Delete if existing](../general/aip-0135-standard-methods-delete.md#delete-if-existing)
- AIP-136: [Custom method restrictions](../general/aip-0136-custom-methods.md#declarative-friendly-resources)

Additionally, new sections in [AIP-154](../general/aip-0154-resource-freshness-validation.md#declarative-friendly-resources)
and [AIP-163](../general/aip-0163-change-validation.md#declarative-friendly-resources) mandate the use of these
concepts for declarative-friendly resources.

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-122](../general/aip-0122-resource-names.md): Clarified when to use full resource names
  ([#629](https://github.com/aip-dev/google.aip.dev/pull/629))
- [AIP-132](../general/aip-0132-standard-methods-list.md): Loosened guidance around top-level resources
  ([#602](https://github.com/aip-dev/google.aip.dev/pull/602))
- [AIP-132](../general/aip-0132-standard-methods-list.md): Added `PERMISSION_DENIED` guidance
  ([#582](https://github.com/aip-dev/google.aip.dev/pull/582))
- [AIP-151](../general/aip-0151-long-running-operations.md): Clarified that `stream` and LROs are mutually incompatible
  ([#597](https://github.com/aip-dev/google.aip.dev/pull/597))
- [AIP-216](../general/aip-0216-states.md): Clarified that states are not directly set on Create
  ([#606](https://github.com/aip-dev/google.aip.dev/pull/606))

Special thanks to Andrew Paseltiner and Peter Novotney for some of these
changes, and to several others who send minor corrections not noted here.

## August 2020: Field patterns, redux

> Source: <https://google.aip.dev/news/2020-08>

Highlights:
- Reviewing: [AIP-147](../general/aip-0147-sensitive-fields.md)

Welcome to the fifth edition of the **AIP newsletter**, which is designed to
keep you up to date about the AIP program, and particular proposals making
their way through the system. (Our apologies for not publishing a newsletter in
July.)

We have one new AIP this month, on sensitive fields. As always, the AIP
newsletter kicks off what is effectively a "public comment" period: the AIP
editors are happy with this proposal, but we want to ensure that you are too.
Assuming feedback is sufficiently positive, we intend to formally approve these
proposals on Friday, August 28, 2020.

### AIPs under review

#### AIP-147: Sensitive fields

> Sometimes APIs need to collect sensitive information such as private
> encryption keys meant to be _stored_ by the underlying service but not
> intended to be _read_ after writing due to the sensitive nature of the data.

[Sensitive fields][aip-147] are fields that are stored by a service but, once
set, not retrievable by the user, such as passwords or private keys. These are
not particularly common in APIs, and often it is sufficient to set them as
`INPUT_ONLY` (as described in AIP-203).

However, there is a challenge in situations where the service needs to provide
some kind of indication that a value has been provided, or provide an
obfuscated value that the original user ought to recognize. This AIP provides a
standard for each of those situations.

A special thanks to [Michael Bleigh][] for writing this AIP.

**Summary:** [AIP-147][] provides patterns for indicators around sensitive
fields.

We are aiming to approve AIP-147 on August 28. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/583).

[michael bleigh]: https://github.com/mbleigh
[aip-147]: ../general/aip-0147-sensitive-fields.md

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-135](../general/aip-0135-standard-methods-delete.md): Add "get" guidance for soft delete.
  ([#526](https://github.com/aip-dev/google.aip.dev/pull/526))
- [AIP-140](../general/aip-0140-field-names.md): Word segments in field names must not begin with a number.
  ([#528](https://github.com/aip-dev/google.aip.dev/pull/528))
- [AIP-151](../general/aip-0151-long-running-operations.md): Add guidance for parallel operations.
  ([#535](https://github.com/aip-dev/google.aip.dev/pull/535))
- [AIP-158](../general/aip-0158-pagination.md): Clarify that `page_size` is always an optional field.
  ([#537](https://github.com/aip-dev/google.aip.dev/pull/537))

## June 2020: Field patterns

> Source: <https://google.aip.dev/news/2020-06>

Highlights:
- Reviewing: [AIP-145](../general/aip-0145-ranges.md), [AIP-146](../general/aip-0146-generic-fields.md)

Welcome to the fourth edition of the **AIP newsletter**, which is designed to
keep you up to date about the AIP program, and particular proposals making
their way through the system.

This month, we have two new AIPs, both around patterns for specific kinds of
fields.

As always, the AIP newsletter kicks off what is effectively a "public comment"
period: the AIP editors are happy with these proposals, but we want to ensure
that you are too. Assuming feedback is sufficiently positive, we intend to
formally approve these proposals on Friday, June 26, 2020.

### AIPs under review

#### AIP-145: Ranges

> Services often need to represent ranges of discrete or continuous values.
> These have wide differences in meaning, and come in many types: integers,
> floats, and timestamps, just to name a few, and the expected meaning of a
> range can vary in subtle ways depending on the type of range being discussed.

[Ranges][aip-145] are fields that represent a range of discrete or continuous
values. These are often integers or floats, but can be other values where
ranges make sense, such as dates.

The primary challenge for ranges is whether their values (particularly their
end values) should be inclusive or exclusive. Most developers are used to
exclusive end values, but with some notable and precise exceptions (example:
dates are an exception, but not timestamps), and the AIP attempts to encode
this using the idea of "colloquial precedent".

**Summary:** [AIP-145][] provides patterns for ranges of values: two fields
that represent a start and end value.

We are aiming to approve AIP-145 on June 26. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/523).

[aip-145]: ../general/aip-0145-ranges.md

#### AIP-146: Generic fields

> Occasionally it is appropriate to have a generic or polymorphic field of some
> kind that can conform to multiple schemata, or even be entirely free-form.

[Generic fields][aip-146] discusses the various ways to approach a polymorphic
or entirely generic field in the API. These provide implementation flexibility,
but the tradeoff is a less clear API contract. There are several ways to
provide a generic field, and the AIP enumerates them and discussed the
tradeoffs.

**Summary:** [AIP-146][] offers four patterns for generic fields, and describes
the tradeoffs of each.

We are aiming to approve AIP-146 on June 26. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/524).

[aip-146]: ../general/aip-0146-generic-fields.md

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-122](../general/aip-0122-resource-names.md): Corrected a mistaken piece of guidance about
  capitalization ([#513](https://github.com/aip-dev/google.aip.dev/pull/513))
- [AIP-132](../general/aip-0132-standard-methods-list.md): Removed mandate to document default ordering
  ([#512](https://github.com/aip-dev/google.aip.dev/pull/512))
- [AIP-140](../general/aip-0140-field-names.md): Add guidance for URI fields
  ([#519](https://github.com/aip-dev/google.aip.dev/pull/519))
- [AIP-143](../general/aip-0143-standardized-codes.md): Change guidance for countries to `region_code`
  ([#507](https://github.com/aip-dev/google.aip.dev/pull/507))
- [AIP-203](../general/aip-0203-field-behavior-documentation.md): Clarified behavior for updating immutable fields
  ([#516](https://github.com/aip-dev/google.aip.dev/pull/516))

## May 2020: Jobs and filters

> Source: <https://google.aip.dev/news/2020-05>

Highlights:
- Reviewing: [AIP-152](../general/aip-0152-jobs.md), [AIP-160](../general/aip-0160-filtering.md)

Welcome to the third edition of the **AIP newsletter**, which is designed to
keep you up to date about the AIP program, and particular proposals making
their way through the system.

This month, we have one new AIP, which is around _jobs_: resources created for
managing a task that may be repeated. We also have one AIP from April that we
have delayed finalizing.

As always, the AIP newsletter kicks off what is effectively a "public comment"
period: the AIP editors are happy with these proposals, but we want to ensure
that you are too. Assuming feedback is sufficiently positive, we intend to
formally approve these proposals on Friday, May 29, 2020.

### AIPs under review

#### AIP-152: Jobs

> Occasionally, APIs may need to expose a task that takes significant time to
> complete, and where a transient long-running operation is not appropriate.
> For example, a task could need to run repeatedly, or have separate
> permissions for configuring the task as opposed to running it.

[Jobs][aip-152] are resources that are created that represent a (usually)
repeated task in an API. The idea is that the job is configured once, and
exists as an independent resource, which can either be executed by a user, or
by the system on a schedule.

Jobs are useful when more structure or more permanence is needed than a simple
RPC with a long-running operation can provide. They can also be useful if a
service requires a permission model that distinguishes between who can
_configure_ a job as opposed to who can _run_ it.

**Summary:** [AIP-152][] provides patterns for jobs: first-class resources that
represent tasks that are run repeatedly, whether by a user or by the system on
a schedule.

We are aiming to approve AIP-152 on May 29. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/504).

[aip-152]: ../general/aip-0152-jobs.md

#### AIP-160: Filtering

> Often, when listing resources, it is desirable to filter over the collection
> and only return results that the user is interested in.

[Filtering][aip-160] involves taking a list of resources (usually) and only
providing the results that the user wants, specified using a familiar syntax
similar to that of Google search.

This AIP is a holdover from last month's newsletter: we intended to approve it
in April, but several teams brought forth issues and clarifications that
necessitated further iteration. (Thanks!!) These are now represented in the
approval pull request ([#473][]), and we hope to approve this AIP in May.

**Summary:** [AIP-160][] offers a detailed breakdown of the filtering syntax
and how to provide filtering results in list and search methods.

We are aiming to approve AIP-160 on May 29. If you have feedback, please [leave
a comment][#473].

[#473]: https://github.com/aip-dev/google.aip.dev/pull/473
[aip-160]: ../general/aip-0160-filtering.md

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-122](../general/aip-0122-resource-names.md): Tighten restrictions on resource names
  ([#496](https://github.com/aip-dev/google.aip.dev/pull/496))
- [AIP-192](../general/aip-0192-documentation.md): Mandate use of absolute links in comments
  ([#480](https://github.com/aip-dev/google.aip.dev/pull/480))

## April 2020: Data Series

> Source: <https://google.aip.dev/news/2020-04>

Highlights:
- Reviewing: [AIP-124](../general/aip-0124-resource-association.md), [AIP-144](../general/aip-0144-repeated-fields.md), [AIP-160](../general/aip-0160-filtering.md)

Welcome to the second edition of the **AIP newsletter**, which is designed to
keep you up to date about the AIP program, and particular proposals making
their way through the system.

This month's new AIPs (unintentionally) share a common theme: handling lists
and series of data, whether in fields, resource relationships, or actual list
methods. These new AIPs are long overdue: they codify knowledge that has long
been reasonably consistent, but tribal.

The AIP newsletter kicks off what is effectively a "public comment" period: the
AIP editors are happy with these proposals, but we want to ensure that you are
too. Assuming feedback is sufficiently positive, we intend to formally approve
these proposals on Friday, April 24, 2020.

### AIPs under review

#### AIP-124: Resource associations

> APIs sometimes have resource hierarchies that can not be cleanly expressed in
> the usual tree structure.

[Resource association][aip-124] comes into play when a resource needs something
other than a direct parent-child relationship. This might mean a many-to-many
relationship, or it might be a one-to-many association that is distinct from
the parent-child relationship.

We have had several APIs struggle with unusual associations over the past year
or so. In general, this has been handled reasonably consistently, but we never
codified the guidance into an official AIP.

**Summary:** [AIP-124][] provides patterns for the two most common
associations: a resource with multiple different one-to-many relationships, and
a resource with a many-to-many association with another resource.

We are aiming to approve AIP-124 on April 24. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/475).

[aip-124]: ../general/aip-0124-resource-association.md

#### AIP-144: Repeated fields

> Representing lists of data in an API is trickier than it often appears. Users
> often need to modify lists in place, and longer data series within a single
> resource pose a challenge for pagination.

[Repeated fields][aip-144] are somewhat common in APIs, and a common question
that we get is how to handle adding or removing a single item from them
atomically. Additionally, repeated fields can become a trap if they are
unbounded in size and become too large.

This is codification of guidance that we have been giving on a case-by-case
basis for some time. In particular, this documents the various restrictions on
the two update strategies.

**Summary:** [AIP-144][] lays out guidance for repeated fields, and details two
distinct strategies for updating repeated fields.

We are aiming to approve AIP-144 on April 24. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/476).

[aip-144]: ../general/aip-0144-repeated-fields.md

#### AIP-160: Filtering

> Often, when listing resources, it is desirable to filter over the collection
> and only return results that the user is interested in.

[Filtering][aip-160] involves taking a list of resources (usually) and only
providing the results that the user wants, specified using a familiar syntax
similar to that of Google search.

This is likely the most-requested AIP of all time. We have had internal
filtering documents for ages, but we have not had a public version, and one has
been sorely needed for years. Also, this work would likely still be unfinished
if not for the efforts of [Tristan Swadell][]; we are grateful for his efforts.

**Summary:** [AIP-160][] offers a detailed breakdown of the filtering syntax
and how to provide filtering results in list and search methods.

We are aiming to approve AIP-160 on April 24. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/473).

[aip-160]: ../general/aip-0160-filtering.md
[tristan swadell]: https://github.com/tristonianjones

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-133](../general/aip-0133-standard-methods-create.md): Clarify which fields can be required
  ([#460](https://github.com/aip-dev/google.aip.dev/pull/460))
- [AIP-140](../general/aip-0140-field-names.md): Add guidance about message and field name conflicts
  ([#470](https://github.com/aip-dev/google.aip.dev/pull/470))
- [AIP-151](../general/aip-0151-long-running-operations.md): Clarify that both `response_type` and `metadata_type` are
  expected ([#469](https://github.com/aip-dev/google.aip.dev/pull/469))
- [AIP-231](../general/aip-0231-batch-methods-get.md): Clarify Batch Get behavior if no resource names are sent
  ([#474](https://github.com/aip-dev/google.aip.dev/pull/474))

## March 2020: Welcome to the AIP Newsletter

> Source: <https://google.aip.dev/news/2020-03>

Highlights:
- Reviewing: [AIP-153](../general/aip-0153-import-and-export.md), [AIP-162](../general/aip-0162-resource-revisions.md), [AIP-163](../general/aip-0163-change-validation.md), [AIP-165](../general/aip-0165-criteria-based-delete.md), [AIP-194](../general/aip-0194-automatic-retry-configuration.md)
- The API linter is here!

Welcome to the first (hopefully monthly) edition of the **AIP newsletter**,
which is designed to keep you up to date about the AIP program, and particular
proposals making their way through the system.

In this edition, we will discuss five pending proposals. This is intended as a
"public comment" period: the AIP editors are happy with these proposals, but we
want to ensure that you are too. Assuming feedback is sufficiently positive, we
intend to formally approve these proposals on Friday, March 27, 2020.

### API linter

As many readers know, we have published an [API linter][], which is able to
check much of the guidance provided in API Improvement Proposals for APIs
defined in protocol buffers.

The linter now has over 150 rules, and is running on many new and existing APIs
at Google, hopefully pushing us toward greater consistency.

[api linter]: https://github.com/api-linter

### AIPs under review

#### AIP-153: Import and export

> Many users want to be able to load data into an API, or get their existing
> data out of an API. This is particularly important for enterprise users, who
> are often concerned about vendor lock.

[Import and export][aip-153] are particularly important concepts for enterprise
APIs, although they are increasing in importance for consumer and SaaS APIs as
well.

We have actually had a reasonably consistent import and export story in Google
Cloud for a long time, but it has largely been passed along by tribal knowledge
("go look at X and copy what they did"). Therefore, this AIP attempts to codify
what we believe is a long-standing practice.

**Summary:** [AIP-153][] mandates that both import and export methods return
[long-running operations][aip-151]. Unlike most API methods, they do support
partial failures, which are handled through the LRO metadata. Finally, they
have a specified place for per-source and per-destination configuration,
distinct from configuration for the data itself.

We are aiming to approve AIP-153 on March 27. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/422).

[aip-151]: ../general/aip-0151-long-running-operations.md
[aip-153]: ../general/aip-0153-import-and-export.md

#### AIP-162: Resource revisions

> Some APIs need to have resources with a revision history, where users can
> reason about the state of the resource over time.

[Resource revisions][aip-162] is a concept we are seeing crop up more and more,
and we are seeing an increasing number of situations where audit logging is a
necessary but insufficient solution. Several APIs have struggled with how to
model a resource's history over time, and handle common use cases like commit
and rollback, which is what prompted this AIP.

This is new guidance, put together by the AIP team as well as several API teams
who needed this functionality near the end of 2019. It has been positively
received by the teams that needed it, and so we would like to codify it.

**Summary:** [AIP-162][] mandates the use of revision IDs that are appended to
a resource name with the `@` character for signifying revisions, and sets out
method structures for most common operations (listing revisions, rollback,
etc.). It also proposes a tagging mechanism for user-friendly revision names.

We are aiming to approve AIP-162 on March 27. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/436).

[aip-162]: ../general/aip-0162-resource-revisions.md

#### AIP-163: Change validation

> Occasionally, a user wants to validate an intended change to see what the
> result will be before actually making the change. For example, a request to
> provision new servers in a fleet will have an impact on the overall fleet
> size and cost, and could potentially have unexpected downstream effects.

[Change validation][aip-163] is the concept of performing a "dry run" on an API
request, and returning back the result without making any changes.

This is effectively a migration of long-standing guidance that was not very
fleshed out. The previous API design guide mentioned `validate_only` as an
entry in the standard fields table with minimal explanation. This proposal
fleshes that out with an example, and addresses some questions we have received
over time.

**Summary:** [AIP-163][] offers guidance for "dry run" requests using a
`bool validate_only` field in the request message, and addresses some common
situations around permissions and incomplete output.

We are aiming to approve AIP-163 on March 27. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/437).

[aip-163]: ../general/aip-0163-change-validation.md

#### AIP-165: Criteria-based delete

> Occasionally, an API may need to provide a mechanism to delete a large number
> of resources based on some set of filter parameters, rather than requiring
> the individual resource name of the resources to be deleted.

[Criteria-based delete][aip-165] is designed to address problems where a user
needs to delete so many items that [batch delete][aip-235] simply becomes
infeasible.

This proposal represents a concession of sorts: we have long tried to avoid
delete-by-filter because of concerns that users would accidentally delete
important records and be unable to recover them. However, several APIs have had
legitimate reasons to need to do this, because the number of records the user
would want to delete was so high.

**Summary:** [AIP-165][] offers guidance for criteria-based delete, with a
common name (`Purge`) and structure, and mandates a dry-run by default with a
`force` flag to actually perform the purge.

We are aiming to approve AIP-165 on March 27. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/438).

[aip-165]: ../general/aip-0165-criteria-based-delete.md
[aip-235]: ../general/aip-0235-batch-methods-delete.md

#### AIP-194: Retries for gRPC clients

> RPCs sometimes fail. When one does, the client performing the RPC needs to
> know whether it is safe to retry the operation. When status codes are used
> consistently across multiple APIs, clients can respond to failures
> appropriately.

[Retries for gRPC clients][aip-194] handles how to deal with errors, and in
particular when a client can transparently retry those errors.

This proposal came about because of a need for first-party client libraries to
be able to transparently retry some server errors. gRPC offers a configuration
strategy for this, which is defined by API producers.

**Summary:** [AIP-194][] offers guidance for configuring what error codes from
an API are safe to retry. It recommends usually retrying `UNAVAILABLE` and
nothing else.

We are aiming to approve AIP-194 on March 27. If you have feedback, please
[leave a comment](https://github.com/aip-dev/google.aip.dev/pull/439).

[aip-194]: ../general/aip-0194-automatic-retry-configuration.md

### Recent updates

In addition to the new AIPs under review, we have added the following guidance
to existing AIPs:

- [AIP-8](../general/aip-0008-aip-style-and-guidance.md): AIPs have reverse-chronological changelogs
  ([#425](https://github.com/aip-dev/google.aip.dev/pull/425))
- [AIP-135](../general/aip-0135-standard-methods-delete.md): Delete methods send 403 errors if the user lacks access
  ([#409](https://github.com/aip-dev/google.aip.dev/pull/409))
- [AIP-140](../general/aip-0140-field-names.md): `display_name` and `title` standard fields
  ([#405](https://github.com/aip-dev/google.aip.dev/pull/405))
- [AIP-158](../general/aip-0158-pagination.md): Field order for pagination response messages
  ([#419](https://github.com/aip-dev/google.aip.dev/pull/419))
- [AIP-193](../general/aip-0193-errors.md): Added reference to new `ErrorInfo` message
  ([#396](https://github.com/aip-dev/google.aip.dev/pull/396))

### What is coming?

We have more coming over the course of the next few months, including
long-awaited public guidance for filtering and versioning.

You also may notice some pull requests around making AIPs more generic. We are
exploring the possibility of bringing AIPs to even more API producers across
multiple companies, so that others can publish their standards under a common
information architecture. This effort is still nascent, but we are excited and
hopeful. Stay tuned!
