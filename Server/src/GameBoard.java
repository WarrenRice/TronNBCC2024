
/**
 * 
 * @author Jose Lorenzo Calma
 *	delete this if not needed.
 */
public class GameBoard {
	private int[][] arena;
	
	public GameBoard() {
		arena = new int[40][40];
	}
	
	public GameBoard(int size) {
		arena = new int[size][size];
	}
}
