\# Lab 5: Issues Found and Fixed (helpdesk\_system.py)



| # | Issue | Type | Tool / Code | Severity | Line(s) (original) | Description | Fix Approach |

|---|-------|------|-------------|----------|--------------------|-------------|--------------|

| 1 | Shell injection in `ping\_user\_machine` | Security | Bandit B602 | High | 38 | `subprocess.call("ping -c 1 " + hostname, shell=True)` lets a hostname like `x; del \*` run extra commands | Pass a list of arguments without `shell=True`, validate the hostname with a regex, choose `-n`/`-c` by OS |

| 2 | Hardcoded admin password | Security | Bandit B105 | Low (but serious) | 8, 54 | `ADMIN\_PASSWORD = "helpdesk@123"` is visible to anyone who reads the code or repo | Read it from the environment variable `HELPDESK\_ADMIN\_PASSWORD`; refuse to close tickets if it is not set |

| 3 | Bare `except: pass` hides errors | Bug / Security | Bandit B110, Pylint W0702, Flake8 E722 | Medium | 23-24 | `add\_note(999, ...)` fails silently, so the note is lost without any message | Catch only `KeyError` and print a clear message |

| 4 | Mutable default argument | Bug | Pylint W0102 | Medium | 10 | `audit\_trail=\[]` is shared across every call, so the logs pile up between tickets | Default to `None` and create a new list inside the function |

| 5 | Urgency not validated (not flagged by any tool) | Logic bug | Found by running the program | High | 13, 48, 52 | Urgency `-7` was accepted as a ticket, and typing `abc` crashed the program with `ValueError` | Check that urgency is 1-5 in `raise\_ticket`, catch `ValueError` in `main()` and print "Ticket rejected" |

| 6 | File opened without `with`/encoding | Bug | Pylint R1732, W1514 | Medium | 41-43 | File may not close if an error happens; encoding depends on the OS | `with open(file, "w", encoding="utf-8") as handle:` |

| 7 | Comparison to `None` with `==` | Style / Bug | Pylint C0121, Flake8 E711 | Low | 33 | `tech == None` should use identity check | Use `is None` |

| 8 | Function name not snake\_case | Style | Pylint C0103 | Low | 30 | `unresolvedHighPriority` breaks PEP 8 naming | Renamed to `unresolved\_high\_priority` |

| 9 | Iterating keys then indexing | Style | Pylint C0206 | Low | 32-33 | `for t in tickets: tickets\[t]\[...]` | Use `for ticket\_id, ticket in tickets.items()` |

| 10 | Old `%` string formatting | Style | Pylint C0209 | Low | 14 | `"%s raised #%d" % (...)` | Use an f-string |

| 11 | Unused variable `t2` | Style | Pylint W0612, Flake8 F841 | Low | 47 | Value assigned but never used | Call `raise\_ticket(...)` without assigning |

| 12 | Missing docstrings | Style | Pylint C0114, C0116 | Low | all functions | No module or function docstrings | Added a docstring to the module and every function |

| 13 | Global constant naming | Style | Pylint C0103 | Low | 7 | `ticket\_counter` is module-level but not UPPER\_CASE | Renamed to `TICKET\_COUNTER` |

| 14 | Lines too long | Style | Flake8 E501, Pylint C0301 | Low | 13, 14, 52 | Lines over 79 characters | Split the dictionary and calls over several lines |

| 15 | Missing blank lines | Style | Flake8 E302, E305 | Low | 10-58 | Only 1 blank line between functions | 2 blank lines between top-level definitions |

| 16 | No `\_\_main\_\_` guard | Style | Manual review | Low | 58 | `main()` runs even when the file is imported | Wrapped in `if \_\_name\_\_ == "\_\_main\_\_":` |



\## Results



| Tool | Before | After |

|------|--------|-------|

| Pylint | 5.53/10 | 10.00/10 |

| Bandit | 4 issues (1 High, 3 Low) | 0 issues |

| Flake8 | 15 issues | 0 issues |

