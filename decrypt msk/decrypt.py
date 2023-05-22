import blowfish

cipher = blowfish.Cipher(b"qm7psvaMXQoay7kARXpNPcLNWqsbqcOyI4lqHtxFh26HSuE6RHNq7J4e", byte_order = "little")

f_data='in/music_skill.msk'
f_out='out/data.msk'
with open(f_data, 'rb') as f:
    with open(f_out, 'wb') as f_out:
        while True:
            buf = f.read(8)
            if not buf:
                break
            dec = cipher.decrypt_block(buf)
            f_out.write(dec)
