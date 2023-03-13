# timesheet
[IN DEVELOPMENT] a tool for tracking the hours you work


## Package structure
Directory tree generated using [file-tree-generator](https://marketplace.visualstudio.com/items?itemName=Shinotatwu-DS.file-tree-generator) Visual Studio Code extension:
```
📦timesheet
 ┣ 📂outputs
 ┃ ┣ 📜.gitkeep
 ┣ 📂scripts
 ┃ ┗ 📜main.py
 ┣ 📂tests
 ┃ ┗ 📜test_timesheet.py
 ┣ 📂timesheet
 ┃ ┣ 📜timesheet.py
 ┃ ┗ 📜__init__.py
 ┣ 📜.gitignore
 ┣ 📜.pre-commit-config.yaml
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┗ 📜setup.py
```

## `precommit` installation

Install python `pre-commit` with:
```bash
pip install pre-commit
```

Within repository folder run:
```bash
pre-commit install
```

The hooks within `.pre-commit-config.yaml` will now be triggered every time you use the `git commit` command. For more information see [pre-commit.com/](https://pre-commit.com/).
