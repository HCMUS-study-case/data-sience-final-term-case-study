# data-sience-final-term-case-study

## Member

1. Nguyễn Phú Tân - 20120573
2. Nguyễn Lê Tuấn Khải - 20120503
3. Nguyễn Minh Quân - 20120554
4. Nguyễn Đình Phong - 20120546

## Data Source

Stock data ASIA PACIFIC INVESTMENT in Hanoi Stock Exchange[reference](https://www.stockbiz.vn/Stocks/API/ForeignerTrading.aspx)

Dataset includes 3 files:

## Installation

### 1. Setup environment

#### 1.1. Install python 3.10.6 and virtualenv (venv)

##### 1.1.1. Install python 3.10.6

##### 1.1.2. Install virtualenv library via pip

```
pip install virtualenv
```

##### 1.1.3. Create a virtual environment

```
python -m virtualenv venv (linux or mac)
```

or

```
py -3 -m venv venv (windows)
```

1.1.4. Activate the virtual environment

```
source venv/bin/activate
```

or

```
Set-ExecutionPolicy ExecutionPolicy RemoteSign -Scope Process
venv\Scripts\activate
```

1.1.5. Install the required libraries

```
pip install pipenv
pipenv install
```

### 2. Choose your aproach to code

#### 2.1. Jupyter Notebook (Web Browser)

##### 2.1.1. Run Jupyter Notebook

- In the terminal, run the following command:

```terminal
   jupyter lab
```

- The Jupyter Notebook will open in your default browser. _**Press**_ _Ctrl+C_ in the terminal to stop the server.

#### 2.2. Jupyter Notebook (VSCode)

##### 2.2.1. Install Jupyter extension

- Type jupyter in the extensions search box and install the Jupyter extension by Microsoft. Such as: Jupyter, Jupyter Keymap, Jupyter Notebook Renderers, Jupyter Slide Show, Jupyter Cell Tags, e.g.
- Reload VSCode.

##### 2.2.2. Run Jupyter Notebook

- In the VSCode, create a new file with the extension .ipynb.
- Open this file and click on the Jupyter icon in the left panel.
- Choose the kernel you want to use. **Sometimes**, we recommend you to choose the kernel with the name of the virtual environment you created.

### 3. Notes

- Please, use the virtual environment to run the code. If you don't use the virtual environment, you may have some problems with the libraries. And we don't want to waste your time to fix the problems.

- Please complete your task in jira dashboard. If you have any questions, please contact us via slack.

- Please, use the git to manage your code. If you don't know how to use git, please contact us via slack.

- Important:

  - Please, don't push your code to the main branch or the develop branch.
  - Please create a new branch for each task. The branch name must be match the syntax:

  ```
  feature/<task-id>-<task-name>
  fix/<task-id>-<task-name>
  bug/<task-id>-<task-name>

  That is the valid syntaxes, and the invalid syntaxes are:
  hotfix/<task-id>-<task-name>
  release/<task-id>-<task-name>

  Which <task-id> is the id of the task in jira dashboard and <task-name> is the name of the task in jira dashboard.

  Remember: the task name must be in lowercase and use "-" to separate words.
  ```

  - Don't forget to create a pull request to merge your code to the develop branch. After that, you can assign to someone to check and merge your branch. Very obvious, if your branch not pass the check (including automation test or manual test), you can't merge your branch to the develop branch.
  - Because of jupyter notebook can't use git for detect a change in the jupyter file extracted, so we use a additional library to detect a change in the jupyter file (nbdime). Hence, you should check this library is installed in your virtual environment. If not, please install it via pip.
    > pip install nbdime

- How to use nbdime with git
  - To use nbdime with git, you need to install nbdime and enable the git extension. Please check this tool installed, If not run the following commands in your terminal:
  ```
  pip install nbdime
  nbdime config-git --enable --global
  ```
  - After that, you can use git as usual. If you want to see the diff of your notebook, you can use the following command:
  ```
  git diff
  ```
  - If you want to see the diff of your notebook in the web browser, you can use the following command:
  ```
  git difftool
  or
  git difftool --tool=nbdiffweb
  or
  git difftool --tool=nbdiffweb -- "*.ipynb"
  ```
- In this repository, we use reviewNB to detect a change in the jupyter file when you create a pull request.
