import snake
use_pypy = False
if not use_pypy: import pygame
if not use_pypy: import plotille
import multiprocessing as mp

# function for threapool to use
def run_one_AI_game(tuple_of_args):
    name, ai_type, board_size_x, board_size_y, screen, screen_size, max_moves, debug, does_draw = tuple_of_args
    game = snake.Board(board_size_x, board_size_y, screen, screen_size, max_moves, debug=debug, does_draw=does_draw)
    game.reset()
    result = False
    while not result:
        result = game.run_with_ai_input(ai_type)
    print('Game {name} finished with score {result[0]} and {result[1]} moves'.format(name=name, result=result))
    return result

debug = False

if __name__ == '__main__':

    # things you might want to change

    # running_type = 'human'
    running_type = 'ai'
    # replay under 20 replays games where score is <20 (built to catch loop cases)
    # running_type = 'replay_under_20_ai'
    does_draw = True
    num_games = 500
    board_size = (12, 11)
    ai_type = 'tail'
    # ai_type = 'path'
    # ai_type = 'random'

    max_moves = ((board_size[0]*board_size[1])**(3.36/2)) if ai_type == 'tail' else float('inf')
    screen_size = 900

    if use_pypy: does_draw = False
    result_log = []
    screen = None
    if not use_pypy:
        if does_draw or running_type == 'debug_ai':
            pygame.init()
            screen = pygame.display.set_mode((screen_size, screen_size))

    if use_pypy or (running_type == 'ai' and not does_draw and not debug):
        pool = mp.Pool(processes=12)
        map_result = pool.map_async(run_one_AI_game, [(str(i), ai_type, board_size[0], board_size[1], screen, screen_size, max_moves, debug, does_draw) for i in range(num_games)])
        result_log = map_result.get()
        pool.close()
    elif running_type == 'human':
        for i in range(num_games):
            board = snake.Board(board_size[0], board_size[1], screen, screen_size, max_moves, debug=debug, does_draw=does_draw)
            result = False
            while not result:
                result = board.run_with_human_input()
            print('Game {i} finished with score {result[0]} and {result[1]} moves'.format(i=i, result=result))
            result_log.append(result)
    elif running_type == 'ai' and (does_draw or debug):
        for i in range(num_games):
            result_log.append(run_one_AI_game((i, ai_type, board_size[0], board_size[1], screen, screen_size, max_moves, debug, does_draw)))
    elif running_type == 'replay_under_20_ai':
        for i in range(num_games):
            game = snake.Board(board_size[0], board_size[1], screen, screen_size, max_moves, debug, does_draw, True)
            result = False
            while not result:
                result = game.run_with_ai_input()
            if result[0] < 20:
                foods = game.foods
                moves = game.moves
                while True:
                    game.reconstruct_game(moves.copy(), foods.copy())
            else:
                print('Game {i} finished with score {result[0]} and {result[1]} moves'.format(i=i, result=result))
    else:
        raise Exception('unknown running type')

    total_score = 0
    total_moves = 0
    total_wins = 0
    max_score = float('-inf')
    min_score = float('inf')
    all_moves = []
    scores = []
    for result in result_log:
        score, moves = result
        all_moves.append(moves)
        scores.append(score)
        if score == board_size[0] * board_size[1]:
            total_wins += 1
        total_score += score
        total_moves += moves
        if score > max_score:
            max_score = score
        if score < min_score:
            min_score = score

    if not use_pypy:
        fig = plotille.Figure()
        fig.width = 60
        fig.height = 30
        fig.color_mode = 'byte'
        fig.histogram(all_moves, bins=100)
        print(fig.show(legend=True))

        fig2 = plotille.Figure()
        fig2.width = 60
        fig2.height = 30
        fig2.color_mode = 'byte'
        fig2.histogram(scores, bins=100)
        print(fig2.show(legend=True))

    print('average score: {average}'.format(average=total_score/num_games))
    print('average moves: {average}'.format(average=total_moves/num_games))
    print('max score: {max_score}'.format(max_score=max_score))
    print('min score: {min_score}'.format(min_score=min_score))
    print('win %: {percent}'.format(percent=100*total_wins/num_games))
    if not use_pypy: pygame.quit()
