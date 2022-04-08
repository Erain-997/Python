set -x

version=$1
#关掉Corona进程
taskkill //IM "Corona Simulator.exe"
#删掉现有截图和log
rm -rf $(dirname $(pwd))/sultan_ui/img/*
rm -rf $(dirname $(pwd))/sultan_ui/service/log/*

cd /g/server/version
#得到当前所在分支名
a=$(git branch|grep "*")
CurrentBranchName=${a/* /}

if [ $CurrentBranchName = $version ];then
  echo "传参为当前分支"
  git reset --hard HEAD^
  echo n|git pull -f origin $version
else
  echo "需要切换分支"
  echo n|git checkout -f $version
fi
rm -rf "G:\python_code\sultan_ui\reports\main.log"
sed -i 's/return tGuideAndPop1,tGuideAndPop2,tGuideAndPop3/return nil,nil,nil/g' /g/server/version/scene/placeMap/popQueue.lua
sleep 5