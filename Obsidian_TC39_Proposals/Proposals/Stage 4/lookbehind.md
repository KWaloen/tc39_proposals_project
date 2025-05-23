[[Stage 4]]<br>Classification: [[Syntactic Change]] [[Semantic Change]]<br>Human Validated: KW<br>Title: RegExp Lookbehind Assertions<br>Authors: Gorkem Yakin, Nozomu Katō, Daniel Ehrenberg<br>Champions: Daniel Ehrenberg, Mathias Bynens<br>Last Presented: January 2018<br>Stage Upgrades:<br>Stage 1: NA  
Stage 2: 2016-12-06  
Stage 2.7: NA  
Stage 3: 2017-03-22  
Stage 4: 2018-01-24<br>Last Commit: 2018-01-26<br>Topics: #others #regex<br>Keywords: #assertions #pattern_matching #regex<br>GitHub Link: https://github.com/tc39/proposal-regexp-lookbehind <br>GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2018-01/jan-23.md#conclusionresolution-16
# Proposal Description:
# RegExp Lookbehind Assertions

Authors: Gorkem Yakin, Nozomu Katō, Daniel Ehrenberg

Stage 4

## Introduction

Lookarounds are zero-width assertions that match a string without consuming anything. ECMAScript has lookahead assertions that does this in forward direction, but the language is missing a way to do this backward which the lookbehind assertions provide. With lookbehind assertions, one can make sure that a pattern is or isn't preceded by another, e.g. matching a dollar amount without capturing the dollar sign.

## High Level API

There are two versions of lookbehind assertions: positive and negative.

Positive lookbehind assertions are denoted as `(?<=...)` and they ensure that the pattern contained within precedes the pattern following the assertion. For example, if one wants to match a dollar amount without capturing the dollar sign, `/(?<=\$)\d+(\.\d*)?/` can be used, matching `'$10.53'` and returning `'10.53'`. This, however, wouldn't match `€10.53`.

Negative lookbehind assertions are denoted as `(?<!...)` and, on the other hand, make sure that the pattern within doesn't precede the pattern following the assertion. For example, `/(?<!\$)\d+(?:\.\d*)/` wouldn't match `'$10.53'`, but would `'€10.53'`.

All regular expression patterns, even unbounded ones, are allowed as part of lookbehind assertions. Therefore, one could, for example, write `/(?<=\$\d+\.)\d+/` to match a dollar amount and capture just the fraction part.

Patterns normally match starting from the leftmost sub-pattern and move on to the sub-pattern on the right if the left sub-pattern succeeds. When contained within a lookbehind assertion, the order of matching would be reversed. Patterns would match starting from the rightmost sub-pattern and advance to the left instead. For example, given `/(?<=\$\d+\.)\d+/`, the pattern would first find a number and ensure first that it is preceded by `.` going backward, then `\d+` starting from `.`, and lastly `$` starting from where `\d+` within the assertion begins. The backtracking direction would also be reversed as a result of this.

## Details

Within a lookbehind, the semantics are that match proceeds backwards--the RegExp fragment within the backreference is reversed, and the string is traversed from end to start. This has a few implications on the semantics.

An earlier proposal was to disallow unbounded repetitions within backreferences. Perl uses these more limited semantics. However, it appears to be possible to implement more broad semantics providing for unbounded repetitions if the details are nailed down in a particular way. A draft implementation exists in V8 with these semantics.

### Greediness proceeds from right to left

Firstly, capture groups within a lookbehind assertion would have different values compared to when they are outside if the groups have sub-patterns with greedy quantifiers. When within a lookbehind assertion, groups on the right would capture most characters rather than the ones on the left. For example, given `/(?<=(\d+)(\d+))$/` and the string `'1053'`, the second group would capture `'053'` and the first group would be `'1'`. With `/^(\d+)(\d+)/`, on the other hand, the first group would capture `'105'` and the second group would be `'3'`.

### Numbering capture groups

Within a lookbehind, capture groups are numbered left to right. In the example `/(?<=(\d+)(\d+))$/` matched against the string `'1053'`, `match[1]` would be `"1"` and `match[2]` would be `"053"`.

### Referring to capture groups

Within a backreference, it is only possible to refer to captured groups that have already been evaluated. That is, the group has to be to the right of the backreference. For example, `/(?<=(.)\1)/` would not be a very useful RegExp, as `\1` cannot be resolved and would match against the empty string. Instead, to look for two copies of the same letter preceding the contents, one would write `/(?<=\1(.))/`.

### Negative assertions

Analogous to the negative lookahead assertion `/(?!.)/` long present in ECMAScript RegExps, this proposal includes a negative lookbehind assertion `/(?<!.)/`.

## Draft specification

[specification fragment](https://tc39.github.io/proposal-regexp-lookbehind/) by Thomas Wood and Claude Pache.

## Implementations

* [V8](https://bugs.chromium.org/p/v8/issues/detail?id=4545), shipping in Chrome 62
* [XS](https://github.com/Moddable-OpenSource/moddable/blob/public/xs/sources/xsre.c), in [January 17, 2018 update](http://blog.moddable.tech/blog/january-17-2017-big-update-to-moddable-sdk/)
<br>