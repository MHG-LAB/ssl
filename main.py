import ssl, socket
import time

def check(domain):
    item={}
    item["domain"] = domain
    c = ssl.create_default_context()
    s = c.wrap_socket(socket.socket(), server_hostname=item["domain"])
    s.connect((item["domain"], 443))
    cert = s.getpeercert()

    item["subject"]=cert['subject']
    item["start"]=cert['notBefore']
    item["expire"]=cert['notAfter']
    item["issuer"]=cert['issuer']
    item["check"]=time.ctime(time.time())
    nowstamp=time.mktime(time.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y"))
    expirestamp=time.mktime(time.strptime(item["expire"],"%b %d %H:%M:%S %Y GMT"))
    item["remain"]=int((expirestamp-nowstamp)/86400)

    if expirestamp<nowstamp:
        item["status"]="Expired"
        item["statuscolor"]="error"
    elif item["remain"]<10 and item["remain"]>=0:
        item["status"]="Soon Expired"
        item["statuscolor"]="warning"
    elif item["remain"]>=10:
        item["status"]="Valid"
        item["statuscolor"]="success"
    else:
        item["status"]="Invalid"
        item["statuscolor"]="error"
    return item

def get(item):
    rs='''<div class="column" v-for="item in items">
            <div class="ui segment">
                <h3 class="ui floated header sk-pl-2">'''+str(item["domain"])+'''&nbsp;&nbsp;
                    <small class="sk-text-'''+str(item["statuscolor"])+'''">'''+str(item["status"])+'''</small>
                </h3>
                <div class="ui clearing divider"></div>
                <div class="sk-pl-2">
                    <table class="ui collapsing table unstackable">
                        <tbody>
                            <tr>
                                <td class="item-title sk-text-right">Last check</td>
                                <td>'''+str(item["check"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Subject</td>
                                <td>'''+str(item["subject"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Valid from</td>
                                <td>'''+str(item["start"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Valid until</td>
                                <td>'''+str(item["expire"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Remaining</td>
                                <td>'''+str(item["remain"])+''' Days</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Issuer</td>
                                <td>'''+str(item["issuer"])+'''</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    '''
    return rs




f = open("./domains", "rb")
File = f.read().decode("utf8","ignore")
f.close()
Lines = File.splitlines()
result=""
for i in Lines:
    if i:
        print(i)
        result+=get(check(i))
HTML='''<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <title>SSL透明度报告</title>
    <link rel="shortcut icon" type="image/x-icon" sizes="16x16 32x32 48x48 64x64" href="https://cdn.jsdelivr.net/npm/mhg@0.0.0/favicon/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="description" content="SSL透明度报告">
    <meta name="theme-color" content="#F6B352">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.3.1/dist/semantic.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/suka.css@0.1.2">
    <style>
        .item-title {
            color: #adadad
        }

        .ui.table tr td,
        .ui.table,
        .ui.table tbody {
            border: none;
        }

        .ui.table tr td {
            padding: .3rem;
            line-height: 1.2rem;
        }
    </style>
    <!--[if lt IE 9]><script src="https://cdn.jsdelivr.net/npm/html5shiv@3.7.3"></script><script src="https://cdn.jsdelivr.net/npm/respond.js@1.4.2/dest/respond.min.js"></script><![endif]-->
    <meta property="og:type" content="Website">
    <meta name="twitter:card" content="summary">
</head>

<body class="sk-p-4 sk-pt-8 sk-pb-6">
    <h1 class="ui center aligned header">
        <i id="icon" class="expeditedssl icon" data-position="left center" style="color: #009688;"></i>SSL Status</h1>
    <div class="ui container sk-pt-4">
        <div class="ui container two column stackable grid container" id="result">
	'''+result+'''
	</div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.3.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.3.1/dist/semantic.min.js"></script>
</body>

</html>
'''

f = open("./public/index.html", "w",encoding="utf-8")
print(HTML,file = f)
f.close()
