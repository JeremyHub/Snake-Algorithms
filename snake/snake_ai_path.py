import main
debug = main.debug

if debug:
    import os
    from os.path import exists
    import logging
    file_path = "path_ai_log.txt"
    if exists(file_path):
        os.remove(file_path)
    logging.basicConfig(filename=file_path,
                                filemode='a',
                                format='',
                                datefmt='',
                                level=logging.INFO)

def get_action(snake, food, board_size):
    if not check_hamiltonian(board_size):
        raise Exception("Hamiltonian path is not possible")

def check_hamiltonian(board_size):
    if board_size[0] > 1 and board_size[1] > 1:
        if not board_size[0]%2 or not board_size[1]%2:
            return True
    return False