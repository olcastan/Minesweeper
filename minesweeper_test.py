import unittest
from src.Minesweeper import (Minesweeper, CellStatus, GameStatus)


class MineSweeperTest(unittest.TestCase):
  def setUp(self):
    self.minesweeper = Minesweeper()

  def test_canary(self):
    self.assertTrue(True)

  def test_user_exposes_unexposed_cell(self):
    self.minesweeper.expose_cell(1, 2)

    self.assertEqual(CellStatus.EXPOSED, self.minesweeper.get_cell_state(1, 2))

  def test_user_exposes_exposed_cell(self):
    self.minesweeper.expose_cell(1, 2)
    self.minesweeper.expose_cell(1, 2)

    self.assertEqual(CellStatus.EXPOSED,
    self.minesweeper.get_cell_state(1, 2))

  def test_user_exposes_cell_above_column_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose_cell(0, 11)

  def test_user_exposes_cell_below_column_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose_cell(0, -1)

  def test_user_exposes_cell_above_row_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose_cell(11, 0)

  def test_user_exposes_cell_below_row_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.expose_cell(-1, 0)

  def test_user_seals_unexposed_cell(self):
    self.minesweeper.toggle_seal(1, 3)

    self.assertEqual(CellStatus.SEALED,
    self.minesweeper.get_cell_state(1, 3))

  def test_user_unseals_sealed_cell(self):
    self.minesweeper.toggle_seal(7, 7)
    self.minesweeper.toggle_seal(7, 7)

    self.assertEqual(CellStatus.UNEXPOSED, self.minesweeper.get_cell_state(7, 7))

  def test_user_seals_cell_above_column_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(0, 12)

  def test_user_seals_cell_below_column_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(0, -1)

  def test_user_seals_cell_above_row_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(12, 0)

  def test_user_seals_cell_below_row_bounds(self):
    with self.assertRaises(IndexError):
      self.minesweeper.toggle_seal(-1, 0)

  def test_user_seals_exposed_cell(self):
    self.minesweeper.expose_cell(0, 2)
    self.minesweeper.toggle_seal(0, 2)

    self.assertEqual(CellStatus.EXPOSED, self.minesweeper.get_cell_state(0, 2))

  def test_user_exposes_sealed_cell(self):
    self.minesweeper.toggle_seal(0, 1)
    self.minesweeper.expose_cell(0, 1)

    self.assertEqual(CellStatus.SEALED, self.minesweeper.get_cell_state(0, 1))

  def test_expose_calls_expose_neighbors(self):
    class MineSweeperStub(Minesweeper):
      def expose_neighbors(self, row, col):
        self.flag = True

    minesweeper = MineSweeperStub()
    minesweeper.expose_cell(5, 5)

    self.assertEqual(True, minesweeper.flag)

  def test_expose_call_on_sealed_cell_doesnt_call_expose_neighbors(self):
    class MinesweeperStub(Minesweeper):
      flag = False

      def expose_neighbors(self, row, col):
        self.flag = True

    minesweeper = MinesweeperStub()
    minesweeper.toggle_seal(4, 4)
    minesweeper.expose_cell(4, 4)

    self.assertEqual(False, minesweeper.flag)


  def test_expose_neighbor_call_on_top_left_cell_only_exposes_existing_cells_which_is_3_cell(self):
    class MinesweeperStub(Minesweeper):
      count = 0

      def expose_neighbors(self, i, j):

        self.flag = True
        neighbors = [[i, j+1], [i+1, j], [i+1, j+1], [i, j-1], [i+1, j-1], [i-1, j], [i-1, j+1], [i-1, j-1]]
        for cell in neighbors:
          if 0 <= cell[0] <= 10 - 1 and 0 <= cell[1] <= 10 - 1:
            self.count += 1

    minesweeper = MinesweeperStub()
    minesweeper.expose_cell(0, 0)

    self.assertEqual(3, minesweeper.count)

  def test_expose_neighbor_call_on_bottom_left_cell_only_exposes_existing_cells_which_is_3_cells(self):
    class MinesweeperStub(Minesweeper):
      count = 0

      def expose_neighbors(self, i, j):
        self.flag = True
        neighbors = [[i, j+1], [i+1, j], [i+1, j+1], [i, j-1], [i+1, j-1], [i-1, j], [i-1, j+1], [i-1, j-1]]
        for cell in neighbors:
          if 0 <= cell[0] <= 10 - 1 and 0 <= cell[1] <= 10 - 1:
            self.count += 1


    minesweeper = MinesweeperStub()
    minesweeper.expose_cell(9, 9)

    self.assertEqual(3, minesweeper.count)


  def test_checks_if_cell_is_not_a_mine(self):

    self.assertEqual(False, self.minesweeper.is_mine_at(3, 3))

  def test_set_cell_to_mine_and_check_if_cell_is_a_mine(self):
    self.minesweeper.set_mine(3, 2)

    self.assertEqual(True, self.minesweeper.is_mine_at(3, 2))

  def test_assign_mine_to_cell_then_seal_said_cell_also_verify_said_cell_is_mined_AND_sealed(self):

    self.minesweeper.set_mine(3, 2)
    self.minesweeper.toggle_seal(3, 2)

    self.assertEqual(True, self.minesweeper.is_mine_at(3, 2))
    self.assertEqual(CellStatus.SEALED, self.minesweeper.get_cell_state(3, 2))

  def test_is_mine_at_call_below_row_bounds(self):

    self.assertEqual(False, self.minesweeper.is_mine_at(-1, 4))

  def test_is_mine_at_call_above_row_bounds(self):

    self.assertEqual(False, self.minesweeper.is_mine_at(10, 5))

  def test_is_mine_at_call_below_column_bounds(self):

    self.assertEqual(False, self.minesweeper.is_mine_at(5, -1))

  def test_is_mine_at_call_above_column_bounds(self):

    self.assertEqual(False, self.minesweeper.is_mine_at(7, 10))

  def test_set_mine_at_5_6_then_verify_5_5_is_adjancent_cell_with_one_mine(self):
    self.minesweeper.set_mine(5, 6)

    self.assertEqual(1, self.minesweeper.adjacent_mine_count_at(5, 5))

  def test_cell_4_6_has_adjacent_count_of_0_because_no_set_mine_call_was_performed_on_neighboring_cell(self):

    self.assertEqual(0, self.minesweeper.adjacent_mine_count_at(4, 6))

  def test_cell_3_4_has_adjacent_count_of_0_as_no_neighbors_are_mines(self):
    self.minesweeper.set_mine(3,4)

    self.assertEqual(0, self.minesweeper.adjacent_mine_count_at(3, 4))

  def test_set_mine_at_3_4_verify_3_5_has_adjacent_count_1(self):
    self.minesweeper.set_mine(3,4)

    self.assertEqual(1, self.minesweeper.adjacent_mine_count_at(3, 5))

  def test_set_mine_at_3_4_and_2_6_verify_3_5_has_adjacent_count_2(self):
    self.minesweeper.set_mine(3, 4)
    self.minesweeper.set_mine(2, 6)

    self.assertEqual(2, self.minesweeper.adjacent_mine_count_at(3, 5))

  def test_set_mine_at_0_1_verify_0_0_has_adjacent_count_1(self):
    self.minesweeper.set_mine(0, 1)

    self.assertEqual(1, self.minesweeper.adjacent_mine_count_at(0, 0))

  def test_verify_0_9_adjacent_call_returns_0(self):

    self.assertEqual(0, self.minesweeper.adjacent_mine_count_at(0, 9))

  def test_verify_9_0_adjacent_call_returns_0(self):

    self.assertEqual(0, self.minesweeper.adjacent_mine_count_at(9, 0))

  def test_set_mine_9_8_get_adjacent_count_for_9_9_returns_1(self):
    self.minesweeper.set_mine(9, 8)

    self.assertEqual(1, self.minesweeper.adjacent_mine_count_at(9, 9))

  def test_exposing_adjacent_cell_doesnt_expose_neighbors(self):
    self.minesweeper.set_mine(5, 6)
    self.minesweeper.expose_cell(5, 5)

    self.assertEqual(False, self.minesweeper.flag)

  def test_expose_mined_cell_get_game_status_returns_LOST(self):
    self.minesweeper.set_mine(7,8)
    self.minesweeper.set_mine(7,9)

    self.minesweeper.expose_cell(7,9)

    self.assertEqual(GameStatus.LOST, self.minesweeper.get_game_status())

  def test_get_game_status_return_INPROGRESS(self):

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_some_cells_are_UNEXPOSED_though_all_mines_are_SEALED(self):
    self.minesweeper.set_mine(4,5)
    self.minesweeper.set_mine(5,5)

    self.minesweeper.toggle_seal(4,5)
    self.minesweeper.toggle_seal(5,5)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_game_INPROGRESS_after_empty_cell_is_SEALED(self):
    self.minesweeper.set_mine(4,5)
    self.minesweeper.set_mine(5,5)

    self.minesweeper.toggle_seal(4,5)
    self.minesweeper.toggle_seal(5,5)
    self.minesweeper.toggle_seal(5,6)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_game_INPROGRESS_after_adjacent_cell_is_UNEXPOSED_but_mines_are_SEALED(self):
    self.minesweeper.set_mine(4,5)
    self.minesweeper.set_mine(5,5)

    self.minesweeper.toggle_seal(4,5)
    self.minesweeper.toggle_seal(5,5)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_game_INPROGRESS_after_all_non_mines_exposed_but_one_mined_not_SEALED(self):
    self.minesweeper.set_mine(4,5)
    self.minesweeper.set_mine(5,5)

    self.minesweeper.toggle_seal(4,5)


    self.minesweeper.expose_cell(0,0)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_game_WON_after_mines_are_SEALED_and_cells_EXPOSED(self):
    self.minesweeper.set_mine(4,5)
    self.minesweeper.set_mine(5,5)

    self.minesweeper.toggle_seal(4,5)
    self.minesweeper.toggle_seal(5,5)

    self.minesweeper.expose_cell(0,0)

    self.assertEqual(GameStatus.WON, self.minesweeper.get_game_status())

  def test_call_set_ten_mines_and_verify_there_are_10_mines_with_seed_0(self):
    self.minesweeper.randomize(1)

    self.assertEqual(10, len(self.minesweeper.minedCell))

if __name__ == '__main__':
    unittest.main()
