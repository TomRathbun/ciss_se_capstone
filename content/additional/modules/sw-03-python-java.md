# From Python to Java

> **Hiring bar:** if you are selected onto the contract, you will write **Java** (JDBC, JMS/ActiveMQ, daemons, often JavaFX) on VMs.  
> **On-ramp:** most interns arrive stronger in **Python**. This module uses Python only as a **translation aid**. Graded work after this page is **Java**.

## Learning outcomes

After this module you can:

- Name what transfers from Python (control flow, functions, JSON, SQL ideas) and what does **not**  
- Read a small **Java class** and say how it maps to a Python script  
- Use **static types**, **visibility**, **packages**, and **Maven** without treating them as decoration  
- Translate a short Python snippet into compiling Java  
- Explain why this program is not a Python shop  

## Why Java here (not “Python is bad”)

Python is an excellent teaching and tooling language. The **program stack** you will be hired into is Java-centric:

| Need on the contract | Why Java shows up |
|----------------------|-------------------|
| Existing services | JDBC, JMS, JBoss/WildFly, Java 8 baseline |
| Operator desktops | JavaFX next to the same language as the backend |
| Build / artifacts | Maven + Nexus, not `pip install` on the server |
| Type contracts | Interfaces and compile-time checks next to ICDs |

You may still use Python for personal scratch work. **Do not submit Python as the implementation** of SW-A03 onward unless the assignment explicitly allows a comparison appendix.

SE link: language choice is a **design constraint** allocated to the software component — same as “the ICD is JSON over AMQP.”

## Mental model: same idea, different compiler

```text
Python                         Java
------                         ----
.py files, run by CPython      .java files → javac → .class → JVM
pip / uv / venv                Maven (pom.xml) + JDK
duck typing                    declared types + interfaces
def / indent                   method + { braces }
None                           null (and you must think about it)
with open(...)                 try-with-resources
raise ValueError               throw new IllegalArgumentException
dict / list                    Map / List (java.util)
```

The **algorithm** is the same. The **packaging, types, and lifecycle** are what trip Python-first interns.

## Side-by-side: a tiny program

**Python**

```python
from dataclasses import dataclass

@dataclass
class Employee:
    badge: str
    name: str

    def display(self) -> str:
        return f"{self.badge}: {self.name}"

def find_by_badge(people: list[Employee], badge: str) -> Employee | None:
    for person in people:
        if person.badge == badge:
            return person
    return None

if __name__ == "__main__":
    roster = [Employee("E42", "Amira")]
    found = find_by_badge(roster, "E42")
    print(found.display() if found else "missing")
```

**Java (same behavior)**

```java
package com.ciss.demo;

import java.util.List;

public final class Employee {
    private final String badge;
    private final String name;

    public Employee(String badge, String name) {
        this.badge = badge;
        this.name = name;
    }

    public String getBadge() { return badge; }
    public String getName() { return name; }

    public String display() {
        return badge + ": " + name;
    }

    public static Employee findByBadge(List<Employee> people, String badge) {
        for (Employee person : people) {
            if (person.badge.equals(badge)) {
                return person;
            }
        }
        return null;
    }

    public static void main(String[] args) {
        List<Employee> roster = List.of(new Employee("E42", "Amira"));
        Employee found = findByBadge(roster, "E42");
        System.out.println(found != null ? found.display() : "missing");
    }
}
```

Read the Java column **out loud**: package, class, fields, constructor, methods, `main`. That is the daily unit of work.

## Differences that actually bite

### 1. Types are real at compile time

| Python | Java |
|--------|------|
| `badge: str` is a hint (unless you run a type checker) | `String badge` is enforced by `javac` |
| A function can return `int` or `None` casually | Return type is part of the method; `null` is still possible for objects |

If the compiler complains, **fix the type** — do not cast your way out of every error.

### 2. `==` vs `.equals`

```python
if name == "Amira":      # compares value
```

```java
if (name == "Amira") { }           // often WRONG — reference identity
if (name.equals("Amira")) { }      // value
if ("Amira".equals(name)) { }      // null-safe idiom
```

This is the #1 Python-to-Java bug in intern labs.

### 3. Visibility and “one class, one file”

| Python | Java |
|--------|------|
| `_name` is a convention | `private` / `package` / `protected` / `public` are rules |
| Many classes in one file | **Public** class name = file name (`Employee.java`) |

Program code uses **private fields + constructor + getters** (or package-visible in small lab classes). Do not make every field `public`.

### 4. Packages vs imports

```python
from pathlib import Path
```

```java
package com.ciss.demo;           // this file lives in src/main/java/com/ciss/demo/
import java.nio.file.Path;     // then you use Path
```

Maven layout is not optional decoration:

```text
src/main/java/com/ciss/demo/Employee.java
src/test/java/com/ciss/demo/EmployeeTest.java
pom.xml
```

### 5. Dependencies: `uv`/`pip` vs Maven

| Python | Java on this program |
|--------|----------------------|
| `pyproject.toml` / `requirements.txt` | **`pom.xml`** |
| `uv add psycopg` | `<dependency>` for `org.postgresql:postgresql` |
| venv on the laptop | JAR on the classpath; later **Nexus** for org artifacts |

You will not `pip install` the production service. Learn to read a `pom.xml`.

### 6. Errors

```python
try:
    n = int(raw)
except ValueError:
    raise SystemExit("bad number")
```

```java
try {
    int n = Integer.parseInt(raw);
} catch (NumberFormatException e) {
    throw new IllegalArgumentException("bad number", e);
}
```

Java also has **checked exceptions** (`SQLException`, `IOException`) you must `catch` or declare `throws`. Python has no equivalent. That is why JDBC code looks “noisy.”

### 7. Resources (files, sockets, DB)

```python
with open(path, encoding="utf-8") as f:
    text = f.read()
```

```java
try (var reader = Files.newBufferedReader(path)) {
    String text = reader.lines().collect(Collectors.joining("\n"));
}
```

**try-with-resources** is the Java `with`. Always close `Connection`, `PreparedStatement`, JMS `Session`.

### 8. Null

Python `None` is similar to Java `null`, but Java will **NPE** the moment you call a method on it. After you find an `Employee`, test `!= null` before `display()`. Later you will see `Optional<T>` — optional in this course, useful to know.

### 9. Collections

| Python | Java |
|--------|------|
| `list`, `[]` | `List`, `ArrayList`, `List.of(...)` |
| `dict` | `Map`, `HashMap`, `Map.of(...)` |
| `for x in items` | `for (Type x : items)` |
| list comprehension | stream API (optional here) — a `for` loop is fine |

Java 8 baseline on the program may **not** have `List.of` (Java 9+). For **Java 8** labs:

```java
List<Employee> roster = Arrays.asList(new Employee("E42", "Amira"));
```

Say which language level you compiled with.

### 10. `main` and the entry point

```python
if __name__ == "__main__":
    ...
```

```java
public static void main(String[] args) { ... }
```

One `main` per runnable class. Maven/`exec-maven-plugin` or the VS Code Run link must name that class.

## What you can keep from Python

- Structured thinking: functions with one job, names that match the domain  
- JSON as an ICD payload (same fields; different parser)  
- SQL ideas (parameterize; never concatenate user strings)  
- Tests as the way you know it works  
- Git habits from SW-01 / SW-02  

## What you must stop doing in Java

| Python habit | What to do in Java |
|--------------|--------------------|
| One 200-line script | Classes + package + `main` |
| `==` for strings | `.equals` |
| Mutable default args | Don’t; Java does not have this foot-gun |
| `pip install` in the README as the deploy story | `pom.xml` + `mvn -q compile` |
| “It runs in my notebook” | `mvn` from the project root on the **lab JDK** |
| Swallowing errors | Log + fail; don’t empty `catch (Exception e) {}` |

## Maven in one picture (for Python people)

```text
pom.xml     ≈  pyproject.toml + lock of declared deps
mvn compile ≈  import check + bytecode build
mvn test    ≈  pytest
mvn package ≈  build a wheel/sdist — here a JAR
target/     ≈  .venv build dirt — do not commit
```

## Drill (40 min)

1. Type both listings above (or clone a lab stub). Run the Java `main`.  
2. Break the Java with `name == "Amira"` on a `new String("Amira")` — observe; fix with `.equals`.  
3. Table of **eight** Python→Java mappings in your own words (not a paste of this page).  
4. Translate the assignment snippet (SW-A03P) to Java; `mvn -q compile` must succeed.  
5. One paragraph: why the contract still wants Java even though you are faster in Python.

## Integrity

- Translation must be **your** Java. An AI dump you cannot explain fails the hiring bar.  
- Do not submit only Python “because it is equivalent.”

## Further reading

| Topic | Source |
|-------|--------|
| Official tour | [dev.java/learn](https://dev.java/learn/) |
| Java vs Python (syntax) | Search “Python to Java cheatsheet” — verify against **Java 8** if that is the lab target |
| Maven | [Maven in 5 minutes](https://maven.apache.org/guides/getting-started/) |

## Next

**VS Code for Java** — JDK, Extension Pack, run/debug the class you just translated.
