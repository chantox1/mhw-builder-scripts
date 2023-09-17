import os
import blowfish

key = b"TZNgJfzyD2WKiuV4SglmI6oN5jP2hhRJcBwzUooyfIUTM4ptDYGjuRTP"

def decrypt(input_dir, output_dir):
    cipher = blowfish.Cipher(key, byte_order="little")

    for fname in os.listdir(input_dir):
        if not (os.path.splitext(fname)[1] == ".mib"):
            continue

        fpath = os.path.join(input_dir, fname)
        if not os.path.isfile(fpath):
            continue

        out_path = os.path.join(output_dir, fname)
        with open(fpath, 'rb') as f:
            with open(out_path, 'wb') as f_out:
                while buf := f.read(8):
                    dec = cipher.decrypt_block(buf)
                    f_out.write(dec)
