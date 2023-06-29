# Aung Kyaw Min Htet
# Assigment VI
# Registation in server and to save mongo database

import json
import socket
import pymongo


class TCPserver:
    def __init__(self):
        self.server_ip = "localhost"
        self.server_port = 9898

        # This is from mongo database
        self.connection = pymongo.MongoClient("localhost", 27017)
        self.database = self.connection["akmh"]
        self.collector = self.database["user_info_one"]
        self.candidate = self.database["candidate_info"]

    def main_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print("server is listening from ip {} and port- {}".format(self.server_ip, self.server_port))
        try:
            while True:
                client, address = server.accept()
                print("Connect from client ip - {} and port - {}.".format(address[0], address[1]))
                self.handle_client(client)
        except Exception as err:
            print(err)

    def handle_client(self, sock_client):

        with sock_client as sock:
            data_list = []  # to accept from client input data
            recv_sms = sock.recv(1024)
            data_list = recv_sms.decode('utf-8').split(' ')
            print(data_list)

            if data_list[0] == "login":  # Login for Voting
                self.server_login(sock, data_list)

            elif data_list[0] == "gad":  # to show all data from database
                print("Receive command :", data_list[0])
                self.get_all_data(sock)

            elif data_list[0] == "candidate_info":  # to show candidate information
                self.candidate_info(sock)

            elif data_list[0] == "emailcheck":  # email checking for user register
                self.email_checking(sock, data_list[1])

            elif data_list[0] == "register":  # users register
                self.registration(sock, data_list)

            elif data_list[0] == "c_emailcheck":  # candidate email checking
                self.candi_email_check(sock, data_list[1])

            elif data_list[0] == "candi_register":  # candidate register
                self.candi_register(sock, data_list)

            elif data_list[0] == "point_update":  # point update from client
                self.vote_point_update(data_list)

            elif data_list[0] == "check_point":  # check point for vote again
                self.check_point(sock, data_list)

            elif data_list[0] == "update_money":  # update money
                self.update_money(sock, data_list)

            elif data_list[0] == "r_point_change":  # this update remain money buy point
                self.remain_money_buy_point(sock, data_list)

            elif data_list[0] == "m_point_change":     # this update money buy point
                self.update_money_buy_point(sock, data_list)

            elif data_list[0] == "transfer_email":  # this is transfer point with email
                self.transfer_point_email(sock, data_list)

            elif data_list[0] == "transfer_phone":  # this is transfer point with phone
                self.transfer_point_phone(sock, data_list)

            elif data_list[0] == "delete_account":   # this is delete user account
                self.delete_account(sock, data_list)

            elif data_list[0] == "vote_ranking":   # this is check voting ranking
                self.voting_ranking(sock)

            else:
                sms = bytes("Invalid Option!", 'utf-8')
                sock.send(sms)

    def get_all_data(self, sock):
        data_collector: dict = {}
        for i in self.collector.find({}, {"_id": 0, "name": 1, "email": 1, "password": 1}):
            ids = len(data_collector)
            db = {ids: {"name": i["name"], "email": i["email"], "password": i["password"]}}
            data_collector.update(db)
        str_data = json.dumps(data_collector)
        print(type(str_data))
        print(str_data)

        send_str_data = bytes(str_data, 'utf-8')
        sock.send(send_str_data)
        print("Tips - Client use gad function.")

    def server_login(self, sock, data_list):
        print("Tips - User use login section.")
        server_email = data_list[1]
        server_password = data_list[2]
        flag = -1
        sms_s = {}
        for i in self.collector.find({}, {"_id": 0, "name": 1, "email": 1, "password": 1, "info": 1, "point": 1,
                                          "money": 1}):
            if server_email == i["email"] and server_password == i["password"]:
                sms = {"name": i["name"], "email": i["email"], "info": i["info"], "point": i["point"],
                       "money": i["money"]}
                sms_s = json.dumps(sms)
                flag = 1
                break
            # else:
            #     sock.send(bytes("Account Not Found!", 'utf-8'))
            #     break

        if flag == 1:
            print(sms_s)
            str_data = bytes(sms_s, 'utf-8')
            sock.send(str_data)
        else:
            str_data = bytes("Username and password not found.", 'utf-8')
            sock.send(str_data)

    def candidate_info(self, sock):
        candidate_data = {}
        for i in self.candidate.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
            id = len(candidate_data) + 1
            inset_data = {id: {"name": i["name"], "vote_point": i["vote_point"]}}
            candidate_data.update(inset_data)
        to_send = json.dumps(candidate_data)
        print(to_send)
        sock.send(bytes(to_send, 'utf-8'))

    def email_checking(self, sock, email):
        email_exist = 0
        print(email)
        for i in self.collector.find({}, {"_id": 0, "email": 1}):
            if i["email"] == email:
                email_exist = 1

        if email_exist == 0:  # email not already exist
            sock.send(bytes("notExit", "utf-8"))

        else:
            sock.send(bytes("Exit Email", "utf-8"))

    def registration(self, sock, data_list: list):
        data_form: [dict, int] = {"email": data_list[1], "password": data_list[2], "phone": int(data_list[3]),
                                  "money": data_list[4], "name": data_list[5], "info": data_list[6],
                                  "point": int(data_list[7])}
        ids = self.collector.insert_one(data_form)

        sock.send(bytes(str(ids.inserted_id), 'utf-8'))

    def candi_email_check(self, sock, email):
        candi_email_exit = 0
        for i in self.candidate.find({}, {"_id": 0, "email": 1}):
            # print(i["email"])
            if i["email"] == email:
                candi_email_exit = 1
        if candi_email_exit == 0:
            sock.send(bytes("notExit", 'utf-8'))
        else:
            sock.send(bytes("Candidate email is already register!", 'utf-8'))

    def candi_register(self, sock, data_list):
        candi_data_form = {"name": data_list[1], "email": data_list[2], "phone": data_list[3],
                           "vote_point": int(data_list[4]), "info": data_list[5]}
        ids = self.candidate.insert_one(candi_data_form)
        # print("Candidate data is registered :", ids.inserted_id)

        sock.send(bytes(str(ids.inserted_id), 'utf-8'))

    def vote_point_update(self, data_list):
        print("candidate name :{} and voter name :{}".format(data_list[1], data_list[2]))
        u_candi_name = data_list[1]
        u_voter_name = data_list[2]

        self.candidate.update_one({"name": u_candi_name},
                                  {"$inc": {"vote_point": +10}, "$push": {"voter_list": u_voter_name}})
        self.collector.update_one({"name": u_voter_name}, {"$inc": {"point": -10}})

    def check_point(self, sock, data_list):
        check_p = 0
        for i in self.collector.find({"name": data_list[1]}, {"_id": 0, "point": 1}):
            check_p = i["point"]
            break
        print("Remain point is:", check_p)
        sock.send(bytes(str(check_p), 'utf-8'))

    def update_money(self, sock, data_list):
        u_money = 0
        money = int(data_list[2])
        self.collector.update_one({"name": data_list[1]},
                                  {"$inc": {"money": +money}})
        for i in self.collector.find({"name": data_list[1]}, {"_id": 0, "money": 1}):
            print("Remain money :", i["money"])
            u_money = i["money"]
            break
        sock.send(bytes(str(u_money), 'utf-8'))

    def remain_money_buy_point(self, sock, data_list):
        point = int(data_list[2])
        money = int(data_list[3])
        print(point)
        print(money)
        u_money = 0
        self.collector.update_one({"name": data_list[1]},
                                   {"$inc": {"point": +point, "money": -money}})

        for i in self.collector.find({"name": data_list[1]}, {"_id": 0, "money": 1}):
            u_money = i["money"]
            print(u_money)
        sock.send(bytes(str(u_money), 'utf-8'))

    def update_money_buy_point(self, sock, data_list):
        point = int(data_list[2])
        money = int(data_list[3])
        print(point)
        print(money)
        u_money = 0
        self.collector.update_one({"name": data_list[1]}, {"$inc": {"point": +point, "money": -money}})

        for i in self.collector.find({"name": data_list[1]}, {"_id": 0, "money": 1}):
            u_money = i["money"]
        sock.send(bytes(str(u_money), 'utf-8'))
    def transfer_point_email(self, sock, data_list):
        email = data_list[1]
        point = int(data_list[2])
        reduce_email = data_list[3]
        print("increase email :", email)
        print("reduce email :", reduce_email)
        self.collector.update_one({"email": email}, {"$inc": {"point": +point}})
        self.collector.update_one({"email": reduce_email}, {"$inc": {"point": -point}})

        sock.send(bytes("Update :", 'utf-8'))

    def transfer_point_phone(self, sock, data_list):
        phone = int(data_list[1])
        point = int(data_list[2])
        reduce_email = data_list[3]
        self.collector.update_one({"phone": phone}, {"$inc": {"point": +point}})
        self.collector.update_one({"email": reduce_email}, {"$inc": {"point": -point}})

        sock.send(bytes("Updated", 'utf-8'))

    def voting_ranking(self, sock):
        voting_data: dict = {}
        for i in self.candidate.find({}, {"_id": 0, "name": 1, "vote_point": 1}):
            name = i["name"]
            point = i["vote_point"]
            voting_data.update({name: point})
        print(voting_data)
        data_str = json.dumps(voting_data)

        sock.send(bytes(data_str, 'utf-8'))


    def delete_account(self, sock, data_list):
        self.collector.delete_one({"name": data_list[1]})

        sock.send(bytes("deleted", 'utf-8'))

if __name__ == '__main__':
    server_connect = TCPserver()
    server_connect.main_server()
