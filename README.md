\[tool.poetry]

name = "my-bank-project"

version = "0.1.0"

description = "Bank project"

authors = \["Your Name <you@example.com>"]

requires\_python = ">=3.9"

dependencies = {}



\[build-system]

requires = \["poetry-core>=2.0.0,<3.0.0"]

build-backend = "poetry.core.masonry.api"



\[tool.poetry.group.lint.dependencies]

flake8 = "^7.3.0"

black = "^26.5.1"

isort = "^8.0.1"

mypy = "^2.1.0"



\[tool.black]

line-length = 88

target-version = \['py39', 'py310', 'py311']



\[tool.isort]

profile = "black"

line\_length = 88



\[tool.mypy]

python\_version = "3.9"

warn\_return\_any = true

check\_untyped\_defs = true

disallow\_untyped\_defs = true

