
# UVによるパッケージ化

- リポジトリの作成
  ```uv init xxx --lib```
- ビルド ```uv build```
  - このときに、src/xxx/hoge.pyという構造にするとよい。
  - pyproject.tomlには以下を追加する。

    ```
    [project.scripts]
    xxx = "src/xxx/hoge:main"
    [tool.hatch.build.targets.wheel]
    packages = ["src/hyper-tokuma"]
    ```


- パブリッシュ ```uv publish --publish-url https://test.pypi.org/legacy/ --token $TEST_PYPI_TOKEN```
  - testpypiのAPIトークンをTEST_PYPI_TOKENという環境変数にセットしているとする。このときトークンは`pypi-`から始まる。


# Pytest

```python -m coverage run -m pytest```

```python -m coverage report```
- カバレッジの表示

# NoxによるBuild

`NOX_DEFAULT_VENV_BACKENV=uv`を環境変数として指定。

buildなどの実行
- `nox`

noxで実行されるものの確認
- `nox list`

デフォルトで実行するものを指定するときは`noxfile.py`で`nox.options.sessions`に指定



実行段階で選ぶ場合は`nox --session tests`


仮想環境を再利用し、インストールをスキップする場合。
`nox -R`

pythonバージョンは`nox --python 3.12`でも指定可能。

noxにコマンド変数を与える場合
- noxfile.pyに`session.run('pytest', *session.posargs)`を指定。
- ターミナル上で`nox --session tests -- --verbose`のように、`--`で区切ってオプション引数を渡す。
