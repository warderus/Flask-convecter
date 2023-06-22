def convecter():
    data_7609 = []
    reader = open("7609.txt", "r")
    for i in reader:
        data_7609.append(i)
    data_7609 = [line.rstrip() for line in data_7609]
    reader.close()

    data_ASR = []
    reader = open("ASR.txt", "r")
    for i in reader:
        data_ASR.append(i)
    data_ASR = [line.rstrip() for line in data_ASR]
    reader.close()

    data_ASR_add = []
    reader = open("ASR.txt", "r")
    for i in reader:
        data_ASR_add.append(i)
    data_ASR_add = [line.rstrip() for line in data_ASR_add]
    reader.close()

    counter = 0
    counter_ASR_config = 36
    counter_review = 0
    counter_interface = 0
    counter_ip = 0
    counter_service1 = 0
    counter_service2 = 0
    counter_second1 = 0
    counter_second2 = 0
    counter_ipred = 0

    def return_number(begin_number, counter):
        for second_number, item in enumerate(data_7609[begin_number+1:]):
            if item == "!":
                second_number += counter
                return second_number

    def search_vlan(string):
        vlan = ""
        for item in string:
            if item.isdigit():
                vlan += (item)
        return vlan

    def search_ip(string):
        ip = ""
        for number, item in enumerate(string):
            if item.isdigit():
                ip += item
            if item == ".":
                ip += item
            if number != 0 and item == " " and string[number-1].isdigit():
                ip += item
        return ip

    def search_and_replace_vlan(element, data, counter_ASR_config):
        for number, item in enumerate(data[counter_ASR_config-72:
                                           counter_ASR_config-36]):
            number = number + counter_ASR_config-72
            if str(item).find("vlan") != -1:
                data[number] = item.replace("vlan", element)
        return data

    def search_and_replace_description(element, data, counter_ASR_config):
        for number, item in enumerate(data[counter_ASR_config-72:
                                           counter_ASR_config-36]):
            number = number + counter_ASR_config-72
            if str(item).find("review") != -1:
                data[number] = element
        return data

    def search_and_replace_address(element, data, counter_ASR_config):
        for number, item in enumerate(data[counter_ASR_config-72:
                                           counter_ASR_config-36]):
            number = number + counter_ASR_config-72
            if str(item).find("ipaddr") != -1:
                data[number] = " ipv4 address " + element
        return data

    def search_and_add_address(element, data, counter_ASR_config,
                               counter_second1, counter_second2):
        for number, item in enumerate(data[counter_ASR_config-72:
                                           counter_ASR_config-36]):
            number = number + counter_ASR_config-72
            if str(item).find("second1") != -1:
                counter_second1 += 1
                data[number] = " ipv4 address " + element + " secondary"
                return data, counter_second1, counter_second2
            elif str(item).find("second2") != -1:
                counter_second2 += 1
                data[number] = " ipv4 address " + element + "secondary"
                return data, counter_second1, counter_second2

    def search_and_add_no_ip_redirects(element, data, counter_ASR_config):
        for number, item in enumerate(data[counter_ASR_config-72:
                                           counter_ASR_config-36]):
            number = number + counter_ASR_config-72
            if str(item).find("ipred") != -1:
                data[number] = " no ip redirects"
        return data

    def search_and_add_service_policy(element,  data, counter_ASR_config,
                                      counter_service1, counter_service2):
        for number, item in enumerate(data[counter_ASR_config-72:
                                           counter_ASR_config-36]):
            number = number + counter_ASR_config-72
            if str(item).find("ser-pol input") != -1:
                counter_service1 += 1
                data[number] = element
                return data, counter_service1, counter_service2
            elif str(item).find("ser-pol output") != -1:
                counter_service2 += 1
                data[number] = element
                return data, counter_service1, counter_service2

    for begin_number, item in enumerate(data_7609):
        counter += 1
        if item == "!":
            second_number = return_number(begin_number, counter)
            for item_for_transfer in data_7609[begin_number+1:second_number]:
                item_for_transfer = str(item_for_transfer)
                if item_for_transfer.find("interface") != -1:
                    data_ASR += data_ASR_add
                    counter_interface += 1
                    counter_ASR_config += 36
                    vlan = search_vlan(item_for_transfer)
                    data_ASR = search_and_replace_vlan(vlan, data_ASR,
                                                       counter_ASR_config)
                elif item_for_transfer.find("description") != -1:
                    counter_review += 1
                    data_ASR = search_and_replace_description(
                        item_for_transfer, data_ASR, counter_ASR_config)
                elif item_for_transfer.find("ip address") != -1 and \
                        item_for_transfer.find("no") == -1 and \
                        item_for_transfer.find("secondary") == -1:
                    counter_ip += 1
                    ip = search_ip(item_for_transfer)
                    data_ASR = search_and_replace_address(ip, data_ASR,
                                                          counter_ASR_config)
                elif item_for_transfer.find("secondary") != -1:
                    ip = search_ip(item_for_transfer)
                    general_data = search_and_add_address(ip, data_ASR,
                                                          counter_ASR_config,
                                                          counter_second1,
                                                          counter_second2)
                    data_ASR = general_data[0]
                    counter_second1 = general_data[1]
                    counter_second2 = general_data[2]
                elif item_for_transfer.find("no ip redirects") != -1:
                    counter_ipred += 1
                    data_ASR = search_and_add_no_ip_redirects(
                        item_for_transfer, data_ASR, counter_ASR_config)
                elif item_for_transfer.find("service-policy") != -1:
                    police_data = search_and_add_service_policy(
                        item_for_transfer, data_ASR, counter_ASR_config,
                        counter_service1, counter_service2)
                    data_ASR = police_data[0]
                    counter_service1 = police_data[1]
                    counter_service2 = police_data[2]

    for counter in range(counter_interface-counter_review):
        data_ASR.remove(" review")

    for counter in range(counter_interface-counter_ip):
        data_ASR.remove(" ipaddr")

    for counter in range(counter_interface-counter_second1):
        data_ASR.remove(" second1")

    for counter in range(counter_interface-counter_second2):
        data_ASR.remove(" second2")

    for counter in range(counter_interface-counter_ipred):
        data_ASR.remove(" ipred")

    for counter in range(counter_interface-counter_service1):
        data_ASR.remove(" ser-pol input")

    for counter in range(counter_interface-counter_service2):
        data_ASR.remove(" ser-pol output")

    for counter in range(36):
        data_ASR.pop()

    fileptr = open("clients.txt", "w")
    for i in data_ASR:
        fileptr.write("%s\n" % str(i))
    fileptr.close()


def write_data_to_file(text):
    fileptr = open("7609.txt", "w")
    for i in text:
        fileptr.write(str(i))
    fileptr.close()


def file_to_text():
    text = []
    reader = open("clients.txt", "r")
    for i in reader:
        text.append(i)
    clients = [line.rstrip() for line in text]
    reader.close()
    for i in clients:
        print(i)
    return clients


if __name__ == "__main__":
    convecter()
