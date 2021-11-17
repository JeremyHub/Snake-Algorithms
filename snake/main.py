import snake
import pygame
import concurrent.futures
import snake_ai

if __name__ == '__main__':
    # things you might want to change
    # running_type = 'human'
    running_type = 'ai'
    does_draw = True
    num_games = 10

    board_size = 10
    max_moves = (board_size**3) * 2.3
    screen_size = 900

    result_log = []
    debug = snake_ai.debug
    if does_draw:
        pygame.init()
        screen = pygame.display.set_mode((screen_size, screen_size))
    else:
        screen = None

    if running_type == 'human':
        for i in range(num_games):
            board = snake.Board(board_size, board_size, screen, screen_size, max_moves, debug, does_draw)
            result = False
            while not result:
                result = board.run_with_human_input()
            print(f'Game {i} finished with score {result[0]} and {result[1]} moves')
            result_log.append(result)
    elif running_type == 'ai' and not does_draw:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result_log = [executor.submit(snake.run_one_AI_game, i, board_size, board_size, screen, screen_size, max_moves, debug, does_draw) for i in range(num_games)]
    elif running_type == 'ai' and does_draw:
        for i in range(num_games):
            result_log.append(snake.run_one_AI_game(i, board_size, board_size, screen, screen_size, max_moves, debug, does_draw))
    else:
        raise Exception('unknown running type')

    total_score = 0
    total_moves = 0
    total_wins = 0
    max_score = float('-inf')
    min_score = float('inf')
    for result in result_log:
        if running_type == 'ai' and not does_draw: score, moves = result.result()
        else: score, moves = result
        if score == board_size**2:
            total_wins += 1
        total_score += score
        total_moves += moves
        if score > max_score:
            max_score = score
        if score < min_score:
            min_score = score
    print(f'average score: {total_score / num_games}')
    print(f'average moves: {total_moves / num_games}')
    print(f'max score: {max_score}')
    print(f'min score: {min_score}')
    print(f'win %: {total_wins / num_games}')
    pygame.quit()