ls *.jpg > list
echo "<table>" > list.html
echo "<tr>" >> list.html
cnt=0
cat list | while read i;
do
    cnt=`expr $cnt + 1`
    flag=`expr $cnt % $1`
    if (test $flag -eq 0)
#简直傲娇到死的设计 test 你妹啊混蛋, 调了我1h = =
    then 
        echo "</tr>" >> list.html
        echo "<tr>" >> list.html
    fi
    prev="<td><img src = \"./"
    url=$prev$i"\" height=150></td>"
    echo $url >> list.html
done
echo "</tr>" >> list.html
echo "</table>" >> list.html
rm -f list
