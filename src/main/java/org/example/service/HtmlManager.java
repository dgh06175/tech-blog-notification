package org.example.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;

public class HtmlManager {
    public static String request(String rawUrl) {
        StringBuilder response = new StringBuilder();
        try {
            URL url = new URL(rawUrl);

            URLConnection urlConnection = url.openConnection();

            BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
            String inputLine;

            // 한 줄씩 읽어서 StringBuilder에 저장
            while ((inputLine = reader.readLine()) != null) {
                response.append(inputLine);
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return response.toString();
    }
}


