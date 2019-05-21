from multiprocessing.connection import Listener
from repository import *
from door_lock import *

WORKER_SOCKET_NAME = '/tmp/worker'
ADDER_SOCKET_NAME = '/tmp/adder'

username_to_add = None

def process_read_command(card_serial):
    if name_to_add:
        add_card(username_to_add, card_serial)
        return

    if not is_authorized(card_serial):
        return

    open_door()

def process_add_command():
    pass

if __name__ == '__main__':
    listener = Listener(WORKER_SOCKET_NAME, 'AF_UNIX')
    initialize_door()

    while True:
        conn = listener.accept()

        print('connection accepted from', listener.last_accepted)
        msg = conn.recv()
        print('Message: ', msg)
        command = msg['type']
        value = msg['value']
        if command == 'read':
            process_read_command(value)
        elif command == 'add':
            process_add_command()
        else:
            log_message('error', '[worker] Unknown command: ' + command)

        listener.close()

# from multiprocessing.connection import Client

# address = ('localhost', 6000)
# conn = Client(address, authkey='secret password')
# conn.send('close')
# # can also send arbitrary objects:
# # conn.send(['a', 2.5, None, int, sum])
# conn.close()
