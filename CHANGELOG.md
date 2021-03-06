# Changelog

<!--next-version-placeholder-->

## v0.4.2 (2022-07-10)
### Fix
* **commands/layeritem.py:** Optimize control points before updating the spline in case of a deleted knot; have end knot deletion without neighbouring polygon covered ([`891fb18`](https://github.com/MedVisBonn/eyelab/commit/891fb1884836893f7219a97a87e472ca147c8ffe))
* **treeview/layeritem.py:** Compute start and end index for spline with non x.5 knot positions in mind ([`f0c7f8b`](https://github.com/MedVisBonn/eyelab/commit/f0c7f8bd58128087a313ee526bf3b1d12a54f10c))

### Documentation
* **README.md:** Fix wrong link to eyepy ([`e28f334`](https://github.com/MedVisBonn/eyelab/commit/e28f33424bf75b11ec5b7b9ac83e93ac8ded0d7b))

## v0.4.1 (2022-07-05)
### Fix
* **pyproject.toml:** Update dependencies and set numpy ">=1.22" to solve dependabot alert ([`94841f5`](https://github.com/MedVisBonn/eyelab/commit/94841f555aab4c237e5ebc94d8f999ef4dcf6e64))
* **main.py:** Always enable save button until areaitem is integrated in undo/redo framework - closes #2 ([`9889a33`](https://github.com/MedVisBonn/eyelab/commit/9889a33e84105edc07c7c177898b55745d64c739))
* **layeritem.py:** Fix bug where b-scans can not be initialized because of directly neighbouring spline regions ([`dba053c`](https://github.com/MedVisBonn/eyelab/commit/dba053cb8c796bcae6ae2a0059b17cd1f3e9800d))

## v0.4.0 (2022-06-09)
### Feature
* **scene.py:** Show current B-scan index ([`e5f19e0`](https://github.com/MedVisBonn/eyelab/commit/e5f19e0aa335f6d0ee1a1b1bbdfa77b4c00a66de))
* **main.py:** Add "thin out" action to deactivate B-scans for sparse annotation. ([`4602daf`](https://github.com/MedVisBonn/eyelab/commit/4602daf5a27a4123ef7acc00fc19fdea1dd796ed))
* **main.py:** Add About dialog for information about the software ([`5d06f3f`](https://github.com/MedVisBonn/eyelab/commit/5d06f3f619d799fc5fe4ea4e4fa0f317a79b22f1))
* **main.py:** Show save path and document status in window title ([`a0ec610`](https://github.com/MedVisBonn/eyelab/commit/a0ec610ddded35319e8567adf3c839a888accd14))

## v0.3.2 (2022-06-05)
### Fix
* **main.py:** Fix saving ([`bbb8c13`](https://github.com/MedVisBonn/eyelab/commit/bbb8c136654ac3b620ed077eec9b7a7fb0afb72f))

## v0.3.1 (2022-06-03)
### Fix
* **layeritem.py:** Check if layer knots are structured correct - update dependencies ([`833f939`](https://github.com/MedVisBonn/eyelab/commit/833f93984906859bcf11261bd266e6c14855da53))

## v0.3.0 (2022-06-03)
### Feature
* **eyelab:** Add redo/undo framework for layer editing ([`6436e4d`](https://github.com/MedVisBonn/eyelab/commit/6436e4da5982fe9a39102e115a9bcccd0ca23378))
* **eyelab:** Work in progress; layeritem integrated with redo/undo framework ([`ffe7148`](https://github.com/MedVisBonn/eyelab/commit/ffe7148f804eaa56b353d0bf4fcfbcfa4a119c13))
* **eyelab:** Work in progress; integrate redo/undo framework; edit multiple layer segments independent of each other ([`4d05e94`](https://github.com/MedVisBonn/eyelab/commit/4d05e94397e48c54d9432c3132213e2cddf62dc0))

## v0.2.0 (2022-04-25)
### Feature
* **layereditor.py:** Enable editing the annotation name ([`7774e5d`](https://github.com/MedVisBonn/eyelab/commit/7774e5dc1597bf7da039fdb46186f51a845873b4))
* **viewtab.py:** Enable duplication of annotations ([`6a1174b`](https://github.com/MedVisBonn/eyelab/commit/6a1174bc6e8ddb09902ae5fd1db750b18fa62bd3))

### Fix
* **main.py:** Add try/except block for version checking ([`650622f`](https://github.com/MedVisBonn/eyelab/commit/650622f6b4d734f0b9ab68530234bb40ff785a41))
* **layereditor.py:** Show qlineedit when qlabel is double click and hide if edit is finished or layereditor is left with mouse ([`a91b44a`](https://github.com/MedVisBonn/eyelab/commit/a91b44a41904c83943f0d638dc89b2a0f967dc1c))
* **graphicsview.py:** Fit images to view when resizing ([`78d63f8`](https://github.com/MedVisBonn/eyelab/commit/78d63f86b43de64a9d3b964a50c4995766645fb1))
* **pyproject.toml:** Freeze PySide6 version to 6.1.3 because of missing DLL on Windows 7 in later versions ([`be3f6ee`](https://github.com/MedVisBonn/eyelab/commit/be3f6ee9834df44035a0557de9327d741eb09739))

### Documentation
* **README.md:** Update pyinstaller command ([`b18f29d`](https://github.com/MedVisBonn/eyelab/commit/b18f29db819015a1a9a0f7a3aab70fdee86f68a5))
* **README.md:** Add PyPI and DOI badge ([`990a7f4`](https://github.com/MedVisBonn/eyelab/commit/990a7f41d8ab43adc779eaad80c761693e5250c2))

## v0.1.1 (2022-03-31)
### Fix
* **eyelab:** Update to eyepie v0.6.3 for intensity_transform fix ([`572f2a8`](https://github.com/MedVisBonn/eyelab/commit/572f2a8c83ecbfc8ef1fd786fa35a3dd68934e9c))
* **eyelab:** Set eyepie version to 0.6.2 to support saving and loading of intensity transforms ([`4e1c7f5`](https://github.com/MedVisBonn/eyelab/commit/4e1c7f53c9ce1d211be247cf75a0362309be4182))
