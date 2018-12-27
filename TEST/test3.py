
s = "UPDATE tss_member_package set isStatisticRemediationClassHour=isStatisticRemediationClassHour + %d , notStatisticRemediationClassHour=notStatisticRemediationClassHour - %d where id ='%s';"
set={'2c92828665aa68940165b2e014283f3f':1,
'2c92828665aa68940165b2dfcf823667':2,
'2c92828665aa68940165b2e01e5840e6':2,
'2c92828665aa68940165b2e01edc40fb':2}
for i,j in set.items():
    print(s%(j,j,i))