/*
To compile app, write in command line: javac InterCV.java
To run app, write in command line:     java InterCV.java
To close app, press in command line:   ctrl+c
*/

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Path;

public class InterCV {

    public static void main(String[] args) throws IOException {

        int port = 8080;

        HttpServer server = HttpServer.create(
                new InetSocketAddress(port), 
                0
        );

        server.createContext("/", new PageHandler());
        server.createContext("/runRW", new PythonHandler());

        server.setExecutor(null); // default executor
        server.start();

        // To close the app, press ctrl+c in terminal
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Stopping InterCV...");
            server.stop(0);
            System.out.println("InterCV stopped!");
        }));

        System.out.println("InterCV running at http://localhost:" + port);
    }

    // --------------------------------------------------------------------

    // Make general page handler that can handle all http pages
    static class PageHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange exchange) throws IOException {

            String path = exchange.getRequestURI().getPath();
            
            // ALL URLs that need to be called MUST be included here, otherwise JAVA defaults back to the homepage
            String file = switch (path) {
                // HTML pages
                case "/education.html" -> "resources/education.html";
                case "/workExperience.html" -> "resources/workExperience.html";
                case "/publications.html" -> "resources/publications.html";
                case "/grantsAndDiploma.html" -> "resources/grantsAndDiploma.html";
                case "/projects.html" -> "resources/projects.html";
                // Stylesheets
                case "/stylesheets/generalPageStyle.css" -> "resources/stylesheets/generalPageStyle.css";
                case "/stylesheets/homepageStyle.css" -> "resources/stylesheets/homepageStyle.css";
                case "/stylesheets/publicationsStyle.css" -> "resources/stylesheets/publicationsStyle.css";
                case "/stylesheets/projectsStyle.css" -> "resources/stylesheets/projectsStyle.css";
                // Images
                case "/images/CV_billede.jpg" -> "resources/images/CV_billede.jpg";
                case "/images/image_for_education.jpg" -> "resources/images/image_for_education.jpg";
                case "/images/image_for_Rud2026PPCF.png" -> "resources/images/image_for_Rud2026PPCF.png";
                case "/images/image_for_Rud2025NF-2.png" -> "resources/images/image_for_Rud2025NF-2.png";
                case "/images/image_for_Rud2025NF-1.png" -> "resources/images/image_for_Rud2025NF-1.png";
                case "/images/image_for_Rud2024NF-2.png" -> "resources/images/image_for_Rud2024NF-2.png";
                case "/images/image_for_Rud2024NF-1.png" -> "resources/images/image_for_Rud2024NF-1.png";
                case "/images/chiral_Kernel_perturb_unc_n40_v3_rescale-elliptic-law-sqrt2_alphaR-015_alphaI-01_M1e6_nogrid_normalized.png" -> "resources/images/chiral_Kernel_perturb_unc_n40_v3_rescale-elliptic-law-sqrt2_alphaR-015_alphaI-01_M1e6_nogrid_normalized.png";
                // Scripts
                case "/randomwalk.js" -> "scripts/randomwalk.js";
                default -> "resources/homepage.html";
            };

            // Read the bytes of the corresponding file chosen above
            byte[] bytes = Files.readAllBytes(Path.of(file));

            // Declare content type variable
            String contentType;

            // Ensure that Java knows how to read each file depending on file suffix
            if (file.endsWith(".css")) {
                contentType = "text/css; charset=UTF-8";
            } else if (file.endsWith(".html")) {
                contentType = "text/html; charset=UTF-8";
            } else if (file.endsWith(".js")) {
                contentType = "application/javascript; charset=UTF-8";
            } else if (file.endsWith(".jpg") || file.endsWith(".jpeg")) {
                contentType = "image/jpeg";
            } else if (file.endsWith(".png")) {
                contentType = "image/png";
            } else if (file.endsWith(".gif")) {
                contentType = "image/gif";
            } else {
                contentType = "application/octet-stream";
            }

            // Need to set the headers of the response
            exchange.getResponseHeaders()
                    .set("Content-Type", contentType);

            // Need to send the headers of the response before the body
            exchange.sendResponseHeaders(200, bytes.length); // rcode is HTTP status code. 200 means "OK" or "Ran Successfully".

            // Now I can send the body
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }

    // Make a general handler that handles calls to python scripts
    static class PythonHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange exchange) throws IOException {

            // If the method of the request is not "POST"
            if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
                exchange.sendResponseHeaders(405, -1); // rcode 405 means "Method Not Allowed"
                return;
            }

            // Read JSON sent from JavaScript
            String requestBody = new String(
                exchange.getRequestBody().readAllBytes(),
                java.nio.charset.StandardCharsets.UTF_8
            ); // Receives either {"BM":true} or {"BM":false}

            System.out.println("Received: " + requestBody);

            ProcessBuilder processBuilder = new ProcessBuilder(
                    "python",
                    "pythonScripts/random_walk.py",
                    requestBody
            );

            processBuilder.redirectErrorStream(true); // Merge errors with standard output, so they can be read with getInputStream() method.

            Process process = processBuilder.start();

            String result = new String(
                    process.getInputStream().readAllBytes()
            );

            try {
                process.waitFor(); // Just wait a bit in case the process is not terminated
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                exchange.sendResponseHeaders(500, -1); // rcode 500 means "Internal Server Error".
                return;
            }

            // The python scripts dumps a JSON, pass it on directly to the html browser
            String json = result.trim();

            byte[] response = json.getBytes(java.nio.charset.StandardCharsets.UTF_8);

            exchange.getResponseHeaders()
                    .set("Content-Type", "application/json; charset=UTF-8");

            exchange.sendResponseHeaders(200, response.length); // rcode 200 means "OK".

            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response);
            }
        }
    }
}