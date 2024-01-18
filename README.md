# [Emu rocks](https://emu.rocks)!<sup>*</sup>
![An emu, rocking](emu.png)
<sup>*</sup> It's marginally ok


Pros:
  * It's free
  * It has a funny bird for a mascot
  * It has a decent minimalistic theme going on
  * You can easily arrange images to the left, right, or center
  * It's okay for writing something like a blog post that is very plain
  * You can add html <b>like this</b> and it works just fine


Cons:
  * It's not that great
  * It's not blazing fast
  * Markdown is infinitely superior in every way


The concept is you can use the option key (⌥) and letters that are easy to recall:

| Key Combination | Symbol | Description                         | Example Usage                                        |
|-----------------|--------|-------------------------------------|------------------------------------------------------|
| Option-B        | ∫      | Bold tagging                        | `∫bold text∫` → **bold text**                        |
| Option-I        | ˆ      | Italicized tagging                  | `ˆitalicized textˆ` → *italicized text*              |
| Option-L        | ¬      | Link tagging (with optional title)  | `¬link text\|url¬` → [link text](url)                |
|                 |        |                                     | `¬link text\|url\|title¬` → [link text](url "title") |
|                 |        | Image tagging (with optional title) | `¬\|url¬` → ![link text](url)                        |
|                 |        |                                     | `¬\|url\|title¬` → ![link text](url "title")         |

You can also surround words with brackets to denote the heading level. Level one headers are centered.

```
[This is a level one header]
[[This is a level two header]]
...
[[[[[[This is a level six header]]]]]]
```

...and curly brackets are used for blockquotes:

```
{This is a blockquote}
{{This is a nested blockquote}}
```

This is what it looks like when you write it:

---

```
[Emu rocks!]

¬|./emu.webp|300x300|A cartoon emu rocking out with a guitar|>¬

[[[Emu: Not Your Daddy's Markup Language]]]
Unless you are my son, then it ˆisˆ your markup language. Er, mine.

[[[Ok.. What Is It, Then?]]]
It's ¬a simple opinionated html page generator|https://github.com/ehamiter/emu¬ that lets you write pages that look more or less ∫exactly like this one∫ by using a few common-sense tags. ¬Check out the source that generated this page|https://raw.githubusercontent.com/ehamiter/emu/main/index.emu¬!

[[[We got GPTS For That]]]
Learn more about Emu ¬straight from the emu's mouth, Eddie|https://chat.openai.com/g/g-2x5PhBpwM-eddie-the-emu|He's a GPT!¬. He can help explain what Emu is, what it's useful for, how to hack on it, and so forth.

{Emus are little more than feathered stomachs borne on mighty legs and ruled by a tiny brain. If an emu wants one of your sandwiches, he will get it, and then run away. He cannot help you with your sudoku.
— Richard Fortey}
```

---

This is what it looks like when you read it:

![](emu-document.png)
