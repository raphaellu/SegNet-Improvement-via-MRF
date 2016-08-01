i=0
for f in *.png
do
    echo "processing $f $i"
    mv $f $i.png
    let "i++"
done
