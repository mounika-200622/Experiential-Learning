\# Lab 5: Reflection



\## 1. Which issues were the easiest to fix, and which were the hardest? Why?



\*\*Easiest:\*\* the style issues from Flake8 and Pylint. Missing blank lines (E302), lines that were too long (E501), `== None` instead of `is None`, the camelCase function name, missing docstrings and the missing final newline. Each one had a clear message and a fix that was one or two lines long, and they did not change how the program behaves.



\*\*Hardest:\*\* the shell injection in `ping\_user\_machine` (Bandit B602). Removing `shell=True` was not enough. Bandit then reported B603/B607, so I also had to validate the hostname with a regex and pass the command as a list. I also had to handle the difference between Windows (`ping -n`) and Linux (`ping -c`). The hardcoded password was also tricky, because removing it meant deciding where the password should come from (an environment variable) and what to do when it is missing.



The urgency bug was hard in a different way: none of the tools reported it. I only found it by running the program and noticing that a ticket with urgency `-7` was accepted and that typing `abc` crashed the program.



\## 2. Did the static analysis tools report any false positives? If so, describe one example.



Yes. Bandit B404 flags `import subprocess` just because the module is imported, even though using it is fine once the call is safe. After my fix, B603 and B607 still warned about the `subprocess.call` with a list and a regex-checked hostname, which is no longer exploitable. I marked these with `# nosec` comments that name the specific codes, after checking that the risk was handled. I did not just hide them.



Also, Pylint's `global-statement` (W0603) is reasonable advice, but for a small script with one counter, a global is acceptable, so I disabled it on that one line instead of redesigning the program into a class.



\## 3. How would you integrate static analysis tools into your actual software development workflow?



\- \*\*Locally:\*\* run Flake8 and Pylint in the editor (VS Code extensions) so problems show while typing, and use a \*\*pre-commit hook\*\* that runs Flake8, Pylint and Bandit before every commit.

\- \*\*In CI:\*\* add a GitHub Actions workflow that runs all three tools on every push and pull request, and fails the build if Bandit finds Medium/High issues, Flake8 finds any errors, or the Pylint score drops below 9.5.

\- \*\*Configuration:\*\* keep the settings in `.pylintrc` / `setup.cfg` so the whole team uses the same rules, and require a written reason for every `# nosec` or `# pylint: disable`.



\## 4. What tangible improvements did you observe in code quality, readability, or potential robustness after applying the fixes?



\- \*\*Scores:\*\* Pylint went from \*\*5.53/10 to 10.00/10\*\*, Bandit from \*\*4 issues (1 High) to 0\*\*, Flake8 from \*\*15 issues to 0\*\*.

\- \*\*Security:\*\* a hostname can no longer inject shell commands, and the admin password is no longer stored in the source code or on GitHub.

\- \*\*Robustness:\*\* invalid urgency values (`-7`, `9`, `abc`) are rejected with a clear message instead of being saved or crashing the program. A note on a missing ticket now prints a message instead of failing silently. Files are always closed properly with `with`.

\- \*\*Readability:\*\* every function has a docstring, names follow PEP 8, and long lines are split, so the code is easier to read and explain.

\- \*\*Lesson learned:\*\* the tools caught most problems quickly, but not the logic bug. Static analysis does not replace testing and actually running the program.

