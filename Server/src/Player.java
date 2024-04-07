import java.util.ArrayList;
import java.util.List;

/**
 * The Player class represents a player in the game,
 * holding data about their state, position, and other properties.
 */
public class Player {
    private int playerId;
    private int posX;
    private int posY;
    private boolean ready;
    private boolean alive;
    private String username;
    // Constant delimiter used in toString method for separating player properties
    public static final String PROPERTY_DELIMITER = "▐";
    private List<Integer> previousPosX;
    private List<Integer> previousPosY;
    
    /**
     * Constructs a new Player with the specified details.
     * @param playerId Unique identifier for the player.
     * @param username The player's chosen username.
     * @param posX The starting X position of the player.
     * @param posY The starting Y position of the player.
     */
    public Player(int playerId, String username, int posX, int posY) {
        this.playerId = playerId;
        this.username = username;
        this.posX = posX;
        this.posY = posY;
        this.ready = false;
        this.alive = true;
        this.previousPosX = new ArrayList<>();
        this.previousPosY = new ArrayList<>();
    }
    
    // Getters and setters for player properties follow

    public int getPlayerId() {
        return playerId;
    }

    public void setPlayerId(int playerId) {
        this.playerId = playerId;
    }

    public String getUsername() {
        return username;
    }

    public int getPosX() {
        return posX;
    }

    public int getPosY() {
        return posY;
    }

    public boolean getReady() {
        return ready;
    }

    public void setReady(boolean ready) {
        this.ready = ready;
    }

    public boolean getAlive() {
        return alive;
    }

    public void setAlive(boolean alive) {
        this.alive = alive;
    }

    /**
     * Returns the current position of the player as a String.
     * @return A string representing the player's current X and Y coordinates.
     */
    public String getPosition() {
        return posX + "," + posY;
    }

    /**
     * Returns a string containing the last specified number of positions
     * the player was in, as a comma-separated list.
     * @param numPositions The number of past positions to retrieve.
     * @return A string of past positions.
     */
    public String getLastPositions(int numPositions) {
        StringBuilder positions = new StringBuilder();
        int lastIndex = previousPosX.size() - 1;
        for (int i = 0; i < numPositions; i++) {
            int currIndex = lastIndex - i;
            if (currIndex < 0) break;
            positions.append(previousPosX.get(currIndex)).append(",").append(previousPosY.get(currIndex)).append(",");
        }
        return positions.toString();
    }

    @Override
    public String toString() {
        return playerId + PROPERTY_DELIMITER + getPosition();
    }

    /**
     * Returns a string representing the player's lobby status,
     * including readiness and position.
     * @return A string containing the player's lobby status.
     */
    public String getLobbyStatus() {
        String status = ready ? "R" : "N";
        return status + "," + username + "," + getPosition();
    }

    /**
     * Updates the player's position, storing the previous position.
     * @param posX The new X coordinate of the player.
     * @param posY The new Y coordinate of the player.
     */
    public void setPosition(int posX, int posY) {
        previousPosX.add(this.posX);
        previousPosY.add(this.posY);
        this.posX = posX;
        this.posY = posY;
    }
}
