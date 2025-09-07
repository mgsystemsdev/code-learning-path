



---

### 1️⃣ Naming and Using Variables

In Python, a **variable** is like a box with a label on it.
You can store information inside and reuse it later.

```python
message = "Hello, Python!"   # VARIABLE assignment
print(message)               # OUTPUT the variable
```

* `message` → the label.
* `"Hello, Python!"` → the content inside the box.

**Rules for variable names:**

* Use only letters, numbers, and underscores (`_`).
* Must start with a letter or underscore, never a number.
* No spaces allowed.
* Use lowercase\_with\_underscores for readability.

✅ Good: `user_name`, `age2`, `city_name`
❌ Bad: `2name`, `user-name`, `city name`

---

### 2️⃣ Avoiding Name Errors

If you try to use a variable that doesn’t exist (maybe a typo), Python raises a **NameError**.

```python
mesage = "Hello"   # Oops, typo
print(message)     # ERROR: NameError
```

👉 Always double-check spelling, letter case, and whether the variable is defined *before* using it.

---

### 3️⃣ Variables Are Labels

Important mental model: variables don’t **hold** data, they **point** to it.
Think of the label as a sticky note you put on a box. If you change the label, the content inside can change too.

```python
x = 10
y = x        # y points to same data as x
x = 20
print(y)     # still 10, because y was pointing to old value
```

This shows that variables act more like **labels** than permanent storage.

---

### 4️⃣ Strings

A **string** is text wrapped in quotes — either single (`'Hello'`) or double (`"Hello"`).

```python
name = "ada lovelace"
print(name.title())   # Ada Lovelace
print(name.upper())   # ADA LOVELACE
print(name.lower())   # ada lovelace
```

**Concatenation**: join strings with `+` or use **f-strings** (newer Python).

```python
first = "ada"
last = "lovelace"
print(first + " " + last)                 # ada lovelace
print(f"{first.title()} {last.title()}")  # Ada Lovelace
```

---

### 5️⃣ Numbers

Python handles numbers directly.

```python
age = 23
print(age)          # 23
print(age + 7)      # 30
print(2 * 3)        # 6
print(2 ** 3)       # 8 (exponent)
print(3 / 2)        # 1.5 (float division)
print(3 // 2)       # 1   (integer division)
```

Mixing numbers and strings will cause errors:

```python
age = 23
# print("Happy " + age + "rd birthday!")  # ERROR
print("Happy " + str(age) + "rd birthday!")  # ✅ works
```

---

### 6️⃣ Comments

A **comment** is text ignored by Python, used for explanations.

```python
# This program greets the user
message = "Hello, world!"
print(message)  # OUTPUT greeting
```

Good comments explain *why* code exists, not just *what* it does.

--------------------------

Skeleton Flashcards

### 1️⃣ Naming and Using Variables

```python
message = "Hello"     # VARIABLE
print(message)        # OUTPUT
```

---

### 2️⃣ Avoiding Name Errors

```python
mesage = "Hi"         # VARIABLE with typo
print(message)        # ERROR: not defined
```

---

### 3️⃣ Variables as Labels

```python
x = 10                # VARIABLE
y = x                 # VARIABLE label copy
x = 20                # UPDATE
print(y)              # OUTPUT old value
```

---

### 4️⃣ Strings

```python
name = "ada"          # VARIABLE
print(name.title())   # OUTPUT capitalized
print(name.upper())   # OUTPUT all caps
print(name.lower())   # OUTPUT lowercase
```

---

### 5️⃣ Numbers

```python
age = 23              # VARIABLE (integer)
print(age + 7)        # OUTPUT addition
print(2 ** 3)         # OUTPUT exponent
print(3 / 2)          # OUTPUT float
print(3 // 2)         # OUTPUT integer division
```

---

### 6️⃣ Comments

```python
# This is a comment   # COMMENT
message = "Hello"     # VARIABLE
print(message)        # OUTPUT
```



