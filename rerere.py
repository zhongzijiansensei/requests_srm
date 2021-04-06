import re
str = 'UUID(9079fec2-38e8-48ae-87e6-1f42dd9fae90)'
r=re.search("9(.+?)0", str)
print (r.group())