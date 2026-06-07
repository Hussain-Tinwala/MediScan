
# Contributing to MediScan 🩺

First off, thank you for considering contributing to MediScan! 

MediScan is an open-science initiative aimed at providing an accessible, highly accurate AI diagnostic baseline for researchers and developers. Whether you are fixing a bug, expanding our ML pipelines, or improving the Streamlit UI, your help is essential to making open-source healthcare AI more accessible.

This document outlines the process for contributing to the project.

## 🚀 How Can I Contribute?

### 1. Reporting Bugs & Requesting Features
If you find a bug or have a feature request, please check the [Issues](../../issues) page first to see if it has already been reported. If not, open a new issue. Please include as much detail as possible (e.g., OS, Python version, steps to reproduce).

### 2. Picking up an Issue
If you want to write code, look at our open issues. Issues labeled `good first issue` or `help wanted` are specifically reserved for new contributors and are a great place to start!

## 🛠️ Development Workflow

We follow the standard open-source Fork & Pull Request workflow. 

### Step 1: Fork and Clone
1. **Fork** the MediScan repository to your own GitHub account.
2. **Clone** your fork locally.

3. Add the original repository as an `upstream` remote.





### Step 2: Environment Setup

Ensure you have Python installed. Set up your virtual environment as outlined in the [README.md](https://www.google.com/search?q=README.md%23%25EF%25B8%258F-installation).

### Step 3: Create a Branch

Always create a new branch for your work. Do not work directly on the `main` branch.

```bash
git checkout -b feature/your-feature-name
# or for a bug fix:
git checkout -b fix/your-bug-fix

```

### Step 4: Make Your Changes

* Keep your commits focused and logical.
* If you are modifying the ML models or OCR parsers, please ensure your changes do not break existing data pipelines.
* If you are updating the frontend, ensure the Streamlit components degrade gracefully on different screen sizes.

### Step 5: Submit a Pull Request (PR)

1. Push your branch to your fork on GitHub:
```
git push origin feature/your-feature-name
```


2. Navigate to the original MediScan repository and click **Compare & pull request**.
3. Fill out the PR template. Clearly describe what you changed, why you changed it, and link to any relevant open issues (e.g., `Closes #12`).

## 📋 Code Review Process

Once you submit a PR, a maintainer will review your code. We may request changes or ask for clarification. Once everything looks good, your PR will be merged into the main branch!

## 🧪 Coding Standards

* **Python:** We follow standard PEP-8 conventions.
* **Dependencies:** If your PR requires a new library, please remember to update the `requirements.txt` file.
* **Documentation:** If you are adding a new feature, please include comments explaining your logic, especially within the OpenCV or Pandas data transformations.

Thank you for helping us build better open-source medical infrastructure!