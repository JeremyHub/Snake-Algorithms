import snake
import pygame
import concurrent.futures
import plotille

# function for threapool to use
def run_one_AI_game(name, ai_type, board_size_x, board_size_y, screen, screen_size, max_moves, debug, does_draw):
    game = snake.Board(board_size_x, board_size_y, screen, screen_size, max_moves, debug=debug, does_draw=does_draw)
    game.reset()
    result = False
    while not result:
        result = game.run_with_ai_input(ai_type)
    print(f'Game {name} finished with score {result[0]} and {result[1]} moves')
    return result

debug = False

if __name__ == '__main__':

    # things you might want to change

    # running_type = 'human'
    running_type = 'ai'
    # running_type = 'replay_under_20_ai'
    does_draw = False
    num_games = 100
    board_size = (15, 15)
    ai_type = 'tail'
    # ai_type = 'path'

    max_moves = ((board_size[0]*board_size[1])**(3.36/2))
    screen_size = 900

    result_log = []
    if does_draw or running_type == 'debug_ai':
        pygame.init()
        screen = pygame.display.set_mode((screen_size, screen_size))
    else:
        screen = None

    if running_type == 'human':
        for i in range(num_games):
            board = snake.Board(board_size[0], board_size[1], screen, screen_size, max_moves, debug, does_draw)
            result = False
            while not result:
                result = board.run_with_human_input()
            print(f'Game {i} finished with score {result[0]} and {result[1]} moves')
            result_log.append(result)
    elif running_type == 'ai' and not does_draw and not debug:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            result_log = [executor.submit(run_one_AI_game, ai_type, i, board_size[0], board_size[1], screen, screen_size, max_moves, debug, does_draw) for i in range(num_games)]
    elif running_type == 'ai' and (does_draw or debug):
        for i in range(num_games):
            result_log.append(run_one_AI_game(i, ai_type, board_size[0], board_size[1], screen, screen_size, max_moves, debug, does_draw))
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
                print(f'Game {i} finished with score {result[0]} and {result[1]} moves')
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
        if running_type == 'ai' and not (does_draw or debug): score, moves = result.result()
        else: score, moves = result
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

    print(f'average score: {total_score / num_games}')
    print(f'average moves: {total_moves / num_games}')
    print(f'max score: {max_score}')
    print(f'min score: {min_score}')
    print(f'win %: {100*total_wins / num_games}')
    pygame.quit()
