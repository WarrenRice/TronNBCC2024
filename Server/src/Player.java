import java.util.ArrayList;
import java.util.List;

public class Player {
	private int playerId;
	private int posX;
	private int posY;
	private boolean ready;
	private boolean alive;
	public static final String PROPERTY_DELIMETER = "▐";
	private List<Integer> previousPosX;
	private List<Integer> previousPosY;
	
	public Player(int playerId, int posX, int posY) {
		this.playerId = playerId;
		this.posX = posX;
		this.posY = posY;
		this.ready = false;
		this.alive = true;
		this.previousPosX = new ArrayList<>();
		this.previousPosY = new ArrayList<>();
	}
	
	public int getPlayerId() {
		return playerId;
	}
	public void setPlayerId(int playerId) {
		this.playerId = playerId;
	}

	public int getPosX() {
		return posX;
	}
	
	public int getPosY() {
		return posY;
	}
	
	public boolean getReady() {
		return this.ready;
	}
	
	public void setReady(boolean ready) {
		this.ready = ready;
	}
	
	public boolean getAlive() {
		return this.alive;
	}
	
	public void setAlive(boolean alive) {
		this.alive = alive;
	}
	
	public String getPosition() {
		return posX + "," +
				posY;
	}
	
	public String getLastPositions(int numPositions) {
		String positions = "";
		int lastIndex = previousPosX.size() - 1;
		for (int i = 0; i < numPositions; i++) {
			int currIndex = lastIndex - i;
			if (currIndex < 0) break;
			positions += previousPosX.get(currIndex) + "," + previousPosY.get(currIndex) + ",";
		}
		return positions;
	}
	
	public String toString() {
		return playerId + PROPERTY_DELIMETER + 
				getPosition();
	}
	
	public String getLobbyStatus() {
		String status = ready ? "R" : "N";
		return status + "," + getPosition();
	}
	
	public void setPosition(int posX, int posY) {
		previousPosX.add(this.posX);
		previousPosY.add(this.posY);
		this.posX = posX;
		this.posY = posY;
	}
	
}
