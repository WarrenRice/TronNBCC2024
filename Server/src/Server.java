import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
/**
 * The Server class handles network connections and communicates with clients.
 * It processes incoming requests and interacts with the GameManager to update game state.
 */
public class Server extends Thread {
	public static final String PROPERTY_DELIMETER = "▐";    // Delimiter used for parsing client messages

	private ServerSocket serverSocket;    // Server socket to listen for incoming client connections

	private GameManager gameManager;    // GameManager instance to manage game state and player interactions

  /**
  * Constructs a new Server object that listens on the specified port.
  * @param port The port number on which the server will listen.
  * @throws IOException If an I/O error occurs when opening the socket.
  */
	public Server(int port) throws IOException {
		serverSocket = new ServerSocket(port);        // Initialize the server socket to listen on the given port

		serverSocket.setSoTimeout(0);        // Set timeout to infinity (0 means no timeout)

		gameManager = new GameManager();        // Initialize the game manager

	}
	 /**
     * The main execution method for the server thread.
     * Accepts client connections and processes their requests in a loop.
     */	
	public void run() {
		while (true) {// Infinite loop to continuously accept client connections
			try {
				System.out.println("Waiting for client on port " 
						+ serverSocket.getLocalPort());
				
				Socket socket = serverSocket.accept();                // Accept a client connection
		
	            
				System.out.println("Connection from client on address: "+ socket.getRemoteSocketAddress());
                // Set up a reader to receive data from the client

				BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                // Read input from the client

				String clientInput = reader.readLine();
                // Process the client input and generate a response

				String serverOutput = handleClientInput(clientInput);
                // Output the server response for debugging/logging

				System.out.println(serverOutput);
	            
				System.out.println("=================================");
                // Set up a writer to send data to the client

	            PrintWriter writer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);
                // Send the response back to the client

	            writer.println(serverOutput);
                // Close the reader, writer, and socket

	            reader.close();
	            writer.close();
				socket.close();
			} catch (IOException e) {
				e.printStackTrace();// Print the exception stack trace

			}
		}
	}
    /**
     * Processes the input received from a client and generates an appropriate response.
     * @param clientInput The string input received from the client.
     * @return A response string based on the client input and game state.
     */
	
	private String handleClientInput(String clientInput) {
		System.out.println(clientInput);// Output the client input for debugging/logging

		
		try {
			// Handling different types of client inputs
			if (clientInput.contains("CONNECTION")) {
                // If the client wants to connect, get the username and add a new player

				String username = clientInput.split(PROPERTY_DELIMETER)[1];
				return gameManager.addNewPlayer(username).toString();
			}
			if (clientInput.equals("GET_PLAYERS")) {
                // If the client requests the list of players, return it

				return gameManager.getPlayerLobbyStatus();
			}
			if (clientInput.contains("READY")) {
                // If a player is ready, update their status

				String playerId = clientInput.split(PROPERTY_DELIMETER)[1];
				gameManager.setPlayerReady(Integer.parseInt(playerId));
				return "Player " + playerId + "is now ready.";
			}
			if (clientInput.equals("GET_POSITIONS")) {
                // If the request is for all players' positions, return them

				return gameManager.getAllPlayerPositions();
			}
			if (clientInput.contains("GET_POSITION")) {
                // If the request is for a single player's position, return it

				String playerId = clientInput.split(PROPERTY_DELIMETER)[1];
				return gameManager.getPlayerPosition(playerId);
			}
			if (clientInput.equals("RESET")) {
                // If the request is to reset the game, reset it

				gameManager.reset();
				return "Successfully reset the game server.";
			}
			if (clientInput.contains("SAVE_POSITION")) {
                // If the request is to save a player's position, save it

				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);
				int playerId = Integer.parseInt(splitInput[1]);
				int posX = Integer.parseInt(splitInput[2]);
				int posY = Integer.parseInt(splitInput[3]);
				gameManager.savePlayerPosition(playerId, posX, posY);
				return "Successully saved the position";
			}
			if (clientInput.contains("DISCONNECTED")) {
                // If a player is disconnected, remove them

				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);
				int playerId = Integer.parseInt(splitInput[1]);
				gameManager.removePlayer(playerId);
				return "Successfully removed the player";
			}	
			
			if (clientInput.contains("DIE")) {
                // If a player dies, set their status to dead

				String[] splitInput = clientInput.split(PROPERTY_DELIMETER);
				int playerId = Integer.parseInt(splitInput[1]);
				gameManager.setPlayerDead(playerId);
				return "Successfully saved player " + playerId + " to dead";
			}
            // Throw an exception if the client input doesn't match any expected commands

			throw new Exception("Invalid client input...");
		} catch (Exception e) {
			return "ERROR:" + e.toString();
		}
	}
}
