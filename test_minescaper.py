#Test Cases

if __name__ == "__main__":
    # --- Task 1 ---
    board = create_mine_board(5, [(0, 2), (2, 2), (3, 4), (4, 3)])
    expected = [[0, 1, -1,  1,  0],
                [0, 2,  2,  2,  0],
                [0, 1, -1,  2,  1],
                [0, 1,  2,  3, -1],
                [0, 0,  1, -1,  2]]
    assert board == expected, f"Task 1 failed:\n{board}"
    print("Task 1 passed ✓")

    # --- Task 2 ---
    b3 = [[0]*3 for _ in range(3)]
    assert process_input(b3, (1, 1), 'Wdf') == (0, 2, True),  "T2 case 1"
    assert process_input(b3, (0, 2), 'fdW') == (0, 2, False), "T2 case 2"
    assert process_input(b3, (1, 1), 'rts') == (2, 1, False), "T2 case 3"
    assert process_input(b3, (1, 0), 'aF')  == (1, 0, False), "T2 case 4"
    assert process_input(b3, (1, 1), 'aFh657') == (1, 0, True), "T2 case 5"
    print("Task 2 passed ✓")

    # --- Task 3 ---
    board3 = [[1, -1, 1,  1, -1],
              [1,  1, 1,  1,  1],
              [0,  0, 0,  0,  0],
              [0,  0, 1,  1,  1],
              [0,  0, 1, -1,  1]]
    result = reveal_zeros(board3, {(0, 0), (1, 0)}, (2, 0))
    assert (2, 0) in result and (4, 0) in result, "Task 3 failed"
    print("Task 3 passed ✓")

    # --- Task 4 ---
    board4 = [[0, 1, -1,  1,  0],
              [1, 3,  2,  2,  0],
              [-1, 2, -1,  2,  1],
              [1, 2,  2,  3, -1],
              [0, 0,  1, -1,  2]]
    gb = create_game_board(board4, {(0, 0), (0, 1), (1, 1)},
                           (1, 0), {(2, 2)}, show_all=False)
    assert gb[1][0] == '[1]', f"Task 4 player pos wrong: {gb[1][0]}"
    assert gb[2][2] == ' F ', f"Task 4 flag wrong: {gb[2][2]}"
    assert gb[4][4] == ' E ', f"Task 4 exit wrong: {gb[4][4]}"
    print("Task 4 passed ✓")

    print("\nAll tasks passed.")
