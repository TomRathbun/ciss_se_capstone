# SW-A03P — Python → Java Translation

**Weight:** 10% · **Due:** After sw-03-python-java · **Module:** sw-03-python-java

## Prompt

Prove you can **think in Python and ship in Java**. The contract language is Java. Python here is only the specification.

## Given (do not submit this as the solution)

```python
def passing_scores(rows: list[tuple[str, int]], minimum: int) -> list[str]:
    """Return names whose score is >= minimum, in input order."""
    names = []
    for name, score in rows:
        if score >= minimum:
            names.append(name)
    return names

if __name__ == "__main__":
    data = [("Amira", 82), ("Bilal", 59), ("Chen", 90)]
    print(passing_scores(data, 60))  # ['Amira', 'Chen']
```

## Deliverables

1. **Java class** (Maven project or single `src/main/java/...` file the instructor accepts) that implements the same behavior. `main` prints the two passing names.  
2. **Run evidence:** `mvn -q compile` (or `javac`) plus program output.  
3. **Mapping table** (≥ 8 rows): Python idea → Java idea (must include `==` vs `.equals`, types, `None`/`null`, packages or Maven, `with` vs try-with-resources **or** exceptions).  
4. **Hiring-bar paragraph** (4–6 sentences): why this program uses Java; how you will use Python privately without turning in Python as the product.  
5. **One bug you hit** while translating (compiler or `==`) and how you fixed it.

## Quality bar

- Java compiles; output matches the Python spec.  
- You can explain every line without reading it from a chatbot.  
- No “it works in a notebook” substitute.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| translation | 15 | Correct Java; same behavior |
| literacy | 10 | Mapping table + `==`/types understood |
| communication | 5 | Evidence + honest hiring-bar note |
