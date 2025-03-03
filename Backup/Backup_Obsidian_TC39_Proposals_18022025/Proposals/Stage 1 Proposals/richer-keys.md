#Stage1Tag
Classification: [[API Change]]
Human Validated: KW
Title: Richer Keys
Authors: Bradley Farias
Champions: Bradley Farias
Date: January 2019
Last Commit: 2019-10-28
GitHub Link: https://github.com/tc39/proposal-richer-keys
GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2019-01/jan-30.md#richer-keys-for-stage-2

# Proposal Description:
This is a grouped set of efforts being pushed as a single proposal due to cross cutting and overlapping ideas of how to represent and deal with identity.

## Efforts

# * [Collection#reKey](collection-rekey/)

## Collection {toKey, toValue}

This proposal seeks to add a `toKey` and `toValue` parameter to collection creation.

[Rendered Spec][Specification]

## Status

**Stage:** 1

**Champion:** Bradley Farias (@bmeck)

## Motivation

Often times, developers are forced to marshal data through normalization processes when they insert it or look up data within a collection. This leads to subclassing, which is verbose and potentially fragile; or, relying on the collection consumer's vigilance. This proposal seeks to allow improved developer experience with specialization of collection types by allowing automated marshalling for common workflows.

## API

```mjs
new Map([], {
  toKey(key) {return normalizedKey;},
  toValue(value) {return normalizedValue;},
});
new WeakMap([], {
  toKey(key) {return normalizedKey;},
  toValue(value) {return normalizedValue;},
});
new Set([], {
  toValue(value) {return normalizedValue;},
});
new WeakSet([], {
  toValue(value) {return normalizedValue;},
});
```

## Examples

### Specialized maps

Given an application with User Objects it may be desirable to create collections based upon username and email for separate purposes.

```mjs
new Map(undefined, {
  toKey({email}) {
    return email;
  },
  toValue(state) {
    return state instanceof AccountState ? 
      state :
      new AccountState(state);
  }
});
```

```mjs
new Set(undefined, {
  toValue({username}) {
    return username;
  }
});
```

### Checked keys

It is a common occurance to want to check types when performaning operations on collections. This can be done during keying.

```mjs
new Map(undefined, {
  toKey(user) {
    if (user instanceof User !== true) {
      throw new TypeError('Expected User for key');
    }
    return user;
  }
});
```

## FAQ

### How do other languages handle this customized keying?

A collection of references can be found via [this document](https://docs.google.com/document/d/1qxSLyiButKocM6ENufhvnNJcZh18nDAWcFT2HlTJahQ/edit#).

Generally it falls into using container types. If you wanted to create a `Map` of `People` by `person.email`. You would implement a wrapper class `PersonByEmail` to use as your key, and others for keying of other aspects. Static typing and compiler/language enforced coercion can alleviate problems with misusing collections, but wrapping and unwrapping is manual in scenarios with dynamic typing that cannot be coerced automatically.

This proposal would provide a hook to do that manual wrapping and unwrapping without requiring the user of a collection to remain vigilant about properly marshalling keys before providing them to the collection.

### When are the normalization steps applied?

Normalization is applied when data is incoming to find the identity of the key location in `[[MapData]]` and when placing the value in `[[SetData]]` or `[[MapData]]`. e.g.

```mjs
const map = new Map([], {
  toKey: String
});
// stored using { [[Key]]: "1", [[Value]]: "one" } in map.[[MapData]]
map.set(1, 'one');
// looks for corresponding { [[Key]]: "1" } in map.[[MapData]]
map.has(1); // true
// functions directly exposing the underlying entry list are unaffected
[...map.entries()]; // [["1", "one"]]

const set = new Set([], {toValue: JSON.stringify});
// stored using { [[Value]]: '{"path": "/foo"}' } in set.[[SetData]]
set.add({path: '/foo'});
// looks for corresponding { [[Value]]: '{"path": "/foo"}' } in set.[[SetData]]
set.has({path: '/foo')};
// functions directly exposing the underlying entry list are unaffected
[...set]; // ['{"path": "/foo"}']
```

Normalization is not done when iterating or returning internal data, it is only done on parameters.

### Why are Sets only given `toValue`?

Sets are collections of values, and do not have a mapping operation from one value to another.

### Why not `value[Symbol.toKey]`?

Having specialized identity conflicts with the idea of having multiple kinds of specialized maps per type of value. It also would cause conflicts when wanting to specialize keys that are based upon primitives.

### Why not encourage extending collections?

1. This would be succeptible to prototype crawling such as:

```mjs
myCustomMap.__proto__.get.call(myCustomMap, key);
```

which would somewhat invalidate the idea of checking types of keys.

2. It prevents needing to synchronize all of the methods which is a fair amount of boiler plate and potential place for code going out of sync. It also means that your custom implementation will work even if new methods are added to collections in the JS standard library:

```mjs
class MyMap extends Map {
  constructor([...entries]) {
    super(entries.map(...));
  }
  delete(k) { ... }
  get(k) { ... }
  has(k) { ... }
  set(k, v) { ... }
}
```

If we add something like `emplace()` this code now needs to be updated or it will have bugs if people expect it to work like a standard Map.

This is roughly [the fragile base class problem](https://en.wikipedia.org/wiki/Fragile_base_class), where `Map` is the base class.

1. Even if this is a userland solution, it seems prudent to allow easier usage of maps. We should aim to alleviate developers without requiring that all new features have new kernel semantics. I spoke of this with respect to [expanding the standard library](https://docs.google.com/presentation/d/1QSwQYJz4c1VESEKTWPqrAPbDn_y9lTBBjaWRjej1c-w/view#slide=id.p).

2. Composition, while extending is nice it doesn't always allow for simple chaining and composition of features. If we introduce `RekeyableMap` as a concrete base class it may conflict with other base classes that may be introduced like if there was `InsertIfMissingMap`. Since both are base classes it would not allow both features to be combined easily.

## TODO

The following is a high-level list of tasks to progress through each stage of the [TC39 proposal process](https://tc39.github.io/process-document/):

### Stage 1 Entrance Criteria

* [x] Identified a "[champion][Champion]" who will advance the addition.
* [x] [Prose][Prose] outlining the problem or need and the general shape of a solution.
* [x] Illustrative [examples][Examples] of usage.
* [x] High-level [API][API].

### Stage 2 Entrance Criteria

* [x] [Initial specification text][Specification].
* [ ] [Transpiler support][Transpiler] (_Optional_).

### Stage 3 Entrance Criteria

* [ ] [Complete specification text][Specification].
* [ ] Designated reviewers have [signed off][Stage3ReviewerSignOff] on the current spec text.
* [ ] The ECMAScript editor has [signed off][Stage3EditorSignOff] on the current spec text.

### Stage 4 Entrance Criteria

* [ ] [Test262](https://github.com/tc39/test262) acceptance tests have been written for mainline usage scenarios and [merged][Test262PullRequest].
* [ ] Two compatible implementations which pass the acceptance tests: [\[1\]][Implementation1], [\[2\]][Implementation2].
* [ ] A [pull request][Ecma262PullRequest] has been sent to tc39/ecma262 with the integrated spec text.
* [ ] The ECMAScript editor has signed off on the [pull request][Ecma262PullRequest].



[Champion]: #status
[Prose]: #motivations
[Examples]: #examples
[API]: #api
[Specification]: https://tc39.github.io/proposal-richer-keys/collection-rekey/index.html
[Transpiler]: #todo
[Stage3ReviewerSignOff]: #todo
[Stage3EditorSignOff]: #todo
[Test262PullRequest]: #todo
[Implementation1]: #todo
[Implementation2]: #todo
[Ecma262PullRequest]: #todo

# * [compositeKey](compositeKey/)

## compositeKey, compositeSymbol

This proposal seeks to add APIs to create composite keys while still allowing the components of the composite key to be GC'd.

### API

In all APIs order of arguments is preserved in the path to the key. `compositeKey(a, b)` is different from `compositeKey(b, a)`.

`compositeKey` requires at least one component must be a valid key that can be placed in a `WeakMap` . This is because the main use case for `compositeKey` is to allow GC to occur when the lifetime of the components is ended. `compositeSymbol` is for strongly putting the key on an Object and does not benefit from this.

```mjs
compositeKey(...parts: [...any]) : Object.freeze({__proto__:null})

compositeSymbol(...parts: [...any]) : Symbol()
```

## Where will it live

A builtin module; how to import builtin modules TBD based upon current TC39 discussions.

### FAQ

#### Why have both `compositeKey` and `compositeSymbol`?

They are serving two slightly different use cases.

#### `compositeKey`

Allows using a Map/Set/WeakMap to weakly and/or privately associate data with the lifetime of a group of values.

#### `compositeSymbol`

Allows strongly attaching data to an Object that is associtated with a group of values. This API can be roughly recreated by using:

```mjs
let symbols = new WeakMap;
compositeSymbol = (...parts) => {
  const key = compositeKey(...parts);
  if (!symbols.has(key)) symbols.set(key, Symbol());
  return symbols.get(key);
}
```

However, this causes a problem of not being a global cache like `Symbol.for` or `compositeKey` and may cause fragmentation. It also would be ideal to have `compositeSymbol` act like `Symbol.for` in order to reduce total number of possible entries being held onto.

### Why a frozen empty Object for `compositeKey`?

So that properties cannot be added to the object that will leak to the global or can be used as a public side channel.

This gives a few constraints:

1. The return value must be frozen and a frozen prototype to prevent the side channel from being able to be obtained purely off the reference itself. This leads to `null` being a good choice for the prototype.

2. This constraint must be applied to all properties of the object. While no properties are planned for the return value, the values of properties should follow these rules and/or be a primitive.

### Why require a lifetime?

This prevents accidental leakage by always ensuring keys have a lifetime associated with them.

### What scope is the idempotentcy?

Still up for debate but some TC39 members would like it to be per Realm.

Having it be per Realm allows the key store to be more granular and free up segments as Realms are GC'd, but means that there could be multiple keys that correspond to `compositeKey(A, B)` if you obtain multiple `compositeKey` instances from multiple realms.

Having it be across Realms means that you cannot cause duplicate keys for component parts, and matches with `Symbol.for`. Since the result of `compositeKey` has a null prototype there is not a way to distinguish which Realm the result was first created in.

Currently, this proposal is looking to progress with cross Realm idempotentcy.

### When can the key be GC'd

The path to a key in the key store can be GC'd once any owner of a lifetime in the path is GC'd. This means once any single non-primitive component is GC'd the key cannot be obtained again using these APIs. The key itself is an object subject to normal GC rules and will be removed when it is no longer strongly held.

If you only store keys in `WeakMap`s the key and associated values can be GC'd as soon a component of the key is GC'd.

If you store keys in strongly held structues like a `Map`; the key will not be able to be GC'd since the key could still be obtained inspecting `map.keys()` which could be used to get the value associated with the key.

### How could I create a composite key that can return its components?

You can create a `Map` that strongly preserves your components in order: 

```mjs
const myValues = new Map();

const components = [a, b];
const myKey = compositeKey(...components);
myValues.set(myKey, components);


// ...

let [a, b] = myValues.get(myKey);
```

## Polyfill

A polyfill is available in the [core-js](https://github.com/zloirock/core-js) library. You can find it in the [ECMAScript proposals section](https://github.com/zloirock/core-js#compositekey-and-compositesymbol-methods).

