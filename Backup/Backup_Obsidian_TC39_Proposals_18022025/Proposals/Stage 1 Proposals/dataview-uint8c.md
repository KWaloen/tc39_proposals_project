#Stage1Tag
Classification: [[API Change]]
Human Validated: KW
Title: DataView get/set Uint8Clamped methods
Authors: Jordan Harband
Champions: Jordan Harband
Date: July 2023
Last Commit: 2024-10-10
GitHub Link: https://github.com/tc39/proposal-dataview-get-set-uint8clamped
GitHub Note Link: https://github.com/tc39/notes/blob/HEAD/meetings/2023-07/july-13.md#dataview-getset-uint8clamped-methods-for-stage-1-or-2-or-3

# Proposal Description:
# DataView get/set Uint8Clamped methods

There are currently 11 kinds of Typed Array in the language.

Stage: 1

## Motivation/Use Case

I'd like to dynamically dispatch to DataView methods based on the "type" of the Typed Array. This works great for all of the types except Uint8Clamped.

## Problem
Only 10 of them have DataView get/set methods.

Here's a matrix representing the consistently available functionality for each of them:

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>constructor</th>
      <th>shared prototype</th>
      <th>ArrayBuffers</th>
      <th>DataView get method</th>
      <th>DataView set method</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Int8Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Uint8Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Uint8ClampedArray</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:x:</td>
      <td>:x:</td>
    </tr>
    <tr>
      <td>Int16Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Uint16Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Int32Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Uint32Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>BigInt64Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>BigUint64Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Float32Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
    <tr>
      <td>Float64Array</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
      <td>:white_check_mark:</td>
    </tr>
  </tbody>
</table>

## Solution

Add the get and set methods to round out Typed Array support.

## Use Cases
 - dynamic dispatch based on Typed Array type: https://github.com/esfx/esfx/blob/main/packages/struct-type/src/internal/numbers.ts#L122-L133