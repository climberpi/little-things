ls *.jpg > list
echo "<table>" > list.html
echo "<tr>" >> list.html
cnt=0
cat list | while read i;
do
    cnt=`expr $cnt + 1`
    flag=`expr $cnt % $1`
    if (test $flag -eq 0)
#��ֱ������������� test ���ð��쵰, ������1h = =
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
