package opendota;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.*;

public class Main {

    public static void main(String[] args) throws Exception {
//        HttpServer server = HttpServer.create(new InetSocketAddress(Integer.valueOf(args.length > 0 ? args[0] : "5600")), 0);
//        server.createContext("/", new MyHandler());
//        server.setExecutor(java.util.concurrent.Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors()));
//        server.start();

//        Map jsonObj = new Gson().fromJson(new JsonReader(new FileReader("H:/Minchuk/replays_data.json")), Map.class);
//        parseReplays("H:/Minchuk/replays/uncompressed/", "H:/Minchuk/parsed_replays/", "H:/Minchuk/");
    }

    private static void parseReplays(String sourceFolder, String ouputFolder, String errorFolder) {
        File rootFolder = new File(sourceFolder);

        for (File file : rootFolder.listFiles()) {
            try (InputStream is = new FileInputStream(file);
                 OutputStream os = new FileOutputStream(ouputFolder + file.getName() + ".txt");
                 PrintWriter pr = new PrintWriter(new BufferedWriter(new FileWriter(errorFolder + "log.txt", true)))
            ) {
                new Parse(is, os, pr);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
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
            } catch (Exception e) {
                e.printStackTrace();
            }
            os.close();
            OutputStream os2 = t.getResponseBody();
            os2.close();
            pr.close();
        }
    }
}
