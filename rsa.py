import math
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

#print(math.gcd(20,8))
def is_prime(number):
	count = 0
	if number == 2:
		return True
	if number < 2:
		return False
	if number % 2 == 0:
		return False
	for i in range(1,number+1):
		if number % i == 0:
			count +=1
	if count == 2:
		return True
	return False

def random_e(phi):
	e = random.randrange(1,phi)
	g = np.gcd(e,phi)
	while g!=1:
		e = random.randrange(1,phi)
		g = np.gcd(e,phi)
	return e

def inverse_d(e, phi):
	# phi_x +e_y = 1
	r1 = phi
	r2 = e
	t1 = 0
	t2 = 1

	while r2 > 0:
		q = r1 // r2
		r = r1 - q * r2

		t = t1 - t2 * q
		# print("q = " + str(q))
		# print("r1 = " + str(r1))
		# print("r2 = " + str(r2))
		# print("r = " + str(r))
		# print("t1 = " + str(t1))
		# print("t2 = " + str(t2))
		# print("t = " + str(t))
		r1 = r2
		r2 = r 

		t1 = t2
		t2 = t
		# print("t1 = " + str(t1))
		# print("t2 = " + str(t2))
		# print("t = " + str(t))


	d = t1
	print("d1 = " + str(d))
	if d < 0:
		d= t2 + t1
		print("d2 = " + str(d))
	if r1 == 1 or d == e:
		d = d+phi
		print("d3 = " + str(d))
	return d

def generate_key(p,q):
	n = p*q # calc n
	phi_n = (p-1)*(q-1) # calc phi
	e = random_e(phi_n) # find e 
	d = inverse_d(e,phi_n)
	return ((e,n),(d,n))


def encrypt(pk, messager):
	public_key, n = pk
	Cipher = []
	# C = M^e mod n
	for char in messager:
		a = pow(ord(char),public_key,n)
		Cipher.append(a)
	return Cipher

def decryption(pk,ciphertext):
	private_key , n = pk
	#M = C^d mod n
	plain_text = []

	temp = []
	for char in ciphertext:
		print(type(char))
		a = str(pow(char,private_key,n))
		temp.append(a)
	print(temp)
	for char2 in temp:
		a = chr(int(char2))
		plain_text.append(a)
	return ''.join(plain_text)

if __name__ == "__main__":
	pass
	print("============RSA=================")
	p = int(input("-Enter a prime number (2,3,5,7,11,13,17,19): "))
	while is_prime(p)!= True:
		print("please nhập đúng format của p là số nguyên số")
		p = int(input("-Enter a prime number (2,3,5,7,11,13,17,19): "))
	q = int(input("-Entetr a prime number # p : "))
	while is_prime(q)!= True:
		print("please nhập đúng format của q là số nguyên số")
		q = int(input("-Entetr a prime number # p : "))
	print(" - Generating your public / private key-pairs now . . .")
	public_key, private_key = generate_key(p,q)
	print("---Public Key ---")
	print(public_key)
	print("---Private Key ---")
	print(private_key)
	messager = input("Please nhập đoạn tin cần mã hoá: ")
	encrypt = encrypt(public_key,messager)
	print(" - Your encrypted message is: ", ''.join(map(lambda x: str(x), encrypt)))
	print("-----------------")
	print("messager la : " , decryption(private_key,encrypt))
