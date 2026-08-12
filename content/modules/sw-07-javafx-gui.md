# JavaFX for Desktop GUIs

## Learning outcomes

After this module you can:

- Explain when a **desktop GUI** (JavaFX) is a good fit vs a web UI  
- Create a minimal **JavaFX** application with a stage, scene, and layout  
- Wire **controls** (buttons, text fields, tables) to event handlers  
- Keep **UI thread** work safe; push slow work off the FX Application Thread  
- Structure UI code so business rules stay out of event handlers (SE-friendly)  

## Why JavaFX here

Some CISS tools are **operator / engineer desktops** (config, monitoring, training utilities), not only browsers. JavaFX is the modern Java UI toolkit for that class of app.

| Fit | Less ideal |
|-----|------------|
| Internal tools, lab consoles, offline demos | Public internet products (usually web) |
| Rich local charts / controls | Pixel-perfect marketing sites |
| Same language as backend demos (Java) | Teams standardized on another UI stack |

SE link: screens implement **use cases**; labels and validation should still map to **EARS requirements** and acceptance criteria — the GUI is design, not a place to invent new business rules.

## Concepts

```text
Application
  └── Stage (window)
        └── Scene
              └── Parent (layout: VBox, BorderPane, GridPane, …)
                    └── Controls (Button, TextField, TableView, …)
```

- **FX Application Thread** — all UI create/update work happens here.  
- **FXML** (optional) — XML layout + controller class (MVC-ish).  
- **Properties / bindings** — reactive UI state (`StringProperty`, etc.).

## Tooling

| Need | Approach |
|------|----------|
| JDK | 17+ (same as other SW modules) |
| JavaFX libraries | Maven coordinates `org.openjfx:javafx-controls` (and `javafx-fxml` if used) |
| VS Code | Extension Pack for Java + run config that puts JavaFX modules on the module path **or** use a fat/classpath setup your lab provides |
| Scene Builder (optional) | Visual FXML editor — nice, not required |

### Maven dependencies (JavaFX 21 example)

```xml
<properties>
  <javafx.version>21.0.2</javafx.version>
</properties>

<dependencies>
  <dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-controls</artifactId>
    <version>${javafx.version}</version>
  </dependency>
  <dependency>
    <groupId>org.openjfx</groupId>
    <artifactId>javafx-fxml</artifactId>
    <version>${javafx.version}</version>
  </dependency>
</dependencies>
```

### `javafx-maven-plugin` (run from CLI)

```xml
<plugin>
  <groupId>org.openjfx</groupId>
  <artifactId>javafx-maven-plugin</artifactId>
  <version>0.0.8</version>
  <configuration>
    <mainClass>com.ciss.demo.HelloFxApp</mainClass>
  </configuration>
</plugin>
```

```bash
mvn -q javafx:run
```

If the lab image already has a working sample project, prefer that over fighting module-path settings on day one.

## Minimal application (code UI)

```java
package com.ciss.demo;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class HelloFxApp extends Application {

    @Override
    public void start(Stage stage) {
        Label title = new Label("CISS lab console");
        TextField badge = new TextField();
        badge.setPromptText("Badge code");
        Label status = new Label("Ready");

        Button checkIn = new Button("Check in");
        checkIn.setOnAction(e -> {
            String code = badge.getText() == null ? "" : badge.getText().trim();
            if (code.isEmpty()) {
                status.setText("Enter a badge code");
                return;
            }
            // Call service layer — do not put SQL here
            status.setText("Checked in: " + code);
        });

        VBox root = new VBox(10, title, badge, checkIn, status);
        root.setPadding(new Insets(16));

        stage.setTitle("Hello JavaFX");
        stage.setScene(new Scene(root, 360, 200));
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
```

## Layout cheat sheet

| Pane | Use when… |
|------|-----------|
| `VBox` / `HBox` | Simple vertical / horizontal stacks |
| `BorderPane` | Top toolbar, center content, bottom status |
| `GridPane` | Forms (label | field rows) |
| `StackPane` | Overlay / centering single node |
| `TabPane` | Multiple screens in one window |

Prefer **one main window** + clear navigation over dozens of free-floating stages.

## FXML sketch (optional)

`hello.fxml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.VBox?>
<VBox xmlns:fx="http://javafx.com/fxml" fx:controller="com.ciss.demo.HelloController" spacing="10">
  <Label text="CISS lab console"/>
  <TextField fx:id="badgeField" promptText="Badge code"/>
  <Button text="Check in" onAction="#onCheckIn"/>
  <Label fx:id="statusLabel" text="Ready"/>
</VBox>
```

Controller:

```java
public class HelloController {
    @FXML private TextField badgeField;
    @FXML private Label statusLabel;

    @FXML
    private void onCheckIn() {
        statusLabel.setText("Checked in: " + badgeField.getText());
    }
}
```

Load with `FXMLLoader` in `start(...)`.

## UI thread rules (do not skip)

| Do | Don’t |
|----|--------|
| Update controls on the FX Application Thread | Call `status.setText` from a background AMQP/DB thread |
| Use `Platform.runLater(() -> …)` to marshal back to UI | Block the UI thread with long JDBC or network calls |
| Run slow work in `Task` / executor | Freeze the window “until the query finishes” |

```java
Task<String> task = new Task<>() {
    @Override protected String call() throws Exception {
        return repository.findName(badge); // background
    }
};
task.setOnSucceeded(e -> status.setText(task.getValue())); // UI thread
task.setOnFailed(e -> status.setText("Lookup failed"));
new Thread(task, "db-lookup").start();
```

## Structure that scales (SE-friendly)

```text
ui/          JavaFX views + controllers (thin)
service/     Use-case logic, validation (EARS-facing rules)
repository/  JDBC / messaging adapters
```

Event handlers:

1. Read inputs  
2. Call **service**  
3. Show result / error  

They should not open JDBC connections or parse AMQP payloads directly.

## Tables (operator views)

`TableView` + `ObservableList` is the usual pattern for lists (employees, events, messages).

```java
TableView<TimeEventRow> table = new TableView<>(rows);
TableColumn<TimeEventRow, String> colBadge = new TableColumn<>("Badge");
colBadge.setCellValueFactory(c -> c.getValue().badgeProperty());
table.getColumns().add(colBadge);
```

Refresh the list from a service after actions — don’t duplicate business rules in cell factories.

## Drill (45–60 min)

1. Create a JavaFX Maven project (or use the lab template).  
2. Build a small **Check-in console**: badge field, Check in / Check out buttons, status label.  
3. Reject empty badge with a clear message (GUI-level validation).  
4. Stretch: disable buttons while a background `Task` “simulates” a 2s server call.  
5. Stretch: `TableView` of the last 10 actions in memory.  

Commit UI code separately from later JDBC wiring if you combine with the Postgres module.

## Common failures

| Symptom | Checks |
|---------|--------|
| `JavaFX runtime components are missing` | Module path / `javafx-maven-plugin` / lab template |
| Controls don’t update from consumer thread | Need `Platform.runLater` |
| UI freezes | Long work on FX thread |
| Blank window | Forgot `stage.show()` or empty scene root |

## Integrity

- Desktop demos still follow course integrity: your logic, cite AI if used heavily.  
- No classified operational data in screenshots submitted for grading.

## Further reading

| Topic | Source |
|-------|--------|
| OpenJFX | [openjfx.io](https://openjfx.io/) |
| Getting started | [OpenJFX docs — Getting started](https://openjfx.io/openjfx-docs/) |
| Oracle legacy trail (concepts still useful) | Search “JavaFX getting started tutorial” on Oracle docs archives |
| VS Code Java | Course module **VS Code for Java Development** |

## Next

**CI/CD and Jenkins** — automate build and test of your Java (and JavaFX) projects; green pipeline before merge.  
Also combine GUI work with **PostgreSQL** / **ActiveMQ** via a thin service layer; long-running consumers often live in a **daemon**, not the desktop process.
