import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Date;

public class ServidorTCPBasico {
  public static void main(String[] args) {
    try {
      ServerSocket servidor = new ServerSocket(8000);
      System.out.println("Servidor ouvindo a porta 8000");
      while(true) {
        Socket cliente = servidor.accept();
        System.out.println("Cliente conectado: " + cliente.getInetAddress().getHostAddress());
        ObjectOutputStream saida = new ObjectOutputStream(cliente.getOutputStream());
        saida.flush();
        saida.writeObject(new Date());
        saida.close();
        cliente.close();
      }
    }
    catch(Exception e) {
       System.out.println("Erro: " + e.getMessage());
    }
    
  }
}