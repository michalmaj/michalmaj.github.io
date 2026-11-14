# Adding and maintaining content

This guide is for whoever maintains the teaching site: adding a course, a task set or a link to
course materials, and getting the change safely to <https://michalmaj.github.io/>.
It describes the system as it works today.

## How the site is made

The site is generated from two directories of this repository:

- `content/` holds the pages, in Markdown, one directory per language (`pl/`, `en/`);
- `data/` holds courses, linked repositories, interface strings and the registries of published
  URLs and anchors.

The pipeline (`uv run teaching-hub …`):

1. validates the data and the pages;
2. assembles one renderer project per space and language;
3. renders them with Zensical, which produces the published site, and MkDocs Material, as a
   control build;
4. composes the builds into one site in `_site/`;
5. checks the result.

GitHub Actions publishes `_site/` from `main` to GitHub Pages.

| Space | Polish | English |
|---|---|---|
| home page and licensing | `/`, `/licensing/` | `/en/`, `/en/licensing/` |
| teaching space | `/courses/…` | `/en/courses/…` |
| professional space (reserved, disabled) | `/for-employers/` | `/en/for-employers/` |

Polish is the default language. An English page exists only where English content exists; nothing
is translated automatically.

## Files at a glance

| What | Where |
|---|---|
| home page | `content/<lang>/home/index.md` |
| licensing page | `content/<lang>/home/licensing.md` |
| catalogue introduction (optional) | `content/<lang>/courses/index.md` |
| "how to use" page (optional) | `content/<lang>/courses/how-to-use.md` |
| repository catalog: page text (optional) | `content/<lang>/courses/repositories.md` |
| course description | `content/<lang>/courses/<course-id>/index.md` |
| task set | `content/<lang>/courses/<course-id>/task-sets/NN-<slug>.md` |
| guide (information page of a course) | `content/<lang>/courses/<course-id>/guides/<slug>.md` |
| courses | `data/courses.yml` |
| linked repositories | `data/repositories.yml` |
| third-party material (optional, only when used) | `data/third-party.yml`, files in `assets/third-party/` |
| interface strings | `data/i18n/pl.yml`, `data/i18n/en.yml` |
| published URLs | `data/published-urls.txt` |
| published anchors that changed | `data/anchor-aliases.yml` |

Any other file under `content/` fails validation (`unexpected-file`).

## Add a course

1. **Add an entry to `data/courses.yml`:**

   ```yaml
   courses:
     - id: software-engineering        # URL segment: /courses/software-engineering/
       name:
         pl: "Inżynieria oprogramowania"  # required
         en: "Software Engineering"       # only when there is English content
       summary:
         pl: "One or two sentences shown on the course card."
       order: 1                          # position in the catalogue
   ```

   - The `id` is lowercase ASCII letters, digits and hyphens. It becomes part of public URLs, so do
     not change it after publication.
   - Some names are reserved because the site or the renderer uses them (`how-to-use`, `assets`,
     `search`, `stylesheets`, `javascripts`, `404`).
2. **Optionally write the course description** in `content/<lang>/courses/<course-id>/index.md`.
   This page is Markdown only, without front matter. The course name, the breadcrumb, the list of
   task sets and the repositories used are added by the pipeline.
3. **Add at least one task set or guide.**

A course is shown in a language only when it has all three, in that language:

- a name;
- a description (a `summary` or a non-empty `index.md`);
- at least one published task set or guide.

Published material of a course that cannot be shown is an error (`course-not-visible`), so nothing
disappears silently.

## Add a task set

A task set is one file: `content/<lang>/courses/<course-id>/task-sets/NN-<slug>.md`.

- **`NN`** is the position of the set in the course: two digits, unique per course and language. The
  page shows it as "Zestaw N" / "Set N".
- **`<slug>`** is the URL: `/courses/<course-id>/task-sets/<slug>/`. It is lowercase ASCII with hyphens
  and is not changed after publication.

```markdown
---
title: "Jestem developerem"
summary: "Shown on the task set card on the course page."
status: published                   # published | archived
estimated_duration_minutes: 90      # optional
requires: [other-set-slug]          # optional: sets of the same course to do first
materials:                          # optional: materials for the whole set
  - repository: software-engineering-in-practice
    path: START-HERE.pl.md
    lang: pl
    label: "Zacznij tutaj"
tasks:                              # optional: per-task settings, keyed by task id
  lab-01:
    materials:
      - repository: software-engineering-in-practice
        path: labs/01-workstation/README.pl.md
        lang: pl
        label: "Instrukcja: Lab 01"
  lab-02:
    optional: true
---
## Cel

Free Markdown before the tasks.

## Zadania

### Witaj na swoim stanowisku pracy {#lab-01}

What to do, what the result is, how to check it.

### Terminal jako narzędzie pracy {#lab-02}

…
```

Rules checked by `validate`:

- **Tasks section:** the page needs a section with the heading of `section_tasks` from `data/i18n`
  ("Zadania" in Polish, "Tasks" in English). Each task in it is a level-3 heading with an explicit
  id: `### Title {#task-id}`.
- **Task ids** are lowercase with hyphens and unique in the set. They are public anchors
  (`…/task-sets/<slug>/#lab-01`), so do not change them after publication.
- **Task settings:** every key under `tasks:` must match a task heading.
- **References:** `requires` and `replaced_by` must name task sets of the same course and language.

What the pipeline adds:

- **The page title**, "Zestaw N · title", so do not write your own `#` title.
- **Task numbers** in front of task titles ("Zadanie 1.", "Zadanie 2." …), and an "optional" badge
  where `optional: true`.
- **Materials:** set-level materials go into the materials section (heading `section_materials`:
  "Materiały" / "Materials"). The pipeline creates that section before the tasks if the page has
  none. Task materials go under each task.

An English version is a file with the same name under `content/en/…`. Its task ids should match the
Polish version; a difference is reported as a warning.

## Add a guide

A guide is an information page of a course: `content/<lang>/courses/<course-id>/guides/<slug>.md`,
at `/courses/<course-id>/guides/<slug>/`. Its front matter has `title`, `summary`, `status`, `order`
(position among the course's guides) and `materials`. It does not need a tasks section.

## Materials and links to repositories

A material is either a file or directory in a registered repository, or an external page:

```yaml
- repository: software-engineering-in-practice   # id from data/repositories.yml
  path: labs/05-works-on-my-machine/README.pl.md # a file; a directory ends with "/"
  ref: v2.0.0                                    # optional tag or branch; default: the repository's default_branch
  lang: pl                                       # language of the material: pl | en
  label: "Instrukcja: Lab 05"
- url: https://git-scm.com/doc                    # external material, https only
  lang: en
  label: "Git documentation"
```

The site shows each material as a link (GitHub `blob/` for a file, `tree/` for a directory) with
a language badge.

**Register every repository** in `data/repositories.yml`:

```yaml
repositories:
  - id: software-engineering-in-practice
    name: Software Engineering in Practice
    url: https://github.com/michalmaj/software-engineering-in-practice
    default_branch: main
    maturity: not_assessed     # not_assessed | in_development | stable | maintenance | archived
    description:
      pl: "One or two sentences for the repository catalog."
    technologies: [Python, Go, Java]
    content_languages: [en, pl]
    licenses: {code: MIT, content: CC-BY-4.0}   # SPDX ids, as in the repository's license files
    issue_templates: true      # the repository has issue templates or forms
    documentation_url: https://…  # optional: a published site of the repository
```

Record only facts checked in the repository itself: technologies from its project files, languages
of its materials and the licenses of its license files. A repository with one MIT `LICENSE` for the
whole project has MIT for both code and content.

**Checks on materials:**

- Material paths must stay inside the repository, and links in pages must not point to local paths
  or services (`file:`, `/Users/…`, `C:\…`, `localhost`) (`local-path`). Instruction text and code
  blocks may still mention such paths.
- `uv run teaching-hub check-materials --repos-root <dir>` checks that every
  `(repository, ref, path)` exists, read-only, in local clones named after the repository id
  (`<dir>/<repository-id>`). Branches are read from `origin/<branch>`, so fetch first.
- In pull requests, CI runs the same check in fresh clones.

**Links to files of this repository** (for example `LICENSE`) must point to files that exist in the
same commit; production builds check this (`broken-repository-link`).

## Repository catalog

`/courses/repositories/` lists **every repository in `data/repositories.yml`**. It exists in a
language when `content/<lang>/courses/repositories.md` exists. That file holds the text shown above
the cards, for example how to give feedback; it is Markdown only, without front matter.

Each card shows:

- the name, linked to the repository, and the description in the page's language;
- technologies, languages of the materials and licenses;
- "w rozbudowie" / "in development" when `maturity: in_development`;
- the courses that use the repository: only public courses whose published task sets or guides
  link it, so there is never a link to a course that is not published;
- links to the repository and to report a problem. With `issue_templates: true` the link opens the
  repository's chooser of issue forms (`/issues/new/choose`); otherwise it opens a blank issue
  (`/issues/new`). Keep the flag in line with the repository's `.github/ISSUE_TEMPLATE/`.

Because the catalog links every registered repository, the licensing page lists the licenses of
all of them.

## Status: published and archived

| `status` | Page | Navigation, lists | Search |
|---|---|---|---|
| `published` | built | listed | indexed |
| `archived` | built at the same URL, with an "archived" notice | not listed | not indexed |

Use `archived` to retire a task set or guide without breaking its URL. On an archived task set,
`replaced_by: <slug>` adds a link to the set that replaces it.

**Drafts never go into `content/`;** `status: draft` there is an error. Draft files are kept outside
the repository, in a directory with the same layout as `content/`. To preview them locally,
overlay that directory with `uv run teaching-hub build --drafts <dir>`. Draft pages then carry a "draft" banner. Draft preview
is refused in CI, and production builds never include drafts.

## Public URLs and anchors

**`data/published-urls.txt`** lists every public page of the site.

- **List and record:** `uv run teaching-hub urls` lists the URLs the current content produces;
  `uv run teaching-hub urls --write` writes them to the file. Commit the file together with the
  content change.
- **New pages:** a production build fails when a public page is not in the file
  (`url-not-registered`).
- **Removed pages:** validation fails when a URL in the file is no longer produced (`url-removed`).
  There are no redirects, so keep URLs stable; archive instead of deleting. Removing a page on
  purpose means removing its line in the same change.
- **The home page:** `/` in the file records that the site is published. Removing the Polish home
  page while `/` is listed stops the deployment with an error. Unpublishing the whole site on
  purpose means removing the home page and its URLs in one change, and then disabling GitHub Pages
  in the repository settings; the last deployment stays online until then.

**Heading anchors.**

- **How ids are made:** heading ids come from the heading text, written without diacritics:
  "Materiały do zajęć" becomes `#materialy-do-zajec`. Task ids are explicit (`{#lab-01}`).
- **Changed anchors:** a heading anchor is a public link too. When a published heading id changes
  (for example after renaming the heading), add an entry to **`data/anchor-aliases.yml`**:

  ```yaml
  aliases:
    - page: /licensing/                 # public URL of the page
      anchor: materiay-osob-trzecich    # the id that was published
      target: materialy-osob-trzecich   # the heading id it now stands for
  ```

  The old id stays on the heading, so old links keep working.
- **Keep the entries:** do not remove them. A build fails when an alias or its target is missing
  from the page (`broken-anchor-alias`).

## Search

Each build has a search index. When the site is composed, the builds of one language that share a
search group get one combined index:

- **Teaching group:** the home space and the teaching space (`search_group: teaching` in
  `renderer/spaces/*.yml`). Searching from `/` finds course material, and searching from a course
  page finds `/licensing/`.
- **Professional space:** it has its own group, so its pages and teaching pages never appear in each
  other's results.

Languages are never mixed, archived pages stay out of the index, and drafts are never built into it.
A production build checks that the builds of a group list the same existing pages and anchors, each
once (`search-index`).

## Interface strings

Text that the pipeline adds to pages comes from `data/i18n/pl.yml` and `data/i18n/en.yml`:
navigation labels, section headings, badges, footers, the 404 page and accessible names of buttons.
Every key must exist in both files.

## Build and check locally

You need [uv](https://docs.astral.sh/uv/). Run these commands from the repository root:

```bash
uv sync --locked                       # install the pinned tools
uv run pytest                          # tests (uses a placeholder fixture, never real content)
uv run teaching-hub validate           # data and pages
uv run teaching-hub urls               # public URLs of the current content
uv run teaching-hub build --production # Zensical build into _site/, with the production checks
uv run teaching-hub build --production --renderer material --build-dir build/material --site-dir _site-material
python3 -m http.server -d _site 8000   # look at it: http://127.0.0.1:8000/
```

- **Production checks** run as part of `build --production`. They cover:
  - internal links, anchors and resources, and every expected page;
  - canonical URLs, one sitemap and `robots.txt`;
  - the URL registry, anchor aliases and search indexes;
  - links to this repository's files;
  - no draft banners, test fixture identifiers, private files or third-party requests.
- **Re-checking a built site:** `uv run teaching-hub check --production --source .` checks it again.
- **Browser tests:** `tests/test_browser.py` checks keyboard use, accessibility and search in a real
  browser. It runs only when `TEACHING_HUB_CHROME` points to Chrome or Chromium, and needs
  Node.js 22+.

## From a branch to the published site

1. **Create a branch from `main`** and commit the change, including `data/published-urls.txt` and,
   if needed, `data/anchor-aliases.yml`.
2. **Open a pull request.** CI runs three checks:
   - **`Tests`**: the test suite.
   - **`Build and check`**: the pipeline on the placeholder fixture; it also confirms that draft
     preview is refused in CI.
   - **`Production content`**: the repository's real content.
     - It validates, checks materials in fresh clones of the linked repositories, builds with both
       renderers and runs the production checks.
     - It uploads the site as the `production-site` artifact (kept for 7 days).
     - It never deploys.
3. **Review.** Download the `production-site` artifact from the pull request's Actions run and look at
   the changed pages, on a phone width too.
4. **Merge.** `main` accepts changes only through pull requests with the three checks passing.
   **Merging deploys the site.**
5. **Deployment.** The Pages workflow on `main` runs the tests, the private-file check and the
   publication-state check, validates, builds with both renderers, checks the artifact and deploys.
   If any step fails, nothing is deployed and the previous version stays online. The workflow never
   runs for pull requests.
6. **After deployment,** open the changed pages on <https://michalmaj.github.io/>.

## Keeping drafts and private files out

- **Drafts** live outside the repository and only reach a local preview. A production build refuses
  them, and the checks fail if a draft banner appears in the site.
- **Private files:** `.gitignore` excludes private documents and generated output.
  `teaching-hub check-tracked` (in CI and before every deployment) fails if such files are tracked.
  The patterns are in `PRIVATE_PATTERNS` in `src/teaching_hub/check.py`.
- **The test fixture** (`tests/fixtures/sample/`) is placeholder data for the tests. A production
  build refuses it, and its identifiers must never reach the site.
- **Third-party material** (optional, only when the site uses any): every file in
  `assets/third-party/` needs an entry in `data/third-party.yml` with author, source and license. The licensing page lists these entries.

## Current limits

- **Files under `content/`:** only the Markdown files listed above are accepted. The pipeline does
  not copy images or other files into the site.
- **No redirects:** a published URL can only be kept or deliberately removed.
- **The professional space** (`/for-employers/`) is reserved and disabled; files there are ignored
  with a warning.
