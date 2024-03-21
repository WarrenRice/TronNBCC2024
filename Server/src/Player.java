
public class Player {
	private int playerId;
	private int color;
	private int posX;
	private int posY;
	private boolean ready;
	private boolean alive;
	public static final String PROPERTY_DELIMETER = "▐";
	
	public Player(int playerId, int color, int posX, int posY) {
		this.playerId = playerId;
		this.color = color;
		this.posX = posX;
		this.posY = posY;
		this.ready = false;
		this.alive = true;
	}
	
	public int getPlayerId() {
		return playerId;
	}
	public void setPlayerId(int playerId) {
		this.playerId = playerId;
	}
	public int getColor() {
		return color;
	}
	public void setColor(int color) {
		this.color = color;
	}
	public int getPosX() {
		return posX;
	}
	public void setPosX(int posX) {
		this.posX = posX;
	}
	public int getPosY() {
		return posY;
	}
	public void setPosY(int posY) {
		this.posY = posY;
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
	
	public String toString() {
		return playerId + PROPERTY_DELIMETER + 
				getPosition();
	}
	
	public String getLobbyStatus() {
		String status = ready ? "R" : "N";
		return status + "," + getPosition();
	}
	
}
