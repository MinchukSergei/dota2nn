package opendota;

import java.io.*;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
    
public class Main {

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(Integer.valueOf(args.length > 0 ? args[0] : "5600")), 0);
        server.createContext("/", new MyHandler());
        server.setExecutor(java.util.concurrent.Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors()));
        server.start();
    }
    
    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange t) throws IOException {
            t.sendResponseHeaders(200, 0);
            InputStream is = t.getRequestBody();
            OutputStream os = new FileOutputStream("./output.txt");
            PrintWriter pr = new PrintWriter(new BufferedWriter(new FileWriter("./log.txt", true)));
            try {
            	new Parse(is, os, pr);
            }
            catch (Exception e)
            {
            	e.printStackTrace();
            }
            os.close();
            OutputStream os2 = t.getResponseBody();
            os2.close();
            pr.close();
        }
    }
}
