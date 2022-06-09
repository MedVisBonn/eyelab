# Changelog

<!--next-version-placeholder-->

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
