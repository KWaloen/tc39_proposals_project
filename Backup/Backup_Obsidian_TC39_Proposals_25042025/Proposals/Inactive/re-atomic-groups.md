[[Inactive]]<br>Classification: [[Semantic Change]] [[Syntactic Change]]<br>Human Validated: KW<br>Title: RegExp Atomic Groups & Possessive Quantifiers<br>Authors: Justin Ridgewell<br>Never presented; engines are not interested in the feature, mainly because it doesn't solve backtracking for most users<br>Last Presented: None<br>Stage Upgrades:<br>Stage 1: NA
Stage 2: NA  
Stage 2.7: NA  
Stage 3: NA  
Stage 4: NA<br>Last Commit: 2020-01-26<br>Keywords: #regex #concurrency #atomic <br>GitHub Link: https://github.com/jridgewell/proposal-regexp-atomic-and-possessive <br>GitHub Note Link: None
# Proposal Description:<br>
# proposal-regexp-atomic-and-possessive

A proposal to add Atomic Groups and Possessive Quantifiers to `RegExp`s.

## Atomic Groups

Atomic groups, denoted by `(?>TEXT_TO_MATCH)`, prevent backtracking once
the group matches and "locks". Even if backtracking into an alternate
branch could allow a full match, the atomic group will not unlock.

```js
const atomic = /a(?>bc|b)c/;

// (?>bc) matches, so atomic group "locks".
// Then, the "c" after the group matches.
atomic.test('abcc'); // => true

// (?>bc) matches, so atomic group "locks".
// The rest of the expression no longer matches.
// Because the atomic group is locked, it will **not** backtrack
// to the alternate (b) branch.
atomic.test('abc'); // => false

// Atomic groups do not capture their match.
atomic.exec('abcc'); // => ['abcc']
```

## Possessive Quantifiers

Possessive quantifiers, denoted by using `+` after a quantifier, prevent
backtracking once the token has matched. Even if backtracking would
allow a full match, the possessive quantifier will not allow it.

```js
const possessive = /^(a|.b)++$/;

// (a) matches
possessive.test('a'); // => true
// (a) matches, then (.b) matches
possessive.test('abb'); // => true

// (a) matches, (a) matches, but we can't match "b"
// Because it's possessive, it will not **not** backtrack
// to the (.b) branch.
possessive.test('aab'); // => false
```

## Champions

- Justin Ridgewell ([@jridgewell](https://github.com/jridgewell/))

## Status

Current [Stage](https://tc39.es/process-document/): 0

## Motivation

JavaScript's Regular Expressions are great, but developers can
unintentionally write one with "catastrophic backtracking". These regexs
can completely freeze the program, and is especially dangerous for
servers.

Atomic Groups and Possessive Quantifiers allow developers to write
understandable performance guarantees. Since they do not allow
backtracking, they'll never suffer exponential execution time.

```js
const regex = /^(a|[ab])*$/;

function test(length) {
  const str = 'a'.repeat(length) + 'c';
  const now = performance.now();
  regex.test(str);
  return performance.now() - now;
}

for (let i = 0; i < 50; i++) {
  console.log({ length: i, time: test(i) });
}
```

| String Length | Time (seconds) |
|--------------:|---------------:|
|       ...snip |           0.00 |
|            19 |           0.01 |
|            20 |           0.01 |
|            21 |           0.03 |
|            22 |           0.06 |
|            23 |           0.11 |
|            24 |           0.23 |
|            25 |           0.44 |
|            26 |           0.89 |
|            27 |           1.79 |
|            28 |           3.65 |
|            29 |           7.32 |
|            30 |          14.29 |
|            31 |          28.45 |
|            32 |          57.94 |
|            33 |         114.02 |
|            34 |         233.58 |
| I got bored waiting...         |



## Related

- [Atomic Grouping](https://www.regular-expressions.info/atomic.html)
- [Possessive Quantifiers](https://www.regular-expressions.info/possessive.html)
  - [ES Discourse](https://es.discourse.group/t/possessive-regexp-matching/203/5)