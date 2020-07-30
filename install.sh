set -e

DESTDIR=${HOME}/.local/share/krita/pykrita

pyuic5 colorPlanner/colorPlannerForm.ui > colorPlanner/colorPlannerForm.py
pyuic5 colorPlanner/colorPlannerMaskSelectForm.ui > colorPlanner/colorPlannerMaskSelectForm.py
pyuic5 colorPlanner/colorPlannerDialogForm.ui > colorPlanner/colorPlannerDialogForm.py

if [ -e ${DESTDIR}/colorPlanner ]; then
    rm -r ${DESTDIR}/colorPlanner
fi;

cp colorPlanner.desktop ${DESTDIR}

mkdir ${DESTDIR}/colorPlanner
cp -r colorPlanner/*.py ${DESTDIR}/colorPlanner
