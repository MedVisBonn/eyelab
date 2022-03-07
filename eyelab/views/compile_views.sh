#!/bin/bash
for i in ui/*.ui; do
	[ -f "$i" ] || break
	pyside6-uic --from-imports $i --output ${i/.ui/.py};
done
