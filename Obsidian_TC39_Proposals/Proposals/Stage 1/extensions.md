[[Stage 1]]<br>Classification:  [[Syntactic Change]] [[Semantic Change]] <br>Human Validated: KW<br>Title: Extensions<br>Authors: HE Shi-Jun<br>Champions: HE Shi-Jun<br>Last Presented: November 2020<br>Stage Upgrades:<br>Stage 1: 2020-12-29  
Stage 2: NA  
Stage 2.7: NA  
Stage 3: NA  
Stage 4: NA<br>Last Commit: 2023-01-18<br>Topics: #others #objects<br>Keywords: #extension #accessor #namespace <br>GitHub Link: https://github.com/tc39/proposal-extensions <br>GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2020-11/nov-19.md#extensions-for-stage-1
# Proposal Description:
# Extensions and `::` operator

## Proposal status

This is an ECMAScript (JavaScript) proposal in stage 1.

Note: The proposal could be seen as the reshape of the "virtual method" part of the old [[bind-syntax]] proposal, see https://github.com/tc39/proposal-bind-operator/issues/56.

## Simple examples

### Example of ad-hoc extension methods and accessors
```js
// define two extension methods
const ::toArray = function () { return [...this] }
const ::toSet = function () { return new Set(this) }

// define a extension accessor
const ::allDivs = {
	get() { return this.querySelectorAll('div') }
}

// reuse built-in prototype methods and accessors
const ::flatMap = Array.prototype.flatMap
const ::size = Object.getOwnPropertyDescriptor(Set.prototype, 'size')

// Use extension methods and accesors to calculate
// the count of all classes of div element.
let classCount = document::allDivs
	::flatMap(e => e.classList::toArray())
	::toSet()::size
```

roughly equals to:

```js
// define two extension methods
const $toArray = function () { return [...this] }
const $toSet = function () { return new Set(this) }

// define a extension accessor
const $allDivs = {
	get() { return this.querySelectorAll('div') }
}

// reuse built-in prototype method and accessor
const $flatMap = Array.prototype.flatMap
const $size = Object.getOwnPropertyDescriptor(Set.prototype, 'size')

// Use extension methods and accesors to calculate
// the count of all classes of div element.
let $
$ = $allDivs.get.call(document)
$ = $flatMap.call($, e => $toArray.call(e.classList))
$ = $toSet.call($)
$ = $size.get.call($)
let classCount = $
```

### Example of using constructors or namespace object as extensions

```js
// util.js
export const toArray = iterable => [...iterable]
export const toSet = iterable => new Set(iterable)
```

```js
import * as util from './util.js'

const ::allDivs = {
	get() { return this.querySelectorAll('div') }
}

let classCount = document::allDivs
	::Array:flatMap(
		e => e.classList::util:toArray())
	::util:toSet()
	::Set:size
```

roughly equals to:

```js
import * as util from './util.js'

const $allDivs = {
	get() { return this.querySelectorAll('div') }
}

let $
$ = $allDivs.get.call(document)
$ = Array.prototype.flatMap.call($,
	e => util.toArray(e.classList))
$ = util.toSet($)
$ = Object.getOwnPropertyDescriptor(Set.prototype, 'size').get.call($)
let classCount = $
```

## Changes of the old bind operator proposal

- keep `obj::foo()` syntax for extension methods
- repurpose `obj::foo` as extension getters and add `obj::foo =` as extension setters
- separate namespace for ad-hoc extension methods and accessors, do not pollute normal binding names
- add `obj::ext:name` syntax
- change operator precedence to same as `.`
- remove `::obj.foo` (use cases can be solved by custom extension + library, or other proposals)

## Other matrials

- [design details](docs/design.md)
- [slide for stage 1](https://johnhax.net/2020/tc39-nov-ext/slide)
- [experimental implementation](experimental)
<br>