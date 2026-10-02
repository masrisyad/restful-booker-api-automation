# Git Workflow Guide

This document contains the Git workflow used in the RESTful Booker API Automation project.

Every development task should be linked to a Jira work item using the Jira key in:

- Branch name
- Commit message
- Pull Request title

Example Jira work item:

```text
RBA-2 Setup API Automation Framework
```

---

## 1. Check Current Branch

Before starting development, verify the current Git branch.

```bash
git branch --show-current
```

Example output:

```text
main
```

---

## 2. Update Local Main Branch

Switch to the main branch:

```bash
git switch main
```

Pull the latest changes:

```bash
git pull origin main
```

This ensures development starts from the latest version of the project.

---

## 3. Create a Development Branch

Branch naming convention:

```text
<JIRA-KEY>-<short-description>
```

Example:

```text
RBA-2-setup-api-automation-framework
```

Create and switch to the new branch:

```bash
git switch -c RBA-2-setup-api-automation-framework
```

Verify the active branch:

```bash
git branch --show-current
```

Expected output:

```text
RBA-2-setup-api-automation-framework
```

---

## 4. Push the New Branch to GitHub

For the first push of a new branch:

```bash
git push -u origin RBA-2-setup-api-automation-framework
```

The `-u` option creates a tracking relationship between the local branch and the remote GitHub branch.

After this, future pushes can simply use:

```bash
git push
```

---

## 5. Check Development Changes

After modifying or creating files, check the current Git status:

```bash
git status
```

Example:

```text
Changes not staged for commit:

    modified: README.md

Untracked files:

    pytest.ini
    requirements.txt
    src/
    tests/
```

Files that should normally NOT be committed:

```text
.env
.venv/
__pycache__/
.pytest_cache/
reports/*.html
reports/*.xml
```

Files that SHOULD be committed:

```text
.env.example
pytest.ini
requirements.txt
src/
tests/
README.md
```

---

## 6. Add Files to Git Staging

Add all project changes:

```bash
git add .
```

Check the status again:

```bash
git status
```

Expected output:

```text
Changes to be committed:
```

Review the file list before committing.

Make sure files such as `.env` or `.venv` are not included.

---

## 7. Commit Changes

Commit naming convention:

```text
<JIRA-KEY> <description>
```

Example:

```bash
git commit -m "RBA-2 setup API automation framework"
```

Other examples:

```bash
git commit -m "RBA-3 add health check API test"
```

```bash
git commit -m "RBA-4 implement authentication API automation"
```

```bash
git commit -m "RBA-6 implement create booking automation"
```

The Jira key allows the commit to be traced back to the corresponding Jira work item.

---

## 8. Push Changes to GitHub

After committing:

```bash
git push
```

If the branch has not been pushed before:

```bash
git push -u origin <branch-name>
```

Example:

```bash
git push -u origin RBA-2-setup-api-automation-framework
```

---

## 9. Verify Repository Status

After pushing:

```bash
git status
```

Expected result:

```text
On branch RBA-2-setup-api-automation-framework

Your branch is up to date with
'origin/RBA-2-setup-api-automation-framework'.

nothing to commit, working tree clean
```

`working tree clean` means all committed changes have been saved locally and pushed correctly.

---

## 10. Create a Pull Request

Open the GitHub repository.

GitHub will usually display:

```text
Compare & pull request
```

Pull Request naming convention:

```text
<JIRA-KEY> <description>
```

Example:

```text
RBA-2 Setup API Automation Framework
```

Recommended Pull Request description:

```markdown
## Jira

RBA-2

## Summary

Setup the initial REST API automation framework.

## Changes

- Added Python API automation project structure
- Added pytest configuration
- Added environment configuration
- Added reusable Base API Client
- Added pytest fixtures
- Added Smoke, Regression, Negative, and E2E markers
- Added project dependencies
- Added project documentation

## Test

```bash
python -m pytest
```

## Result

Framework loads successfully without import or configuration errors.
```

---

## 11. Pull Request Review Flow

```text
Jira Work Item
      ↓
Move Jira to In Progress
      ↓
Create Git Branch
      ↓
Develop / Modify Code
      ↓
git status
      ↓
git add .
      ↓
git commit
      ↓
git push
      ↓
Create Pull Request
      ↓
Code Review / CI
      ↓
Merge to Main
      ↓
Move Jira to Done
```

---

## 12. Merge Pull Request

After the Pull Request passes review and CI checks, merge it into `main`.

Then switch back to the local main branch:

```bash
git switch main
```

Update local main:

```bash
git pull origin main
```

---

## 13. Delete Local Development Branch

After the Pull Request has been merged:

```bash
git branch -d RBA-2-setup-api-automation-framework
```

Delete the remote branch if GitHub has not already deleted it:

```bash
git push origin --delete RBA-2-setup-api-automation-framework
```

---

## 14. Start the Next Jira Task

Example:

```text
RBA-3 Implement Health Check API Automation
```

Make sure `main` is updated:

```bash
git switch main
git pull origin main
```

Create the next branch:

```bash
git switch -c RBA-3-health-check-automation
```

Push the branch:

```bash
git push -u origin RBA-3-health-check-automation
```

Development can now begin for `RBA-3`.

---

## Git Naming Convention Summary

| Git Activity | Convention | Example |
|---|---|---|
| Jira Work Item | `JIRA-KEY Description` | `RBA-3 Implement Health Check API Automation` |
| Branch | `JIRA-KEY-short-description` | `RBA-3-health-check-automation` |
| Commit | `JIRA-KEY description` | `RBA-3 add health check API test` |
| Pull Request | `JIRA-KEY Description` | `RBA-3 Implement Health Check API Automation` |

---

## Common Git Commands

Check repository status:

```bash
git status
```

Check current branch:

```bash
git branch --show-current
```

List all local branches:

```bash
git branch
```

Switch branch:

```bash
git switch <branch-name>
```

Create a new branch:

```bash
git switch -c <branch-name>
```

Get latest main branch:

```bash
git pull origin main
```

Stage all changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "RBA-X description"
```

Push changes:

```bash
git push
```

View recent commits:

```bash
git log --oneline -10
```

---

## Recommended Daily Git Workflow

For every Jira work item:

```bash
git switch main
git pull origin main
git switch -c RBA-X-short-description
```

Develop and test the change.

Then:

```bash
git status
git add .
git status
git commit -m "RBA-X description"
git push -u origin RBA-X-short-description
```

Create a Pull Request in GitHub.

After the Pull Request is merged:

```bash
git switch main
git pull origin main
git branch -d RBA-X-short-description
```

Then continue with the next Jira work item.
