
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
