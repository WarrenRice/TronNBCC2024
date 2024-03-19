
public class Player {
	private int playerId;
	private int color;
	private int posX;
	private int posY;
	private boolean alive;
	public static final String PROPERTY_DELIMETER = "▐";
	
	public Player(int playerId, int color, int posX, int posY) {
		this.playerId = playerId;
		this.color = color;
		this.posX = posX;
		this.posY = posY;
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
	
	public String getPosition() {
		return posX + PROPERTY_DELIMETER +
				posY + PROPERTY_DELIMETER;
	}
	
	public String toString() {
		return playerId + PROPERTY_DELIMETER + 
				color + PROPERTY_DELIMETER + 
				posX + PROPERTY_DELIMETER +
				posY + PROPERTY_DELIMETER +
				alive;
	}
	
}
