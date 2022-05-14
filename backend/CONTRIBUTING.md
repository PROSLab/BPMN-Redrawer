# Project Guidelines

## Project Structure

- Api, containing all the modules related to the REST APIs management:
  - Controllers, to expose the functionalities through APIs;
  - Services, to manage the business logic (Object/Keypoint Detection, OCR, conversion...) 
  - Repositories, to store and retrieve data from Firebase;
  - Schemas, containing all the needed DTOs;
- Bpmn, containing the modules to manage all the BPMN elements;
- Firebase, to manage the Firebase configuration and services;
- Commons, where the common utilities are placed; 
- Tests, folder containing all the tests of the backend.

## How to submit changes

Keep your commits small, clean and single purpose. Do not commit directly on master branch: open a branch, do some changes, open a pull request.

### Pull requests
- After you submit your pull request, verify that all status checks are passing.
- Always squash and merge, do not directly merge commits to branch or rebase and merge.
- Follow the styleguides.

## Styleguides

### Commit messages

- Use the present tense
- Limit the first line to 72 characters or less

### Pull request title

- Limit the first line to 72 characters or less
- It must be the same as the task title.

### Python styleguide

All python code is linted with [Black](https://black.readthedocs.io/en/stable/) and checked with [Flake8](https://flake8.pycqa.org/en/latest/).
Make sure to install them as a pre-commit hook, you can do it by following this guide [pre-commits: black and flake8](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/).

### Documentation styleguide

- Docstrings follow [numpy-style standards](https://numpydoc.readthedocs.io/en/latest/format.html)

## Testing

We use [PyTest](https://docs.pytest.org/en/6.2.x/) and [Tox](https://tox.wiki/en/latest/index.html) to run tests.
Tests are located in the tests folder. You can create new folders or files by following the pytest conventions.
