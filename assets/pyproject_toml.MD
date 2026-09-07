# `pyproject.toml` 编写规则

本文档规定 Piper SDK 中 `pyproject.toml` 的位置、职责和修改边界。当前项目使用 `setuptools` 和 `setup.py` 维护包元数据，`pyproject.toml` 仅用于声明 PEP 517 构建后端及其构建依赖。

## 1. 文件位置

`pyproject.toml` 必须位于仓库根目录，并与 `setup.py` 同级：

```text
piper_sdk/
├── pyproject.toml
├── setup.py
├── tox.ini
├── piper_sdk/
│   ├── __init__.py
│   └── ...
└── assets/
```

不要在 Python 包源码目录 `piper_sdk/` 内创建 `pyproject.toml`。执行 `pip install .` 时，构建工具以仓库根目录作为项目根；源码目录中的同名文件会形成错误层级的独立配置，无法正确描述根项目的构建方式。

## 2. 当前最小配置

当前根目录配置如下：

```toml
[build-system]
requires = [
    "setuptools>=39.0,<60; python_version < '3.7'",
    "setuptools>=39.0; python_version >= '3.7'",
]
build-backend = "setuptools.build_meta"
```

各字段含义：

|字段|作用|
|---|---|
|`[build-system]`|声明 PEP 517 构建环境需要的工具。|
|`requires`|构建隔离环境中需要安装的依赖。此处仅需要 `setuptools`。|
|`build-backend`|指定由 `setuptools.build_meta` 调用 `setuptools` 执行构建。|

Python `<3.7` 的 `setuptools` 限制为 `<60`，用于支持项目声明的 Python 3.6 兼容范围；Python `>=3.7` 使用 `setuptools>=39.0`。

## 3. 元数据唯一来源

包元数据必须只在 `setup.py` 中维护，包括：

- 包名和版本号。
- Python 版本范围和运行时依赖。
- 包发现规则与打包数据。
- `piper-can` 命令行入口。
- 许可证、分类器、项目链接和描述。

因此，当前 `pyproject.toml` 不应增加 `[project]` 配置，也不应重复填写 `name`、`version`、`dependencies`、`scripts` 或包发现配置。重复维护会导致 `setup.py` 与 `pyproject.toml` 的版本、依赖或入口命令不一致。

## 4. 修改规则

|修改目的|修改位置|要求|
|---|---|---|
|修改发布版本|`setup.py` 与 `piper_sdk/version.py`|按版本维护策略同步更新，不在 `pyproject.toml` 中重复版本号。|
|修改运行时依赖|`setup.py` 的 `install_requires`|同时评估支持的 Python 版本。|
|修改构建后端或构建期依赖|根目录 `pyproject.toml`|确认 `pip install .`、源码分发和支持的 Python 版本均可构建。|
|新增测试工具配置|根目录 `pyproject.toml` 的 `[tool.<tool-name>]`|仅当工具明确支持该配置方式，且不与 `tox.ini` 或其他配置重复时添加。|
|迁移到 PEP 621 元数据|单独的迁移任务|先完整迁移并移除重复元数据，不要逐项混用 `setup.py` 和 `[project]`。|

## 5. 验证方式

修改构建配置后，至少执行：

```shell
python3 -m pip install .
python3 -m build
```

若项目仍需支持 Python 3.6，还应在可用的 Python 3.6 环境中验证构建。`tox.ini` 中定义的测试环境用于验证各受支持 Python 版本的测试运行。

## 6. 禁止事项

- 不要在 `piper_sdk/` 包目录中放置第二个 `pyproject.toml`。
- 不要同时在 `setup.py` 与 `[project]` 中维护同一份包元数据。
- 不要为了增加工具配置而修改 `build-backend`。
- 不要移除 Python 版本条件或放宽 `setuptools` 约束，除非已完成对应 Python 版本的构建验证。
