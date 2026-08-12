# VS Code for Java Development

## Learning outcomes

After this module you can:

- Install and configure **VS Code** for Java work  
- Open a **Maven or Gradle** project and run a `main` method  
- Use **run, debug, breakpoints**, and the Problems panel  
- Navigate code (go to definition, find references, format)  

## Why VS Code

VS Code is a lightweight editor with strong Java support via extensions. On this track we standardize on it so everyone can:

| Task | How VS Code helps |
|------|-------------------|
| Edit Java | Language Server (intellisense, errors) |
| Build | Maven/Gradle terminals + extensions |
| Debug | Breakpoints, step, variables, stack |
| Git | Built-in source control (pairs with Git + Jira/Bitbucket/GitLab workflow modules) |

You may use IntelliJ later; skills transfer. For class demos, **VS Code**.

## Install checklist

1. **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/)  
2. **JDK 17+** (LTS) — Temurin/Oracle/OpenJDK; verify:

```bash
java -version
javac -version
```

3. **Extension Pack for Java** (Microsoft) — includes Language Support, Debugger, Test Runner, Maven, Project Manager.  
4. Optional: **Gradle for Java**, **Lombok** only if the project needs it, **GitLens** (optional).

Set `java.configuration.runtimes` / `java.jdt.ls.java.home` if VS Code cannot find your JDK (**Settings** → search `java home`).

## Open a project the right way

Prefer **File → Open Folder** on the project root (where `pom.xml` or `build.gradle` lives), not a single `.java` file.

```text
my-app/
  pom.xml          ← Maven root
  src/main/java/...
  src/test/java/...
```

Wait for “Java projects loading…” to finish. Use the **Java Projects** view in the sidebar.

## Create / run a tiny app

### Maven quickstart (terminal)

```bash
mvn -B archetype:generate \
  -DgroupId=com.ciss.demo \
  -DartifactId=hello-java \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DarchetypeVersion=1.5 \
  -DinteractiveMode=false
cd hello-java
```

Open the folder in VS Code. Find `App.java`, click **Run** above `main`, or:

```bash
mvn -q compile exec:java -Dexec.mainClass="com.ciss.demo.App"
```

### Debug

1. Click left of a line number → **breakpoint** (red dot).  
2. **Run → Start Debugging** (or F5) with a Java launch config.  
3. Use Continue / Step Over / Step Into / Step Out.  
4. Inspect **Variables** and **Call Stack**.

If launch.json is missing, the Java extension usually offers “Run and Debug” auto-config.

## Everyday editor skills

| Action | Typical shortcut (Windows) | Why |
|--------|----------------------------|-----|
| Command Palette | `Ctrl+Shift+P` | All commands |
| Go to file | `Ctrl+P` | Jump by name |
| Go to symbol | `Ctrl+T` | Classes/methods |
| Go to definition | `F12` | Follow types |
| Find references | `Shift+F12` | Who calls this? |
| Rename symbol | `F2` | Safe rename |
| Format document | `Shift+Alt+F` | Consistent style |
| Problems panel | `Ctrl+Shift+M` | Compiler/lint errors |
| Integrated terminal | `` Ctrl+` `` | Maven/Git without leaving IDE |

## Project hygiene in the editor

- Enable **format on save** (optional team rule).  
- Do not commit `.class`, `target/`, `.idea/` unless team says so — use `.gitignore`.  
- Use workspace trust carefully on unknown repos.

### Minimal `.gitignore` fragment (Java)

```gitignore
target/
build/
.idea/
*.iml
*.class
.vscode/*.log
```

(You may commit shared `.vscode/extensions.json` / launch snippets if the team agrees.)

## Drill (25 min)

1. Generate or open a Maven project.  
2. Change `App` to print two lines; run it.  
3. Set a breakpoint; debug and step.  
4. Introduce a compile error; fix via Problems panel.  
5. Make a Git commit of your change (from VS Code Source Control or terminal).  

## Integrity

- Course work must be your reasoning; AI autocomplete is fine if you understand and can explain every line.  
- Cite AI for substantial generated blocks (same rule as SE modules).

## Further reading

| Topic | Source |
|-------|--------|
| Java in VS Code | [code.visualstudio.com/docs/java/java-tutorial](https://code.visualstudio.com/docs/java/java-tutorial) |
| Extension pack | [Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack) |
| Maven in 5 minutes | [Maven Getting Started](https://maven.apache.org/guides/getting-started/) |
| JDK | [Adoptium Temurin](https://adoptium.net/) |

## Next

**PostgreSQL with Java** — JDBC connectivity, queries, and safe parameter binding.
