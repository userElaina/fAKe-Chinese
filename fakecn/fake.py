import os
import json
import string
import random
from datetime import datetime,timedelta

BIRTH_START='19260817'
BIRTH_END='20220222'
DEFAULT_USERNAME_LEN=8
DEFAULT_PASSWORD_LEN=16

__birth_start=datetime.strptime(str(BIRTH_START),"%Y%m%d")
__birth_end=datetime.strptime(str(BIRTH_END),"%Y%m%d")
__birth_se=(__birth_end-__birth_start).days+1

dirpath=os.path.dirname(__file__)
readstr=lambda p:open(os.path.join(dirpath,p),'rb').read()


area_id2name=[i.split(',') for i in readstr('area.csv').decode('utf8').split()[1:]]
area_id2name={i[0]:i[1] for i in area_id2name}

def id_check_digit(x:str)->str:
    if len(x)!=17:
        raise ValueError(x)
    check_sum=0
    for _i,i in enumerate(x):
        check_sum+=((1<<(17-_i))%11)*int(i)
    check_digit=(12-(check_sum%11))%11
    return str(check_digit) if check_digit<10 else 'X'

def fake_id(area_id:str=None,birth:str=None,ex_id:str=None,sex:str=None)->str:
    ans=''

    if not area_id:
        area_id=random.choice(list(area_id2name))
    ans+=str(area_id)

    if not birth:
        birth=datetime.strftime(__birth_start+timedelta(random.randint(0,__birth_se)),"%Y%m%d")
    ans+=str(birth)

    if not ex_id:
        ex_id=str(random.randint(10,99))
    ans+=str(ex_id)

    if not sex:
        sex_id=random.randint(0,9)
    else:
        sex=str(sex).lower()
        sex_id=random.randrange(int(sex=='male'),10,step=2) if sex.endswith('male') else sex
    ans+=str(sex_id)

    ans+=id_check_digit(ans)
    return ans


name_first=readstr('name_first.list').decode('utf8').split()
name_last=readstr('name_last.list').decode('utf8').split()
name_lastp=readstr('name_lastp.list').decode('utf8').split()
name_lastp=[float(i) for i in name_lastp]

def fake_name(last:str=None)->str:
    if not last:
        last=random.choices(name_last,weights=name_lastp,k=1)[0]
    return last+random.choice(name_first)


mobile_prefix=json.loads(readstr('mobile_prefix.json'))

def fake_mobile()->str:
    return random.choice(mobile_prefix[random.choice(list(mobile_prefix))])+''.join(random.choices('0123456789',k=8))


bank_bin=[i.split(',') for i in readstr('bin.csv').decode('utf8').split()[1:]]
bank_bin={i[0]:i[1:] for i in bank_bin}

def card_check_digit(x:str)->str:
    check_sum1=''
    check_sum=0
    for _i,i in enumerate(x):
        if _i&1:
            check_sum+=int(i)
        else:
            check_sum1+=str(int(i)<<1)
    check_sum+=sum(int(i) for i in check_sum1)
    check_digit=(-check_sum)%10
    return str(check_digit)

def fake_card(bin:str=None)->str:
    number=''

    if not bin:
        bin=random.choice(list(bank_bin))
    bin=str(bin)
    number+=bin

    if bin in bank_bin:
        length=int(bank_bin[bin][-1])

    number+=''.join(random.choices('0123456789',k=length-len(bin)-1))
    number=number+card_check_digit(number)
    return number

ua=json.loads(readstr('ua.json'))
def fake_ua(x:str=None)->str:
    if x not in ua:
        x=random.choice(list(ua))
    return random.choice(ua[x])


def fake_str(n:int,level:int=15)->str:
    s=''
    ss=list()
    if level&1:
        s+=string.digits
        ss.append(random.choice(string.digits))
    if level&2:
        s+=string.ascii_lowercase
        ss.append(random.choice(string.ascii_lowercase))
    if level&4:
        s+=string.ascii_uppercase
        ss.append(random.choice(string.ascii_uppercase))
    if level&8:
        s+=string.punctuation
        ss.append(random.choice(string.punctuation))
    ss+=random.choices(s,k=n)
    random.shuffle(ss)
    return ''.join(ss)

def fake_username(n:int=DEFAULT_USERNAME_LEN)->str:
    try:
        n=max(int(n),1)
    except:
        n=DEFAULT_USERNAME_LEN
    return random.choice(string.ascii_lowercase)+fake_str(n-1,level=3)

def fake_password(n:int=DEFAULT_PASSWORD_LEN,level:int=15)->str:
    try:
        n=max(int(n),4)
    except:
        n=DEFAULT_PASSWORD_LEN
    return fake_str(n,level)

def fake_qq(n:int=None)->str:
    if n:
        return random.choice('123456789')+fake_str(n-1,1)
    else:
        return random.randint(100000000,9999999999)


def fake()->dict:
    return {
        'name':fake_name(),
        'id':fake_id(),
        'mobile':fake_mobile(),
        'card':fake_card(),
        'ua':fake_ua(),
        'qq':fake_qq(),
        'username':fake_username(),
        'password':fake_password(),
    }
