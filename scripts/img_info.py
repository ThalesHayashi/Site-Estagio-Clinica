import sys, os, struct

def jpeg_size(fname):
    with open(fname, 'rb') as f:
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i+1]
        if marker == 0xC0 or marker == 0xC2:
            # SOF0 or SOF2
            length = struct.unpack('>H', data[i+2:i+4])[0]
            bits = data[i+4]
            height = struct.unpack('>H', data[i+5:i+7])[0]
            width = struct.unpack('>H', data[i+7:i+9])[0]
            return width, height
        else:
            if i+4 > len(data):
                break
            length = struct.unpack('>H', data[i+2:i+4])[0]
            i += 2 + length
    return None


def png_size(fname):
    with open(fname, 'rb') as f:
        sig = f.read(8)
        if sig != b'\x89PNG\r\n\x1a\n':
            return None
        # IHDR chunk
        length = struct.unpack('>I', f.read(4))[0]
        chunk = f.read(4)
        if chunk != b'IHDR':
            return None
        width = struct.unpack('>I', f.read(4))[0]
        height = struct.unpack('>I', f.read(4))[0]
        return width, height


def main(dirpath):
    for name in sorted(os.listdir(dirpath)):
        path = os.path.join(dirpath, name)
        if not os.path.isfile(path):
            continue
        low = name.lower()
        try:
            if low.endswith('.jpg') or low.endswith('.jpeg'):
                s = jpeg_size(path)
            elif low.endswith('.png'):
                s = png_size(path)
            else:
                s = None
        except Exception as e:
            s = None
        size = os.path.getsize(path)
        print(f"{name}\t{size} bytes\t{('x'.join(map(str,s)) if s else 'unknown')}")

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv)>1 else '.'
    main(d)
