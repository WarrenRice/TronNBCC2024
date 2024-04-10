import java.util.ArrayList;
import java.util.List;

public class Player {
    private int playerId;                                                                                       // Unique identifier for the player

    private int posX;                                                                                           // X coordinate of the player's position

    private int posY;                                                                                           // Y coordinate of the player's position

    private boolean ready;                                                                                     // Indicates if the player is ready in the lobby

    private boolean alive;                                                                                      // Indicates if the player is alive in the game

    private String username;                                                                                   // Player's chosen username

    public static final String PROPERTY_DELIMITER = "▐";                                                       // Constant delimiter used in toString method for separating player properties

    private List<Integer> previousPosX;                                                                        // List to store previous X positions of the player

    private List<Integer> previousPosY;                                                                       // List to store previous Y positions of the player

    
  
    public Player(int playerId, String username, int posX, int posY) {
        this.playerId = playerId;                                                                           // Initialize player ID
        this.username = username;                                                                           // Initialize username
        this.posX = posX;                                                                                   // Initialize starting X position
        this.posY = posY;                                                                                   // Initialize starting Y position
        this.ready = false;                                                                                 // Set initial ready state to false
        this.alive = true;                                                                                  // Set initial alive state to true
        this.previousPosX = new ArrayList<>();                                                              // Initialize list for tracking previous X positions
        this.previousPosY = new ArrayList<>();                                                              // Initialize list for tracking previous Y positions

    }
    

    public int getPlayerId() {
        return playerId;                                                                                   // Return player ID

    }

    public void setPlayerId(int playerId) {
        this.playerId = playerId;                                                                          // Set player ID

    }

    public String getUsername() {
        return username;                                                                                   // Return username

    }

    public int getPosX() {
        return posX;                                                                                       // Return current X position

    }

    public int getPosY() {
        return posY;                                                                                      // Return current Y position

    }

    public boolean getReady() {
        return ready;                                                                                     // Return readiness status

    }

    public void setReady(boolean ready) {
        this.ready = ready;                                                                              // Set readiness status

    }

    public boolean getAlive() {
        return alive;                                                                                    // Return alive status

    }

    public void setAlive(boolean alive) {
        this.alive = alive;                                                                              // Set alive status

    }

  
    public String getPosition() {
        return posX + "," + posY;                                                                      // Return a string combining X and Y positions

    }


    public String getLastPositions(int numPositions) {
        StringBuilder positions = new StringBuilder();

        int lastIndex = previousPosX.size() - 1;                                                                                  // Start from the last position recorded

        for (int i = 0; i < numPositions; i++) {
            int currIndex = lastIndex - i;
            if (currIndex < 0) break;                                                                                              // Break the loop if no more positions are available
            positions.append(previousPosX.get(currIndex)).append(",").append(previousPosY.get(currIndex)).append(",");            // Append the position to the string builder
        }
        return positions.toString();                                                                                              // Return the string of past positions
    }

    public String toString() {
        return playerId + PROPERTY_DELIMITER + getPosition();                                                                     // Return a string representation of the player using the PROPERTY_DELIMITER

    }
   public String getLobbyStatus() {
        String status = ready ? "R" : "N";                                                                                       // Return a string indicating if the player is ready along with their username and position

        return status + "," + username + "," + getPosition();
    }
    public void setPosition(int posX, int posY) {                                                                                // Record the current position as previous before updating

        previousPosX.add(this.posX);
        previousPosY.add(this.posY);
                                                                                                                                 // Update the player's current position
        this.posX = posX;
        this.posY = posY;
    }
}
