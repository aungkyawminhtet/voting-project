#AKMH
import json
import socket
from collections import Counter


class TCPclient:
    def __init__(self, sms):
        self.client_ip = "localhost"
        self.client_port = 9898

        self.input_checking(sms)

    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.client_ip, self.client_port))

        return client  # to send and receive data

    def input_checking(self, input_sms):

        if input_sms == "reg":
            self.registor()
        elif input_sms == "login":
            self.client_login(input_sms)
        elif input_sms == "gad":
            self.get_all_data(input_sms)
        else:
            print("Invalid Option!")

    def get_all_data(self, sms):

        client = self.run_client()

        # send data to server
        send_sms = bytes(sms, 'utf-8')
        client.send(send_sms)

        # received data from server
        recv_from_server = client.recv(4029)

        print(recv_from_server.decode('utf-8'))
        # dict_data: dict = json.loads(recv_from_server.decode('utf-8'))
        # print(type(dict_data))
        # print(dict_data)
        client.close()

    def registor(self):
        print("#####---This is register section---####")
        while True:
            r_email = input("Enter your Register email==> :")

            flag = self.email_checking(r_email)
            if flag == -1:
                print("Valid Email")
            else:
                print("Invalid Email")
                self.registor()

            try:
                option = input("Press 1 registration fo Voter\nPress 2 Registration for Candidate! :")
                if option == '1':
                    self.reg_for_voter(r_email)
                elif option == '2':
                    self.reg_for_candidate(r_email)
                else:
                    print("Invalid Option!")
            except Exception as err:
                print(err)

    def reg_for_voter(self, r_email):
        print("#####---This is Registration For voter Section.---#####")
        if self.email_check_inDB(r_email):
            try:
                pass1 = input("Enter your password to register :")
                pass2 = input("Enter your password Again to register :")

                if pass1 == pass2:
                    print("correct password")
                    name = input("Enter your name :")
                    phone = int(input("Enter your phone number :"))
                    money = input("Enter your Money :")

                    data_list = [r_email, pass1, phone, money, name]
                    self.final_registration(data_list)

                else:
                    print("Password was not match!")
                    self.reg_for_voter(r_email)
            except Exception as err:
                print(err)
        else:
            print("Email is already Exit!")
            self.registor()

    def email_check_inDB(self, email):
        client = self.run_client()
        data = "emailcheck" + " " + email
        client.send(bytes(data, 'utf-8'))

        received = client.recv(4096).decode('utf-8')

        if received == "notExit":
            print("Eamil not Exit.")
            client.close()
            return True
        else:
            client.close()
            return False  # -------------------------------------------------------------

    def final_registration(self, data_list):
        data_form = "register" + " " + data_list[0] + " " + data_list[1] + " " + str(
            data_list[2]) + " " + data_list[3] + " " + data_list[4] + " " + "User" + " " + "100"

        client = self.run_client()
        client.send(bytes(data_form, 'utf-8'))

        receive = client.recv(4096).decode('utf-8')
        print(receive)

        if receive:
            print("Registration is success!", receive)
            info = "login"
            self.client_login(info)
        client.close()

    def email_checking(self, r_email):
        name_count = 0
        for i in range(len(r_email)):
            # print(r_email[i])
            if r_email[i] == "@":
                # print("Name end here")
                break
            name_count += 1
        # print("name counter :", name_count)
        email_name = r_email[0:name_count]
        email_form = r_email[name_count:]
        print(email_name)
        print(email_form)

        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            achar = email_name[i]
            if (ord(achar) > 31 and ord(achar) < 48) or (ord(achar) > 57 and ord(achar) < 65) or (
                    ord(achar) > 90 and ord(achar) < 61) or (ord(achar) > 122 and ord(achar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com",
                       "@gmail.com"]
        for i in range(len(domain_form)):
            if domain_form[i] == email_form:
                email_flag = 1

        if name_flag == -1 or email_flag == 1:
            return -1
        else:
            return 1

    def reg_for_candidate(self, r_email):
        print("#####---This is registration for candidate---####")
        if self.candi_email_checking_inDB(r_email):
            try:
                client = self.run_client()
                name = input("Enter your candidate name :")
                phone = int(input("Enter your candidate phone number :"))
                vote_point = 0
                info = "candidate info"
                candi_data_form = "candi_register" + " " + name + " " + r_email + " " + str(phone) + " " + str(
                    vote_point) + " " + info
                client.send(bytes(candi_data_form, 'utf-8'))

                candi_received = client.recv(4096).decode('utf-8')
                print("Candidate registor success", candi_received)

                info = "login"
                self.client_login(info)

            except Exception as err:
                print(err)

    def candi_email_checking_inDB(self, c_email):  # c_email = check email
        print(c_email)
        client = self.run_client()
        data = "c_emailcheck" + " " + c_email
        client.send(bytes(data, 'utf-8'))

        received = client.recv(4096).decode('utf-8')
        print(received)

        if received == "notExit":
            client.close()
            return True
        else:
            self.registor()
            client.close()
            return False

    def client_login(self, info):
        print("#####---This is Login Section.---#####")
        try:
            l_email = input("Enter your email to login :")
            l_password = input("Enter your login password :")
            client = self.run_client()
            send_sms = info + ' ' + l_email + ' ' + l_password
            l_send_sms = bytes(send_sms, 'utf-8')
            client.send(l_send_sms)

            recv_from_server = client.recv(4029)
            sever_data_dic = json.loads(recv_from_server.decode('utf-8'))
            self.option_choice(sever_data_dic)

        except Exception as err:
            print(err)

    def option_choice(self, server_data_dic):
        min_point = int(server_data_dic["point"])
        if min_point > 5:
            print("#####---This is Voter information Section---#####")
            print("name :", server_data_dic["name"])
            print("email :", server_data_dic["email"])
            print("info :", server_data_dic["info"])
            print("point :", server_data_dic["point"])
            print("Money: ", server_data_dic["money"])

            try:
                option = input("Press 1 to Vote for User Option\nPress 2 to get Main Option\nPress 3 to Exit :")

                if option == '1':
                    self.user_option(server_data_dic)
                elif option == '2':
                    self.input_checking(sms)
                elif option == '3':
                    exit(1)
                else:
                    print("Invalid Option!")
                    self.option_choice(server_data_dic)
            except Exception as err:
                print(err)
        else:
            print("Your Vote Point is too low. Fist You should buy Point!")
            self.point_change(server_data_dic)

    def user_option(self, server_data_dic):
        print("#####---This is User option For Vote---#####")
        try:
            option = input(
                "Press 1 to Voting:\nPress 2 to get more point:\nPress 3 to Transfer Point:\nPress 4 to get Voting "
                "Ranking:\nPress 5 to"
                "change User Information:\nPress 6 to Delete Account:\nPress 7 to Exit:")

            if option == '1':
                self.voting(server_data_dic)
            elif option == '2':
                self.point_change(server_data_dic)
            elif option == '3':
                self.transfer_point(server_data_dic)
            elif option == '4':
                self.voting_ranking(server_data_dic)
            elif option == '6':
                self.delete_account(server_data_dic)
            else:
                print("Invalid Option!")

        except Exception as err:
            print(err)
            self.user_option(server_data_dic)

    def voting(self, server_data_dic):
        print("#####---This is Voting Section---#####")
        client = self.run_client()
        sms = bytes("candidate_info", 'utf-8')
        client.send(sms)

        info = client.recv(4096).decode('utf-8')
        # print(info.decode('utf-8'))

        candi_info = json.loads(info)

        for i in candi_info:
            print("No :", i, "Name :", candi_info[i]["name"], "vote_point :", candi_info[i]["vote_point"])

        self.vote_for_voter(candi_info, server_data_dic)

    def vote_for_voter(self, candi_info, server_data_dic):
        try:
            print("Tips : One Vote for 10 point.")
            voter_name = input("Enter your Candidate Name :")
            candi = 0
            for i in candi_info:
                # vote_point = candi_info[i]["vote_point"]
                # print("poit is : ", vote_point)
                if voter_name == candi_info[i]["name"]:
                    candi = 1

            if candi == 1:
                self.vote_point_update(voter_name, server_data_dic)
                print("You are Voted!")

                # -------Change-----------
                client = self.run_client()
                point_sms = "check_point" + " " + server_data_dic["name"]
                client.send(bytes(point_sms, 'utf-8'))

                recev_point_sms = client.recv(4096).decode('utf-8')
                print("Remain point is :", int(recev_point_sms))
                remain_point = int(recev_point_sms)

                if remain_point > 5:
                    try:
                        v_option = int(input("Press 1 to Vote Again\nPress 2 to Exit :"))
                        if v_option == 1:
                            self.vote_for_voter(candi_info, server_data_dic)
                        elif v_option == 2:
                            exit(1)
                        else:
                            print("Voter Option Invalid!")

                    except Exception as err:
                        print(err)
                else:
                    print("----Your Voting point is less than 10 point----")
                    p_change_sms = input("Do you want to change point (y/n)? :").lower()  # point change check
                    if p_change_sms == 'y':
                        self.point_change(server_data_dic)
                    else:
                        print("Thank You for Voting!")

            else:
                print("Candidate Name is Invalid! Check Candidate List!")
                self.option_choice(server_data_dic)

        except Exception as err:
            print(err)

    def vote_point_update(self, voter_name, server_data_dic):  # to send vote data in server
        print("####---This vote point update section---####")
        vote_point_data_form = "point_update" + " " + voter_name + " " + server_data_dic["name"]
        client = self.run_client()
        client.send(bytes(vote_point_data_form, 'utf-8'))

        # recev_data = client.recv(4096)
        # print(recev_data.decode('utf-8'))

    def point_change(self, server_data_dic):  # User money information and point change
        print("#####---Vote point Change Section!---#####")
        client = self.run_client()

        p_name = server_data_dic["name"]
        print("Your Username is :", p_name)
        print("Your money is Remain :", server_data_dic["money"])
        # r_money = server_data_dic["money"]  # remain money
        m_option = input("Do you want to more add money (y/n)? :").lower()  # m_option = money option

        if m_option == 'y':
            p_money = int(input("Enter your Money :"))  # this section is update money to database
            u_money = "update_money" + " " + p_name + " " + str(p_money)  # u_money is update money to database
            client.send(bytes(u_money, 'utf-8'))

            from_server = int(client.recv(4099).decode('utf-8'))
            print("Your money is :", from_server)
            self.decision_point_change(server_data_dic, from_server)

        else:
            print("###--Point is 1 point For 100$--##")
            print("Your remain money is :", server_data_dic["money"])
            c_money: int = int(input("Change as much as you want point. Enter your money :"))
            point_change = round(c_money/100)
            print(point_change)
            point_update = "r_point_change" + " " + server_data_dic["name"] + " " + str(point_change) + " " + str(c_money)
            client.send(bytes(point_update, 'utf-8'))

            print("your money is :", client.recv(4096).decode('utf-8'))

    def decision_point_change(self, server_data_dic, from_server):  # this section is to decide point change and to go vote option
        try:
            u_option = input("Press 1 to Vote Option\nPress 2 to Change Point :")

            if u_option == '1':
                self.option_choice(server_data_dic)
            elif u_option == '2':
                self.update_money_buy_point(server_data_dic, from_server)
            else:

                print("Invalid Option")
                self.decision_point_change(server_data_dic, from_server)
        except Exception as err:
            print(err)

    def update_money_buy_point(self, server_data_dic, from_server):
        print("###--Point is 1 point For 100$--##")
        print("Your remain money is :", from_server)
        m_money: int = int(input("Change as much as you want point. Enter your money :")) # c is change
        m_change_pt = round(m_money / 100)  # m is money
        print(m_change_pt)
        point_change = "m_point_change" + " " + server_data_dic["name"] + " " + str(m_change_pt) + " " + str(m_money)
        client = self.run_client()
        client.send(bytes(point_change, 'utf-8'))

        print("Your remain money is :", client.recv(4096).decode('utf-8'))

    def transfer_point(self, server_data_dic):
        print("Your point remain is:", server_data_dic["point"])
        t_email = input("Press 1 is Email Transfer\nPress 2 is Phone Transfer :")
        if t_email == '1':
            transfer_email = input("Enter your Transfer Eamil :")
            transfer_pt = input("Enter your Transfer Point :")
            client = self.run_client()
            transfer_sms = "transfer_email" + " " + transfer_email + " " + str(transfer_pt) + " " + server_data_dic[
                "email"]
            client.send(bytes(transfer_sms, 'utf-8'))

            print("recv sms :", client.recv(4096).decode('utf-8'))
            self.option_choice(server_data_dic)

        elif t_email == '2':
            print("Your point remain is :", server_data_dic["point"])
            transfer_phone = input("Enter your Transfer Phone :")
            transfer_pt = input("Enter your Transfer Point :")
            client = self.run_client()
            transfer_sms = "transfer_phone" + " " + str(transfer_phone) + " " + str(transfer_pt) + " " + \
                           server_data_dic["email"]
            client.send(bytes(transfer_sms, 'utf-8'))

            print("recv sms :", client.recv(4096).decode('utf-8'))
            self.option_choice(server_data_dic)
        else:
            print("Invalid Transfer point")
            self.transfer_point(server_data_dic)

    def voting_ranking(self, server_data_dic):
        client = self.run_client()
        sms = "vote_ranking"
        client.send(bytes(sms, 'utf-8'))

        recv_sms = client.recv(4096).decode('utf-8')
        data_dic = json.loads(recv_sms)
        # print(data_dic)

        data = Counter(data_dic)

        data_value = {}  # to collect name if voting point same
        for value in data.values():
            data_value[value] = []

        for (key, value) in data.items():
            data_value[value].append(key)

        maxVote = sorted(data_value.keys(), reverse=True)[0]  # to find max vote point
        print("Maximum Voter point is :", maxVote)

        if len(data_value[maxVote]) > 1:
            name = sorted(data_value[maxVote])[0]
            print("Maximum Voter Name is :", name)
        else:
            print("Maximum Voter Name is :", data_value[maxVote][0])
        self.option_choice(server_data_dic)

    def delete_account(self, server_data_dic):
        client = self.run_client()
        delete_sms = "delete_account" + " " + server_data_dic["name"]
        client.send(bytes(delete_sms, 'utf-8'))

        print("Account is :", client.recv(4096).decode('utf-8'))
        self.option_choice(server_data_dic)


if __name__ == '__main__':
    while True:
        print("#####---This is only comment reg, login, gad---#####")
        sms: str = input("Enter your comment : ")
        run_client = TCPclient(sms)
