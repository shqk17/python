import json

flieLog = open("./request_data.txt", "r")
a = str(flieLog.read())
print(a)
s = json.loads(a)
print(s)
for j in range(1,3):
    print(j)
# flieLog.close()
# flieLog = open("./request_data.txt", "a")
# a = {'type': '1', 'pageSize': '15'}
# b = {'type': '2', 'sq': 'sfd'}
# dict = {'url': 'http://192.168.0.4:8080/tss/tssMemberPackageController/tssMemberPackageList.do',
#         'host': '192.168.0.4:8081',
#         'cookie': 'JSESSIONID=7C3924476D01F76AB658DF5FAEE7A9BF; navbar-fixed-top=true; sidebar-fixed=true; breadcrumbs-fixed=true; page-header-fixed=false; page-header-isShow=false; Hm_lvt_25437122cff4baad62984b1f218a0b02=1551681252,1551682176; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Hm_lpvt_25437122cff4baad62984b1f218a0b02=1551841384',
#         'duanyan': '4028829d67a572f50167a5852cac00cf',
#         'threadsNum': '10000',
#         'thinkTime': 'thinkTime'}
# dict['a'] = a
# dict['b'] = b
# print(json.dumps(dict))
