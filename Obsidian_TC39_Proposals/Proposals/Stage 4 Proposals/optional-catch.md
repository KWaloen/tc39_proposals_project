#Stage4Tag
Classification: [[Syntactic Change]]
Human Validated: KW
Title: Optional catch binding
Authors: Michael Ficarra
Champions: Michael Ficarra
Date: May 2018
Last Commit: 2018-05-22
Expected Publication Year: 2019
GitHub Link: https://github.com/tc39/proposal-optional-catch-binding
GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2018-05/may-22.md#conclusionresolution-7

# Proposal Description:
This proposal makes a grammatical change to ECMAScript, allowing the omission
of a `catch` binding in cases where the binding would not be used. This occurs
frequently with patterns such as 

```js
try {
  // try to use a web feature which may not be implemented
} catch (unused) {
  // fall back to a less desirable web feature with broader support
}
```

or

```js
let isTheFeatureImplemented = false;
try {
  // stress the required bits of the web API
  isTheFeatureImplemented = true;
} catch (unused) {}
```

or

```js
let parseResult = someFallbackValue;
try {
  parseResult = JSON.parse(potentiallyMalformedJSON);
} catch (unused) {}
```

and it is a common opinion that variables which are declared or written to but
never read signify a programming error.

The grammar change introduced by this proposal allows for the `catch` binding
and its surrounding parentheses to be omitted, as in

```js
try {
  // ...
} catch {
  // ...
}
```

See [the the full text of the proposal](https://tc39.github.io/proposal-optional-catch-binding/) for more info.
