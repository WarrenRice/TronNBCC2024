import java.io.IOException;


public class Main {
    final static int PORT = 6066;                                                                    // Constant for the port number on which the server will listen

    
    public static void main(String[] args) {
        try {
            Thread t = new Server(PORT);                                                              // Initialize a new server thread on the specified port

            
            t.start();                                                                              // Start the server thread, which begins listening for connections

        } catch (IOException e) {
            e.printStackTrace();                                                                     // Handle IOException by printing the stack trace to diagnose the error

        }
    }
}
