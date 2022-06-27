import csv
from csv import reader
import csv, os

RUNNUM=3294


exists_flag = False

f= open('test.csv', 'r')
lines = csv.reader(f, delimiter=',')

idx=0
for row in lines:
    
    if(row[0]==str(RUNNUM)):
        exists_flag = True        
        break;
    else:
        exists_flag = False
    idx=idx+1

print('index:', idx)

updated_line = ('3294','192', '1.9', '255', '2.97', 'C12', 'SRC', '2018-04-05|15:57:11')

print('exists_flag:',exists_flag)
overwrite_flag = False
if(exists_flag):
    query = input('Run Number %i exits ! Are you sure you want to overwrite it? [y/n]\n >>')
    if(query=='y' or query=='Y' or query=='yes' or query=='YES'):
        print('OK, will overwrite run number in csv file !')
        overwrite_flag = True
    elif(query=='n' or query=='N' or query=='no' or query=='NO'):
        print('Will not overwrite ')
        overwrite_flag = False


if(overwrite_flag):

    print('passed1')
    with open('test.csv') as inf, open('test_mode.csv', 'w') as outf:
        reader = csv.reader(inf)
        writer = csv.writer(outf)
        for line in reader:
            print('line:', line[0])
            print('RUNNUM:', str(RUNNUM))
            #search for RUNNUM, and replace line when it finds it
            if(line[0]==str(RUNNUM)):
                print('passed2')
                print('replacing line ', line, 'with\n',updated_line)
                writer.writerow(updated_line)                
            else:
                print('else')
                writer.writerow(line)
            writer.writerows(reader)

    
