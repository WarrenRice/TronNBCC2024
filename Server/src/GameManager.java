import java.util.ArrayList;
import java.util.List;

public class GameManager {
	public int playerCount = 0;
	public List<Player> playerList;
	// game state 0 is waiting
	// game state 1 is playing
	public int gameState = 0;
	
	public GameManager() {
		playerList = new ArrayList<>();
	}
	
	public Player addNewPlayer() {
		playerCount++;
		// todo determine player position based on player count
		Player newPlayer = new Player(playerCount, playerCount, 0, 0);
		playerList.add(newPlayer);
		return newPlayer;
	}
	
	public String getPlayerPosition(String id) {
		return playerList.get(Integer.parseInt(id)).getPosition();
	}
	
	public void reset() {
		playerCount = 0;
		playerList = new ArrayList<>();
	}
}
