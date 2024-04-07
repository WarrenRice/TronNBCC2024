import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
/**
 * The GameManager class manages the state and actions of players in the game.
 * It maintains a map of players, their status, and facilitates game state management.
 */
public class GameManager {
//	public List<Player> playerList;
	public Map<Integer, Player> playerMap;
	public int gameState = 0;
	public static final String PROPERTY_DELIMETER = "▐";
	 /**
     * Constructor for GameManager initializes a new player map.
     */	
	public GameManager() {
//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();
	}
    /**
     * Adds a new player to the game if there is room.
     * @param username The username for the new player.
     * @return The new player object.
     * @throws Exception if the lobby is full.
     */
	public Player addNewPlayer(String username) throws Exception {
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
		Player newPlayer = new Player(id, username, playerPos[0], playerPos[1]);
//		playerList.add(newPlayer);
		playerMap.put(id, newPlayer);
		return newPlayer;
	}
    /**
     * Gets the position of a player based on their ID.
     * @param id The ID of the player.
     * @return The position of the player as a string.
     */
	public String getPlayerPosition(String id) {
//		return playerList.get(Integer.parseInt(id)).getPosition();
		return playerMap.get(Integer.parseInt(id)).getPosition();
	}
	  /**
     * Resets the game manager, clearing all player data.
     */
	public void reset() {
//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();
	}
	   /**
     * Determines the initial position for a player based on their ID.
     * @param playerId The player's ID.
     * @return An array of two integers representing the player's initial position.
     * @throws Exception if the player ID is invalid.
     */
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
	   /**
     * Compiles and returns the positions of all players.
     * @return A string of player positions and states, delimited by the PROPERTY_DELIMITER.
     */
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
	  /**
     * Saves the new position of a player.
     * @param playerId The ID of the player whose position is to be updated.
     * @param posX The new X coordinate of the player.
     * @param posY The new Y coordinate of the player.
     */	
	public void savePlayerPosition(int playerId, int posX, int posY) {
//		Player player = playerList.get(playerId);
		Player player = playerMap.get(playerId);
		player.setPosition(posX, posY);
	}
	
	// function for obtaining lobby status of players
	 /**
     * Returns the lobby status of all players.
     * @return A string representing the lobby status of all players.
     */
	public String getPlayerLobbyStatus() {
		String playerStatus = "";
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
	  /**
     * Sets a player as ready in the lobby.
     * @param playerId The ID of the player to set as ready.
     */
	public void setPlayerReady(int playerId) {
		playerMap.get(playerId).setReady(true);
	}
	  /**
     * Sets a player's status to dead.
     * @param playerId The ID of the player to set as dead.
     */
	public void setPlayerDead(int playerId) {
		playerMap.get(playerId).setAlive(false);
	}
    /**
     * Removes a player from the game manager.
     * @param playerId The ID of the player to remove.
     */

	public void removePlayer(int playerId) {
		playerMap.remove(playerId);
	}
}
