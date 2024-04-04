import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Server extends Thread {
	public static final String PROPERTY_DELIMETER = "▐";
	private ServerSocket serverSocket;
	private GameManager gameManager;
	
	public Server(int port) throws IOException {
		serverSocket = new ServerSocket(port);
		serverSocket.setSoTimeout(0);
		gameManager = new GameManager();
	}
	
	public void run() {
		while (true) {
			try {
				System.out.println("Waiting for client on port " 
						+ serverSocket.getLocalPort());
				
				Socket socket = serverSocket.accept();		
	            
				System.out.println("Connection from client on address: "+ socket.getRemoteSocketAddress());
	            
				BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	           
				String clientInput = reader.readLine();
	            
				String serverOutput = handleClientInput(clientInput);
	            
				System.out.println(serverOutput);
	            
				System.out.println("=================================");
	            
	            PrintWriter writer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);
	            writer.println(serverOutput);
	            reader.close();
	            writer.close();
				socket.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	private String handleClientInput(String clientInput) {
		System.out.println(clientInput);
		
		try {
			if (clientInput.equals("CONNECTION")) {
				return gameManager.addNewPlayer().toString();
			}
			if (clientInput.equals("GET_PLAYERS")) {
				return gameManager.getPlayerLobbyStatus();
			}
			if (clientInput.contains("READY")) {
				String playerId = clientInput.split(PROPERTY_DELIMETER)[1];
				gameManager.setPlayerReady(Integer.parseInt(playerId));
				return "Player " + playerId + "is now ready.";
			}
			if (clientInput.equals("GET_POSITIONS")) {
				return gameManager.getAllPlayerPositions();
			}
			if (clientInput.contains("GET_POSITION")) {
				String playerId = clientInput.split(PROPERTY_DELIMETER)[1];
				return gameManager.getPlayerPosition(playerId);
			}
			if (clientInput.equals("RESET")) {
				gameManager.reset();
				return "Successfully reset the game server.";
			}
			if (clientInput.contains("SAVE_POSITION")) {
				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);
				int playerId = Integer.parseInt(splitInput[1]);
				int posX = Integer.parseInt(splitInput[2]);
				int posY = Integer.parseInt(splitInput[3]);
				gameManager.savePlayerPosition(playerId, posX, posY);
				return "Successully saved the position";
			}
			if (clientInput.contains("DISCONNECTED")) {
				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);
				int playerId = Integer.parseInt(splitInput[1]);
				gameManager.removePlayer(playerId);
				return "Successfully removed the player";
			}	
			
			if (clientInput.contains("DIE")) {
				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);
				int playerId = Integer.parseInt(splitInput[1]);
				gameManager.setPlayerDead(playerId);
				return "Successfully saved player " + playerId + " to dead";
			}
			throw new Exception("Invalid client input...");
		} catch (Exception e) {
			return "ERROR:" + e.toString();
		}
	}
}
