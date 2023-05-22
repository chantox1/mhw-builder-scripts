import csv, json
import os, errno
import blowfish

def decrypt(f_in, f_out, cipher):
    with open(f_in, 'rb') as f_in:
        with open(f_out, 'wb') as f_out:
            while True:
                buf = f_in.read(8)
                if not buf:
                    break
                dec = cipher.decrypt_block(buf)
                f_out.write(dec)

cipher = blowfish.Cipher(b"PCEBFfRCbwIdy6AZIoNA5lXV6FEki0yBEyW4FPXZUyWgeauqY8PYeZkM", byte_order = "little")

input_dir='in'
output_dir='out'
for fname in os.listdir(input_dir):
    fpath = os.path.join(input_dir, fname)
    f_out = os.path.join(output_dir, fname)
    if os.path.isfile(fpath):
        decrypt(fpath, f_out, cipher)
