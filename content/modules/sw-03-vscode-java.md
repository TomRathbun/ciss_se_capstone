# VS Code for Java Development

## Learning outcomes

After this module you can:

- Install and configure **VS Code** for Java work  
- Choose and install an appropriate **JDK** (understand LTS, OpenJDK vs Oracle, JDK vs JRE)  
- Open a **Maven or Gradle** project and run a `main` method  
- Use **run, debug, breakpoints**, and the Problems panel  
- Navigate code (go to definition, find references, format)  
- Know the recommended Java-related extensions for the intern track  

## Why VS Code

VS Code is a lightweight editor with strong Java support via extensions. On this track we standardize on it so everyone can:

| Task | How VS Code helps |
|------|-------------------|
| Edit Java | Language Server (intellisense, errors) |
| Build | Maven/Gradle terminals + extensions |
| Debug | Breakpoints, step, variables, stack |
| Git | Built-in source control (pairs with Git + Jira/Bitbucket/GitLab workflow modules) |

You may use IntelliJ later; skills transfer. For class demos, **VS Code**.

## Recommended Java-related extensions

Install these so the whole cohort has the same baseline tooling:

| Extension | Publisher / ID | Why |
|-----------|----------------|-----|
| **Extension Pack for Java** | Microsoft (`vscjava.vscode-java-pack`) | **Required.** Bundles Language Support for Java, Debugger, Test Runner, Maven for Java, Project Manager for Java, and more. |
| **Gradle for Java** | Microsoft (`vscjava.vscode-gradle`) | Install if any project uses Gradle instead of (or in addition to) Maven. |
| **Lombok Annotations Support for VS Code** | Gabriel Rinaldi / community | Only if a project uses Lombok (`@Data`, `@Builder`, etc.). |
| **Spring Boot Extension Pack** | VMware / Broadcom (`vmware.vscode-boot-dev-pack`) | Useful when exploring Spring / Spring Boot (even if production code is still on Java 8). Includes Spring Boot Tools, Spring Initializr, etc. |
| **GitLens** | GitKraken | Optional but highly recommended — richer blame, history, and PR awareness. |
| **XML** / **YAML** language support | Red Hat or Microsoft | Helpful for `pom.xml`, `application.yml`, Spring configs, and ICDs. |

**How to install**

1. `Ctrl+Shift+X` (Extensions view)  
2. Search by name or ID  
3. Install → reload if prompted  

Teams sometimes commit a shared `.vscode/extensions.json` so VS Code prompts everyone for the same set. Prefer that once the list stabilizes.

## Java versions and runtimes

**Operational reality:** many of our systems still run on **Java 8**. An upgrade is planned. For learning, tooling, and future-ready skills you should also install a current **LTS** JDK.

### LTS (Long-Term Support)

Oracle and the broader OpenJDK community designate certain releases as LTS. These receive longer support windows:

| Version | Status (2026) | Notes |
|---------|---------------|-------|
| **8** | Legacy LTS | Still widely used in enterprise / defense systems; our current baseline. |
| **11** | LTS | Transitional; many organizations stopped here. |
| **17** | LTS | Minimum for modern Spring Boot 3+/4.x. |
| **21** | LTS | Strong current choice for new development. |
| **25** | LTS (GA Sep 2025) | Newest LTS; good target for personal/dev machines. |

Non-LTS releases (9, 10, 12–16, 18–20, 22–24, 26…) have short support windows and are generally avoided for production.

**Recommendation for interns**

- Install a current LTS (21 or 25) as your primary JDK for VS Code, learning, and any new sample code.  
- Be able to switch to (or at least understand) a Java 8 toolchain when you touch the real operational codebase.  
- Multiple JDKs side-by-side are normal.

### OpenJDK vs Oracle JDK

| Aspect | OpenJDK builds (Temurin, Corretto, Zulu, Microsoft, Red Hat, …) | Oracle JDK |
|--------|------------------------------------------------------------------|------------|
| License | GPLv2 + Classpath Exception — free for production use | Commercial terms for most production use (Java SE Universal Subscription) |
| Cost | Free | Subscription often required |
| Behavior | Same language + bytecode standard | Nearly identical; minor packaging / tooling differences |
| Recommendation | **Prefer these** for class and most team work | Acceptable for some development scenarios; check license before production deployment |

Primary download site for interns: **[Adoptium Temurin](https://adoptium.net/)** (Eclipse Adoptium project). Other solid free options: Amazon Corretto, Azul Zulu, Microsoft Build of OpenJDK.

### JDK vs JRE

- **JDK** (Java Development Kit) = compiler (`javac`), debugger, tools + runtime. **Install this.**  
- **JRE** (Java Runtime Environment) = runtime only. Historical packaging; modern practice is to install the full JDK even when you only need to run applications. Custom slim runtimes can be produced later with `jlink`.

VS Code’s Java Language Server and Maven/Gradle tooling expect a full JDK.

### Licenses (practical summary)

- OpenJDK distributions under the Classpath Exception are safe for commercial/production use without per-seat or per-core fees from the JDK vendor.  
- Oracle’s own builds after certain update levels (especially post-8u202 and for 11+) carry OTN / subscription obligations for production. Do not assume “Oracle Java is free forever.”  
- When in doubt for a real system, document the exact vendor + version + update level and confirm with the program’s licensing/compliance owners.

### Package / version management

On the systems you will administer (RHEL family):

- `yum` / `dnf` packages may provide older OpenJDK builds.  
- For developer machines, common approaches are:  
  - Direct Temurin / Corretto installers or tarballs  
  - **SDKMAN!** (`sdk install java …`) or **asdf** for easy multi-version switching  
  - Setting `JAVA_HOME` (and optionally `PATH`) per shell or per IDE  

In VS Code, point the Language Server at the correct JDK via:

- Settings → search `java.jdt.ls.java.home` or `java.configuration.runtimes`

Verify what you actually have:

```bash
java -version
javac -version
echo $JAVA_HOME
```

### Spring Framework and Spring Boot

- **Spring** is the dominant enterprise Java application framework (dependency injection, AOP, data access, messaging, web, etc.).  
- **Spring Boot** adds opinionated auto-configuration, embedded servers, and “starter” dependencies so you can stand up services quickly.

**Version note that matters for the upgrade path:**

- Spring Boot **2.7** was the last line that still supported Java 8; its open-source support has ended.  
- Spring Boot **3.x and 4.x require Java 17+** (they also support newer LTS releases such as 21 and 25).

While production code remains on Java 8 you will mostly see classic Java + JBoss / ActiveMQ / JDBC patterns. Once the platform moves to a modern LTS, Spring Boot becomes a natural fit for new services. Installing the Spring Boot Extension Pack now lets you explore the modern style on a current JDK without conflicting with the Java 8 operational baseline.

## Install checklist

1. **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/)  
2. **JDK**  
   - Primary (learning / modern work): Temurin or Corretto **LTS 21 or 25**  
   - Awareness: Java 8 toolchain available when needed for legacy code  
   - Verify with `java -version` / `javac -version`  
3. **Extension Pack for Java** (Microsoft) — required  
4. Other recommended extensions from the table above (Gradle, Lombok if needed, Spring Boot pack, GitLens, XML/YAML)  
5. Configure `java.jdt.ls.java.home` / `java.configuration.runtimes` if VS Code does not auto-detect your JDK

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

1. Install the recommended extensions and a current LTS JDK; confirm `java -version`.  
2. Generate or open a Maven project.  
3. Change `App` to print two lines; run it.  
4. Set a breakpoint; debug and step.  
5. Introduce a compile error; fix via Problems panel.  
6. Make a Git commit of your change (from VS Code Source Control or terminal).  

## Integrity

- Course work must be your reasoning; AI autocomplete is fine if you understand and can explain every line.  
- Cite AI for substantial generated blocks (same rule as SE modules).

## Further reading

| Topic | Source |
|-------|--------|
| Java in VS Code | [code.visualstudio.com/docs/java/java-tutorial](https://code.visualstudio.com/docs/java/java-tutorial) |
| Extension Pack for Java | [Marketplace](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack) |
| Temurin / Adoptium (recommended OpenJDK) | [adoptium.net](https://adoptium.net/) |
| Oracle Java SE Support Roadmap | [oracle.com/java/technologies/java-se-support-roadmap.html](https://www.oracle.com/java/technologies/java-se-support-roadmap.html) |
| Maven in 5 minutes | [Maven Getting Started](https://maven.apache.org/guides/getting-started/) |
| Spring Boot | [spring.io/projects/spring-boot](https://spring.io/projects/spring-boot) |

## Next

**PostgreSQL with Java** — JDBC connectivity, queries, and safe parameter binding.
