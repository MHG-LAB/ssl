import ssl, socket
import time

S=""
def tup2str(tup):
    global S
    def tt(a):
        global S
        for i in a:
            if str(type(i[0]))=="<class 'str'>":
                if len(i)==1:
                    S+=i[0]+";"
                elif len(i)==2:
                    S=S+i[0]+"="+i[1]+";"
                else:
                    S+=str(i)+";"
            elif str(type(i))=="<class 'tuple'>":
                tt(i)
            else:
                S+=str(i)
    S=""
    tt(tup)
    print(S)
    return S

def check(domain):
    item={}
    try:
        item["domain"] = domain
        c = ssl.create_default_context()
        s = c.wrap_socket(socket.socket(), server_hostname=item["domain"])
        s.connect((item["domain"], 443))
        cert = s.getpeercert()
        #print(cert)

        item["check"]=time.ctime(time.time())
        nowstamp=time.mktime(time.strptime(time.ctime(time.time()),"%a %b %d %H:%M:%S %Y"))
        expirestamp=time.mktime(time.strptime(cert['notAfter'],"%b %d %H:%M:%S %Y GMT"))
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

        for i in cert:
            if str(type(cert[i]))=="<class 'tuple'>":
                item[i]=tup2str(cert[i])
            else:
                item[i]=str(cert[i])
    
            
    except:
        item["version"]="Invalid"
        item["serialNumber"]="Invalid"
        item["subjectAltName"]="Invalid"
        item["OCSP"]="Invalid"
        item["caIssuers"]="Invalid"
        
        item["subject"]="Invalid"
        item['notBefore']="Invalid"
        item['notAfter']="Invalid"
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
                                <td class="item-title sk-text-right">SubjectAltName</td>
                                <td>'''+str(item["subjectAltName"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Valid from</td>
                                <td>'''+str(item['notBefore'])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Valid until</td>
                                <td>'''+str(item['notAfter'])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Remaining</td>
                                <td>'''+str(item["remain"])+''' Days</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Issuer</td>
                                <td>'''+str(item["issuer"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">Version</td>
                                <td>'''+str(item["version"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">SerialNumber</td>
                                <td>'''+str(item["serialNumber"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">OCSP</td>
                                <td>'''+str(item["OCSP"])+'''</td>
                            </tr>
                            <tr>
                                <td class="item-title sk-text-right">CaIssuers</td>
                                <td>'''+str(item["caIssuers"])+'''</td>
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
