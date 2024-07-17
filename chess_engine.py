class game_Status():
    def __init__(self):
        
        #盤面の設定
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]



        #手番 True->白, False->黒
        self.white_to_move = True

        self.moveLog = []

    def make_move(self, move_start, move_end):
        
        #移動先と移動元のrowとcol
        start_row = int(move_start[0])
        start_col = int(move_start[1])
        end_row = int(move_end[0])
        end_col = int(move_end[1])

        #動かした駒と取った駒
        piece_move = self.board[start_row][start_col]
        piece_captured = self.board[end_row][end_col]

        #元のセルを空欄にし、動かした駒を移動先のセルにおく
        self.board[start_row][start_col] = '--'
        self.board[end_row][end_col] = piece_move
        
        #手番を変更
        self.white_to_move = not self.white_to_move

        #動かした駒のをログに保存
        move = [start_row,start_col, end_row, end_col, piece_move, piece_captured]
        self.moveLog.append(move)
        print(self.moveLog)

    #駒を戻せるように保存しておく
    def undo_move(self, ):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()

            '''
            move 0: start row
                 1: start col
                 2: end row
                 3: end col
                 4: piece moved
                 5: piece captured
            '''

            self.board[move[0]][move[1]] = move[4]
            self.board[move[2]][move[3]] = move[5]
            self.white_to_move = not self.white_to_move

        print('undo_move', self.moveLog)

    #移動可能かを確認
    def get_valid_moves(self):
        moves = self.get_all_possible_moves()


        return moves
    
    #駒ごとにチェック
    def get_all_possible_moves(self):
        moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece_color = self.board[row][col][0]
                piece_type = self.board[row][col][1]
                if(piece_color == 'w' and self.white_to_move) or (piece_color == 'b' and not self.white_to_move):
                    #駒ごとに移動可能かチェック
                    if piece_type == 'P':
                        self.get_Pawn_moves(row, col, moves)
                    if piece_type == 'N':
                        self.get_Night_moves(row, col, moves)
                    if piece_type == 'B':
                        self.get_Bishop_moves(row, col, moves)
                    pass
        return moves
    
    #ポーンの移動
    def get_Pawn_moves(self, row, col, moves):

        if self.white_to_move:
            row_adj = -1
            row_start = 6
            row_start_adj = -2
            opp_piece = 'b'
        else:
            row_adj = 1
            row_start = 1
            row_start_adj = 2
            opp_piece = 'w'

        if row > 0 and row < 7:
            end_row = row + row_adj
            end_col = col
            #前に進む場合
            if self.board[end_row][end_col] == '--':
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

                end_row = row + row_start_adj
                end_col = col

                if row == row_start and self.board[end_row][end_col] == '--':
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)

            #相手の駒を取る場合
            #白:左, 黒:右
            if col-1 >= 0:
                end_row = row + row_adj
                end_col = col - 1
                if self.board[end_row][end_col][0] == opp_piece:
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)

            if col+1 <= 7:
                end_row = row + row_adj
                end_col = col + 1
                if self.board[end_row][end_col][0] == opp_piece:
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)

    #ナイトの移動
    def get_Night_moves(self, row, col, moves):
        #上方向に移動
        if row > 1 and col > 0:
            end_row = row -2
            end_col = col -1
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

        if row > 1 and col < 7:
            end_row = row - 2
            end_col = col + 1
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

        #左方向に移動
        if row > 0 and col > 1:
            end_row = row -1
            end_col = col -2
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

        if row < 7 and col > 1:
            end_row = row + 1
            end_col = col - 2
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)


        #下方向に移動
        if row < 6 and col > 0:
            end_row = row + 2
            end_col = col - 1
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

        if row < 6 and col < 7:
            end_row = row + 2
            end_col = col + 1
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

        #右方向に移動
        if row > 0 and col < 6:
            end_row = row - 1
            end_col = col + 2
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

        if row < 7 and col < 6:
            end_row = row + 1
            end_col = col + 2
            if self.board[end_row][end_col] == '--' or self.board[end_row][end_col][0] != self.board[row][col][0]:
                move = (str(row) + str(col), str(end_row) + str(end_col))
                moves.append(move)

    #ビショップの移動
    def get_Bishop_moves(self, row, col, moves):
        #row:減少、col:増加
        for row_num in range(row -1, -1, -1):
            if col + (row - row_num) < 8:
                end_row = row_num
                end_col = col + row -row_num
                if self.board[end_row][end_col] == '--':
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                
                #同じ色の駒があった場合->そこを含まない、かつ、それ以上先に進まない    
                elif self.board[end_row][end_col][0] == self.board[row][col][0]:
                    break
                #違う色の駒があった場合->そこを取って終わる
                else :
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                    break

        #row:増加、col:減少
        for row_num in range(row + 1, 8):
            if col + (row - row_num) >= 0:
                end_row = row_num
                end_col = col + row -row_num
                if self.board[end_row][end_col] == '--':
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                
                #同じ色の駒があった場合->そこを含まない、かつ、それ以上先に進まない    
                elif self.board[end_row][end_col][0] == self.board[row][col][0]:
                    break
                #違う色の駒があった場合->そこを取って終わる
                else :
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                    break

        #row:減少、col:減少
        for row_num in range(row -1, -1, -1):
            if col + (row - row_num) >= 0:
                end_row = row_num
                end_col = col - (row -row_num)
                if self.board[end_row][end_col] == '--':
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                
                #同じ色の駒があった場合->そこを含まない、かつ、それ以上先に進まない    
                elif self.board[end_row][end_col][0] == self.board[row][col][0]:
                    break
                #違う色の駒があった場合->そこを取って終わる
                else :
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                    break

        #row:増加、col:増加
        for row_num in range(row + 1, 8):
            if col - (row - row_num) < 8:
                end_row = row_num
                end_col = col - (row -row_num)
                if self.board[end_row][end_col] == '--':
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                
                #同じ色の駒があった場合->そこを含まない、かつ、それ以上先に進まない    
                elif self.board[end_row][end_col][0] == self.board[row][col][0]:
                    break
                #違う色の駒があった場合->そこを取って終わる
                else :
                    move = (str(row) + str(col), str(end_row) + str(end_col))
                    moves.append(move)
                    break
    
    