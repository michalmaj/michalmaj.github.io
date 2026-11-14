# michalmaj.github.io

Source of the teaching site published at <https://michalmaj.github.io/>: course pages, task sets
and links to the repositories with code and exercises.

## Structure

| Path | Contents |
|---|---|
| `content/` | pages in Markdown, one directory per language (`pl/`, `en/`) |
| `data/` | courses, linked repositories, interface strings, published URLs |
| `renderer/` | site generator configuration and theme |
| `src/teaching_hub/` | build pipeline: validation, assembly, rendering and checks |
| `tests/` | tests and a placeholder fixture that is never published |
| `docs/` | [how to add and maintain content](docs/adding-content.md) |

## Build locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked
uv run teaching-hub validate
uv run teaching-hub build --production
```

The site is written to `_site/`. GitHub Actions builds and publishes it from `main`.

## Reporting problems

Found a mistake, an unclear instruction or a broken link? Please report it in
[GitHub Issues](https://github.com/michalmaj/michalmaj.github.io/issues).

## License

- Code (pipeline, tests, configuration, workflows): [MIT](LICENSE).
- Original teaching content: [CC BY 4.0](LICENSE-CONTENT.md).
- Linked repositories and third-party material keep their own licenses.
