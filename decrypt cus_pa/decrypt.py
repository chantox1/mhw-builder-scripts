import blowfish

cipher = blowfish.Cipher(b"PCEBFfRCbwIdy6AZIoNA5lXV6FEki0yBEyW4FPXZUyWgeauqY8PYeZkM", byte_order = "little")

f_data='in/customParts.cus_pa'
f_out='out/customParts.cus_pa'
with open(f_data, 'rb') as f:
    with open(f_out, 'wb') as f_out:
        while True:
            buf = f.read(8)
            if not buf:
                break
            dec = cipher.decrypt_block(buf)
            f_out.write(dec)
