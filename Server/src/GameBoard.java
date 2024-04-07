
/**
 * 
 * @author Jose Lorenzo Calma
 *	delete this if not needed.
 */
public class GameBoard {
    // 2D array representing the game board where the game takes place
    private int[][] arena;
    
    /**
     * Default constructor that initializes the game board with a default size of 100x100.
     */
    public GameBoard() {
        // Initialize the arena with a default size of 100x100
        arena = new int[100][100];
    }
    
    /**
     * Constructor that initializes the game board with a specified size.
     * @param size The width and height of the square game board.
     */
    public GameBoard(int size) {
        // Initialize the arena with the specified size, creating a square board
        arena = new int[size][size];
    }
}