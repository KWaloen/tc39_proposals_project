[[Stage 3]]<br>Classification: [[API Change]]<br>Human Validated: KW<br>Title: Time Zone Canonicalization<br>Authors: Justin Grant<br>Champions: Justin Grant, Richard Gibson<br>Last Presented: July 2023<br>Stage Upgrades:<br>Stage 1: 2023-04-01  
Stage 2: 2023-05-18  
Stage 2.7: NA  
Stage 3: 2023-07-15  
Stage 4: NA<br>Last Commit: 2023-09-26<br>Topics: #intl #others<br>Keywords: #date_time #identifier <br>GitHub Link: https://github.com/tc39/proposal-canonical-tz#readme <br>GitHub Note Link: https://github.com/tc39/notes/blob/main/meetings/2023-07/july-12.md#time-zone-canonicalization-for-stage-3
# Proposal Description:
# Handling Time Zone Canonicalization Changes

Time zones in ECMAScript rely on IANA Time Zone Database ([TZDB](https://www.iana.org/time-zones)) identifiers like `America/Los_Angeles` or `Asia/Tokyo`.
This proposal improves developer experience when the canonical identifier of a time zone is changed in TZDB, for example from `Europe/Kiev` to `Europe/Kyiv`.

## Status

This proposal is currently [Stage 3](https://github.com/tc39/proposals/tree/main#stage-3) following the [TC39 process](https://tc39.es/process-document/).

This proposal reached Stage 3 at the July 2023 TC39 meeting.
Stage 3 reviewers were: Philip Chimento ([@ptomato](https://github.com/ptomato)), Daniel Minor ([@dminor](https://github.com/dminor)), and Jordan Harband ([@ljharb](https://github.com/ljharb)).

It was agreed at that meeting that this proposal should be merged into the [[temporal]] proposal which is also at Stage 3.
This merger will happen via a normative PR into the Temporal repo, which this proposal's champions will file soon.
After that PR lands, unresolved issues in this repo will be migrated to the [ECMA-402 repo](https://github.com/tc39/ecma402) and may be addressed via later normative PRs to ECMA-402.

Here are [Slides](https://docs.google.com/presentation/d/1MVBKAB8U16ynSHmO6Mkt26hT5U-28OjyG9-L-GFdikE) for the July 2023 TC39 plenary meeting where this proposal advanced to Stage 3.

Here are [Slides](https://docs.google.com/presentation/d/13vW8JxkbzyzGubT5ZkqUIxtpOQGNSUlguVwgcrbitog/) for the May 2023 TC39 plenary meeting where this proposal advanced to Stage 2.

Here are [Slides](https://docs.google.com/presentation/d/13vW8JxkbzyzGubT5ZkqUIxtpOQGNSUlguVwgcrbitog/) from the March 2023 TC39 plenary meeting where this proposal advanced to Stage 1.

This proposal's specification is "stacked" on top of the [Temporal proposal](https://github.com/tc39/proposal-temporal), because this proposal builds on Temporal features, especially the [`Temporal.TimeZone`](https://tc39.es/proposal-temporal/docs/timezone.html) built-in object.

## Specification

The specification text for this proposal can be found at https://tc39.es/proposal-canonical-tz.
This proposal's spec changes are narrow: about 15 lines of spec text changes (mostly one-line changes in existing abstract operations), plus one prose paragraph.

## Champions

- Justin Grant ([@justingrant](https://github.com/justingrant))
- Richard Gibson ([@gibson042](https://github.com/gibson042/))

## Tests

Test262 tests covering this proposal's entire surface area are available at https://github.com/tc39/test262/pull/3837.

## Polyfill

A non-production, for-testing-only polyfill is available.
This proposal's polyfill is stacked on the Temporal proposal's non-production, test-only polyfill. See this proposal's [`polyfill README`](./polyfill/README.md) for more information.

## Contents

- [Motivation](#Motivatione)
- [Definitions](#Definitions)
- [Proposed Solution](#Proposed-Solution---Summary)
- [References](#References)

## Motivation

### Variation between implementations + spec doesn't match web reality

```javascript
Temporal.TimeZone.from('Asia/Kolkata');
// => Asia/Kolkata (Firefox)
// => Asia/Calcutta (Chrome, Safari, Node -- does not conform to ECMA-402)
```

### Vague spec text: _"in the IANA Time Zone Database"_

```javascript
// TZDB has build options and the spec is silent on which to pick.
// Default build options, while conforming, are bad for users.
Temporal.TimeZone.from('Atlantic/Reykjavik');
// => Africa/Abidjan
Temporal.TimeZone.from('Europe/Stockholm');
// => Europe/Berlin
Temporal.TimeZone.from('Europe/Zagreb');
// => Europe/Belgrade
```

### User Complaints

- [CLDR-9892: 'Asia/Calcutta', 'Asia/Saigon' and 'Asia/Katmandu' are canonical even though they became obsolete in 1993](https://unicode-org.atlassian.net/browse/CLDR-9892)
- [Chromium 580195: Asia/Calcutta Timezone Identifier should be replaced by Asia/Kolkata](https://bugs.chromium.org/p/chromium/issues/detail?id=580195)
- [moment.tz.guess() in chrome is different from moment.tz.guess() in IE · Issue #453 · moment/moment-timezone ](https://github.com/moment/moment-timezone/issues/453)
- [CLDR-5612: Timezones very outdated](https://unicode-org.atlassian.net/browse/CLDR-5612)
- [CLDR-9718: Rename from Asia/Calcutta to Asia/Kolkata in Zone - Tzid mapping and windows mapping](https://unicode-org.atlassian.net/browse/CLDR-9718)
- [Incorrect canonical time zone name for Asia/Kolkata · Issue #1076 · tc39/proposal-temporal](https://github.com/tc39/proposal-temporal/issues/1076)
- [[tz] Kyiv not Kiev](https://mm.icann.org/pipermail/tz/2021-January/029695.html) (from [IANA TZDB mailing list](https://mm.icann.org/pipermail/tz/)).
- [WebKit 218542: Incorrect timezone returned for Buenos Aires](https://bugs.webkit.org/show_bug.cgi?id=218542)
- [Firefox 1796393: Javascript returns problematic timezone, breaking sites](https://bugzilla.mozilla.org/show_bug.cgi?id=1796393)
- [Firefox 1825512: Europe/Kyiv is not a valid IANA timezone identifier](https://bugzilla.mozilla.org/show_bug.cgi?id=1825512)
- It's easy to find dozens more.

### Can't depend on static data behaving the same over time

```shell
> npm test
# result = someFunctionToTest('Asia/Calcutta');
# assertEqual(result.timeZone.id, 'Asia/Calcutta');
✅
> brew upgrade node
> npm test
❌
Expected: 'Asia/Calcutta'
Actual: 'Asia/Kolkata'
```

### Comparing persisted identifiers with `===` is unreliable

```javascript
userProfile.timeZoneId = Temporal.Now.timeZoneId();
userProfile.save();
// 1 year later (after canonicalization changed)
userProfile.load();
if (userProfile.timeZoneId !== Temporal.Now.timeZoneId()) {
  alert('You moved!');
}
```

### Temporal makes these problems more disruptive

```javascript
// Today, canonicalization is invisible for most common use cases.
// Intl.DateTimeFormat `format` localizes time zone names.
// Only `resolvedOptions()` exposes the underlying IANA time zone.
timestamp = '2023-03-10T12:00:00Z';
timeZone = 'Asia/Kolkata';
dtf = new Intl.DateTimeFormat('en', { timeZone, timeZoneName: 'long' });
dtf.format(new Date(timestamp));
// => '3/10/2023, India Standard Time'
dtf.resolvedOptions().timeZone;
// => 'Asia/Kolkata' (Firefox)
// => 'Asia/Calcutta' (Chrome, Safari, Node)

// In Temporal, canonical identifiers are *very* noticeable.
zdt = Temporal.Instant.from(timestamp).toZonedDateTimeISO({ timeZone });
zdt.timeZoneId;
// => 'Asia/Kolkata' (Firefox)
// => 'Asia/Calcutta' (Chrome, Safari, Node)
zdt.getTimeZone().id;
// => 'Asia/Kolkata' (Firefox)
// => 'Asia/Calcutta' (Chrome, Safari, Node)
zdt.getTimeZone().toString();
// => 'Asia/Kolkata' (Firefox)
// => 'Asia/Calcutta' (Chrome, Safari, Node)
zdt.toString();
// => '2023-03-10T17:30:00+05:30[Asia/Kolkata]' (Firefox)
// => '2023-03-10T17:30:00+05:30[Asia/Calcutta]' (Chrome, Safari, Node)
```

## Definitions

Additional details related to the terms below can be found at [Time Zone Identifiers](https://tc39.es/ecma262/#sec-time-zone-identifiers) in ECMA-262 and [Use of the IANA Time Zone Database](https://tc39.es/proposal-temporal/#sec-use-of-iana-time-zone-database) in the ECMA-402-amending part of the Temporal specification.

- **Available Named Time Zone Identifier** - Time zone name in TZDB (and accepted in ECMAScript).
  Available named time zone identifiers are ASCII-only and are case-insensitive.
  There are currently 594 available named time zone identifiers (avg length 14.3 chars).
  Currently fewer than 5 identifiers are added per year.
- **Primary Time Zone Identifier** - The preferred identifier for an available named time zone.
- **Non-primary Time Zone Identifier** - Other identifiers for an available named time zone.
  An available named time zone has one primary identifier and 0 or more non-primary ones.
- **Zone** - TZDB term for a collection of rules named by an identifier (see [How to Read the tz Database](https://data.iana.org/time-zones/tz-how-to.html) and [Theory and pragmatics](https://data.iana.org/time-zones/theory.html)).
  There are currently 461 Zones (avg length 14.9 chars).
  Except rare exceptions like `Etc/GMT`, all Zones in TZDB are primary time zone identifiers in ECMAScript.
- **Link** - TZDB term for an Identifier that lacks its own Zone record but instead targets another Identifier and uses its rules.
  When a Zone is renamed, a Link from the old name to the new one is added to [`backward`](https://github.com/eggert/tz/blob/main/backward).
  Renaming to update the spelling of a city happens every few years.
  There are currently 133 Links (avg length 12.2 chars).
  Links in TZDB are generally non-primary time zone identifiers in ECMAScript, but variation in TZDB build options means that some Links in some builds of TZDB are primary time zone identifiers in ECMAScript. 
- **Case-normalization** - Match user-provided IDs to case in IANA TZDB. Example: `america/los_angeles` ⇨ `America/Los_Angeles`
- **Canonicalization** - Return the IANA Zone, resolving Links if needed. Example: Europe/Kiev ⇨ Europe/Kyiv
- **CLDR Canonicalization** - Zone &amp; Link [data](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-bcp47/bcp47/timezone.json) used by V8 & WebKit (via ICU libraries)
- **IANA Canonicalization** - Zone &amp; Link [data](https://github.com/tc39/proposal-temporal/issues/2509#issuecomment-1461418026) used by Firefox (in custom TZDB build)

## Proposed Solution - Summary

Steps below are designed to be "severable"; if blocked due to implementation complexity and/or lack of consensus, we can still move forward on the others.

### Reduce variation between implementations, and between implementations and spec

1. **[DONE - Simplify abstract operations](#1-done---editorial-cleanup-of-identifier-related-terms-and-abstract-operations)** dealing with time zone identifiers.
2. **[DONE - Clarify spec](#2-done---clarify-spec-to-prevent-more-divergence)** to prevent more divergence
3. **[Help V8 and WebKit update 13 out-of-date canonicalizations](#3-fix-out-of-date-canonicalizations-in-v8webkit)** like `Asia/Calcutta`, `Europe/Kiev`, and `Asia/Saigon` before wide Temporal adoption makes this painful. (no spec text required)
4. [**Prescriptive spec text to reduce divergence between implementations.**](#4-prescriptive-spec-text-to-reduce-divergence-between-implementations)
   This step requires finding common ground between implementers as well as TG2 (the ECMA-402 team) about how canonicalization should work.

### Reduce impact of canonicalization changes

5. [**Avoid observable following of Links.**](#5-defer-link-traversing-canonicalization)
   If canonicalization changes don't affect existing code, then it's much less likely for future canonicalization changes to break the Web.
   Because canonicalization is implementation-defined, this change may (or may not; needs research) be safe to ship after Temporal Stage 4, but best to not wait too long.

```javascript
Temporal.TimeZone.from('Asia/Calcutta');
// => Asia/Kolkata (current Temporal behavior on Firefox)
// => Asia/Calcutta (proposed: don't follow Links when returning IDs to callers)
```

6. [**Add `Temporal.TimeZone.prototype.equals`.**](#6-add-temporaltimezoneprototypeequals)
   Because (5) would stop canonicalizing IDs upon `TimeZone` object creation, it'd be helpful to have an ergonomic way to know if two `TimeZone` objects represent the same Zone.

```javascript
// More ergonomic canonical-equality testing
Temporal.TimeZone.from('Asia/Calcutta').equals('Asia/Kolkata');
// => true
```

## Proposed Solution - Details

### 1. DONE - Editorial cleanup of identifier-related terms and Abstract Operations

_Status: Editorial PR merged as [tc39/ecma262#3035](https://github.com/tc39/ecma262/pull/3035)_

A recent PR landed in ECMA-262 refactored the spec text for time zone identifiers.
One change was a new [Time Zone Identifiers](https://tc39.es/ecma262/#sec-time-zone-identifiers) prose section that defines identifier-related terms and concepts.
The other change was refactoring time-zone-identifier-related abstract operations, so that other time-zine-identifier-related functionality in ECMA-262, ECMA-402, and Temporal (including the normative changes in this proposal) can be built of these without resorting to new non-implementation-defined AOs:

**`AvailableNamedTimeZoneIdentifiers()`** - Returns an implementation-defined List of Records, each composed of:

- `[[Identifier]]`: identifier in the IANA TZDB
- `[[PrimaryIdentifier]]`: identifier of transitive IANA Link target (following as many Links as necessary to reach a Zone), with the same special-casing of `"UTC"` as in ECMA-402's [CanonicalizeTimeZoneName](https://tc39.es/ecma402/#sec-canonicalizetimezonename).

**`GetAvailableNamedTimeZoneIdentifier(_identifier_)`** - Filters the result of `AvailableNamedTimeZoneIdentifiers` to return the record where `[[Identifier]]` is an ASCII-case-insensitive match for `_identifier_`, or `~empty~` if there's no match.
This AO:

- Replaces `CanonicalizeTimeZoneName` in [Temporal](https://tc39.es/proposal-temporal/#sec-canonicalizetimezonename) and [ECMA-402](https://tc39.es/ecma402/#sec-canonicalizetimezonename) by using the `[[PrimaryIdentifier]]` of the result.
- Replaces [`IsAvailableTimeZoneName`](https://tc39.es/proposal-temporal/#sec-isavailabletimezonename) in Temporal and [`IsValidTimeZoneName`](https://tc39.es/ecma402/#sec-isvalidtimezonename) in ECMA-402, by comparing the result to `~empty~`.
- Fetches a case-normalized time zone identifier by using the `[[Identifier]]` of the result.
  This capability will be used as part of this proposal.

The specification text of this proposal is stacked on top of these recently-merged editorial changes.

### 2. DONE - Clarify spec to prevent more divergence

_Status: Editorial PR merged as [tc39/proposal-temporal#2573](https://github.com/tc39/proposal-temporal/pull/2573)._

The ECMA-402 section of the Temporal spec now includes a new [Use of the Time Zone Database](https://tc39.es/proposal-temporal/#sec-use-of-iana-time-zone-database) section that recommends best practices for building and handling updates to the IANA Time Zone Database.

These recommendations are broad enough to encompass existing implementations in Firefox and V8/WebKit but not any broader than that.
For example, all ECMAScript implementations seem to avoid use of the the default TZDB build options that perform over-eager canonicalization like `Atlantic/Reykjavik=>Africa/Abidjan`.
We will recommend that all implementations follow this best practice.

The goal of these changes was to provide a web-reality baseline that further cross-implementation alignment can build on.

### 3. Fix out-of-date canonicalizations in V8/WebKit

_Status: At a CLDR meeting on 2023-03-29, CLDR [agreed](https://unicode-org.atlassian.net/browse/CLDR-14453?focusedCommentId=169191) to develop a design proposal to provide IANA current canonicalization info._
_Please follow https://unicode-org.atlassian.net/browse/CLDR-14453 for updates on progress._

The list below shows 13 Links that have been superseded in IANA and Firefox, but still canonicalize to the "old" identifier in CLDR (and hence ICU and therefore V8 and WebKit).
The data below comes from the 2022g version of TZDB, via a simple [CodeSandbox app](https://4rylir.csb.app/) that tests browsers' canonicalization behavior.

There is some urgency to fix these outdated Links because as noted [above](#Temporal-makes-these-problems-more-disruptive), changing canonicalization after Temporal is widely adopted will cause more churn and customer complaints.

To fix these outdated Links, we'd partner with representatives from V8 and WebKit (and maybe ICU and CLDR too) to see if there's a quick, low-cost way for V8/WebKit to update canonicalization of these 13 Zones.

Note that renaming of TZDB identifiers is very infrequent.
From a review of the TZDB [NEWS](https://data.iana.org/time-zones/tzdb/NEWS) file, there was only one rename per year from 2020-2022.
Before that, the last rename was Rangoon => Yangon in 2016.
Ideally ICU would provide a timely solution to these outdated identifiers.
But in the meantime, if implementations had to hand-code overrides in a special-case list, then it would not need to be updated often.

```javascript
// [0] => canonical in V8/WebKit (from CLDR)
// [1] => canonical in Firefox (from IANA)
// [2] => non-canonical Link (if present)
const outofDateLinks = [
  ['Asia/Calcutta', 'Asia/Kolkata'],
  ['Europe/Kiev', 'Europe/Kyiv'],
  ['Asia/Saigon', 'Asia/Ho_Chi_Minh'],
  ['Asia/Rangoon', 'Asia/Yangon'],
  ['Asia/Ulaanbaatar', 'Asia/Ulan_Bator'],
  ['Asia/Katmandu', 'Asia/Kathmandu'],
  ['Africa/Asmera', 'Africa/Asmara'],
  ['America/Coral_Harbour', 'America/Atikokan'],
  ['Atlantic/Faeroe', 'Atlantic/Faroe'],
  ['America/Godthab', 'America/Nuuk'],
  ['Pacific/Truk', 'Pacific/Chuuk', 'Pacific/Yap'],
  ['Pacific/Enderbury', 'Pacific/Kanton'],
  ['Pacific/Ponape', 'Pacific/Pohnpei']
];
```

### 4. Prescriptive spec text to reduce divergence between implementations

_Status: At this point it seems unlikely that we'll get this cross-implementer agreement soon. So it's likely that we'll remove this step from the scope of this proposal, and follow up separately in parallel._

This step involves agreement between implementers and TG2 about how canonicalization should work.
It may require agreeing on (or recommending) which external source of canonicalization (IANA or CLDR) ECMAScript should rely on, and (if IANA) which TZDB build options should be used.
Making progress here requires input from specifiers and implementers who understand the tradeoffs involved.
Note that one acceptable outcome may be to “agree to disagree” as long as we can agree on most parts.
We don’t need perfect alignment to reduce ecosystem variance.

There's useful info in [@anba](https://github.com/anba)'s comments [here](https://github.com/tc39/proposal-temporal/issues/2509#issuecomment-1461418026) that could be used as a starting point.

It will likely be much easier to achieve consensus on this spec text after progress is made on (3) above, because those 13 outdated Links are the largest current difference in canonicalization behavior between Firefox and V8/WebKit.

### 5. Defer Link-traversing canonicalization

_Status: [Spec text](https://tc39.es/proposal-canonical-tz), [polyfill](./polyfill/README.md), and [tests](https://github.com/tc39/test262/pull/3837) are complete._

This normative change would defer Link traversal to enable a Link identifier to be stored in internal slots of `ZonedDateTime`, `TimeZone`, and  `Intl.DateTimeFormat`, so that it can be returned back to the user.

The justification for this change is that canonicalization itself is problematic because it always makes at least some people unhappy: developers of existing code are annoyed when their code behaves differently, while other developers are annoyed if outdated identifiers are used.
To sidestep both problems, this proposed change would make canonicalization mostly invisible to Temporal users, except one place: time zone identifiers returned from `Temporal.Now`.

A tradeoff of this change is that comparing the string representation of `TimeZone` objects (or their `id` properties, or the time zone slot of `Temporal.ZonedDateTime`) would no longer be a reliable way to test for equality.
Therefore, (6) below proposes a new `TimeZone.prototype.equals` API.

This change requires the following normative edits:

- a) Change `GetAvailableNamedTimeZoneIdentifier(id).[[PrimaryIdentifier]]` to `GetAvailableNamedTimeZoneIdentifier(id).[[Identifier]]` in places where user input identifiers are parsed and/or stored.
- b) Call `GetAvailableNamedTimeZoneIdentifier(id).[[PrimaryIdentifier]]` before using identifiers for purposes that require canonicalization, such as the `TimeZoneEquals` abstract operation.

These changes are described in the [spec text](https://tc39.es/proposal-canonical-tz), [polyfill](./polyfill/README.md), and [tests](https://github.com/tc39/test262/pull/3837) of this proposal.

A few performance-related notes:

- Storing user-input identifier strings is not necessary because identifiers are case-normalized by `GetCanonicalTimeZoneIdentifier` before storing.
  There are fewer than 600 identifiers, so built-in time zone identifiers could be stored as a 2-byte (or even 10-bit) indexes into a ~9KB array of ASCII strings.
- This proposal WOULD NOT require storing both original and canonical ID indexes in each `TimeZone`, `ZonedDateTime`, and `Intl.DateTimeFormat` instance.
  Implementations could choose to do this for ease of implementation, but they can also save 1-2 bytes per instance by canonicalizing just-in-time via a 2.3KB map of each identifier's index to its corresponding Zone's identifier's index.

### 6. Add `Temporal.TimeZone.prototype.equals`

_Status: [Spec text](https://tc39.es/proposal-canonical-tz), [polyfill](./polyfill/README.md), and [tests](https://github.com/tc39/test262/pull/3837) are complete._

The final step would expose Temporal's [`TimeZoneEquals`](https://tc39.es/proposal-temporal/#sec-temporal-timezoneequals) to ECMAScript code to enable developers to compare two time zones to see if they resolve to the same Zone.

```javascript
// More ergonomic canonical-equality testing
Temporal.TimeZone.from('Asia/Calcutta').equals('Asia/Kolkata');
// => true
```

This `equals` pattern matches how other Temporal types like `ZonedDateTime` and `PlainDate` offer equality comparisons.

Behavior of `ZonedDateTime.prototype.equals` API would not change, because it (just like all other APIs other than those that return identifiers) would canonicalize before using time zone identifiers.

A reason to include this new API in this proposal instead of waiting until later is that it'd prevent the pattern `tz1.id === tz2.id` from becoming endemic in ECMAScript code, because that pattern will be broken by this proposal.

Without this API, testing for canonical equality is still possible, it's just less ergonomic:

```javascript
const EPOCH = Temporal.Instant.fromNanoseconds(0n);
function canonicalEquals(zone1, zone2) {
  const zdt1 = EPOCH.toZonedDateTimeISO(zone1);
  const zdt2 = EPOCH.toZonedDateTimeISO(zone2);
  return zdt1.equals(zdt2);
}
```

Longer-term extensions (out of scope to this proposal) could be added to force canonicalization at creation time:

```javascript
Temporal.TimeZone.from('Asia/Calcutta', { canonicalize: 'full' });
// => Asia/Kolkata
// Opt-in canonicalization
Temporal.TimeZone.canonicalize('Asia/Calcutta');
// => Asia/Kolkata
```

That said, exposing canonical identifiers has been a source of grief in every software platform.
So adding APIs that make canonicalization more visible might invite more user complaints.
This is another good reason to defer these kinds of APIs until a later proposal. :smile:

## TZDB size calculations

Source: https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-bcp47/bcp47/timezone.json

```javascript
// all identifiers
ianaIdLists = Object.values(t.keyword.u.tz)
  .map((tz) => tz._alias)
  .filter((s) => s)
  .map((s) => s.split(/,* /g));
ids = ianaIdLists.flat();
zones = ianaIdLists.map((list) => list[0]);
links = ianaIdLists.flatMap((list) => list.slice(1));

[ids, zones, links].map((arr) => arr.length);
// => [594, 461, 133]

avgLength = (arr) => arr.join('').length / arr.length;
[ids, zones, links].map((arr) => avgLength(arr).toFixed(1));
// => [14.3, 14.9, 12.2]
```

CLDR Links and Zones above used in V8 and WebKit aren't exactly the same as IANA data used in Firefox.
But CLDR is close enough that the numbers above should be within 20% of Firefox stats.

## References

### ICU4X

Rust localization API (including Temporal-friendly [timezone API](https://github.com/unicode-org/icu4x/tree/main/components/timezone)) that's being implemented now.

See https://github.com/unicode-org/icu4x/issues/2909 for canonicalization API discussion.

### IANA Time Zone Database ([TZDB](https://www.iana.org/time-zones))

Standard repository of time zone data, including Link and Zone identifiers and data required to calculate the UTC offset of moments in time for any time zone.

Maintained via PRs to the [eggert/tz](https://github.com/eggert/tz) repo, with discussion on the [TZDB mailing list](https://mm.icann.org/pipermail/tz/).

The data in the TZDB repo is not intended to be used raw.
Instead, the repo's MAKEFILE offers various build options which will generate data files for use by applications.
Changes in build options can yield very different output, including large differences in canonicalization behavior.

One of the goals of this proposal is to define which of these build options should be used by ECMAScript implementations.

### [global-tz](https://github.com/JodaOrg/global-tz) repo

Provides pre-built TZDB data files using build options that are more aligned with the needs of Java (and also ECMAScript) than the default TZDB build options.

The files in global-tz are claimed (by the [TZDB News](https://github.com/eggert/tz/blob/27148539e699d9abe50df84371a077fdf2bc13de/NEWS#L427-L430) file) to be the same as the results of building TZDB with `make PACKRATDATA=backzone PACKRATLIST=zone.tab`.
This build configuration backs out undesirable (from ECMAScript's point of view) merging of unrelated time zones like `Atlantic/Reykjavik` and `Africa/Abidjan` that may diverge in the future.

Also, this build configuration is similar to the Zones and Links used by Firefox.

This repo is maintained by the champion of [JSR-310](https://jcp.org/en/jsr/detail?id=310), the current Java date/time API and maintainer of the [Joda](https://github.com/JodaOrg/joda-time) date/time API library which is used by older Java implementations and which JSR-310 was based on.

Note that the string serialization format of `Temporal.ZonedDateTime`, including use of IANA time zone identifiers, was designed to be interoperable with [`java.time.ZonedDateTime`](https://docs.oracle.com/javase/8/docs/api/java/time/ZonedDateTime.html).
In addition, ECMAScript's time zone use cases are similar to Java's.
So this may be a useful standard TZDB build configuration to consider recommending for in ECMAScript.
<br>