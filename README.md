<p align="center">
  <img src="Icon.png" alt="Hykit Logo" width="120" height="160">
</p>

<h3 align="center">Hykit</h3>

---

## Getting Started

> [!IMPORTANT]  
> Hykit is currently distributed via GitHub. Install it using pipx:

```bash
pipx install git+https://github.com/NightLum-Studios/Hykit.git
````

---

## Basic Usage

Create a new project from the bundled template:

```bash
hykit create project MyPlugin
```

You can also specify an author:

```bash
hykit create project MyPlugin "NightLum Studio"
```

Validate the current project:

```bash
hykit validate
```

Or validate a specific directory:

```bash
hykit validate ./MyPlugin
```

Check the installed version:

```bash
hykit --version
```
> [!NOTE]
> After project creation, Hykit automatically runs validation to highlight potential issues.
---

## Validation

`hykit validate` focuses on basic project consistency and common mistakes.

It checks:

* that `manifest.json` exists and is valid JSON
* required fields inside the manifest
* the `Main` entry and its corresponding Java file path
* package and class consistency for the main plugin class
* leftover template placeholders in key files
* presence of Gradle build files
* presence of the Gradle wrapper
* missing asset references inside JSON files

> [!NOTE]
> The scanner skips common tooling and cache directories such as `.git`, `.idea`, `.gradle`, `build`, `dist`, `.venv`, `venv`, and `node_modules`.

---

## Notes

> [!NOTE]
> If no author is provided during project creation, Hykit defaults to `hykit`.

> [!WARNING]
> Project names must be filesystem-safe. Values containing slashes, colons, `..`, trailing dots or spaces, or Windows reserved names will be rejected.

---

# For Developers

## Local Development

> [!TIP]
> Install Hykit in editable mode:

```bash
python -m pip install -e .
```

---

## Templates

> [!TIP]
> Templates are loaded from the bundled package by default.
> If not found, Hykit will attempt to load templates from HYKIT_TEMPLATE_PATH.

---

## License

Licensed under **NightLum Studios License (NSL)**.
See the [LICENSE](LICENSE) file for details.


