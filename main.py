import ssl, socket
import time

def check(domain):
    item={}
    try:
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
    except:
        item["subject"]="Invalid"
        item["start"]="Invalid"
        item["expire"]="Invalid"
        item["issuer"]="Invalid"
        item["remain"]="0"
        item["check"]=time.ctime(time.time())
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


f = open("./public/result.txt", "w",encoding="utf-8")
print(result,file = f)
f.close()
