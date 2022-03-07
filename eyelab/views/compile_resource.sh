#!/bin/bash
for i in ui/*.qrc; do
	[ -f "$i" ] || break
	pyside6-rcc $i -o ${i/.qrc/_rc.py};
done
