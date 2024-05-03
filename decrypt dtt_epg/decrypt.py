import blowfish

cipher = blowfish.Cipher(b"sJV4g7d55gKnQB5nS6XJ9pZ1qZmmQwNnSbidUW1OeAhHrpPd6MKbfsrt", byte_order = "little")

f_data='in/data.dtt_epg'
f_out='out/data.dtt_epg'
with open(f_data, 'rb') as f:
    with open(f_out, 'wb') as f_out:
        while True:
            buf = f.read(8)
            if not buf:
                break
            dec = cipher.decrypt_block(buf)
            f_out.write(dec)
