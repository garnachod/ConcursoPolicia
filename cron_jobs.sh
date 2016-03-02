#!/bin/bash
for lang in "es" "en" "fr" "ar"
do
	echo "Generando modelo "$lang
	PYTHONPATH="${PYTHONPATH}:/home/dani/github/ConcursoPolicia/LuigiTasks"
	export PYTHONPATH
	luigi --module TrainText GenerateVecsAnnoyLang_topics --idioma $lang > /dev/null 2>&1
	luigi --module TrainText GenerateVecsAnnoyLang_semantic --idioma $lang > /dev/null 2>&1
done
