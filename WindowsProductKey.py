import winreg


def main():
    regkey_current_version = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
    digital_product_id, dpi_type = winreg.QueryValueEx(regkey_current_version, "DigitalProductId")
    product_name, pn_type = winreg.QueryValueEx(regkey_current_version, "ProductName")
    product_key = decode_key(bytearray(digital_product_id[52:67]))
    print("{0}: {1}".format(product_name, product_key))


def decode_key(key_bytes: bytearray) -> str:
    charset = "BCDFGHJKMPQRTVWXY2346789"
    windows_key = list()
    win8byte = int(key_bytes[14] / 6) & 1
    key_bytes[-1] = ((key_bytes[14] & 0xf7) | (win8byte & 2)) * 4
    last_pos = 0

    for pos in range(24, -1, -1):
        pos_value = 0
        for idx in range(14, -1, -1):
            pos_value = pos_value * 256 + key_bytes[idx]
            key_bytes[idx] = int(pos_value / 24) & 0xff
            pos_value %= 24
            last_pos = pos_value
        windows_key.insert(0, charset[pos_value])

    windows_key[last_pos] = "N"
    windows_key.insert(20, "-")
    windows_key.insert(15, "-")
    windows_key.insert(10, "-")
    windows_key.insert(5, "-")

    return "".join(windows_key)


if __name__ == "__main__":
    main()