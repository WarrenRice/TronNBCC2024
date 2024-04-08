import java.io.IOException;

/**
 * The Main class contains the entry point for a server application.
 * It initializes a server on a specified port and handles exceptions that may occur during its operation.
 */
public class Main {
    // Constant for the port number on which the server will listen
    final static int PORT = 6066;
    
    /**
     * The main method serves as the entry point of the application.
     * @param args Command line arguments (not used in this application).
     */
    public static void main(String[] args) {
        try {
            // Initialize a new server thread on the specified port
            Thread t = new Server(PORT);
            
            // Start the server thread, which begins listening for connections
            t.start();
        } catch (IOException e) {
            // Handle IOException by printing the stack trace to diagnose the error
            e.printStackTrace();
        }
    }
}
