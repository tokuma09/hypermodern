# hypermodern


## ビルド方法

`uv build`でOK。その時に`pyproject.toml`では以下のような設定が必要

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/hello"]
```

