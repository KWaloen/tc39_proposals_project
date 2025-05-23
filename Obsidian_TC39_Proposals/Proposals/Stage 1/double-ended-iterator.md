[[Stage 1]]<br>Classification: [[API Change]]<br>Human Validated: KW<br>Title: Double-Ended Iterator and Destructuring<br>Authors: HE Shi-Jun<br>Champions: HE Shi-Jun<br>Last Presented: September 2020<br>Stage Upgrades:<br>Stage 1: 2022-01-23  
Stage 2: NA  
Stage 2.7: NA  
Stage 3: NA  
Stage 4: NA<br>Last Commit: 2022-07-21<br>Topics: #iterators #arrays #objects<br>Keywords: #iterator #generator #array #destructuring <br>GitHub Link: https://github.com/tc39/proposal-deiter <br>GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2020-09/sept-24.md#double-ended-iterator-and-destructuring-for-stage-1
# Proposal Description:
# Double-Ended Iterator and Destructuring

Status: Stage 1

Author: HE Shi-Jun (hax)

Champion: HE Shi-Jun (hax)

- [Advanced to Stage 1 on Sept 2020](https://github.com/tc39/notes/blob/main/meetings/2020-09/sept-24.md#double-ended-iterator-and-destructuring-for-stage-1)
- [Incubator call on Dec 3, 2020](https://github.com/tc39/incubator-agendas/blob/main/notes/2020/12-03.md)
- [Stage 0 -> 1 (outdated) presentation](https://johnhax.net/2020/tc39-sept-deiter/slide)
- [Stage 1 update on July 21, 2022](https://johnhax.net/2022/deiter/slide)

## Motivation

Python and Ruby support `(first, *rest, last) = [1, 2, 3, 4]`, CoffeeScript supports `[first, rest..., last] = [1, 2, 3, 4]`, and Rust supports `[first, rest @ .., last] = [1, 2, 3, 4]`, all resulting in `first` be `1`, `last` be `4`, and `rest` be `[2, 3]`. But [surprisingly](https://stackoverflow.com/questions/33064377/destructuring-to-get-the-last-element-of-an-array-in-es6) `[first, ...rest, last] = [1, 2, 3, 4]` doesn't work in JavaScript.

And in some cases we really want to get the items from the end, for example getting `matchIndex` from [String.prototype.replace when using a function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace#Specifying_a_function_as_a_parameter):

```js
string.replace(pattern, (fullMatch, ...submatches, matchIndex, fullString) => {
  // `matchIndex` is always the second to last param (the full string is the last param).
  // There may be many submatch params, depending on the pattern.
})
```

## Solution

A naive solution is making `let [first, ...rest, last] = iterable` work as

```js
let [first, ...rest] = iterable
let last = rest.pop()
```

The concern is it requires saving all items in the `rest` array, although you may only need `last`. A possible mitigation is supporting `[..., last] = iterable` which saves the memory of `rest`, but you still need to consume the entire iterator. In the cases where `iterable` is a large array or something like `Number.range(1, 100000)`, it's very inefficient. And in case like `let [first, ..., last] = repeat(10)` which `repeat` is a generator returns infinite sequence of a same value, theoretically both `first` and `last` could be `10`, but you just get a dead loop.

Instead of the naive solution, we introduce the double-ended iterator (like Rust std::iter::DoubleEndedIterator). A double-ended iterator could be consumed from both ends, `next()` consume the first item from the rest items of the sequence, `nextLast()` consume the last item from the rest items of the sequence.

```js
let a = [1, 2, 3, 4, 5, 6]
let deiter = a.values() // suppose values() would be upgraded to return a double-ended iterator
deiter.next() // {value: 1}
deiter.next() // {value: 2}
deiter.nextLast() // {value: 6}
deiter.next() // {value: 3}
deiter.nextLast() // {value: 5}
deiter.nextLast() // {value: 4}
deiter.nextLast() // {done: true}
deiter.next() // {done: true}
```

With double-ended iterators, `let [a, b, ..., c, d] = iterable` would roughly work as

```js
let iter = iterable[Symbol.iterator]()
let a = iter.next().value
let b = iter.next().value
let d = iter.nextLast().value
let c = iter.nextLast().value
iter.return()
```

## Generator

Generator functions provide a concise syntax to create iterators in the userland. For example, you can write `values(arrayLike)` which returns iterator for all array-likes:

```js
function *values(arrayLike) {
  let i = 0
  while (i < arrayLike.length) {
    yield arrayLike[i]
    i++
  }
}
```

To implement double-ended version of `values(arrayLike)` in userland, we could use the [`doubleEnded` helper](double-ended-helper.js):

```js
const values = doubleEnded(function *values(arrayLike, context) {
  let i = 0, j = 0
  while (i + j < arrayLike.length) {
    if (context.method == "nextLast") {
      yield arrayLike[arrayLike.length - 1 - j]
      j++
    } else { // context.method == "next"
      yield arrayLike[i]
      i++
    }
  }
})
```
It could also be used as [[decorators]] (stage 3 proposal):
```js
class IntRange {
  constructor(start, end) {
    if (!Number.isSafeInteger(start)) throw new TypeError()
    if (!Number.isSafeInteger(end)) throw new TypeError()
    this.start = start; this.end = end; Object.freeze(this)
  }
  @doubleEnded *[Symbol.iterator](context) {
    let {start, end} = this
    while (start < end) {
      if (context.method == "nextLast") yield --end
      else yield start++
    }
  }
}
```

## Iterator helpers and reverse iterator

[[Iterator-helpers]] add some useful methods to iterators and async iterators. Most methods are easy to upgrade to support double-ended. For example, `map()` could be implemented like:

```js
// only for demonstration, the real implementation should use internal slots
Iterator.prototype.map = function (fn) {
  let iter = {
    __proto__: Iterator.prototype,
    return(value) { this.return?.(); return {done: true, value} }
  }
  if (this.next) iter.next = () => fn(this.next())
  if (this.nextLast) iter.nextLast = () => fn(this.nextLast())
  return iter
}
// usage
let [first, ..., last] = [1, 2, 3].values().map(x => x * 2)
first // 2
last // 6
```

Furthermore, some extra iterator helpers like `toReversed`, `takeLast`, `dropLast` and `reduceRight`, etc. could be introduced.

For example, `toReversed()`:

```js
// only for demonstration, the real implementation should use internal slots
Iterator.prototype.toReversed = function () {
  let next = this.nextLast?.bind(this)
  let nextLast = this.next?.bind(this)
  let ret = this.return?.bind(this)
  return {
    __proto__: Iterator.prototype,
    next, nextLast, return: ret,
  }
}
// usage
let a = [1, 2, 3, 4]
let [first, ..., last] = a.values().toReversed()
first // 4
last // 1
```

With double-ended iterators and `toReversed()` helpers, we may not need [[reverse-iteration]]. Even we still want reverse iterator as a separate protocol, we could also easily have a default implementation for it.

```js
Iterator.prototype[Symbol.reverseIterator] = function () {
  return this[Symbol.iterator].toReversed()
}
```

## FAQ

### I like the idea of allowing `...` in the middle of the destructuring pattern, but why introduce "double-ended" iterator?

Because JavaScript `[first, ...rest] = sequence` destructuring is based on iterable protocol, so we should make `[first, ...rest, last] = sequence` also based on iterable protocol. And `[a, b, ...rest, c, d, e] = sequence` could be perfectly interpreted as "take first two elements from the sequence, then take last three, and the rest", aka. allowing take elements from the the other end of a sequence, which conceptually same as what "double-ended" mean in the common data structure [deque](https://en.wikipedia.org/wiki/Double-ended_queue).  Note JavaScript already have some Array APIs behave as double-ended: 'indexOf/lastIndexOf, reduce/reduceRight, find/findLast', etc. So generalizing the concept could increase the consistency of all APIs (include user-land libraries) which may based on similar abstraction. See [Optional Mechanisms for Double-ended Destructructing](https://github.com/tc39/proposal-deiter/blob/main/why-deiter.md) for further analysis about the consideration of performance, mental burden and design cost.

### How could a iterator/generator move back to the previous status?

It's not "move back" or "step back", it's "consume the next value from the other end" or "shorten range of values from the other end".

There are two concepts easy to confuse, _bidirectional_ vs. _double-ended_. Bidirectional means you can invoke `next()` (move forward) or `previous()` (move backward). Double-ended means you can invoke `next()` (consume the first item from the rest items of the sequence) or `nextLast()` (consume the last item from the rest items of the sequence).

The initial version of this proposal used `next("back")` which follow Rust `nextBack()`. The term "back" may come from C++ vector/deque (see https://cplusplus.com/reference/vector/vector/back/), means "last element". This term usage is not popular in JavaScript ecosystem and cause confusion, so we changed the word from "back" to "last".

### What is "double-ended", how it differ to "bidirectional"?

To help understand the concepts, you could imagine you use cursors point to positions of a sequence and get value at the position. Normal iteration need only one cursor, and initally the cursor is at the most left side of the sequence. You are only allowed to move the cursor to right direction and get the value of the position via `next()`. Bidrectional means you could also move the cursor to left direction via `previous()`, so go back to the previous position of the sequence, and get the value (again) at the position. 

Double-ended means you have **two** cursors and initally one is at the most left side and can only move to right direction, the other is at most right side and can only move to left direction. So you use `next()` move the first cursor to right and get the value at its position, use `nextLast()` move the second cursor to left and get the value at its position. If two cursors meet the same postion, the sequence is totally consumed. 

You could find these two concept are actually orthogonal, so theorcially we could have both bidirectional and double-ended. So `next()`/`previous()` move the first cursor right/left, `nextLast()`/`previousLast()` move the second cursor left/right.

Note, even these two things could coexist, bidirectional is **not** compatible with JavaScript iterator protocol, because JavaScript iterators are one-shot consumption, and produce `{done: true}` if all values are consumed, and it is required that `next()` always returns `{done: true}` after that, but `previous()` actually require to restore to previous, undone state. 

## Prior art
- Python [iterable unpacking](https://www.python.org/dev/peps/pep-3132/)
- Ruby [array decomposition](https://docs.ruby-lang.org/en/2.7.0/doc/syntax/assignment_rdoc.html#label-Array+Decomposition)
- CoffeeScript [destructuring assignment with splats](https://coffeescript.org/#destructuring)
- Rust [subslice pattern](https://rust-lang.github.io/rfcs/2359-subslice-pattern-syntax.html)
- Rust [std::iter::DoubleEndedIterator](https://doc.rust-lang.org/std/iter/trait.DoubleEndedIterator.html)
- Rust [Macro improved_slice_patterns::destructure_iter](https://docs.rs/improved_slice_patterns/2.0.1/improved_slice_patterns/macro.destructure_iter.html)

## Previous discussions
- https://github.com/tc39/proposal-array-last/issues/31
- https://github.com/tc39/proposal-reverseIterator/issues/1
- https://es.discourse.group/t/bidirectional-iterators/339

## Old discussions
- https://esdiscuss.org/topic/early-spread-operator
- https://esdiscuss.org/topic/parameter-lists-as-arguments-destructuring-sugar#content-3
- https://mail.mozilla.org/pipermail/es-discuss/2012-June/023353.html
- http://web.archive.org/web/20141214094119/https://bugs.ecmascript.org/show_bug.cgi?id=2034
- https://esdiscuss.org/topic/rest-parameter-anywhere
- https://esdiscuss.org/topic/rest-parameters
- https://esdiscuss.org/topic/strawman-complete-array-and-object-destructuring
- https://esdiscuss.org/topic/an-update-on-rest-operator
<br>