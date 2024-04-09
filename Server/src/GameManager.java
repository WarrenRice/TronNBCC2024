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
	public Map<Integer, Player> playerMap;    // Map to store player objects with their ID as the key

	public int gameState = 0;    // Integer to track the game state

	public static final String PROPERTY_DELIMETER = "▐";    // Constant string used as a delimiter in property strings

	 /**
     * Constructor for GameManager initializes a new player map.
     */	
	public GameManager() {
//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();        // Initialize the playerMap as a new HashMap

	}
    /**
     * Adds a new player to the game if there is room.
     * @param username The username for the new player.
     * @return The new player object.
     * @throws Exception if the lobby is full.
     */
	public Player addNewPlayer(String username) throws Exception {
		if (playerMap.size() >= 4) {        // Check if the playerMap has less than 4 players

			throw new Exception("Lobby is full!");
		}// Throw an exception if the lobby is full
		
		int id = -1;
        // Loop through possible player IDs (0-3) to find an unused one

		for (int i = 0; i < 4; i++) {
			if (!playerMap.containsKey(i)) {
				id = i;
				break;
			}
		}
        // Get the initial position for the new player based on their ID

		int[] playerPos = getInitialPosition(id);        // Create a new Player object

		Player newPlayer = new Player(id, username, playerPos[0], playerPos[1]);
//		playerList.add(newPlayer);
		playerMap.put(id, newPlayer);        // Add the new player to the playerMap

		return newPlayer;        // Return the new player object

	}
    /**
     * Gets the position of a player based on their ID.
     * @param id The ID of the player.
     * @return The position of the player as a string.
     */
	public String getPlayerPosition(String id) {
//		return playerList.get(Integer.parseInt(id)).getPosition();
		return playerMap.get(Integer.parseInt(id)).getPosition();        // Retrieve and return the position of the player with the given ID

	}
	  /**
     * Resets the game manager, clearing all player data.
     */
	public void reset() {
//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();        // Clear all entries in the playerMap

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
			return new int[] {0, 49};// Return position for player ID 0
		case 1:
			return new int[] {49, 99};// Return position for player ID 1
		case 2:
			return new int[] {49, 0};// Return position for player ID 2
		case 3:
			return new int[] {99, 49};// Return position for player ID 3
		default:
			throw new Exception("Invalid player id."); // Throw exception for invalid player ID
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
        // Iterate through all possible player IDs

		for (int i = 0; i < 4; i++) {
			Player p = playerMap.get(i);
			if (p == null) {
                // Add "IGNORE" for empty player slots

				positions += "IGNORE" + PROPERTY_DELIMETER;
			} else {
                // Concatenate player information (ID, alive status, position, last positions)

				String alive = p.getAlive() ? "A" : "D";
				positions += p.getPlayerId() +"," + alive + "," + p.getPosition() + "," + p.getLastPositions(4) + PROPERTY_DELIMETER;				
			}
		}
        // Return the concatenated string of player positions and states

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
        // Retrieve the player object and update its position

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
        // Iterate through all possible player IDs

		for (int i = 0; i < 4; i++) {
			Player p = playerMap.get(i);
			if (p != null) {
                // Concatenate the lobby status of each player

				playerStatus += p.getLobbyStatus() + PROPERTY_DELIMETER;
			} else {
                // Add "IGNORE" for empty player slots

				playerStatus += "IGNORE" + PROPERTY_DELIMETER;
			}
		}
        // Return the concatenated lobby status string

		return playerStatus;
	}
	  /**
     * Sets a player as ready in the lobby.
     * @param playerId The ID of the player to set as ready.
     */
	public void setPlayerReady(int playerId) {
        // Set the specified player's ready status to true

		playerMap.get(playerId).setReady(true);
	}
	  /**
     * Sets a player's status to dead.
     * @param playerId The ID of the player to set as dead.
     */
	public void setPlayerDead(int playerId) {
        // Set the specified player's alive status to false

		playerMap.get(playerId).setAlive(false);
	}
    /**
     * Removes a player from the game manager.
     * @param playerId The ID of the player to remove.
     */

	public void removePlayer(int playerId) {
        // Remove the player with the specified ID from the playerMap

		playerMap.remove(playerId);
	}
}
