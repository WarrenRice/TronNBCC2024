import java.io.IOException;

public class Main {
	// Constant for the port number
	final static int PORT = 6066;
	
	// Main method
	public static void main(String[] args) {
		try {
			// Create a new thread for the server
			Thread t = new Server(PORT);
			// Start the server thread
			t.start();
		} catch (IOException e) {
			// Print the stack trace if an IOException occurs
			e.printStackTrace();
		}
	}
}
