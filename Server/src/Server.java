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
	public static final String PROPERTY_DELIMETER = "▐";                                                               // Delimiter used for parsing client messages
	private ServerSocket serverSocket;                                                                                 // Server socket to listen for incoming client connections
	private GameManager gameManager;                                                                                   // GameManager instance to manage game state and player interactions

	public Server(int port) throws IOException {
		serverSocket = new ServerSocket(port);                                                                         // Initialize the server socket to listen on the given port
		serverSocket.setSoTimeout(0);                                                                                  // Set timeout to infinity (0 means no timeout)
		gameManager = new GameManager();                                                                               // Initialize the game manager
	}	
	public void run() {
		while (true) {                                                                                                 // Infinite loop to continuously accept client connections
			try {
				System.out.println("Waiting for client on port " 
						+ serverSocket.getLocalPort());
				
				Socket socket = serverSocket.accept();                                                                 // Accept a client connection
		
	            
				System.out.println("Connection from client on address: "+ socket.getRemoteSocketAddress());

				BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));              // Set up a reader to receive data from the client

				String clientInput = reader.readLine();                                                                 // Read input from the client

				String serverOutput = handleClientInput(clientInput);                                                   // Process the client input and generate a response

				System.out.println(serverOutput);                                                                        // Output the server response for debugging/logging
	            
				System.out.println("=================================");

	            PrintWriter writer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);           // Set up a writer to send data to the client

	            writer.println(serverOutput);                                                                           // Send the response back to the client

                // Close the reader, writer, and socket
	            reader.close();
	            writer.close();
				socket.close();
			} catch (IOException e) {
				e.printStackTrace();                                                                                     // Print the exception stack trace

			}
		}
	}
  
	
	private String handleClientInput(String clientInput) {
		System.out.println(clientInput);                                                                                // Output the client input for debugging/logging

		
		try {
			if (clientInput.contains("CONNECTION")) {			                                                       // Handling different types of client inputs

				String username = clientInput.split(PROPERTY_DELIMETER)[1];                                            // If the client wants to connect, get the username and add a new player

				return gameManager.addNewPlayer(username).toString();
			}
			if (clientInput.equals("GET_PLAYERS")) {

				return gameManager.getPlayerLobbyStatus();                                                             // If the client requests the list of players, return it

			}
			if (clientInput.contains("READY")) {

				String playerId = clientInput.split(PROPERTY_DELIMETER)[1];                                           // If a player is ready, update their status
				gameManager.setPlayerReady(Integer.parseInt(playerId));
				return "Player " + playerId + "is now ready.";
			}
			if (clientInput.equals("GET_POSITIONS")) {
				return gameManager.getAllPlayerPositions();                                                           // If the request is for all players' positions, return them

			}
			if (clientInput.contains("GET_POSITION")) {
				
				String playerId = clientInput.split(PROPERTY_DELIMETER)[1];                                           // If the request is for a single player's position, return it
				return gameManager.getPlayerPosition(playerId);
			}
			if (clientInput.equals("RESET")) {

				gameManager.reset();                                                                                  // If the request is to reset the game, reset it
				return "Successfully reset the game server.";
			}
			if (clientInput.contains("SAVE_POSITION")) {

				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);                                            // If the request is to save a player's position, save it
				int playerId = Integer.parseInt(splitInput[1]);
				int posX = Integer.parseInt(splitInput[2]);
				int posY = Integer.parseInt(splitInput[3]);
				gameManager.savePlayerPosition(playerId, posX, posY);
				return "Successully saved the position";
			}
			if (clientInput.contains("DISCONNECTED")) {

				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);                                               // If a player is disconnected, remove them
				int playerId = Integer.parseInt(splitInput[1]);
				gameManager.removePlayer(playerId);
				return "Successfully removed the player";
			}	
			
			if (clientInput.contains("DIE")) {

				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);                                              // If a player dies, set their status to dead
				int playerId = Integer.parseInt(splitInput[1]);
				gameManager.setPlayerDead(playerId);
				return "Successfully saved player " + playerId + " to dead";
			}

			throw new Exception("Invalid client input...");                                                             // Throw an exception if the client input doesn't match any expected commands
		} catch (Exception e) {
			return "ERROR:" + e.toString();
		}
	}
}
