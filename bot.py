#!/usr/bin/env python3
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py --test prod-like; sleep 1; done

import argparse
from collections import deque
from enum import Enum
import time
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
# Replace "REPLACEME" with your team name!
team_name = "RAICHU"

# ~~~~~============== MAIN LOOP ==============~~~~~

# You should put your code here! We provide some starter code as an example,
# but feel free to change/remove/edit/update any of it as you'd like. If you
# have any questions about the starter code, or what to do next, please ask us!
#
# To help you get started, the sample code below tries to buy BOND for a low
# price, and it prints the current prices for VALE every second. The sample
# code is intended to be a working example, but it needs some improvement
# before it will start making good trades!


def main():
    args = parse_arguments()

    exchange = ExchangeConnection(args=args)

    # Store and print the "hello" message received from the exchange. This
    # contains useful information about your positions. Normally you start with
    # all positions at zero, but if you reconnect during a round, you might
    # have already bought/sold symbols and have non-zero positions.
    hello_message = exchange.read_message()
    print("First message from exchange:", hello_message)

    # Send an order for BOND at a good price, but it is low enough that it is
    # unlikely it will be traded against. Maybe there is a better price to
    # pick? Also, you will need to send more orders over time.
    # exchange.send_add_message(order_id=1, symbol="BOND", dir=Dir.BUY, price=990, size=1)

    # Set up some variables to track the bid and ask price of a symbol. Right
    # now this doesn't track much information, but it's enough to get a sense
    # of the VALE market.
    vale_bid_price, vale_ask_price = None, None
    vale_last_print_time = time.time()

    # Here is the main loop of the program. It will continue to read and
    # process messages in a loop until a "close" message is received. You
    # should write to code handle more types of messages (and not just print
    # the message). Feel free to modify any of the starter code below.
    #
    # Note: a common mistake people make is to call write_message() at least
    # once for every read_message() response.
    #
    # Every message sent to the exchange generates at least one response
    # message. Sending a message in response to every exchange message will
    # cause a feedback loop where your bot's messages will quickly be
    # rate-limited and ignored. Please, don't do that!
    g_order_id = 0
    cur_sell_order_id=-1
    cur_buy_order_id=-1
    if_need_new_sell=True
    if_need_new_buy=True

    cur_vale_bid_price =0
    
    vale_valbf_spread_list =0
    vale_is_trade=0
    valbz_is_trade=0
    vale_is_init=0
    valbz_is_init=0
    vale_bid_price_list=[]
    vale_ask_price_list=[]
    valbz_bid_price_list=[]
    valbz_ask_price_list=[]
    valbz_fake_price_list=[]
    vale_fake_price_list=[]
    vale_valbz_spread_list=[]

    xlf_bid_price_list=[]
    xlf_ask_price_list=[]
    xlf_fake_price_list=[]

    gs_bid_price_list=[]
    gs_ask_price_list=[]
    gs_fake_price_list=[]

    ms_bid_price_list=[]
    ms_ask_price_list=[]
    ms_fake_price_list=[]

    wfc_bid_price_list=[]
    wfc_ask_price_list=[]
    wfc_fake_price_list=[]

    ms_ask_price=0
    ms_bid_price=0
    gs_ask_price=0
    gs_bid_price=0
    wfc_ask_price=0
    wfc_bid_price=0

    gs_is_init=0
    ms_is_init=0
    wfc_is_init=0

    while True:
        g_order_id += 1
        message = exchange.read_message()
        # print(message)

        # Some of the message types below happen infrequently and contain
        # important information to help you understand what your bot is doing,
        # so they are printed in full. We recommend not always printing every
        # message because it can be a lot of information to read. Instead, let
        # your code handle the messages and just print the information
        # important for you!
        if message["type"] == "close":
            print("The round has ended")
            break
        elif message["type"] == "error":
            print(message)
        elif message["type"] == "reject":
            print(message)
        elif message["type"] == "fill":
            print(message)
        elif message["type"]=="out":
            print(message)
            if int(message["order_id"])==cur_sell_order_id:
                if_need_new_sell=True
            if int(message["order_id"])==cur_buy_order_id:
                if_need_new_buy=True
        elif message["type"] == "book":
            # print(message)
            if message["symbol"] == "VALE":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                vale_bid_price = best_price("buy")
                vale_ask_price = best_price("sell")
                if (vale_bid_price!=None) and (vale_ask_price!=None):
                    vale_is_init=1

                now = time.time()
                if now > vale_last_print_time + 1:
                    vale_last_print_time = now
                    print(
                        {
                            "vale_bid_price": vale_bid_price,
                            "vale_ask_price": vale_ask_price,
                        }
                    )
                if vale_bid_price!=None :
                    if len(vale_bid_price_list)>10:
                        del vale_bid_price_list[0]
                    vale_bid_price_list.append(vale_bid_price)
                if vale_ask_price!=None :
                    if len(vale_ask_price_list)>10:
                        del vale_ask_price_list[0]
                    vale_ask_price_list.append(vale_ask_price)
                if (len(vale_bid_price_list)>=1) and (len(vale_ask_price_list)>=1) and (len(valbz_bid_price_list)>=1) and (len(valbz_ask_price_list)>=1):
                    vale_fake_price=(vale_bid_price_list[-1]+vale_ask_price_list[-1])/2
                    valbz_fake_price=(valbz_bid_price_list[-1]+valbz_ask_price_list[-1])/2
                    if vale_fake_price!=None :
                        if len(vale_fake_price_list)>10:
                            del vale_fake_price_list[0]
                        vale_fake_price_list.append(vale_fake_price)

            if message["symbol"] == "VALBZ":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                valbz_bid_price = best_price("buy")
                valbz_ask_price = best_price("sell")
                if (valbz_bid_price!=None) and (valbz_ask_price!=None):
                    valbz_is_init=1
                now = time.time()
                if now > vale_last_print_time + 1:
                    vale_last_print_time = now
                    print(
                        {
                            "valbz_bid_price": vale_bid_price,
                            "valbz_ask_price": vale_ask_price,
                        }
                    )
                if valbz_bid_price!=None :
                    if len(valbz_bid_price_list)>10:
                        del valbz_bid_price_list[0]
                    valbz_bid_price_list.append(valbz_bid_price)
                if valbz_ask_price!=None :
                    if len(valbz_ask_price_list)>10:
                        del valbz_ask_price_list[0]
                    valbz_ask_price_list.append(valbz_ask_price)
                if  (len(vale_bid_price_list)>=1) and (len(vale_ask_price_list)>=1) and (len(valbz_bid_price_list)>=1) and (len(valbz_ask_price_list)>=1):
                    vale_fake_price=(vale_bid_price_list[-1]+vale_ask_price_list[-1])/2
                    valbz_fake_price=(valbz_bid_price_list[-1]+valbz_ask_price_list[-1])/2
                    if valbz_fake_price!=None :
                        if len(valbz_fake_price_list)>10:
                            del valbz_fake_price_list[0]
                        valbz_fake_price_list.append(valbz_fake_price)
                    if (valbz_fake_price>sum(valbz_fake_price_list) / len(valbz_fake_price_list)) and vale_is_init==1:
                        exchange.send_add_message(order_id=g_order_id, symbol="VALE", dir=Dir.BUY, price=vale_bid_price, size=1)
                    elif valbz_is_init==1:
                        exchange.send_add_message(order_id=g_order_id, symbol="VALE", dir=Dir.SELL, price=vale_ask_price, size=1)

            elif message["symbol"] == "BOND":
                print(message)
                bond_sell_price=1001
                bond_buy_price=999
                bond_sell_size=10
                bond_buy_size=10
                
                if if_need_new_sell:
                    exchange.send_add_message(order_id=g_order_id, symbol="BOND", dir=Dir.SELL, price=bond_sell_price, size=bond_sell_size)
                    cur_sell_order_id=g_order_id
                    if_need_new_sell=False
                    print("Put order Type {} Sell Price {} Size {}".format("BOND", bond_sell_price, bond_sell_size))
                if if_need_new_buy:
                    exchange.send_add_message(order_id=g_order_id, symbol="BOND", dir=Dir.BUY, price=bond_buy_price, size=bond_buy_size)
                    cur_buy_order_id=g_order_id
                    if_need_new_buy=False
                    print("Put order Type {} Buy Price {} Size {}".format("BOND", bond_buy_price, bond_buy_size))
            
            elif message["symbol"] == "XLF":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                xlf_bid_price = best_price("buy")
                xlf_ask_price = best_price("sell")
                if (xlf_bid_price!=None) and (xlf_ask_price!=None):
                    xlf_is_init=1
                if xlf_bid_price!=None :
                    if len(xlf_bid_price_list)>10:
                        del xlf_bid_price_list[0]
                    xlf_bid_price_list.append(xlf_bid_price)
                if xlf_ask_price!=None :
                    if len(xlf_ask_price_list)>10:
                        del xlf_ask_price_list[0]
                    xlf_ask_price_list.append(xlf_ask_price)
                if  (len(xlf_bid_price_list)>=1) and (len(xlf_ask_price_list)>=1):
                    xlf_fake_price=(xlf_bid_price_list[-1]+xlf_ask_price_list[-1])/2
                    if xlf_fake_price!=None :
                        if len(xlf_fake_price_list)>15:
                            del xlf_fake_price_list[0]
                        xlf_fake_price_list.append(xlf_fake_price)
                    if len(xlf_fake_price_list)>=5:
                        xlf_mean=sum(xlf_fake_price_list)/len(xlf_fake_price_list)
                        if xlf_ask_price != None and xlf_ask_price < xlf_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="XLF", dir=Dir.BUY, price=xlf_ask_price, size=1)
                        if xlf_bid_price != None and xlf_bid_price > xlf_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="XLF", dir=Dir.SELL, price=xlf_bid_price, size=1)
            
            elif message["symbol"] == "GS":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                gs_bid_price = best_price("buy")
                gs_ask_price = best_price("sell")
                if (gs_bid_price!=None) and (gs_ask_price!=None):
                    gs_is_init=1
                if gs_bid_price!=None :
                    if len(gs_bid_price_list)>10:
                        del gs_bid_price_list[0]
                    gs_bid_price_list.append(gs_bid_price)
                if gs_ask_price!=None :
                    if len(gs_ask_price_list)>10:
                        del gs_ask_price_list[0]
                    gs_ask_price_list.append(gs_ask_price)
                if  (len(gs_bid_price_list)>=1) and (len(gs_ask_price_list)>=1):
                    gs_fake_price=(gs_bid_price_list[-1]+gs_ask_price_list[-1])/2
                    if gs_fake_price!=None :
                        if len(gs_fake_price_list)>15:
                            del gs_fake_price_list[0]
                        gs_fake_price_list.append(gs_fake_price)
                    if len(gs_fake_price_list)>=5:
                        gs_mean=sum(gs_fake_price_list)/len(gs_fake_price_list)
                        if gs_ask_price != None and gs_ask_price < gs_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="GS", dir=Dir.BUY, price=gs_ask_price, size=1)
                        if gs_bid_price != None and gs_bid_price > gs_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="GS", dir=Dir.SELL, price=gs_bid_price, size=1)



            elif message["symbol"] == "MS":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                ms_bid_price = best_price("buy")
                ms_ask_price = best_price("sell")
                if (ms_bid_price!=None) and (ms_ask_price!=None):
                    ms_is_init=1
                if ms_bid_price!=None :
                    if len(ms_bid_price_list)>10:
                        del ms_bid_price_list[0]
                    ms_bid_price_list.append(ms_bid_price)
                if ms_ask_price!=None :
                    if len(ms_ask_price_list)>10:
                        del ms_ask_price_list[0]
                    ms_ask_price_list.append(ms_ask_price)
                if  (len(ms_bid_price_list)>=1) and (len(ms_ask_price_list)>=1):
                    ms_fake_price=(ms_bid_price_list[-1]+ms_ask_price_list[-1])/2
                    if ms_fake_price!=None :
                        if len(ms_fake_price_list)>15:
                            del ms_fake_price_list[0]
                        ms_fake_price_list.append(ms_fake_price)
                    if len(ms_fake_price_list)>=5:
                        ms_mean=sum(ms_fake_price_list)/len(ms_fake_price_list)
                        if ms_ask_price != None and ms_ask_price < ms_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="MS", dir=Dir.BUY, price=ms_ask_price, size=1)
                        if ms_bid_price != None and ms_bid_price > ms_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="MS", dir=Dir.SELL, price=ms_bid_price, size=1)

            elif message["symbol"] == "WFC":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]
                
                wfc_bid_price = best_price("buy")
                wfc_ask_price = best_price("sell")
                if (wfc_bid_price!=None) and (wfc_ask_price!=None):
                    wfc_is_init=1
                if wfc_bid_price!=None :
                    if len(wfc_bid_price_list)>10:
                        del wfc_bid_price_list[0]
                    wfc_bid_price_list.append(wfc_bid_price)
                if wfc_ask_price!=None :
                    if len(wfc_ask_price_list)>10:
                        del wfc_ask_price_list[0]
                    wfc_ask_price_list.append(wfc_ask_price)
                if  (len(wfc_bid_price_list)>=1) and (len(wfc_ask_price_list)>=1):
                    wfc_fake_price=(wfc_bid_price_list[-1]+wfc_ask_price_list[-1])/2
                    if wfc_fake_price!=None :
                        if len(wfc_fake_price_list)>15:
                            del wfc_fake_price_list[0]
                        wfc_fake_price_list.append(wfc_fake_price)
                    if len(wfc_fake_price_list)>=5:
                        wfc_mean=sum(wfc_fake_price_list)/len(wfc_fake_price_list)
                        if wfc_ask_price != None and wfc_ask_price < wfc_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="WFC", dir=Dir.BUY, price=wfc_ask_price, size=1)
                        if wfc_bid_price != None and wfc_bid_price > wfc_mean:
                            exchange.send_add_message(order_id=g_order_id, symbol="WFC", dir=Dir.SELL, price=wfc_bid_price, size=1)

    xlf_fake_price_list=[]


# ~~~~~============== PROVIDED CODE ==============~~~~~

# You probably don't need to edit anything below this line, but feel free to
# ask if you have any questions about what it is doing or how it works. If you
# do need to change anything below this line, please feel free to


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class ExchangeConnection:
    def __init__(self, args):
        self.message_timestamps = deque(maxlen=500)
        self.exchange_hostname = args.exchange_hostname
        self.port = args.port
        exchange_socket = self._connect(add_socket_timeout=args.add_socket_timeout)
        self.reader = exchange_socket.makefile("r", 1)
        self.writer = exchange_socket

        self._write_message({"type": "hello", "team": team_name.upper()})

    def read_message(self):
        """Read a single message from the exchange"""
        message = json.loads(self.reader.readline())
        if "dir" in message:
            message["dir"] = Dir(message["dir"])
        return message

    def send_add_message(
        self, order_id: int, symbol: str, dir: Dir, price: int, size: int
    ):
        """Add a new order"""
        self._write_message(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "price": price,
                "size": size,
            }
        )

    def send_convert_message(self, order_id: int, symbol: str, dir: Dir, size: int):
        """Convert between related symbols"""
        self._write_message(
            {
                "type": "convert",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "size": size,
            }
        )

    def send_cancel_message(self, order_id: int):
        """Cancel an existing order"""
        self._write_message({"type": "cancel", "order_id": order_id})

    def _connect(self, add_socket_timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if add_socket_timeout:
            # Automatically raise an exception if no data has been recieved for
            # multiple seconds. This should not be enabled on an "empty" test
            # exchange.
            s.settimeout(5)
        s.connect((self.exchange_hostname, self.port))
        return s

    def _write_message(self, message):
        what_to_write = json.dumps(message)
        if not what_to_write.endswith("\n"):
            what_to_write = what_to_write + "\n"

        length_to_send = len(what_to_write)
        total_sent = 0
        while total_sent < length_to_send:
            sent_this_time = self.writer.send(
                what_to_write[total_sent:].encode("utf-8")
            )
            if sent_this_time == 0:
                raise Exception("Unable to send data to exchange")
            total_sent += sent_this_time

        now = time.time()
        self.message_timestamps.append(now)
        if len(
            self.message_timestamps
        ) == self.message_timestamps.maxlen and self.message_timestamps[0] > (now - 1):
            print(
                "WARNING: You are sending messages too frequently. The exchange will start ignoring your messages. Make sure you are not sending a message in response to every exchange message."
            )


def parse_arguments():
    test_exchange_port_offsets = {"prod-like": 0, "slower": 1, "empty": 2}

    parser = argparse.ArgumentParser(description="Trade on an ETC exchange!")
    exchange_address_group = parser.add_mutually_exclusive_group(required=True)
    exchange_address_group.add_argument(
        "--production", action="store_true", help="Connect to the production exchange."
    )
    exchange_address_group.add_argument(
        "--test",
        type=str,
        choices=test_exchange_port_offsets.keys(),
        help="Connect to a test exchange.",
    )

    # Connect to a specific host. This is only intended to be used for debugging.
    exchange_address_group.add_argument(
        "--specific-address", type=str, metavar="HOST:PORT", help=argparse.SUPPRESS
    )

    args = parser.parse_args()
    args.add_socket_timeout = True

    if args.production:
        args.exchange_hostname = "production"
        args.port = 25000
    elif args.test:
        args.exchange_hostname = "test-exch-" + team_name
        args.port = 25000 + test_exchange_port_offsets[args.test]
        if args.test == "empty":
            args.add_socket_timeout = False
    elif args.specific_address:
        args.exchange_hostname, port = args.specific_address.split(":")
        args.port = int(port)

    return args


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (
        team_name != "REPLAC" + "EME"
    ), "Please put your team name in the variable [team_name]."

    main()
