import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GameManager {
//	public List<Player> playerList;
	public Map<Integer, Player> playerMap;
	public int gameState = 0;
	public static final String PROPERTY_DELIMETER = "▐";
	
	public GameManager() {
//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();
	}
	
	public Player addNewPlayer() throws Exception {
		if (playerMap.size() >= 4) {
			throw new Exception("Lobby is full!");
		}
		
		int id = -1;
		for (int i = 0; i < 4; i++) {
			if (!playerMap.containsKey(i)) {
				id = i;
				break;
			}
		}
		int[] playerPos = getInitialPosition(id);
		Player newPlayer = new Player(id, playerPos[0], playerPos[1]);
//		playerList.add(newPlayer);
		playerMap.put(id, newPlayer);
		return newPlayer;
	}
	
	public String getPlayerPosition(String id) {
//		return playerList.get(Integer.parseInt(id)).getPosition();
		return playerMap.get(Integer.parseInt(id)).getPosition();
	}
	
	public void reset() {
//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();
	}
	
	public int[] getInitialPosition(int playerId) throws Exception {
		switch(playerId) {
		case 0:
			return new int[] {0, 49};
		case 1:
			return new int[] {49, 99};
		case 2:
			return new int[] {49, 0};
		case 3:
			return new int[] {99, 49};
		default:
			throw new Exception("Invalid player id.");
		}
	}
	
	public String getAllPlayerPositions() {
		String positions = "";
//		for (Player p : playerMap.values()) {
//			String alive = p.getAlive() ? "A" : "D";
//			positions += alive + "," + p.getPosition() + "," + p.getLastPositions(4) + PROPERTY_DELIMETER;
//		}
		
		for (int i = 0; i < 4; i++) {
			Player p = playerMap.get(i);
			if (p == null) {
				positions += "IGNORE" + PROPERTY_DELIMETER;
			} else {
				String alive = p.getAlive() ? "A" : "D";
				positions += p.getPlayerId() +"," + alive + "," + p.getPosition() + "," + p.getLastPositions(4) + PROPERTY_DELIMETER;				
			}
		}
		
		return positions;
	}
	
	public void savePlayerPosition(int playerId, int posX, int posY) {
//		Player player = playerList.get(playerId);
		Player player = playerMap.get(playerId);
		player.setPosition(posX, posY);
	}
	
	// function for obtaining lobby status of players
	public String getPlayerLobbyStatus() {
		String playerStatus = "";
//		for (Player p : playerMap.values()) {
//			playerStatus += p.getLobbyStatus() + PROPERTY_DELIMETER;
//		}
		
		for (int i = 0; i < 4; i++) {
			Player p = playerMap.get(i);
			if (p != null) {
				playerStatus += p.getLobbyStatus() + PROPERTY_DELIMETER;
			} else {
				playerStatus += "IGNORE" + PROPERTY_DELIMETER;
			}
		}
		
		return playerStatus;
	}
	
	public void setPlayerReady(int playerId) {
		playerMap.get(playerId).setReady(true);
	}
	
	public void setPlayerDead(int playerId) {
		playerMap.get(playerId).setAlive(false);
	}
	
	public void removePlayer(int playerId) {
		playerMap.remove(playerId);
	}
}
