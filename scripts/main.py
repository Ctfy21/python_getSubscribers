import multiprocessing
from request_subscribers import receive_subscribers_from_groups
from app import start_web_server


code_queue = multiprocessing.Queue(maxsize=1)

def main():
    multiprocessing.Process(target=receive_subscribers_from_groups, args=(code_queue,)).start()
    start_web_server(code_queue)

    # proc_sub.join()


if __name__ == '__main__':
    main() 