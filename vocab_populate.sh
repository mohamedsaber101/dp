#PUT THE CONTENT IN /tmp/a
id=$1
type=vocabulary

file=/tmp/b
cat /tmp/a |grep -v '='|sed 's/  ----------\*\*-----------  /\*/g' |sed 's/  ---------------------  /\*/g' > /tmp/b
for i in `seq $(cat $file|wc -l | cut -d' ' -f1)`
do
EN=`sed -n ${i}p $file|cut -d'*' -f1`
DE=`sed -n ${i}p $file|cut -d'*' -f2`
echo $EN -**- $DE

echo from revision.models import \*  > /tmp/django_script
echo a=Sentence.objects.get_or_create\(name=\"${id}V-${i}\",DE=\"$DE\",EN=\"$EN\",revision_number=0,state=\'hot\',type=\"$type\"\) >> /tmp/django_script
python manage.py shell < /tmp/django_script




done



