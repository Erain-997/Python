set -x

version=$1
echo $(dirname $(pwd))/sultan_ui/reports/$version/
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/.idea
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/.git
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/api

rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/auto
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/img
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/internal
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/reports
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/service

rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/.gitignore
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/main.py
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/Pipfile
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/Pipfile.lock
rm -rfv $(dirname $(pwd))/sultan_ui/reports/$version/readme.md
rm -rfv $(dirname $(pwd))/sultan_ui/reports/main.log
sleep 1