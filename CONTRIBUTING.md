# 🤝 Contributing to PyQueryTracker

Welcome! 👋  
Thank you for considering a contribution to **PyQueryTracker** — a lightweight and extensible query tracking library for Python applications.

We appreciate all kinds of contributions, from code and documentation to bug reports and feature ideas. This guide will help you get started.

---

## 🚀 Project Overview

**PyQueryTracker** provides a Python decorator to track and analyze query performance in web applications. It’s designed to be easy to integrate into FastAPI, support customizable exporters, and work well in production and development environments.

---

## Assumptions

1. **You're familiar with [GitHub](https://github.com) and the [Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)(PR) workflow.**

## How to Contribute

1. Make sure that the contribution you want to make is explained or detailed in a GitHub issue! Find an [existing issue](https://github.com/MuddyHope/pyquerytracker/issues/) or [open a new one](https://github.com/MuddyHope/pyquerytracker/issues/new).
2. Once done, [fork the pyquerytracker repository](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) in your own GitHub account. Ask a maintainer if you want your issue to be checked before making a PR.
3. [Create a new Git branch](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-and-deleting-branches-within-your-repository).
4. Review the necessary checks that describes the steps to maintain the repository.
5. Make the changes on your branch.
6. Submit the branch as a PR](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) pointing to the `main` branch of the main meilisearch-python repository. A maintainer should comment and/or review your Pull Request within a few days. Although depending on the circumstances, it may take longer.<br>

We do not enforce a naming convention for the PRs, but **please use something descriptive of your changes**, having in mind that the title of your PR will be automatically added to the next

## 🧠 How You Can Contribute

Here are some ways you can help:

- 🐛 Report bugs or suggest improvements via [Issues](https://github.com/MuddyHope/pyquerytracker/issues)
- 📊 Build new exporters (JSON, CSV, Prometheus)
- ⚙️ Integrate with frameworks like FastAPI, Flask
- 🧪 Expand test coverage with Pytest
- 📖 Improve documentation or add examples
- 🧰 Create a CLI wrapper for runtime stats inspection

---

## 🛠️ Development Setup

### 1. Clone the repo

```bash
git clone https://github.com/MuddyHope/pyquerytracker.git
cd pyquerytracker
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`
```

### 3. Install development dependencies

```bash
pip install -r requirements-dev.txt
```

---

## 🧪 Running Tests and Linting

### Run tests with Pytest

```bash
pytest
```

### Format code and sort imports

```bash
black .
isort .
```

---

## 🌿 Working on a Feature

1. Create a new Git branch:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes.

3. Push your branch and [open a Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork).

---

## 📌 Pull Request Guidelines

- Make sure your changes address an existing [issue](https://github.com/MuddyHope/pyquerytracker/issues) or clearly explain what they fix or improve.
- Follow existing formatting (`black`, `isort`).
- Keep commits clean and descriptive.
- A maintainer will review and may request changes before merging.

---

Thank you for contributing to PyQueryTracker! 💙
