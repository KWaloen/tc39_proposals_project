[[Stage 4]]<br>Classification: [[API Change]] <br>Human Validated: KW<br>Title: Promise.allSettled<br>Authors: Jason Williams, Robert Pamely, Mathias Bynens<br>Champions: Mathias Bynens<br>Last Presented: July 2019<br>Stage Upgrades:<br>Stage 1: 2018-09-27  
Stage 2: 2019-01-30  
Stage 2.7: NA  
Stage 3: 2019-03-27  
Stage 4: 2019-07-24<br>Last Commit: 2019-12-09<br>Keywords: #promise #asynchronous <br>GitHub Link: https://github.com/tc39/proposal-promise-allSettled <br>GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2019-07/july-24.md#promiseallsettled
# Proposal Description:
# `Promise.allSettled`

ECMAScript proposal and reference implementation for `Promise.allSettled`.

**Author:** Jason Williams (BBC), Robert Pamely (Bloomberg), Mathias Bynens (Google)

**Champion:** Mathias Bynens (Google)

**Stage:** 4

## Overview and motivation

There are [four main combinators in the `Promise` landscape](https://v8.dev/features/promise-combinators).

| name                 | description                                     |                                                                     |
| -------------------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| `Promise.allSettled` | does not short-circuit                          | this proposal 🆕                                                     |
| `Promise.all`        | short-circuits when an input value is rejected  | added in ES2015 ✅                                                   |
| `Promise.race`       | short-circuits when an input value is settled   | added in ES2015 ✅                                                   |
| `Promise.any`        | short-circuits when an input value is fulfilled | [separate proposal](https://github.com/tc39/proposal-promise-any) 🔜 |

These are all commonly available in userland promise libraries, and they’re all independently useful, each one serving different use cases.

A common use case for _this_ combinator is wanting to take an action after multiple requests have completed, regardless of their success or failure.
Other Promise combinators can short-circuit, discarding the results of input values that lose the race to reach a certain state.
`Promise.allSettled` is unique in always waiting for all of its input values.

`Promise.allSettled` returns a promise that is fulfilled with an array of promise state snapshots, but only after all the original promises have settled, i.e. become either fulfilled or rejected.

## Why `allSettled`?

We say that a promise is _settled_ if it is not pending, i.e. if it is either fulfilled or rejected. See [_promise states and fates_](https://github.com/domenic/promises-unwrapping/blob/master/docs/states-and-fates.md) for more background on the relevant terminology.

Furthermore, the name `allSettled` is commonly used in userland libraries implementing this functionality. See below.

## Examples

Currently you would need to iterate through the array of promises and return a new value with the status known (either through the resolved branch or the rejected branch.

```js
function reflect(promise) {
  return promise.then(
    (v) => {
      return { status: 'fulfilled', value: v };
    },
    (error) => {
      return { status: 'rejected', reason: error };
    }
  );
}

const promises = [ fetch('index.html'), fetch('https://does-not-exist/') ];
const results = await Promise.all(promises.map(reflect));
const successfulPromises = results.filter(p => p.status === 'fulfilled');
```

The proposed API allows a developer to handle these cases without creating a reflect function and/or assigning intermediate results in temporary objects to map through:

```js
const promises = [ fetch('index.html'), fetch('https://does-not-exist/') ];
const results = await Promise.allSettled(promises);
const successfulPromises = results.filter(p => p.status === 'fulfilled');
```

Collecting errors example:

Here we are only interested in the promises which failed, and thus collect the reasons. `allSettled` allows us to do this quite easily.

```js
const promises = [ fetch('index.html'), fetch('https://does-not-exist/') ];

const results = await Promise.allSettled(promises);
const errors = results
  .filter(p => p.status === 'rejected')
  .map(p => p.reason);
```

### Real-world scenarios

A common operation is knowing when all requests have completed regardless of the state of each request. This allows developers to build with progressive enhancement in mind. Not all API responses will be mandatory.

Without `Promise.allSettled` this is tricker than it could be:

```js
const urls = [ /* ... */ ];
const requests = urls.map(x => fetch(x)); // Imagine some of these will fail, and some will succeed.

// Short-circuits on first rejection, all other responses are lost
try {
  await Promise.all(requests);
  console.log('All requests have completed; now I can remove the loading indicator.');
} catch {
  console.log('At least one request has failed, but some of the requests still might not be finished! Oops.');
}
```

Using `Promise.allSettled` would be more suitable for the operation we wish to perform:

```js
// We know all API calls have finished. We use finally but allSettled will never reject.
Promise.allSettled(requests).finally(() => {
  console.log('All requests are completed: either failed or succeeded, I don’t care');
  removeLoadingIndicator();
});
```

## Userland implementations

* https://www.npmjs.com/package/promise.allsettled
* https://www.npmjs.com/package/q
* https://www.npmjs.com/package/rsvp
* http://bluebirdjs.com/docs/api/reflect.html
* https://www.npmjs.com/package/promise-settle
* https://github.com/cujojs/when/blob/master/docs/api.md#whensettle
* https://www.npmjs.com/package/es2015-promise.allsettled
* https://www.npmjs.com/package/promise-all-settled
* https://www.npmjs.com/package/maybe

## Naming in other languages

Similar functionality exists in other languages with different names. Since there is no uniform naming mechanism across languages, this proposal follows the naming precedent of userland JavaScript libraries shown above. The following examples were contributed by jasonwilliams and benjamingr.

**Rust**

[`futures::join`](https://rust-lang-nursery.github.io/futures-api-docs/0.3.0-alpha.5/futures/macro.join.html) (similar to `Promise.allSettled`). "Polls multiple futures simultaneously, returning a tuple of all results once complete."

[`futures::try_join`](https://rust-lang-nursery.github.io/futures-api-docs/0.3.0-alpha.5/futures/macro.try_join.html) (similar to `Promise.all`)

**C#**

`Task.WhenAll` (similar to ECMAScript `Promise.all`). You can use either try/catch or `TaskContinuationOptions.OnlyOnFaulted` to achieve the same behavior as `allSettled`.

`Task.WhenAny` (similar to ECMAScript `Promise.race`)

**Python**

[`asyncio.wait`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait) using the `ALL_COMPLETED` option (similar to `Promise.allSettled`). Returns task objects which are akin to the `allSettled` inspection results.

**Java**

[`allOf`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html#allOf-java.util.concurrent.CompletableFuture...-) (similar to `Promise.all`)

**Dart**

[`Future.wait`](https://api.dartlang.org/stable/2.0.0/dart-async/Future/wait.html) (similar to ECMAScript `Promise.all`)

## Further reading

* https://www.bennadel.com/blog/3289-implementing-q-s-allsettled-promise-method-in-bluebird.htm
* https://github.com/domenic/promises-unwrapping/blob/master/docs/states-and-fates.md
* http://exploringjs.com/es6/ch_promises.html
* https://github.com/kriskowal/q/issues/257 [naming]

## TC39 meeting notes

- [September 2018](https://github.com/tc39/notes/blob/master/meetings/2018-09/sept-27.md#promiseallsettled-for-stage-1)
- [January 2019](https://github.com/tc39/notes/blob/master/meetings/2019-01/jan-30.md#promiseallsettled)
- [March 2019](https://github.com/tc39/notes/blob/master/meetings/2019-03/mar-26.md#promiseallsettled-for-stage-3)
- [July 2019](https://github.com/tc39/notes/blob/master/meetings/2019-07/july-24.md#promiseallsettled)

## Specification

* [Ecmarkup source](https://github.com/tc39/proposal-promise-allSettled/blob/master/spec.html)
* [HTML version](https://tc39.es/proposal-promise-allSettled/)

## Implementations

* [V8](https://bugs.chromium.org/p/v8/issues/detail?id=9060), shipping in Chrome 76
* [SpiderMonkey](https://bugzilla.mozilla.org/show_bug.cgi?id=1539694), shipping in Firefox 68 Nightly
* [JavaScriptCore](https://bugs.webkit.org/show_bug.cgi?id=197600), shipping in Safari TP 85 and Safari 13 Beta
* [Chakra](https://github.com/microsoft/ChakraCore/pull/6138)
* [XS](https://github.com/Moddable-OpenSource/moddable/issues/211), shipping in v9.0.0
* [Spec-compliant polyfill](https://www.npmjs.com/package/promise.allsettled)
<br>