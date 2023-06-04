from board import ChessBoard

def test_swap_coord_ctl() -> None:
    b = ChessBoard(board_state=None)
    assert b.swap_coord_ctl(('A', '1')) == (7, 0)
    assert b.swap_coord_ctl(('A', '8')) == (0, 0)
    assert b.swap_coord_ctl(('H', '1')) == (7, 7)
    assert b.swap_coord_ctl(('H', '8')) == (0, 7)
    assert b.swap_coord_ctl(('H', '4')) == (4, 7)
    
def test_swap_coord_ltc() -> None:
    b = ChessBoard(board_state=None)
    assert b.swap_coord_ltc((7, 0)) == ('A', '1')
    assert b.swap_coord_ltc((0, 0)) == ('A', '8')
    assert b.swap_coord_ltc((7, 7)) == ('H', '1')
    assert b.swap_coord_ltc((0, 7)) == ('H', '8')
    assert b.swap_coord_ltc((4, 7)) == ('H', '4')