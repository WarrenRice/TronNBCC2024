
/**
 * 
 * @author Jose Lorenzo Calma
 *	delete this if not needed.
 */
public class GameBoard {
	private int[][] arena;
	
	public GameBoard() {
		arena = new int[100][100];
	}
	
	public GameBoard(int size) {
		arena = new int[size][size];
	}
}
