#Stage0Tag
Classification: [[Syntactic Change]]
Human Validated: KW
Title: as destructuring patterns
Authors: Kat Marchán
Champions: Kat Marchán
Date: None
Last Commit: None
GitHub Link: https://github.com/zkat/proposal-as-patterns
GitHub Note Link: None

# Proposal Description:

# ECMAScript As-Patterns for Matching and Destructuring

## [Status](https://tc39.github.io/process-document/)

**Stage**: 0

**Author**: Kat Marchán (npm, [@maybekatz](https://twitter.com/maybekatz))

**Champions**: Kat Marchán (npm, [@maybekatz](https://twitter.com/maybekatz))

## Introduction

When matching non-Identifier values, it's often the case that users might want
to also bind that value to an Identifier while doing the matching. For this
reason, it's proposed that destructuring be extended with the ability to do
this sort of binding. Furthermore, the separate [pattern matching
proposal](https://github.com/tc39/proposal-pattern-matching) will benefit from
this change by allowing matching operations against values that are also put
into identifiers, since identifiers are irrefutable patterns.

The syntax uses an `as` keyword, and looks as follows:

```js
const {x: {y} as x} = {x: {y: 1}}
// x is {y: 1}
// y is 1
```

Or:
```js
function foo ([{y} as x, [z] as zed = [1]]) {
  // x is {y: ...}
  // y is x.y
  // z is runs an initializer if arguments[0][1] is undefined
}
```

This applies similarly to `match`:
```js
match (x) {
  when {x: {y: 1} as x} ~> console.log(x.y === 1)
}
```

Note: This syntax is [used by
F#](https://docs.microsoft.com/en-us/dotnet/fsharp/language-reference/pattern-matching).
It's also reminiscent of `as` syntax in `import` statements, so there's some
precedent in the language for this sort of binding (`import * as bar from
'./x.js'`)

## The Big Picture

### Related Active Proposals

* [Pattern matching](https://github.com/tc39/proposal-pattern-matching)
* [Collection literals](https://github.com/zkat/proposal-collection-literals)

## As-Patterns

### Syntax

**12.15.5 Destructuring Assignment Changes**:
```
AssignmentRebinding :
  `as` IdentifierReference

AssignmentElement :
  DestructuringAssignmentTarget
  DestructuringAssignmentTarget AssignmentRebinding
  DestructuringAssignmentTarget Initializer
  DestructuringAssignmentTarget AssignmentRebinding Initializer
```

**13.3.3 Destructuring Binding Patterns Changes**:
```
BindingRebinding :
  `as` IdentifierReference

BindingElement :
  SingleNameBinding
  BindingPattern
  BindingPattern BindingRebinding
  BindingPattern Initializer
  BindingPattern BindingRebinding Initializer
```

**[Match Operator](https://github.com/tc39/proposal-pattern-matching) Syntax Changes**:
```
MatchRebinding :
  `as` IdentifierReference

MatchElement :
  SingleNameBinding
  MatchPattern
  MatchPattern MatchRebinding
  MatchPattern Initializer
  MatchPattern MatchRebinding Initializer
```