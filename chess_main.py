import pygame 
import chess_engine

#pygameの設定
BOARD_WIDTH=BOARD_HEIGHT=480
DIMENTION=8
SQUARE_SIZE = BOARD_WIDTH//DIMENTION
MAX_FPS=24

#駒
IMAGES={}
#ボードの色
COLORS=["#FFF5E1", "#855E42"]

def load_images():
    pieces = ["wP","wR","wN","wB","wK","wQ","bP","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('image/' + piece + '.png'),(SQUARE_SIZE,SQUARE_SIZE*0.95))



def main():
    #クリック
    player_click = []
    square_clicked = ''

    #pygameの初期化
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()

    #駒の画像を読み込む
    load_images()

    gs = chess_engine.game_Status()
    valid_moves = gs.get_valid_moves()

    flg_running = True
    while flg_running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                flg_running = False

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gs.undo_move()
                    valid_moves = gs.get_valid_moves()

            elif e.type ==pygame.MOUSEBUTTONDOWN:
                #クリック位置を取得
                location = pygame.mouse.get_pos()
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE
                print(location[0], location[1],'row=', row, 'col=',col)
                
                
                square_clicked = str(row) + str(col)
                player_click.append(square_clicked)
                print('player_click = ', player_click)

                if len(player_click)==2:
                    if check_valid_move(player_click[0], player_click[1], valid_moves):
                        gs.make_move(player_click[0], player_click[1])
                        square_clicked = ''
                        player_click = []
                        valid_moves = gs.get_valid_moves()
                    else:
                        player_click = [square_clicked]

        #ボードと駒の描画
        draw_game_status(screen, gs, valid_moves, square_clicked)

        clock.tick(MAX_FPS)
        pygame.display.flip()



def draw_game_status(screen, gs, valid_moves, square_clicked):
    draw_board(screen)
    draw_pieces(screen, gs.board)
    draw_squares_color(screen, gs, valid_moves, square_clicked)

#ボードを描画
def draw_board(screen):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = COLORS[ ((r+c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#駒を描画
def draw_pieces(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#移動可能なマスかを判定
def check_valid_move(move_start, move_end, valid_moves):
    if not valid_moves:
        return False
    
    for move in valid_moves:
        if move[0] == move_start and move[1] == move_end:
            return True
    
    return False

#移動可能なマスを表示
def draw_squares_color(screen, gs, valid_moves, square_clicked):
    if square_clicked != '':
        row = int(square_clicked[0])
        col = int(square_clicked[1])

        if (gs.board[row][col][0] == 'w' and gs.white_to_move) or (gs.board[row][col][0] == 'b' and not gs.white_to_move):
            #クリックしたマス
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(150)
            s.fill(pygame.Color('red'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            #移動可能なマス
            s.fill(pygame.Color('orange'))
            for move in valid_moves:
                if move[0] == square_clicked:
                    col_highlight = int(move[1][1])
                    row_highlight = int(move[1][0])
                    screen.blit(s, (col_highlight * SQUARE_SIZE, row_highlight * SQUARE_SIZE))

if __name__ == '__main__':
    main()


