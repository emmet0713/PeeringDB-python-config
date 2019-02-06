from peeringdb import PeeringDB
import requests
from datetime import date, datetime
import textfsm
import xlsxwriter
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
start_time = datetime.now()

def textfsm_parser(textfsm_file_name, data_file_name):
        bgp_template = textfsm.TextFSM(textfsm_file_name)
        return bgp_template.ParseText(data_file_name)

#       SOX = 93
#       MYIX = 250
#       LINx LON1 = 18
#       JBIX = 2279
#       HKIX Peering LAN 1 = 42
#       Equinix SG = 158
#       AMS-IX = 26
#       Set ixlan_id based on IX

ixlan_list = [93,250]

###Reg Ex for Command
textfsm_template_name_ipv4 = open('sh_ip_bgp_sum_template')
textfsm_template_name_ipv6 = open('sh_bgp_ipv6_uni_sum')

###BGP Session Output from Router
textfsm_data_file_name_ipv4 = open('ipv4_bgp_session.txt', 'r').read()
textfsm_data_file_name_ipv6 = open('ipv6_bgp_session.txt', 'r').read()

##File Name
name_list = ['Peering Database', '-', str(date.today()), '.xlsx']
file_name = ''.join(name_list)
workbook= xlsxwriter.Workbook(file_name)

for list in ixlan_list:
        peerings = pdb.all('netixlan', ixlan_id=list)

        ###xlsx writer
        worksheet_ix = workbook.add_worksheet(peerings[0]['name'][:4])
        print('Create sheet for {}'.format(peerings[0]['name']))
        worksheet_ix.write(num_row, 0, '')
        worksheet_ix.write(num_row, 1, 'Name')
        worksheet_ix.write(num_row, 2, 'AS Number')
        worksheet_ix.write(num_row, 3, 'IPv4 Prefix Number')
        worksheet_ix.write(num_row, 4, 'IPv4 Address')
        worksheet_ix.write(num_row, 5, 'IPv6 Prefix Number')
        worksheet_ix.write(num_row, 6, 'IPv6 Address')
        worksheet_ix.write(num_row, 9, 'IPv6 BGP Status')
        worksheet_ix.write(num_row, 10, 'IPv4 Prefix List')
        worksheet_ix.write(num_row, 11, 'IPv6 Prefix List')

        ###Query Data from PeeringDB website
        pdb_username = raw_input('Enter your PeeringDB username: ')
        pdb_password = getpass.getpass('Enter your PeeringDB password: ')
        #device_password = getpass.getpass('Enter your device password')
        url_session.auth = (pdb_username, pdb_password)
        url_request = url_session.post('https://www.peeringdb.com/login?next=/login')

        for peer in peerings:
                ###PeeringDB Database
                for i in value.json()['data']:
                        if (i['role'] == 'NOC' or i['role'] == 'Policy'):
                                email_value_list.append(i['email'])

                email_value_final = ';'.join(email_value_list)
                ix = pdb.all('net', id=peer['net_id'])[0]

                ###RADB Database IPv4
                radb_cmd_line = ''.join(cmd_line)
                radb_cmd_line_remove = 'sed -i -e s/route://g radb_output'
                os.system(radb_cmd_line)
                os.system(radb_cmd_line_remove)
        #       print (radb_cmd_line)
                radb_open_file = open('radb_output', 'r').read()

                ###RADB Database IPv6
                ipv6_radb_cmd_line = ''.join(ipv6_cmd_line)
                ipv6_radb_cmd_line_remove = 'sed -i -e s/route6://g ipv6_radb_output'
                os.system(ipv6_radb_cmd_line)
                os.system(ipv6_radb_cmd_line_remove)
                ipv6_radb_open_file = open('ipv6_radb_output', 'r').read()
        #       print (ipv6_cmd_line)


                bgp_status = ''
                for i in textfsm_output_file_ipv4:
                        fsm_num = 0
                        if (i[fsm_num] == peer['ipaddr4']):
                                if (i[2] ==  'Idle' or i[2] == 'Idle (Admin)'):
                                        bgp_status = 'Idle'
                                elif (i[2] == 'Active'):
                                        bgp_status = 'Active'
                                elif (i[2] == 'Connect'):
                                        bgp_status = 'Connect'
                                elif (i[2] == 'OpenSent' or i[2] == 'OpenConfirm'):
                                        bgp_status = 'OpenSent | OpenConfirmed'
                                else:
                                        bgp_status = 'Established'
                                break
                        else:
                                bgp_status = 'BGP not established'
                        fsm_num += 1

                bgp_status_ipv6 = ''
                for i in textfsm_output_file_ipv6:
                        if (i[0].lower() == peer['ipaddr6']):
                                if (i[2] ==  'Idle' or i[2] == 'Idle (Admin)'):
                                        bgp_status_ipv6 = 'Idle'
                                elif (i[2] == 'Active'):
                                        bgp_status_ipv6  = 'Active'
                                elif (i[2] == 'Connect'):
                                        bgp_status_ipv6 = 'Connect'
                                elif (i[2] == 'OpenSent' or i[2] == 'OpenConfirm'):
                                        bgp_status_ipv6 = 'OpenSent | OpenConfirmed'
                                else:
                                        bgp_status_ipv6 = 'Established'
                                break
                        else:
                                bgp_status_ipv6 = 'BGP not established'

                worksheet_ix.write(num_row+1, 0, num_row+1)
                worksheet_ix.write(num_row+1, 1, ix['name'].encode('utf-8'))
                worksheet_ix.write(num_row+1, 2, ix['asn'] )
                worksheet_ix.write(num_row+1, 3, ix['info_prefixes4'])
                worksheet_ix.write(num_row+1, 4, peer['ipaddr4'])
                worksheet_ix.write(num_row+1, 5, ix['info_prefixes6'])
                worksheet_ix.write(num_row+1, 6, peer['ipaddr6'])
                worksheet_ix.write(num_row+1, 7, email_value_final.encode('utf-8'))
                worksheet_ix.write(num_row+1, 8, bgp_status)
                worksheet_ix.write(num_row+1, 9, bgp_status_ipv6)
                worksheet_ix.write(num_row+1, 10, radb_open_file)
                worksheet_ix.write(num_row+1, 11, ipv6_radb_open_file)

                num_row = num_row+1
workbook.close()
end_time = datetime.now()
total_time = end_time - start_time
print('Total running program: {}'.format(total_time))
