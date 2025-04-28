class TitanIpMapHack:
    @staticmethod
    def get_scan_ins_ip(slot_num):
        return "192.168.120.{}".format(slot_num - ((slot_num - 1) % 2))

    @staticmethod
    def get_scan_ins_ip_and_port_num(sio_ip, site_id):
        slot_num = TitanIpMapHack.get_slot_num_from_slot_ip(sio_ip)
        ip = "192.168.120.{}".format(slot_num - ((slot_num - 1) % 2))
        site_in_apc = site_id + ((slot_num - 1) % 2) * 4
        port = 13000 + site_id + ((slot_num - 1) % 2) * 4
        return ip, site_in_apc, port

    @staticmethod
    def get_scan_ins_ip_from_sio_ip(sio_ip, site_id):
        return TitanIpMapHack.get_scan_ins_ip(TitanIpMapHack.get_slot_num_from_slot_ip(sio_ip))

    @staticmethod
    def get_slot_num_from_slot_ip(slot_ip):
        ip_parts = slot_ip.split('.')
        cluster_num = int(ip_parts[2])
        sio_id = int(ip_parts[3][1:])  # Get the last two digits (after '2')
        sio_id = 10 if sio_id == 0 else sio_id
        slot_num = ((cluster_num - 1) * 10) + sio_id
        return slot_num

    @staticmethod
    def get_slot_ip(slot_num):
        if slot_num == 0:
            return "0"
        cluster_num = ((slot_num - 1) // 10) + 1
        return "192.168.{}.2{:02}".format(cluster_num, 10 if slot_num % 10 == 0 else slot_num % 10)

    @staticmethod
    def get_fp_id(sio_id, site_id):
        return (sio_id - 1) * 4 + site_id

    @staticmethod
    def get_fp_ip(slot_num, site_num):
        if slot_num == 0:
            return "0"
        cluster_num = ((slot_num - 1) // 10) + 1
        sio_id = 10 if slot_num % 10 == 0 else slot_num % 10
        fp_id = TitanIpMapHack.get_fp_id(sio_id, site_num)
        return "192.168.{}.{}".format(cluster_num, fp_id)

    @staticmethod
    def get_titan_hp_fp_ip(sio_ip, site_id):
        octets = sio_ip.split(".")
        sio_thing = int(octets[3])
        fp_id = sio_thing - 200
        return "{}.{}.{}.{}".format(octets[0], octets[1], octets[2], fp_id)

    @staticmethod
    def get_fp_ip_from_sio_ip(sio_ip, site_id):
        octets = sio_ip.split(".")
        sio_thing = int(octets[3])
        sio_id = sio_thing - 200
        return "{}.{}.{}.{}".format(octets[0], octets[1], octets[2], TitanIpMapHack.get_fp_id(sio_id, site_id))

    @staticmethod
    def get_tftp_path(sio_ip):
        octets = sio_ip.split(".")
        cluster = int(octets[2])
        tftp_path = "\\\\192.168.{}.252".format(cluster)
        tftp_path += "\\public\\tftp"
        return tftp_path

if __name__ == "__main__":
    sio_ip = "192.168.122.201"
    #sio_ip = "192.168.122.1"
    print("get_tftp_path  : ",TitanIpMapHack.get_tftp_path(sio_ip))
    print("get_fp_ip_from_sio_ip  : ", TitanIpMapHack.get_fp_ip_from_sio_ip(sio_ip,1))
    print("get_fp_ip : ", TitanIpMapHack.get_fp_ip(2,1))
    print("get_titan_hp_fp_ip : ", TitanIpMapHack.get_titan_hp_fp_ip(sio_ip,1))

