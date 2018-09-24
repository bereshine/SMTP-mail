


def parse_white_space(string,current):
    if current<len(string):
        if string[current]!=" " and string[current]!="\t":
            print "ERROR -- whitespace"
            return False,0.5
        else:
            while string[current]==" " or string[current]=="\t" :
                current=current+1
            return True,current

def parse_null_space(string,current):
        while current < len(string) and (string[current]==" " or string[current]=="\t"):
            current=current+1
        return True,current

def parse_reverse_path(string,current):
    bolean,current=parse_path(string,current)
    return bolean,current

def parse_path(string,current):
    if current< len(string) and string[current]=="<":
        current=current+1
        bolean,current=parse_mailbox(string,current)
        if current<len(string)and bolean==True and string[current]==">":
            current=current+1
            return True,current
        elif current==0.5:
            return False,0.5
        else:
            print "ERROR -- path"
            return False,0.5
    else:
        print "ERROR -- path"
        return False,0.5

def parse_mailbox(string,current):
    if current <len(string):
        bolean,current=parse_local_part(string,current)
        if bolean==True and string[current]=="@":
            bolean2,current=parse_domain(string,current+1)
            if bolean2==True:
                return True, current
            elif current==0.5:
                return False,0.5
            else:
                print "ERROR -- mailbox"
                return 0
        elif current==0.5:
            return False,0.5
        else:
            print "ERROR -- mailbox"
            return False,0.5
    else:
        print "ERROR -- mailbox"
        return False,0.5

def parse_local_part(string, current):
    if current<len(string):
        bolean,current=parse_string(string,current)
    return bolean,current

def parse_string(string,current):
    special = '<>()[]\.,:;@" \t'
    if current+1 < len(string):
        bolean=parse_char(string[current])
        if bolean==0.5:
            return False,0.5
        if bolean==True and (0<=ord(string[current+1])<=127 and string[current+1] not in special)!=True:
            current=current+1
            return True,current
        elif bolean==True and (0<=ord(string[current+1])<=127 and string[current+1] not in special)==True:
            bolean2,current=parse_string(string,current+1)
            return bolean2,current
        else:
            print "ERROR -- string"
            return False,0.5
    else:
        print "ERROR -- string"
        return False,0.5

def parse_char(string):
    special = '<>()[]\.,:;@" \t'
    if 0<=ord(string)<=127 and string not in special:
        #             ord(string) != 60 and  ord(string) != 62 and  ord(string) !=40 \
        # and ord(string)!=41 and ord(string)!=91 and ord(string)!=93 and ord(string)!=92 and ord(string) !=46 \
        # and  ord(string)!= 44 and ord(string)!=58 and ord(string)!=59 and  ord(string)!=64 and ord(string)!=34:
        # #current=current+1
        return True
    else:
        print "ERROR -- char"
        return 0.5

def parse_domain(string,current):
    bolean, current=parse_element(string,current)
    if current==0.5:
        return False,0.5
    if bolean==True and string[current]==".":
        bolean2, current = parse_domain(string, current + 1)
        return bolean2,current
    elif bolean==True:
        return bolean,current
    else:
        print"ERROR -- domain"
        return False,0.5

def parse_element(string,current):
    bolean,current=parse_name(string,current)
    return bolean,current

def parse_name(string,current):
    bolean=parse_alpha(string[current])
    if current+1 < len(string) and bolean==True and (65<=ord(string[current+1])<=90 or 97<=ord(string[current+1])<=122 or 48<=ord(string[current+1])<=57):
        bolean2,current=parse_let_dig_str(string,current+1)
        return True, current
    elif bolean==0.5:
        return False, 0.5
    else:
        print "ERROR -- name"
        return False,0.5

def parse_let_dig_str(string,current):

        if (65<=ord(string[current])<=90 or 97<=ord(string[current])<=122 or 48<=ord(string[current])<=57)  :
            if current<len(string)-1:
                current=current+1

                bolean,current=parse_let_dig_str(string,current)
                return True, current
            else:
                return True, current
        elif (65<=ord(string[current])<=90 or 97<=ord(string[current])<=122 or 48<=ord(string[current])<=57)!=True:

            return True, current
        else:
            current=current+1
            return True, current

def parse_let_dig(string):
    if parse_alpha(string) or parse_digit(string):
        return True
    else:
        print "ERROR -- let-dig"
        return 0

def parse_alpha(string):

    if 65<=ord(string)<=90 or 97<=ord(string)<=122 :
        return True
    else:

        print "ERROR -- a"
        return 0.5

def parse_digit(string):
    if 48<=ord(string)<=57:
        return True
    else:
        print "ERROR -- d"
        return 0

def ok250(str):
    if len(str) == 3 and str[0:3] == '250':
        return True
    elif len(str) > 3 and str[0:3] == '250':
        judge = parse_white_space(str, 3)
        if judge:  # there is a space or tab after 250
            return True
        else:  # there is some other char immediately after 250
            return False
    else:  # either (len is 3 but not 250) or (len bigger than 3 but not start with 250) or (len less than 3)
        return False

def ok354(str):
    if len(str) == 3 and str[0:3] == '354':
        return True
    elif len(str) > 3 and str[0:3] == '354':
        judge = parse_white_space(str, 3)
        if judge:  # there is a space or tab after 250
            return True
        else:  # there is some other char immediately after 250
            return False
    else:  # either (len is 3 but not 250) or (len bigger than 3 but not start with 250) or (len less than 3)
        return False



import re
import socket
import sys

server_hostname = sys.argv[1]
server_port=int(sys.argv[2])


bolean = False
while bolean==False:
    print 'From:'
    mail = raw_input()
    bolean, current = parse_mailbox(mail,0)

flag = True

while flag:
    print 'To:'
    to = raw_input()
    rcpt_list=to.split(',')
    for rcpt in rcpt_list:
        rcpt = rcpt.lstrip()
        bolean, current = parse_mailbox(rcpt, 0)
        if bolean == False:
            flag = True
            break
        else:
            flag = False

print 'Subject:'
sub = raw_input()

mes_list = []
print 'Message:'
mes = raw_input()
while mes != '.':
    mes_list.append(mes)
    mes = raw_input()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server_hostname,server_port))

greeting_220 = clientSocket.recv(1024).decode()

clientSocket.send('HELO cs.unc.edu'.encode())

helo_250 = clientSocket.recv(1024).decode()

mail_cmd='MAIL FROM: <'+mail+'>'
clientSocket.send(mail_cmd.encode())
mail_res = clientSocket.recv(1024).decode()

if ok250(mail_res):
    for rcpt in rcpt_list:
        rcpt_cmd='RCPT TO: <'+rcpt.lstrip()+'>'
        clientSocket.send(rcpt_cmd.encode())
        rcpt_res = clientSocket.recv(1024).decode()
        if not ok250(rcpt_res):
            clientSocket.close()
            print "RCPT command server response error" + rcpt_res
            exit()

    clientSocket.send('DATA'.encode())
    data_res = clientSocket.recv(1024).decode()
    if ok354(data_res):
        h_from = 'From: <'+ mail + '>'
        clientSocket.send(h_from.encode())
        for rcpt in rcpt_list:
            h_to = 'To: <'+rcpt.lstrip() +'>'
            clientSocket.send(h_to.encode())
        h_sub = 'Subject: '+sub
        clientSocket.send(h_sub.encode())


        clientSocket.send(''.encode())

        for mes in mes_list:
            clientSocket.send(mes.encode())

        clientSocket.send('.')
        p_res = clientSocket.recv(1024).decode()
        if ok250(p_res):
            clientSocket.send('QUIT'.encode())
            clientSocket.close()
            exit()
        else:
            clientSocket.close()
            print "period server res error"
            exit()
    else:
        clientSocket.close()
        print "DATA server res error"
        exit()
else:
    clientSocket.close()
    print "MAIL FROM server res error"
    exit()

#
#     clientSocket.send()
#
# for rcpt in rcpt_list:







# # evaluate 250 response condition
# def ok250():
#     try:
#         line = raw_input()
#     except(EOFError):
#         print >> sys.stdout, "QUIT"
#         sys.exit()
#     if line.lstrip().startswith("250 "):
# # save respone in stdrr
#         print >> sys.stderr, line
#     else :
#         print >> sys.stdout, "QUIT"
#         sys.exit()
#
# # evaluate 354 response condition
#
# def ok354():
#
#     try:
#         line = raw_input()
#     except(EOFError):
#         print >> sys.stdout, "QUIT"
#         sys.exit()
#     if line.lstrip().startswith("354 "):
# # save respone in stdrr
#         print >> sys.stderr, line
#     else :
#         print >> sys.stdout, "QUIT"
#         sys.exit()



#
# def main():
#     fname = sys.argv[1]
#     with open(fname,"r+") as file:
#
#         recipientNum = 0
# # have a flag here to represent whether the data has been reading or not
#         readingData = False
#
#         for line in file:
# # evaluate the "From: ......(mailbox)"
#             if line.strip().startswith("From: "):
#
#                 if recipientNum>0 and not readingData:
#                     print "DATA"
#                     ok354()
#                     print "."
#                     ok250()
#
#                 elif recipientNum>0 and readingData:
#                     print "."
#                     ok250()
# # get the index of mailbox
#                 start = line.find('<')
#                 end = line.find('>') + 1
#                 mailFrom = "MAIL FROM: " + line[start:end]
#
#                 sys.stdout.write(mailFrom+'\n')
#                 ok250()
#                 recipientNum = 0
#                 readingData = False
# # evaluate the "To: .....(mailbox)"
#             elif line.strip().startswith("To: "):
# # get the index of mailbox
#                 start = line.find('<')
#                 end = line.find('>') + 1
#                 rcptTo = "RCPT TO: " + line[start:end]
#                 sys.stdout.write(rcptTo + '\n')
#                 ok250()
#                 recipientNum=recipientNum + 1
#
#             elif recipientNum>0 and not readingData:
#                 print "DATA"
#                 ok354()
#                 readingData = True
#                 sys.stdout.write(line)
#
#             elif recipientNum>0 and readingData:
#                 sys.stdout.write(line)
#         else:
#             if readingData:
#                 print "."
#                 ok250()
#             elif not readingData:
#                 print "DATA"
#                 ok354()
#                 print "."
#                 ok250()
#             print >> sys.stdout, "QUIT"
#
# main()
