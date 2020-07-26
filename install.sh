set -e

DESTDIR=${HOME}/.local/share/krita/pykrita

pyuic5 colorPlanner/colorPlannerForm.ui > colorPlanner/colorPlannerForm.py

if [ -e ${DESTDIR}/colorPlanner ]; then
    rm -r ${DESTDIR}/colorPlanner
fi;

cp colorPlanner.desktop ${DESTDIR}

mkdir ${DESTDIR}/colorPlanner
cp -r colorPlanner/*.py ${DESTDIR}/colorPlanner
