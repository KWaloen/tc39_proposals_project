[[Inactive]]<br>Classification: [[API Change]]<br>Human Validated: KW<br>Title: RefCollection<br>Authors: Robin Ricard<br>Withdrawn; replaced with [[symbols-weakmap]]; also there were OCAP/membrane concerns around providing a globally available pre-instantiated RefCollection<br>Last Presented: None<br>Stage Upgrades:<br>Stage 1: NA
Stage 2: NA  
Stage 2.7: NA  
Stage 3: NA  
Stage 4: NA<br>Last Commit: 2020-04-01<br>Topics: #others #memory<br>Keywords: #symbol #memory_management<br>GitHub Link: https://github.com/rricard/proposal-refcollection/ <br>GitHub Note Link: None
# Proposal Description:<br>
# RefCollection

ECMAScript proposal for the RefCollection.

**Author:**

- Robin Ricard (Bloomberg)

**Champions:**

- Robin Ricard (Bloomberg)
- Richard Button (Bloomberg)

**Advisors:**

- Dan Ehrenberg (Igalia)

**Stage:** 0

# Overview

The RefCollection introduces a way to keep value references to objects through symbols.

One of its main goals is to be able to keep track of objects in [[record-tuple]] without introducing anything mutable in them.

The RefCollection is able to automatically track symbols in such a way that when they become unreachable (and since symbols can't be forged) the referenced object can become unreachable as well.

# Examples

```js
const refc = new RefCollection();

const rootRef = refc.ref(document.getElementById("root"));
assert(refc.deref(rootRef) === document.querySelector("#root"));

const otherRootRef = refc.ref(document.querySelector("#root"));
assert(rootRef === otherRootRef);
```

## _with [Records and Tuples][rt]_

```js
const refc = new RefCollection();

const vdom = #{
    type: "div",
    props: #{ id: "root" },
    children: #[
        #{
            type: "button",
            props: #{
                onClick: refc.ref(function () {
                    alert("Clicked!");
                }),
            },
            children: #[
                "Click Me!",
            ],
        },
    ],
};

refc.deref(vdom.children[0].props.onClick).call();
// Alert: Clicked!
```

# API

## `new RefCollection()`

Creates a `RefCollection`. Does not takes any initializer arguments.

## `RefCollection.prototype.ref(obj, sym = Symbol())`

Returns a stable `symbol` for a corresponding object `obj`.

You can optionally give a symbol `sym` that will be used if a new symbol needs to get registered. If the `obj` is already in the RefCollection, `sym` will get discarded. If `sym` is already pointing to an object in the refCollection, expect a `TypeError`.

## `RefCollection.prototype.deref(sym)`

Returns the object corresponding to the symbol `sym`. If a `symbol` not returned by the same `RefCollection` gets passed here you will receive `undefined`.

# Behaviors

## Object-Ref stability

The collection does not let you change or remove from it, only add. So for a same object, expect the same ref symbol.

## Unreachability

The `RefCollection` will mark all objects tracked as unreachable as soon as the collection becomes unreachable.

If a symbol becomes independently unreachable, since they can't be reforged, the collection will mark the corresponding object as unreachable from the collection.

> _Note_: This second point is impossible to polyfill.

# Polyfill

You will find a [polyfill in this same repository][poly].

# FAQ

## Why Symbols?

Symbols are a good way to represent that reference since we can't reforge them to recreate a ref from nothing (which a number or a string would have been possible to forge). 

[rt]: https://github.com/tc39/proposal-record-tuple
[poly]: ./polyfill/refcoll.js