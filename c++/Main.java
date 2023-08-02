import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {
    public static void main(String[] args) {
        String fetchUrl = "http://127.0.0.1:8000/fetch-data/";
        String getAllUrl = "http://127.0.0.1:8000/get-all-data/";

        try {
            // Fetch data from the "fetch-data" endpoint
            String fetchResponse = makeHttpGetRequest(fetchUrl);
            System.out.println("Fetched Data from /fetch-data/ endpoint:\n" + fetchResponse);

            // Fetch data from the "get-all-data" endpoint
            String getAllResponse = makeHttpGetRequest(getAllUrl);
            System.out.println("Fetched Data from /get-all-data/ endpoint:\n" + getAllResponse);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String makeHttpGetRequest(String url) throws IOException {
        URL requestUrl = new URL(url);
        HttpURLConnection connection = (HttpURLConnection) requestUrl.openConnection();
        connection.setRequestMethod("GET");

        // Read the response data
        StringBuilder response = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
        }

        connection.disconnect();
        return response.toString();
    }
}
