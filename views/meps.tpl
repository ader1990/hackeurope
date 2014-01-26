<!DOCTYPE html>
<html>
<head>
<title>Meps</title>
</head>
<body>
<h1>List</h1>

%for mep in meps:
<h3><a href="/mep/{{mep['_id']}}">{{mep['Name']['full']}}</a></h2>
%if (len(mep['cases']) >0 or len(mep['iccsj']) >0):
<h3 style="color:red"> !!! </h1>
%end
Cases:
%if ('cases' in mep):
%numCrimes = len(mep['cases'])
%else:
%numCrimes = 0
%end
<a href="/mep/{{mep['_id']}}">{{numCrimes}}</a>
</br>
Icssj:
%if ('iccsj' in mep):
%numCrimes2 = len(mep['iccsj'])
%else:
%numCrimes2 = 0
%end
<a href="/mep/{{mep['_id']}}">{{numCrimes2}}</a>
</body>
</html>


