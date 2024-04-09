import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GameManager {
	public Map<Integer, Player> playerMap;                                                                // Map to store player objects with their ID as the key

	public int gameState = 0;                                                                             // Integer to track the game state

	public static final String PROPERTY_DELIMETER = "▐";                                                  // Constant string used as a delimiter in property strings

	 
	public GameManager() {                                                                                //Constructor for GameManager initializes a new player map.

		playerMap = new HashMap<>();                                                                     // Initialize the playerMap as a new HashMap

	}
    

	public Player addNewPlayer(String username) throws Exception {                                       // Adds a new player to the game if there is room with player id and position
		if (playerMap.size() >= 4) {                                                                     // Check if the playerMap has less than 4 players

			throw new Exception("Lobby is full!");
		}                                                                                                // Throw an exception if the lobby is full
		
		int id = -1;
                                                                                                         // Loop through possible player IDs (0-3) to find an unused one

		for (int i = 0; i < 4; i++) {
			if (!playerMap.containsKey(i)) {
				id = i;
				break;
			}
		}
                                                                                                           // Get the initial position for the new player based on their ID

		int[] playerPos = getInitialPosition(id);                                                         // Create a new Player object

		Player newPlayer = new Player(id, username, playerPos[0], playerPos[1]);
		playerMap.put(id, newPlayer);                                                                    // Add the new player to the playerMap

		return newPlayer;                                                                                 // Return the new player object

	}
      
	public String getPlayerPosition(String id) {                                                           // Gets the position of a player based on their ID.

//		return playerList.get(Integer.parseInt(id)).getPosition();
		return playerMap.get(Integer.parseInt(id)).getPosition();                                          // Retrieve and return the position of the player with the given ID

	}
	  
	public void reset() {                                                                                  // Resets the game manager, clearing all player data.

//		playerList = new ArrayList<>();
		playerMap = new HashMap<>();                                                                      // Clear all entries in the playerMap

	}

	public int[] getInitialPosition(int playerId) throws Exception {                                        //Determines the initial position for a player based on their ID.

		switch(playerId) {
		case 0:
			return new int[] {0, 49};                                                                        // Return position for player ID 0
		case 1:
			return new int[] {49, 99};                                                                       // Return position for player ID 1
		case 2:
			return new int[] {49, 0};                                                                        // Return position for player ID 2
		case 3:
			return new int[] {99, 49};                                                                       // Return position for player ID 3
		default:
			throw new Exception("Invalid player id.");                                                       // Throw exception for invalid player ID
		}
	}
   
	public String getAllPlayerPositions() {                                                                 //Compiles and returns the positions of all players.
		String positions = "";
//		for (Player p : playerMap.values()) {
//			String alive = p.getAlive() ? "A" : "D";
//			positions += alive + "," + p.getPosition() + "," + p.getLastPositions(4) + PROPERTY_DELIMETER;
//		}

		for (int i = 0; i < 4; i++) {                                                                      // Iterate through all possible player IDs

			Player p = playerMap.get(i);
			if (p == null) {

				positions += "IGNORE" + PROPERTY_DELIMETER;                                                // Add "IGNORE" for empty player slots

			} else {
                                                                                                          // Concatenate player information (ID, alive status, position, last positions)

				String alive = p.getAlive() ? "A" : "D";
				positions += p.getPlayerId() +"," + alive + "," + p.getPosition() + "," + p.getLastPositions(4) + PROPERTY_DELIMETER;				
			}
		}

		return positions;                                                                                  // Return the concatenated string of player positions and states

	}
	  
    	
	public void savePlayerPosition(int playerId, int posX, int posY) {                                       //Saves the new position of a player ID , Pos X and Y.

//		Player player = playerList.get(playerId);
        
		Player player = playerMap.get(playerId);                                                          // Retrieve the player object and update its position

		player.setPosition(posX, posY);
	}
	
	 
	public String getPlayerLobbyStatus() {	                                                             // function for obtaining lobby status of players

		String playerStatus = "";

		for (int i = 0; i < 4; i++) {                                                                     // Iterate through all possible player IDs

			Player p = playerMap.get(i);
			if (p != null) {

				playerStatus += p.getLobbyStatus() + PROPERTY_DELIMETER;                                 // Concatenate the lobby status of each player

			} else {

				playerStatus += "IGNORE" + PROPERTY_DELIMETER;                                           // Add "IGNORE" for empty player slots

			}
		}

		return playerStatus;                                                                             // Return the concatenated lobby status string

	}
	
	public void setPlayerReady(int playerId) {

		playerMap.get(playerId).setReady(true);                                                          // Set the specified player's ready status to true

	}
	  
	public void setPlayerDead(int playerId) {

		playerMap.get(playerId).setAlive(false);                                                        // Set the specified player's alive status to false

	}
    

	public void removePlayer(int playerId) {

		playerMap.remove(playerId);                                                                   // Remove the player with the specified ID from the playerMap

	}
}
