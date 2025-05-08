# ⚙️ Custom Language Overview

This is a minimalistic, imperative-style programming language with simple syntax and control flow constructs. It supports basic variable declaration, arithmetic operations, conditional logic, and custom control flow using labels.

---

# ✨ Features

## ✅ Data Types
- `int`
- `float`
- `string`

> **Note:** Operations can only be performed between **two variables** or **two literals** — no mixing.

---

## ✅ Variable Declaration
```c
int x = 10;
float pi = 3.14;
string name = "Foo";
```
## ✅ Arithmetic Operations
Supported:
+ ### +(Addition)

+ ### - (Subtraction)

+ ### * (Multiplication)

+ ### / (Division)

+ ### % (Modulus)

```c
int a = 5;
int b = 3;
int c = a + b;
```

## ✅ Conditional Statements
```c
if(condition);
then statement;
```

### Example:

```c
if(x % even == 0);
then show "Even number";
```
> **Note:** Even here is 2
---

## ✅ Labels & Goto (for Loops)
```c
label loop;
    // statements
end;
if(condition);
then goto loop;
```

## ✅ Variable Deletion
```c
del $var_name;
```
## ✅ Output
```c
show "Hello World";
show variable;
show "Label:" end ' ';
```

## 🧪 Example Programs
### 🔁 Multiplication Loop
```c
int limit = 10;
int fr_var = 0;
int sum = 0;
label add;
    int new_sum = sum * fr_var;
    sum = new_sum;
    del $new_sum;
    fr_var++;
end;
if(fr_var<limit);
then goto add;
show "The sum is:" end ' ';
show sum;
```

### 🔎 Even/Odd Checker
```c
int number = 10;
int even = 2;
if(number % even == 0);
then show "The number is even";
if(number % even == 1);
then show "The number is odd";
```

## ➕ Summation Loop
```c
int limit = 10;
int fr_var = 0;
int sum = 0;
label add;
    int new_sum = sum + fr_var;
    sum = new_sum;
    del $new_sum;
    fr_var++;
end;
if(fr_var<limit);
then goto add;
show "The sum is:" end ' ';
show sum;
```
# ⚠️ Limitations
+ #### Mixed-type operations (like variable + literal) are not allowed.

+ #### Only supports simple control flow (if, goto).

+ #### No functions or return statements yet.

# Happy coding!