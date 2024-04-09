import java.util.ArrayList;
import java.util.List;

/**
 * The Player class represents a player in the game,
 * holding data about their state, position, and other properties.
 */
public class Player {
    private int playerId;    // Unique identifier for the player

    private int posX;    // X coordinate of the player's position

    private int posY;    // Y coordinate of the player's position

    private boolean ready;    // Indicates if the player is ready in the lobby

    private boolean alive;    // Indicates if the player is alive in the game

    private String username;    // Player's chosen username

    // Constant delimiter used in toString method for separating player properties
    public static final String PROPERTY_DELIMITER = "▐";
    private List<Integer> previousPosX;    // List to store previous X positions of the player

    private List<Integer> previousPosY;    // List to store previous Y positions of the player

    
    /**
     * Constructs a new Player with the specified details.
     * @param playerId Unique identifier for the player.
     * @param username The player's chosen username.
     * @param posX The starting X position of the player.
     * @param posY The starting Y position of the player.
     */
    public Player(int playerId, String username, int posX, int posY) {
        this.playerId = playerId;        // Initialize player ID

        this.username = username;        // Initialize username

        this.posX = posX;        // Initialize starting X position

        this.posY = posY;        // Initialize starting Y position

        this.ready = false;        // Set initial ready state to false

        this.alive = true;        // Set initial alive state to true

        this.previousPosX = new ArrayList<>();        // Initialize list for tracking previous X positions

        this.previousPosY = new ArrayList<>();        // Initialize list for tracking previous Y positions

    }
    
    // Getters and setters for player properties follow

    public int getPlayerId() {
        return playerId;        // Return player ID

    }

    public void setPlayerId(int playerId) {
        this.playerId = playerId;        // Set player ID

    }

    public String getUsername() {
        return username;        // Return username

    }

    public int getPosX() {
        return posX;        // Return current X position

    }

    public int getPosY() {
        return posY;        // Return current Y position

    }

    public boolean getReady() {
        return ready;        // Return readiness status

    }

    public void setReady(boolean ready) {
        this.ready = ready;        // Set readiness status

    }

    public boolean getAlive() {
        return alive;        // Return alive status

    }

    public void setAlive(boolean alive) {
        this.alive = alive;        // Set alive status

    }

    /**
     * Returns the current position of the player as a String.
     * @return A string representing the player's current X and Y coordinates.
     */
    public String getPosition() {
        return posX + "," + posY;        // Return a string combining X and Y positions

    }

    /**
     * Returns a string containing the last specified number of positions
     * the player was in, as a comma-separated list.
     * @param numPositions The number of past positions to retrieve.
     * @return A string of past positions.
     */
    public String getLastPositions(int numPositions) {
        StringBuilder positions = new StringBuilder();
        // Start from the last position recorded

        int lastIndex = previousPosX.size() - 1;
        for (int i = 0; i < numPositions; i++) {
            int currIndex = lastIndex - i;
            if (currIndex < 0) break;            // Break the loop if no more positions are available
            // Append the position to the string builder

            positions.append(previousPosX.get(currIndex)).append(",").append(previousPosY.get(currIndex)).append(",");
        }
        return positions.toString();        // Return the string of past positions

    }

    @Override
    public String toString() {
        return playerId + PROPERTY_DELIMITER + getPosition();        // Return a string representation of the player using the PROPERTY_DELIMITER

    }

    /**
     * Returns a string representing the player's lobby status,
     * including readiness and position.
     * @return A string containing the player's lobby status.
     */
    public String getLobbyStatus() {
        String status = ready ? "R" : "N";        // Return a string indicating if the player is ready along with their username and position

        return status + "," + username + "," + getPosition();
    }

    /**
     * Updates the player's position, storing the previous position.
     * @param posX The new X coordinate of the player.
     * @param posY The new Y coordinate of the player.
     */
    public void setPosition(int posX, int posY) {
        // Record the current position as previous before updating

        previousPosX.add(this.posX);
        previousPosY.add(this.posY);
        // Update the player's current position

        this.posX = posX;
        this.posY = posY;
    }
}
