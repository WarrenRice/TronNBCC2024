import java.util.ArrayList;
import java.util.List;

public class GameManager {
	public int playerCount = 0;
	public List<Player> playerList;
	public int gameState = 0;
	public static final String PROPERTY_DELIMETER = "▐";
	
	public GameManager() {
		playerList = new ArrayList<>();
	}
	
	public Player addNewPlayer() throws Exception {
		int[] playerPos = getInitialPosition(playerCount);
		Player newPlayer = new Player(playerCount, playerCount, playerPos[0], playerPos[1]);
		playerList.add(newPlayer);
		playerCount++;
		return newPlayer;
	}
	
	public String getPlayerPosition(String id) {
		return playerList.get(Integer.parseInt(id)).getPosition();
	}
	
	public void reset() {
		playerCount = 0;
		playerList = new ArrayList<>();
	}
	
	public int[] getInitialPosition(int playerId) throws Exception {
		switch(playerId) {
		case 0:
			return new int[] {0, 0};
		case 1:
			return new int[] {0, 39};
		case 2:
			return new int[] {39, 0};
		case 3:
			return new int[] {39, 39};
		default:
			throw new Exception("Invalid player id.");
		}
	}
	
	public String getAllPlayerPositions() {
		String positions = "";
		for (Player p : playerList) {
			String alive = p.getAlive() ? "A" : "D";
			positions += alive + "," + p.getPosition() + "," + p.getLastPositions(4) + PROPERTY_DELIMETER;
		}
		return positions;
	}
	
	public void savePlayerPosition(int playerId, int posX, int posY) {
		Player player = playerList.get(playerId);
		player.setPosition(posX, posY);
	}
	
	// function for obtaining lobby status of players
	public String getPlayerLobbyStatus() {
		String playerStatus = "";
		for (Player p : playerList) {
			playerStatus += p.getLobbyStatus() + PROPERTY_DELIMETER;
		}
		
		return playerStatus;
	}
	
	public void setPlayerReady(int playerId) {
		playerList.get(playerId).setReady(true);
	}
	
	public void setPlayerDead(int playerId) {
		playerList.get(playerId).setAlive(false);
	}
	
	public static void main(String[] args) throws Exception {
		GameManager gm = new GameManager();
		gm.addNewPlayer();
		for (int i = 0; i <= 10; i++) {
			gm.savePlayerPosition(0, i, i);
		}
		gm.addNewPlayer();
		for (int i = 0; i <= 10; i++) {
			gm.savePlayerPosition(1, i, i);
		}
		gm.addNewPlayer();
		for (int i = 0; i <= 10; i++) {
			gm.savePlayerPosition(2, i, i);
		}
		gm.addNewPlayer();
		for (int i = 0; i <= 10; i++) {
			gm.savePlayerPosition(3, i, i);
		}
		System.out.println(gm.getAllPlayerPositions());
	}
}
