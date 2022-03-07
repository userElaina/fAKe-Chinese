import os

dirpath=os.path.join(os.path.dirname(__file__),'fakecn')

full=open(os.path.join(dirpath,'name_full.txt'),'rb').read().decode('utf8').split()
last=open(os.path.join(dirpath,'name_last.txt'),'rb').read().decode('utf8').split()
first=set()

for i in full:
    if i[0] in last:
        first.add(i[1:])
        continue
    if i[:2] in last and len(i)>2:
        first.add(i[2:])
        continue
    print(repr(i))

open(os.path.join(dirpath,'name_first.txt'),'wb').write('\n'.join(sorted(first)).encode('utf8')+b'\n')
