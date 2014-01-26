<!doctype HTML>
<html
<head>
<title>
Mep
</title>
</head>
<body>

<a href="/">Home</a><br><br>

<h2>{{mep['Name']['full']}}</h2>

Justice cases:
<ul>
%if ('cases' in mep):
%caseLen = len(mep['cases'])
%else:
%caseLen = 0
%end
%for i in range(0, caseLen):
Object: {{mep['cases'][i]['obiect']}}<br>
Data: {{mep['cases'][i]['data']}}<br>
{{mep['cases'][i]['numar']}}<br>
<hr>
%end
</ul>
Supreme court cases:
<ul>
%if ('iccsj' in mep):
%caseLen = len(mep['iccsj'])
%else:
%caseLen = 0
%end
%for i in range(0, caseLen):
Object: {{mep['iccsj'][i]['Object'][0]}}<br>
Data: {{mep['iccsj'][i]['Date'][0]}}<br>
%if ('parts' in mep['iccsj'][i]):
%partLen = len(mep['iccsj'][i]['parts'])
%else:
%partLen = 0
%end
%for j in range(0, partLen):
Part: {{mep['iccsj'][i]['parts'][j]['Part']}} <br>
Type: {{mep['iccsj'][i]['parts'][j]['Type']}} <br>
%end
<hr>
%end
</ul>
</body>
</html>


