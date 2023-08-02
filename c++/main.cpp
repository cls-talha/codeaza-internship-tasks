#include <iostream>
#include <string>
#include <curl/curl.h>

// Callback function to receive the response
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}

int main() {
    // URL for the API endpoints
    std::string fetch_url = "http://127.0.0.1:8000/fetch-data/";
    std::string get_all_url = "http://127.0.0.1:8000/get-all-data/";

    // Initialize libcurl
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "Failed to initialize libcurl." << std::endl;
        return 1;
    }

    // Send GET request and fetch data from the "fetch-data" endpoint
    std::string fetch_data;
    curl_easy_setopt(curl, CURLOPT_URL, fetch_url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &fetch_data);
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        std::cerr << "Failed to fetch data from " << fetch_url << ": " << curl_easy_strerror(res) << std::endl;
    } else {
        // Handle the fetched data (fetch_data) here as needed
        std::cout << "Fetched Data from /fetch-data/ endpoint: " << fetch_data << std::endl;
    }

    // Send GET request and fetch data from the "get-all-data" endpoint
    std::string get_all_data;
    curl_easy_setopt(curl, CURLOPT_URL, get_all_url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &get_all_data);
    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        std::cerr << "Failed to fetch data from " << get_all_url << ": " << curl_easy_strerror(res) << std::endl;
    } else {
        // Handle the fetched data (get_all_data) here as needed
        std::cout << "Fetched Data from /get-all-data/ endpoint: " << get_all_data << std::endl;
    }

    // Cleanup libcurl
    curl_easy_cleanup(curl);

    return 0;
}
