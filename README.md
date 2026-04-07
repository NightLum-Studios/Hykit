

<p align="center">
  <img src="Icon.png" alt="Luau Language Support Logo" width="120" height="160">
</p>

<h3 align="center">Hykit</h3>

> [!NOTE]
> This project is currently in active development. Expect changes, improvements, and occasional breaking updates.

---

## Installation

```bash
pipx install hykit
```

or for local development:

```bash
python -m pip install -e .
```

---

## Usage

```bash
hykit create Project MyMod
```

A new project will be generated in your current directory with all placeholders resolved.

---

## Placeholders

Templates use simple, flexible placeholders that adapt to different contexts:

* `{PROJECT_NAME}`
* `{PROJECT_NAME_LOWER}`
* `{PROJECT_NAME_SNAKE}`
* `{PROJECT_NAME_KEBAB}`
* `{PROJECT_NAME_PASCAL}`
* `{PROJECT_NAME_UPPER}`

---

> [!IMPORTANT]
> Choose the correct placeholder depending on context.
> For Java/Kotlin packages, prefer `{PROJECT_NAME_LOWER}` or `{PROJECT_NAME_SNAKE}`.

---

## Example

```text
package dev.{PROJECT_NAME_SNAKE}.plugin;
class {PROJECT_NAME_PASCAL}Plugin
rootProject.name = "{PROJECT_NAME}"
```

Structure is also updated automatically:

```text
src/main/java/dev/{PROJECT_NAME_SNAKE}/plugin/
```

---

## Philosophy

hykit is not just a generator — it's a foundation for building consistent, scalable project structures.

The goal is simple:

* reduce setup time
* enforce clean structure
* stay flexible for future expansion

---

> [!TIP]
> Use hykit as a base layer. You can extend templates, add your own systems, or build internal tooling on top.

---

## Development

```bash
python -m pip install -e .
hykit create Project TestMod
```

---

## License

Licensed under **NightLum Studios License (NSL)**.
See the [LICENSE](LICENSE) file for details.
