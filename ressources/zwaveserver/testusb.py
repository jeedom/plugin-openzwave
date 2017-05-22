import os, sys
from os.path import join


def find_tty_usb2(id_vendor, id_product):
    # find_tty_usb('0658', '0200') -> '/dev/ttyUSB021' for Sigma Designs, Inc.
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the entire lot at once instead of going over all the usb devices each time.
    print('check for idVendor:%s idProduct: %s' % (id_vendor, id_product,))
    for device_base in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', device_base)
        # debug_print(dn)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        # debug_print(idv)
        if idv != id_vendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        # debug_print(idp)
        if idp != id_product:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(device_base + ':'):
                for sub_subdir in os.listdir(str.join(dn, subdir)):
                    if sub_subdir.startswith('ttyUSB'):
                        return join('/dev', sub_subdir)
    return None


def find_tty_usb(id_vendor, id_product):
    """find_tty_usb('0658', '0200') -> '/dev/ttyUSB021' for Sigma Designs, Inc."""
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the entire lot at once instead of going over all the usb devices
    # each time.
    # print('check for idVendor:%s idProduct: %s' % (id_vendor, id_product,))
    for device_base in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', device_base)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != id_vendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != id_product:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(device_base+':'):
                for sub_subdir in os.listdir(join(dn, subdir)):
                    if sub_subdir.startswith('ttyUSB'):
                        return join('/dev', sub_subdir)

if __name__ == '__main__':
    know_sticks = [{'idVendor': '0658', 'idProduct': '0200', 'name': 'Sigma Designs, Inc'},
                   {'idVendor': '10c4', 'idProduct': 'ea60', 'name': 'Cygnal Integrated Products, Inc. CP210x UART Bridge'}]

    for stick in know_sticks:
        _device = find_tty_usb(stick['idVendor'], stick['idProduct'])
        if _device is not None:
            print('USB Z-Wave Stick found:%s use port %s' % (stick['name'], _device,))

    if _device is None:
        print('No USB Z-Wave Stick detected')
        sys.exit(1)
